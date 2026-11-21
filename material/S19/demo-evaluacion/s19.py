"""S19 · RAG mínimo con evaluación y tests integrados. Un solo punto de entrada.

    python s19.py preflight                      comprueba configuración y datos (no llama a nada)
    python s19.py ingestar --config A            reconstruye el índice desde documentos en bruto
    python s19.py preguntar "..." --config A     una consulta: documentos, fuentes o rechazo
    python s19.py calibrar --config A            elige el umbral de evidencia con VALIDACIÓN
    python s19.py lote --conjunto test --config A --salida resultados/mi-test-A
    python s19.py informe resultados/mi-test-A   métricas con numerador, denominador y cobertura
    python s19.py umbrales resultados/mi-validacion-A
    python s19.py regresion resultados/mi-test-A (código de salida 1 si el control falla)
    python s19.py comparar resultados/mi-test-A resultados/mi-test-B
    python s19.py revision resultados/mi-test-A  plantilla de revisión manual
    python s19.py degradar resultados/mi-test-A --modo recuperacion --salida resultados/mi-test-A-mal
    python s19.py estimar                        llamadas y coste previstos del perfil real

Perfil por defecto: `doble` (sin modelos, sin coste, rotulado). Con S19_PERFIL=real los
comandos que consumen la API exigen `--execute`.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

from evaluacion import comparar as cmp
from evaluacion import conjuntos, degradar, informe, regresion
from evaluacion.lote import AVISO_DOBLE, ejecutar_lote
from rag.almacen import AlmacenPg, ErrorIndice
from rag.config import RAIZ, ErrorConfiguracion, aplicar_variante, cargar_calibracion, cargar_config
from rag.consulta import recuperar, responder
from rag.corpus import preparar
from rag.costes import tarifas
from rag.ingesta import CORPUS, indice_esperado, reconstruir_indice
from rag.observabilidad import Trazador
from rag.proveedores import ErrorProveedor, crear_proveedores

DATOS = RAIZ / "datos"


def _config(args, calibrada: bool = True):
    cfg = aplicar_variante(cargar_config(), args.config)
    return cargar_calibracion(cfg) if calibrada else cfg


def _rotulo(cfg) -> None:
    if cfg.perfil == "doble":
        print(f"⚠  {AVISO_DOBLE}\n")


def _guardar(ruta: Path, datos: dict) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _leer(ruta: Path) -> dict:
    return json.loads(ruta.read_text(encoding="utf-8"))


def _ruta_visible(ruta: Path) -> Path:
    return ruta.relative_to(RAIZ) if ruta.is_relative_to(RAIZ) else ruta


# ------------------------------------------------------------------ comandos
def cmd_preflight(args) -> int:
    cfg = _config(args)
    _rotulo(cfg)
    print("Configuración:", json.dumps(cfg.publica(), ensure_ascii=False))
    print("Datos:", json.dumps(conjuntos.comprobar_separacion(), ensure_ascii=False))
    for variante in ("A", "B"):
        c = aplicar_variante(cargar_config(), variante)
        docs, frags = preparar(CORPUS, c.chunk_size, c.chunk_overlap)
        print(
            f"Variante {variante}: chunk_size={c.chunk_size} → {len(docs)} documentos, "
            f"{len(frags)} fragmentos, índice {indice_esperado(c)}"
        )
    try:
        almacen = AlmacenPg(cfg.database_url)
        almacen.preparar_esquema()
        indice = almacen.leer_indice(indice_esperado(cfg))
        print(
            "PostgreSQL: conectado ·",
            f"índice presente ({indice.n_fragmentos} fragmentos)"
            if indice
            else "índice de esta configuración todavía vacío",
        )
    except ErrorIndice as exc:
        print("PostgreSQL: NO disponible ·", exc)
        return 1
    print("Langfuse:", "activado" if Trazador.desde_entorno().activo else "apagado (S19_LANGFUSE=off)")
    print("Preflight correcto: no se ha llamado a ningún modelo.")
    return 0


def cmd_ingestar(args) -> int:
    cfg = _config(args, calibrada=False)
    _rotulo(cfg)
    prov = crear_proveedores(cfg, args.execute)
    almacen = AlmacenPg(cfg.database_url)
    indice = reconstruir_indice(cfg, almacen, prov.embeddings)
    print(
        f"Índice {indice.indice_id} reconstruido: {indice.n_documentos} documentos, "
        f"{indice.n_fragmentos} fragmentos, {indice.embedding_modelo}/{indice.embedding_dim}."
    )
    print(
        f"Filas leídas de PostgreSQL: {almacen.contar(indice.indice_id)} · "
        f"llamadas de embeddings: {prov.embeddings.llamadas}"
    )
    return 0


def cmd_preguntar(args) -> int:
    cfg = _config(args)
    _rotulo(cfg)
    prov = crear_proveedores(cfg, args.execute)
    r = responder(cfg, AlmacenPg(cfg.database_url), prov, indice_esperado(cfg), args.pregunta)
    print("Pregunta:", r.pregunta)
    print(f"Documentos recuperados (hasta 5 distintos): {r.documentos_recuperados}")
    print(f"Fragmentos recuperados: {r.fragmentos_recuperados}")
    print(f"Mejor similitud: {r.mejor_similitud} · umbral de evidencia: {cfg.umbral_evidencia}")
    print("RECHAZO:" if r.rechazo else "RESPUESTA:", r.texto, f"({r.motivo_rechazo})" if r.rechazo else "")
    print("Fuentes:", r.fuentes, "· avisos:", r.avisos)
    print("Latencia (ms):", r.latencia_ms, "· tokens:", r.tokens, "· coste estimado:", r.coste_usd)
    if r.model_version:
        print("Versión de modelo servida:", r.model_version)
    return 0


def cmd_calibrar(args) -> int:
    """Elige el umbral de evidencia con el conjunto de VALIDACIÓN. El test no se toca.

    Si el perfil ya tiene calibración fijada en `datos/calibracion.json`, calcula y compara
    sin sobrescribir; solo escribe si no existe todavía o si se pasa `--fijar`.
    """
    cfg = _config(args, calibrada=False)
    _rotulo(cfg)
    prov = crear_proveedores(cfg, args.execute)
    almacen, indice_id = AlmacenPg(cfg.database_url), indice_esperado(cfg)
    filas = []
    for caso in conjuntos.cargar("validacion"):
        rec = recuperar(cfg, almacen, prov.embeddings, indice_id, caso["pregunta"])
        filas.append(
            {
                "caso_id": caso["caso_id"],
                "respondible": caso["respondible"],
                "mejor_similitud": round(rec.mejor_similitud, 4),
            }
        )
    valores = sorted({f["mejor_similitud"] for f in filas})
    candidatos = [0.0] + [round((a + b) / 2, 4) for a, b in zip(valores, valores[1:], strict=False)]

    def aciertos(t: float) -> int:
        return sum((f["mejor_similitud"] >= t) == f["respondible"] for f in filas)

    # A igualdad de aciertos, el umbral más bajo: abstenerse de más también es un error.
    umbral = max(candidatos, key=lambda t: (aciertos(t), -t))
    ruta = DATOS / "calibracion.json"
    todo = _leer(ruta) if ruta.exists() else {}
    for f in filas:
        print(f"  {f['caso_id']}  {'respondible ' if f['respondible'] else 'sin respuesta'}  {f['mejor_similitud']:.4f}")
    if cfg.perfil in todo and not args.fijar:
        actual = todo[cfg.perfil]
        print(
            f"Umbral calculado = {umbral} ({aciertos(umbral)}/{len(filas)} decisiones correctas en "
            f"validación) · umbral fijado = {actual['umbral_evidencia']} "
            f"(fijado el {actual.get('fijado')})."
        )
        print(
            f"Sin cambios en {_ruta_visible(ruta)}: ya existe calibración fijada para el perfil "
            f"{cfg.perfil}. Repite con --fijar para sobrescribir."
        )
        return 0
    todo[cfg.perfil] = {
        "umbral_evidencia": umbral,
        "embedding_modelo": cfg.embedding_modelo,
        "indice_id": indice_id,
        "config_id": cfg.config_id,
        "conjunto": "validacion",
        "decisiones_correctas": f"{aciertos(umbral)}/{len(filas)}",
        "fijado": dt.date.today().isoformat(),
        "similitudes": filas,
        "aviso": AVISO_DOBLE if cfg.perfil == "doble" else None,
    }
    _guardar(ruta, todo)
    print(
        f"Umbral de evidencia = {umbral} ({aciertos(umbral)}/{len(filas)} decisiones correctas en "
        f"validación). Guardado en {_ruta_visible(ruta)}."
    )
    return 0


def cmd_lote(args) -> int:
    cfg = _config(args)
    _rotulo(cfg)
    prov = crear_proveedores(cfg, args.execute)
    casos = conjuntos.cargar(args.conjunto)
    carpeta = Path(args.salida)
    filas = ejecutar_lote(
        cfg,
        AlmacenPg(cfg.database_url),
        prov,
        indice_esperado(cfg),
        casos,
        args.conjunto,
        carpeta,
        run_id=args.run,
        trazador=Trazador.desde_entorno(),
    )
    errores = sum(1 for f in filas if f["error"])
    print(
        f"{len(filas)} casos → {carpeta}/respuestas.jsonl · rechazos: "
        f"{sum(1 for f in filas if f['rechazo'])} · errores del sistema: {errores}"
    )
    print("Siguiente paso: evaluar la generación en el entorno aislado (ver evaluador/README.md).")
    return 0


def cmd_informe(args) -> int:
    carpeta = Path(args.carpeta)
    respuestas, puntuaciones, manifiesto = informe.cargar_ejecucion(carpeta)
    inf = informe.construir_informe(conjuntos.cargar(manifiesto["conjunto"]), respuestas, puntuaciones, manifiesto)
    _guardar(carpeta / "informe.json", inf)
    tabla = informe.tabla_markdown(inf)
    (carpeta / "informe.md").write_text(tabla, encoding="utf-8")
    print(tabla)
    return 0


def _informe_guardado(carpeta: Path) -> dict:
    ruta = carpeta / "informe.json"
    if not ruta.exists():
        raise ErrorConfiguracion(f"falta {ruta}: ejecuta antes `python s19.py informe {carpeta}`")
    return _leer(ruta)


def cmd_umbrales(args) -> int:
    """Deriva umbrales desde validación. Si ya existen para el perfil, compara sin sobrescribir."""
    inf = _informe_guardado(Path(args.carpeta))
    umbrales = regresion.derivar_umbrales(inf, args.margen)
    ruta = DATOS / f"umbrales.{inf['perfil']}.json"
    if ruta.exists() and not args.fijar:
        actual = _leer(ruta)
        fijadas = {r["metrica"]: r for r in actual.get("reglas", [])}
        print(
            f"Umbrales calculados del perfil {inf['perfil']} (validación ± {args.margen}) "
            f"frente a los fijados en {_ruta_visible(ruta)} "
            f"(fijado el {actual.get('fijado')}, run {actual.get('origen', {}).get('run_id')}):"
        )
        for r in umbrales["reglas"]:
            sentido = "mínimo" if "minimo" in r else "máximo"
            nuevo = r.get("minimo", r.get("maximo"))
            prev = fijadas.get(r["metrica"])
            fijado_txt = f"fijado {prev.get('minimo', prev.get('maximo')):.2f}" if prev is not None else "no estaba fijado"
            print(f"  {r['metrica']:<42} validación {r['validacion']:.2f} → {sentido} {nuevo:.2f} ({fijado_txt})")
        print(
            f"Sin cambios en {_ruta_visible(ruta)}: ya existen umbrales fijados para el perfil "
            f"{inf['perfil']}. Repite con --fijar para sobrescribir."
        )
        return 0
    _guardar(ruta, umbrales)
    print(f"Umbrales del perfil {inf['perfil']} (validación ± {args.margen}) → {_ruta_visible(ruta)}")
    for r in umbrales["reglas"]:
        sentido = "mínimo" if "minimo" in r else "máximo"
        print(f"  {r['metrica']:<42} validación {r['validacion']:.2f} → {sentido} {r.get('minimo', r.get('maximo')):.2f}")
    return 0


def cmd_regresion(args) -> int:
    inf = _informe_guardado(Path(args.carpeta))
    ruta = Path(args.umbrales) if args.umbrales else DATOS / f"umbrales.{inf['perfil']}.json"
    if not ruta.exists():
        print(f"CONTROL DE REGRESIÓN: FALLA · no hay umbrales para el perfil {inf['perfil']} ({ruta.name})")
        return 1
    esperados = len(conjuntos.cargar(inf["conjunto"]))
    fallos = regresion.comprobar(inf, _leer(ruta), esperados)
    if fallos:
        print(f"CONTROL DE REGRESIÓN: FALLA · {inf['run_id']}")
        for f in fallos:
            print("  ✗", f)
        return 1
    print(f"CONTROL DE REGRESIÓN: PASA · {inf['run_id']} cumple las reglas de {ruta.name}")
    return 0


def cmd_comparar(args) -> int:
    a, b = _informe_guardado(Path(args.a)), _informe_guardado(Path(args.b))
    resultado = cmp.comparar(a, b)
    tabla = cmp.tabla_markdown(resultado)
    if args.salida:
        _guardar(Path(args.salida) / "comparacion.json", resultado)
        (Path(args.salida) / "comparacion.md").write_text(tabla, encoding="utf-8")
    print(tabla)
    return 0


def cmd_revision(args) -> int:
    """Plantilla CSV con los casos de revisión elegidos ANTES de ejecutar el test."""
    carpeta = Path(args.carpeta)
    respuestas, puntuaciones, _ = informe.cargar_ejecucion(carpeta)
    por_caso = {f["caso_id"]: f for f in respuestas}
    notas = {(p["caso_id"], p["metrica"]): p for p in puntuaciones or []}
    plan = _leer(DATOS / "revision-casos.json")
    ruta = carpeta / "revision-manual.csv"
    with ruta.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "caso_id",
                "pregunta",
                "respuesta_del_sistema",
                "fuentes_citadas",
                "contexto_entregado",
                "faithfulness",
                "answer_relevancy",
                "correcta (si/no/parcial)",
                "las_fuentes_la_respaldan (si/no)",
                "fiel_pero_incompleta (si/no)",
                "discrepa_del_juez (si/no)",
                "notas",
                "revisor",
                "fecha",
            ]
        )
        for caso_id in plan["casos"]:
            fila = por_caso[caso_id]

            def nota(metrica, caso_id=caso_id):
                p = notas.get((caso_id, metrica))
                return "" if p is None else (p["valor"] if p["evaluable"] else f"no evaluable: {p['motivo']}")

            w.writerow(
                [
                    caso_id,
                    fila["user_input"],
                    fila["response"] or f"ERROR: {fila['error']}",
                    " ".join(fila.get("fuentes", [])),
                    " ‖ ".join(fila["retrieved_contexts"]),
                    nota("faithfulness"),
                    nota("answer_relevancy"),
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                ]
            )
    print(
        f"Plantilla con {len(plan['casos'])} casos → {ruta}. Las columnas humanas van vacías: "
        "las rellena una persona leyendo respuesta y contexto."
    )
    return 0


def cmd_degradar(args) -> int:
    """Copia una ejecución introduciendo un fallo conocido. Sirve para probar el control."""
    m = degradar.degradar(Path(args.carpeta), Path(args.salida), args.modo)
    print(f"⚠  {m['aviso']}")
    print(f"Copia degradada ({args.modo}) → {args.salida}. Ahora: informe y regresion sobre ella.")
    return 0


def cmd_estimar(args) -> int:
    """Llamadas previstas y coste estimado del perfil real. No llama a ninguna API."""
    s, t = _leer(DATOS / "supuestos-coste.json"), tarifas()
    base = cargar_config()
    frags = {v: len(preparar(CORPUS, aplicar_variante(base, v).chunk_size, 0)[1]) for v in ("A", "B")}
    n_val, n_test = len(conjuntos.cargar("validacion")), len(conjuntos.cargar("test"))
    # Recorrido completo: 2 índices, calibración, validación A y B, test A y B.
    emb = frags["A"] + frags["B"] + n_val * 3 + n_test * 2
    gen = n_val * 2 + n_test * 2  # como máximo una generación por caso
    juez_casos = n_val * 2 + n_test * 2  # como máximo: todos los casos respondidos
    juez_llm = juez_casos * s["evaluador"]["llamadas_llm_por_caso"]
    juez_emb = juez_casos * s["evaluador"]["peticiones_embeddings_por_caso"]
    p = t["modelos"]
    g, e = s["generacion"], s["evaluador"]
    coste_gen = gen * (g["tokens_entrada"] * p[g["modelo"]]["entrada"] + g["tokens_salida"] * p[g["modelo"]]["salida"]) / 1e6
    coste_emb = emb * s["embeddings"]["tokens"] * p[s["embeddings"]["modelo"]]["entrada"] / 1e6
    coste_juez = (
        juez_casos
        * (e["tokens_entrada_por_caso"] * p[e["modelo"]]["entrada"] + e["tokens_salida_por_caso"] * p[e["modelo"]]["salida"])
        / 1e6
    )
    techo_juez = (
        juez_llm
        * (
            e["tokens_entrada_por_caso"] / e["llamadas_llm_por_caso"] * p[e["modelo"]]["entrada"]
            + e["max_tokens"] * p[e["modelo"]]["salida"]
        )
        / 1e6
    )
    techo_gen = gen * (g["tokens_entrada"] * p[g["modelo"]]["entrada"] + g["max_tokens"] * p[g["modelo"]]["salida"]) / 1e6
    print(f"Tarifas: {t['fuente']} · consultadas el {t['consultado']} · {t['nivel']}")
    print(f"Fragmentos: A={frags['A']}, B={frags['B']} · validación={n_val} · test={n_test}\n")
    print(f"{'Partida':<34}{'Llamadas (máx.)':>16}{'Estimación USD':>16}{'Cota superior USD':>19}")
    print(f"{'Embeddings del RAG':<34}{emb:>16}{coste_emb:>16.4f}{coste_emb:>19.4f}")
    print(f"{'Generación del RAG':<34}{gen:>16}{coste_gen:>16.4f}{techo_gen:>19.4f}")
    print(f"{'Evaluador · LLM (Ragas)':<34}{juez_llm:>16}{coste_juez:>16.4f}{techo_juez:>19.4f}")
    print(f"{'Evaluador · embeddings':<34}{juez_emb:>16}{'≈ 0,0001':>16}{'≈ 0,0001':>19}")
    total, techo = coste_emb + coste_gen + coste_juez, coste_emb + techo_gen + techo_juez
    print(f"{'TOTAL':<34}{emb + gen + juez_llm + juez_emb:>16}{total:>16.4f}{techo:>19.4f}")
    print("\nLa estimación usa los supuestos de datos/supuestos-coste.json (tamaños, no mediciones de")
    print("tokens). La cota superior supone que cada respuesta agota su máximo de tokens de salida.")
    return 0


def cmd_publicar_evaluador(args) -> int:
    """Envía a Langfuse las puntuaciones de Ragas y, en trazas aparte, el consumo del evaluador."""
    carpeta = Path(args.carpeta)
    _, puntuaciones, manifiesto = informe.cargar_ejecucion(carpeta)
    trazador = Trazador.desde_entorno()
    if not trazador.activo or not puntuaciones:
        print("Nada que publicar: Langfuse apagado o sin puntuaciones.jsonl.")
        return 1
    cfg = aplicar_variante(cargar_config(), manifiesto["config"]["config_id"])
    for caso_id in sorted({p["caso_id"] for p in puntuaciones}):
        trazador.registrar_evaluador(
            manifiesto["run_id"], caso_id, cfg, [p for p in puntuaciones if p["caso_id"] == caso_id]
        )
    trazador.cerrar()
    print(f"Publicadas las puntuaciones de {manifiesto['run_id']} en Langfuse.")
    return 0


# ------------------------------------------------------------------ CLI
def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="S19 · RAG con evaluación y tests")
    sub = p.add_subparsers(dest="comando", required=True)

    def nuevo(nombre, funcion, execute=False, config=True):
        sp = sub.add_parser(nombre)
        sp.set_defaults(funcion=funcion)
        if config:
            sp.add_argument("--config", default="A", help="variante de datos/configuraciones.json")
        if execute:
            sp.add_argument("--execute", action="store_true", help="autoriza llamadas de pago (perfil real)")
        return sp

    nuevo("preflight", cmd_preflight)
    nuevo("ingestar", cmd_ingestar, execute=True)
    nuevo("preguntar", cmd_preguntar, execute=True).add_argument("pregunta")
    sp = nuevo("calibrar", cmd_calibrar, execute=True)
    sp.add_argument("--fijar", action="store_true", help="sobrescribe la calibración fijada de este perfil")
    sp = nuevo("lote", cmd_lote, execute=True)
    sp.add_argument("--conjunto", choices=("test", "validacion"), required=True)
    sp.add_argument("--salida", required=True)
    sp.add_argument("--run", help="identificador de la ejecución (por defecto, con fecha y hora)")
    nuevo("informe", cmd_informe, config=False).add_argument("carpeta")
    sp = nuevo("umbrales", cmd_umbrales, config=False)
    sp.add_argument("carpeta")
    sp.add_argument("--margen", type=float, default=regresion.MARGEN)
    sp.add_argument("--fijar", action="store_true", help="sobrescribe los umbrales fijados de este perfil")
    sp = nuevo("regresion", cmd_regresion, config=False)
    sp.add_argument("carpeta")
    sp.add_argument("--umbrales")
    sp = nuevo("comparar", cmd_comparar, config=False)
    sp.add_argument("a")
    sp.add_argument("b")
    sp.add_argument("--salida")
    nuevo("revision", cmd_revision, config=False).add_argument("carpeta")
    sp = nuevo("degradar", cmd_degradar, config=False)
    sp.add_argument("carpeta")
    sp.add_argument("--modo", choices=degradar.MODOS, required=True)
    sp.add_argument("--salida", required=True)
    nuevo("estimar", cmd_estimar, config=False)
    nuevo("publicar-evaluador", cmd_publicar_evaluador, config=False).add_argument("carpeta")

    args = p.parse_args(argv)
    try:
        return args.funcion(args)
    except (
        ErrorConfiguracion,
        ErrorIndice,
        ErrorProveedor,
        cmp.ComparacionInvalida,
        conjuntos.ErrorFormato,
        ValueError,
    ) as exc:
        print(f"ERROR · {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
