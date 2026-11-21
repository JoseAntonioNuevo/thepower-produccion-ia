"""Línea de comandos del proyecto: los mismos pasos que se siguen en clase.

  uv run python -m agente.cli mcp                       # descubrir las herramientas MCP
  uv run python -m agente.cli ingestar                  # reconstruir el índice del RAG
  uv run python -m agente.cli chat "¿Qué pasa con T-100?" --thread demo --usuario ana
  uv run python -m agente.cli investigar                # ejecutar investigaciones pendientes
  uv run python -m agente.cli recorridos                # los recorridos de aceptación + evidencia

Con S20_ALMACEN=memoria cada comando empieza de cero (no hay nada guardado entre procesos);
`recorridos` hace todo en un mismo proceso para poder enseñarlo sin Docker.
"""

import argparse
import json
import sys
from datetime import datetime

from . import mcp_cliente
from .config import RAIZ, cargar_config
from .rag import ingestar
from .servicios import ConversacionAjena, crear_servicios

CASO = (
    "El ticket T-100 sigue abierto. Resume el problema, consulta la política aplicable y "
    "prepara una recomendación con fuentes. Si falta información pública, investígala."
)


def _imprimir(datos):
    print(json.dumps(datos, ensure_ascii=False, indent=2))


def recorridos(s) -> dict:
    """Ejecuta los recorridos de aceptación del proyecto final y devuelve la evidencia."""

    def turno(usuario, thread, mensaje):
        r = s.conversar(usuario=usuario, thread_id=thread, mensaje=mensaje)
        return {
            "mensaje": mensaje,
            "respuesta": r["respuesta"],
            "ruta": r["ruta"],
            "herramientas": r["herramientas"],
            "fuentes": r["fuentes"],
            "errores": r["errores"],
        }

    pasos = {
        "1_directo": turno("ana", "acept-1", "Hola, ¿qué puedes hacer?"),
        "2_ticket_mcp": turno("ana", "acept-2", "¿En qué estado está el ticket T-200?"),
        "3_ticket_inexistente": turno("ana", "acept-3", "Consulta el ticket T-999"),
        "4_rag_con_cita": turno("ana", "acept-4", "¿Cuál es el límite de peticiones del plan Estándar?"),
        "5_rechazo": turno("ana", "acept-5", "¿Cuál es la política de teletrabajo de los empleados?"),
        "6_caso_completo": turno("ana", "acept-6", CASO),
    }
    # Investigación: el turno 6 dejó un trabajo pendiente; el ejecutor lo procesa aparte.
    hechos = s.investigar_pendientes()
    pasos["6b_ejecutor"] = {"trabajos_procesados": hechos}
    pasos["6c_consulta_posterior"] = turno("ana", "acept-6", CASO)
    informe = s.almacen.leer_trabajo(hechos[0])["informe"] if hechos else None
    pasos["6d_informe"] = informe
    # Memoria y aislamiento.
    pasos["7_memoria"] = turno("ana", "acept-2", "¿Qué ticket estábamos viendo?")
    try:
        s.conversar(usuario="luis", thread_id="acept-2", mensaje="¿Qué ticket estábamos viendo?")
        pasos["8_aislamiento"] = {"bloqueado": False}
    except ConversacionAjena:
        pasos["8_aislamiento"] = {"bloqueado": True, "detalle": "luis no puede leer el hilo de ana"}

    def usadas(clave):
        return [h["nombre"] for h in pasos[clave]["herramientas"]]

    comprobaciones = {
        "directo_sin_herramientas": usadas("1_directo") == [],
        "ticket_por_mcp": usadas("2_ticket_mcp") == ["consultar_ticket"]
        and "ticket:T-200" in pasos["2_ticket_mcp"]["fuentes"],
        "inexistente_explicito": "no existe" in pasos["3_ticket_inexistente"]["respuesta"],
        "rag_con_cita": any(f.startswith("doc:03-limites") for f in pasos["4_rag_con_cita"]["fuentes"]),
        "rechazo_sin_fuentes": pasos["5_rechazo"]["fuentes"] == []
        and "No consta" in pasos["5_rechazo"]["respuesta"],
        "caso_usa_tres_herramientas": usadas("6_caso_completo")
        == ["consultar_ticket", "buscar_documentacion", "investigar"],
        "investigacion_no_se_duplica": len(hechos) == 1,
        "informe_con_fuentes_publicas": bool(informe and informe["informacion_publica"]),
        "memoria_recuerda_ticket": "T-200" in pasos["7_memoria"]["respuesta"],
        "aislamiento_entre_usuarios": pasos["8_aislamiento"]["bloqueado"],
    }
    return {
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "config": s.cfg.publica(),
        "comprobaciones": comprobaciones,
        "todo_ok": all(comprobaciones.values()),
        "pasos": pasos,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="agente", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="orden", required=True)
    sub.add_parser("mcp", help="descubre las herramientas del servidor MCP")
    sub.add_parser("ingestar", help="reconstruye el índice del RAG")
    c = sub.add_parser("chat", help="un turno de conversación")
    c.add_argument("mensaje")
    c.add_argument("--thread", default="demo")
    c.add_argument("--usuario", default="ana")
    i = sub.add_parser("investigar", help="ejecuta las investigaciones pendientes")
    i.add_argument("--ver", help="muestra el informe de un trabajo, p. ej. INV-1a2b3c4d")
    r = sub.add_parser("recorridos", help="recorridos de aceptación y evidencia")
    r.add_argument("--guardar", action="store_true", help="escribe evidencias/recorridos-*.json")
    args = p.parse_args(argv)

    cfg = cargar_config()
    if args.orden == "mcp":
        _imprimir(mcp_cliente.descubrir_herramientas(cfg))
        return 0
    s = crear_servicios(cfg)
    try:
        if args.orden == "ingestar":
            _imprimir(ingestar(s.almacen, s.embeddings))
        elif args.orden == "chat":
            _imprimir(s.conversar(usuario=args.usuario, thread_id=args.thread, mensaje=args.mensaje))
        elif args.orden == "investigar":
            if args.ver:
                _imprimir(s.almacen.leer_trabajo(args.ver))
            else:
                _imprimir({"procesados": s.investigar_pendientes()})
        elif args.orden == "recorridos":
            evidencia = recorridos(s)
            _imprimir({"todo_ok": evidencia["todo_ok"], "comprobaciones": evidencia["comprobaciones"]})
            if args.guardar:
                destino = (
                    RAIZ / "evidencias" / f"recorridos-{cfg.perfil}-{cfg.almacen}-{cfg.fuentes}.json"
                )
                destino.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"Evidencia guardada en {destino.relative_to(RAIZ)}")
            return 0 if evidencia["todo_ok"] else 1
    except ConversacionAjena:
        print("Esa conversación pertenece a otro usuario.", file=sys.stderr)
        return 2
    finally:
        s.cerrar()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
