"""Modo clase: recorre el proyecto paso a paso, en el orden de la presentación de S20.

    uv run python demo_clase.py              # los 14 pasos; Enter para avanzar
    uv run python demo_clase.py --paso 5     # empieza en el paso 5
    uv run python demo_clase.py --solo 12    # solo el paso 12
    uv run python demo_clase.py --lista      # índice de pasos

Cada paso dice qué diapositiva acompaña, qué archivo abrir, qué decir, el comando equivalente
que pueden escribir los alumnos y lo que hay que señalar en la salida. Si PostgreSQL está
arrancado (docker compose up -d --wait) lo usa y empieza con las tablas vacías; si no, sigue en
memoria y lo dice. No llama a ningún modelo ni gasta dinero (perfil doble).
"""

import argparse
import asyncio
import dataclasses
import json
import logging
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
CASO = (
    "El ticket T-100 sigue abierto. Resume el problema, consulta la política aplicable y "
    "prepara una recomendación con fuentes. Si falta información pública, investígala."
)

PASOS = [
    (
        1,
        "El proyecto entero, en verde",
        "6",
        "README.md",
        "Antes de abrir nada: el proyecto completo pasa sus diez comprobaciones de aceptación.",
    ),
    (
        2,
        "Configuración y prompt con versión",
        "7",
        "agente/config.py · agente/prompts.py",
        "Lo que cambia entre el aula y AWS es una variable; el prompt tiene versión.",
    ),
    (
        3,
        "El grafo: una ruta por turno",
        "8",
        "agente/grafo.py",
        "Sin herramientas: inicio → agente. Con un ticket pasa por herramientas y vuelve.",
    ),
    (
        4,
        "El modelo propone, el código decide",
        "9",
        "agente/herramientas.py · agente/grafo.py",
        "Con el límite a 1, la segunda herramienta no se ejecuta.",
    ),
    (
        5,
        "La memoria vive en PostgreSQL",
        "10",
        "agente/almacen.py · esquema.sql",
        "Dos procesos distintos, mismo hilo: en memoria se olvida; en PostgreSQL se recuerda.",
    ),
    (
        6,
        "thread_id no autoriza",
        "11",
        "agente/servicios.py",
        "Luis conoce el hilo de Ana, pero no es suyo.",
    ),
    (
        7,
        "La API",
        "12",
        "agente/api.py",
        "Salud sin modelo, 401 sin token, 200 con token y 404 en un hilo ajeno.",
    ),
    (
        8,
        "Servidor MCP propio",
        "13",
        "servidor_mcp/tickets.py",
        "El agente descubre la herramienta y su contrato; el recurso da contexto.",
    ),
    (
        9,
        "Una llamada MCP: descubrir, comprobar, llamar",
        "14",
        "agente/mcp_cliente.py",
        "Quién decide cada resultado: el servidor o el cliente.",
    ),
    (
        10,
        "De documento a fragmento con cita",
        "15",
        "agente/rag.py",
        "Reingestar no duplica; cada fragmento lleva título y sección para poder citarlo.",
    ),
    (
        11,
        "Responder con cita o decir que no consta",
        "16",
        "agente/rag.py (recuperar)",
        "El umbral convierte la similitud en una decisión.",
    ),
    (
        12,
        "Deep Research: un trabajo con estado",
        "17–18",
        "agente/investigacion.py",
        "Se registra, lo termina el ejecutor, y repetir la pregunta no lo duplica.",
    ),
    (
        13,
        "Seguir un turno: el log JSON",
        "19",
        "agente/observabilidad.py",
        "Con el request_id se encuentra el turno (y su traza en Langfuse, si hay claves).",
    ),
    (
        14,
        "¿Cómo sabemos que funciona?",
        "22",
        "tests/",
        "Tests sin coste y, con Docker, tests de PostgreSQL.",
    ),
]


# ------------------------------------------------------------------ presentación en terminal
def _c(texto, codigo):
    return f"\033[{codigo}m{texto}\033[0m" if COLOR else texto


def menta(t):
    return _c(t, "38;5;79")


def ambar(t):
    return _c(t, "38;5;179")


def gris(t):
    return _c(t, "38;5;245")


def coral(t):
    return _c(t, "38;5;209")


def negrita(t):
    return _c(t, "1")


def comando(texto):
    print(ambar("  $ " + texto))


def dato(clave, valor):
    if not isinstance(valor, str):
        valor = json.dumps(valor, ensure_ascii=False)
    print(f"    {gris(clave + ':'):<28} {valor}")


def bien(texto):
    print(menta("    ✓ ") + texto)


def mal(texto):
    print(coral("    ✗ ") + texto)


# ------------------------------------------------------------------ la demo
class Demo:
    def __init__(self, pausa: bool, usar_postgres: bool, limpiar: bool):
        from agente.config import cargar_config
        from agente.servicios import crear_servicios

        self.pausa = pausa
        os.environ.setdefault("S20_ALMACEN", "memoria")
        self.pg = usar_postgres and self._postgres_disponible()
        os.environ["S20_ALMACEN"] = "postgres" if self.pg else "memoria"
        self.cfg = cargar_config()
        self.s = crear_servicios(self.cfg)
        if self.pg and limpiar:
            self._sql(
                "TRUNCATE conversaciones, trabajos, checkpoints, checkpoint_blobs, checkpoint_writes"
            )
        from agente.rag import ingestar

        ingestar(self.s.almacen, self.s.embeddings)

    # --- utilidades
    def _postgres_disponible(self) -> bool:
        import psycopg

        from agente.config import _database_url

        try:
            with psycopg.connect(_database_url(), connect_timeout=2):
                return True
        except Exception:
            return False

    def _sql(self, sentencia: str):
        with self.s.almacen._pool.connection() as con:
            cursor = con.execute(sentencia)
            return cursor.fetchall() if cursor.description else None

    def esperar(self, texto="Enter para seguir"):
        if self.pausa:
            input(gris(f"  ⏎ {texto} "))

    def turno(self, usuario, hilo, mensaje, s=None, prefijo=""):
        extra = "" if usuario == "ana" else f" --usuario {usuario}"
        comando(f'{prefijo}uv run python -m agente.cli chat "{mensaje}" --thread {hilo}{extra}')
        r = (s or self.s).conversar(usuario=usuario, thread_id=hilo, mensaje=mensaje)
        dato("ruta", r["ruta"])
        dato("herramientas", [f"{h['nombre']} ({'ok' if h['ok'] else 'no'})" for h in r["herramientas"]])
        dato("fuentes", r["fuentes"])
        dato(
            "respuesta",
            r["respuesta"]
            .replace("\n[perfil doble · reglas, sin modelo]", "")
            .replace("\n", " ⏎ ")[:240],
        )
        return r

    def cli_chat(self, almacen, hilo, mensaje, usuario="ana"):
        """Un turno en un PROCESO NUEVO, como si se reiniciara el programa."""
        entorno = {**os.environ, "S20_ALMACEN": almacen}
        r = subprocess.run(
            [
                sys.executable,
                "-m",
                "agente.cli",
                "chat",
                mensaje,
                "--thread",
                hilo,
                "--usuario",
                usuario,
            ],
            cwd=RAIZ,
            env=entorno,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if r.returncode == 2:
            return "«Esa conversación pertenece a otro usuario.»"
        if r.returncode != 0:
            raise RuntimeError(
                r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "fallo del proceso"
            )
        return json.loads(r.stdout)["respuesta"].replace("\n[perfil doble · reglas, sin modelo]", "")

    # --- pasos
    def paso_1(self):
        from agente.cli import recorridos

        comando("uv run python -m agente.cli recorridos")
        ev = recorridos(self.s)
        for nombre, ok in ev["comprobaciones"].items():
            (bien if ok else mal)(nombre)
        dato("todo_ok", ev["todo_ok"])

    def paso_2(self):
        from agente.prompts import prompt_sistema

        comando("abrir agente/config.py y agente/prompts.py")
        publica = self.cfg.publica()
        for clave in (
            "perfil",
            "almacen",
            "fuentes",
            "modelo_chat",
            "modelo_embeddings",
            "prompt_version",
            "max_herramientas",
            "umbral_evidencia",
        ):
            dato(clave, publica[clave])
        print(gris("    prompt v1 (primeras líneas):"))
        for linea in prompt_sistema(self.cfg.prompt_version).splitlines()[:4]:
            print("      " + linea)

    def paso_3(self):
        self.turno("ana", "grafo", "Hola, ¿qué puedes hacer?")
        print()
        self.turno("ana", "grafo", "¿Cómo está el ticket T-200?")

    def paso_4(self):
        from agente.servicios import crear_servicios

        mensaje = "Mira el ticket T-100 y consulta la política aplicable"
        limitado = crear_servicios(dataclasses.replace(self.cfg, max_herramientas=1))
        try:
            self.turno("ana", "limite-1", mensaje, s=limitado, prefijo="S20_MAX_HERRAMIENTAS=1 ")
        finally:
            limitado.cerrar()
        print()
        self.turno("ana", "limite-4", mensaje)

    def paso_5(self):
        pregunta_a, pregunta_b = "¿Cómo está el ticket T-200?", "¿Qué ticket estábamos viendo?"
        hilo = f"reinicio-{int(time.time())}"
        print(negrita("    En memoria (S20_ALMACEN=memoria):"))
        comando(f'S20_ALMACEN=memoria uv run python -m agente.cli chat "{pregunta_a}" --thread {hilo}')
        self.cli_chat("memoria", hilo, pregunta_a)
        comando(f'S20_ALMACEN=memoria uv run python -m agente.cli chat "{pregunta_b}" --thread {hilo}')
        dato("proceso B responde", self.cli_chat("memoria", hilo, pregunta_b))
        print()
        if not self.pg:
            mal(
                "PostgreSQL no está arrancado: haz «docker compose up -d --wait» para ver la otra mitad."
            )
            return
        print(negrita("    En PostgreSQL (S20_ALMACEN=postgres):"))
        comando(f'S20_ALMACEN=postgres uv run python -m agente.cli chat "{pregunta_a}" --thread {hilo}')
        self.cli_chat("postgres", hilo, pregunta_a)
        comando(f'S20_ALMACEN=postgres uv run python -m agente.cli chat "{pregunta_b}" --thread {hilo}')
        dato("proceso B responde", self.cli_chat("postgres", hilo, pregunta_b))
        n = self._sql(f"SELECT count(*) FROM checkpoints WHERE thread_id = '{hilo}'")[0]["count"]
        dato("checkpoints del hilo", n)

    def paso_6(self):
        from agente.servicios import ConversacionAjena

        pregunta = "¿Qué ticket estábamos viendo?"
        comando(f'uv run python -m agente.cli chat "{pregunta}" --thread grafo --usuario luis')
        dato("dueño del hilo «grafo»", self.s.almacen.propietario("grafo"))
        try:
            self.s.conversar(usuario="luis", thread_id="grafo", mensaje="¿Qué ticket estábamos viendo?")
            mal("luis ha podido entrar: esto no debería pasar")
        except ConversacionAjena:
            bien("rechazado: «Esa conversación pertenece a otro usuario.» (en la API, 404)")

    def paso_7(self):
        import httpx

        puerto = 8020
        while puerto < 8040:
            with socket.socket() as so:
                if so.connect_ex(("127.0.0.1", puerto)) != 0:
                    break
            puerto += 1
        comando(f"uv run uvicorn agente.api:app --port {puerto}")
        proceso = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "agente.api:app",
                "--port",
                str(puerto),
                "--log-level",
                "warning",
            ],
            cwd=RAIZ,
            env=dict(os.environ),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        base = f"http://127.0.0.1:{puerto}"
        try:
            for _ in range(60):
                try:
                    salud = httpx.get(f"{base}/health", timeout=1).json()
                    break
                except httpx.HTTPError:
                    time.sleep(0.5)
            else:
                raise RuntimeError("la API no arrancó en 30 s")
            comando(f"curl {base}/health")
            dato("200", salud)
            cuerpo = {
                "thread_id": "api-1",
                "mensaje": "¿Cuál es el límite de peticiones del plan Estándar?",
            }
            comando(f"curl -X POST {base}/chat   (sin token)")
            dato("estado", httpx.post(f"{base}/chat", json=cuerpo, timeout=30).status_code)
            comando(f"curl -X POST {base}/chat -H 'authorization: Bearer token-ana'")
            r = httpx.post(
                f"{base}/chat", json=cuerpo, headers={"authorization": "Bearer token-ana"}, timeout=30
            )
            dato("estado", r.status_code)
            dato("fuentes", r.json()["fuentes"])
            comando(f"curl -X POST {base}/chat -H 'authorization: Bearer token-luis'   (mismo hilo)")
            r = httpx.post(
                f"{base}/chat", json=cuerpo, headers={"authorization": "Bearer token-luis"}, timeout=30
            )
            dato("estado", f"{r.status_code} {r.json()['detail']}")
            print(menta(f"    Swagger: {base}/docs"))
            self.esperar("Enter para parar la API")
        finally:
            proceso.terminate()
            proceso.wait(timeout=10)

    def paso_8(self):
        from mcp import Client

        from agente import mcp_cliente

        comando("uv run python -m agente.cli mcp")
        for h in mcp_cliente.descubrir_herramientas(self.cfg):
            dato("herramienta", h["nombre"])
            dato("descripción", h["descripcion"])
            dato("argumento ticket_id", h["argumentos"]["properties"]["ticket_id"]["pattern"])

        async def recurso():
            async with Client(mcp_cliente._parametros()) as cliente:
                return (await cliente.read_resource("tickets://abiertos")).contents[0].text

        dato("recurso tickets://abiertos", asyncio.run(recurso()))

    def paso_9(self):
        from agente import mcp_cliente

        casos = [
            ("consultar_ticket", {"ticket_id": "T-100"}),
            ("consultar_ticket", {"ticket_id": "T-999"}),
            ("consultar_ticket", {"ticket_id": "T-1"}),
            ("borrar_ticket", {"ticket_id": "T-100"}),
        ]
        for nombre, args in casos:
            t0 = time.perf_counter()
            try:
                r = mcp_cliente.llamar_herramienta(nombre, args, self.cfg)
                resumen = (
                    f"ok: true · {r['ticket']['asunto']}" if r.get("ok") else f"ok: false · {r['error']}"
                )
            except mcp_cliente.ErrorMCP as exc:
                resumen = f"ErrorMCP · {str(exc).splitlines()[0][:70]}"
            dato(f"{nombre} {args['ticket_id']}", f"{resumen}   ({time.perf_counter() - t0:.2f} s)")

    def paso_10(self):
        from agente.rag import CORPUS, fragmentar, ingestar

        comando("uv run python -m agente.cli ingestar   (dos veces)")
        dato("primera", ingestar(self.s.almacen, self.s.embeddings))
        dato("segunda", ingestar(self.s.almacen, self.s.embeddings))
        f = fragmentar(CORPUS / "03-limites-y-cuotas-api.md")[0]
        print(gris("    un fragmento:"))
        dato("fragmento_id", f.fragmento_id)
        dato("titulo", f.titulo)
        dato("seccion", f.seccion)
        dato("contenido", f.contenido[:150] + "…")

    def paso_11(self):
        from agente.rag import recuperar

        for pregunta in (
            "¿Cuál es el límite de peticiones del plan Estándar?",
            "¿Cuál es la política de teletrabajo de los empleados?",
        ):
            r = recuperar(self.cfg, self.s.almacen, self.s.embeddings, pregunta)
            dato(
                "mejor similitud",
                f"{r['mejor_similitud']} (umbral {r['umbral']}) → "
                f"{'responde con cita' if r['ok'] else 'no consta'}",
            )
            self.turno("ana", "umbral", pregunta)
            print()

    def paso_12(self):
        print(negrita("    1 · El agente registra el trabajo"))
        self.turno("ana", "caso", CASO)
        print(negrita("\n    2 · El ejecutor lo termina (otro proceso en clase)"))
        comando("uv run python -m agente.cli investigar")
        hechos = self.s.investigar_pendientes()
        dato("procesados", hechos)
        print(negrita("\n    3 · La misma pregunta lee el mismo trabajo"))
        self.turno("ana", "caso", CASO)
        print(negrita("\n    4 · El ejecutor otra vez: no hay nada que hacer"))
        comando("uv run python -m agente.cli investigar")
        dato("procesados", self.s.investigar_pendientes())
        if hechos:
            informe = self.s.almacen.leer_trabajo(hechos[-1])["informe"]
            comando(f"uv run python -m agente.cli investigar --ver {hechos[-1]}")
            dato("estado", informe["estado"])
            dato("consultas", informe["consultas"])
            dato("política interna", [p["cita"] for p in informe["politica_interna"]])
            dato("información pública", [e["fuente_id"] for e in informe["informacion_publica"]])
            dato("faltan", informe["faltan"])
            dato("consumo", informe["consumo"])

    def paso_13(self):
        lineas = []

        class Captura(logging.Handler):
            def emit(self, registro):
                lineas.append(registro.getMessage())

        registro = logging.getLogger("agente")
        nivel, captura = registro.level, Captura()
        registro.addHandler(captura)
        registro.setLevel(logging.INFO)
        try:
            comando('uv run python -m agente.cli chat "¿Cómo está el ticket T-100?" --thread log')
            self.s.conversar(usuario="ana", thread_id="log", mensaje="¿Cómo está el ticket T-100?")
        finally:
            registro.removeHandler(captura)
            registro.setLevel(nivel)
        evento = json.loads(lineas[-1])
        print(gris("    la línea JSON del turno (en la API sale en la terminal de uvicorn):"))
        for clave in (
            "evento",
            "request_id",
            "thread_id",
            "usuario",
            "ruta",
            "herramientas",
            "fuentes",
            "perfil",
            "prompt_version",
            "duracion_ms",
        ):
            dato(clave, evento.get(clave))
        dato(
            "Langfuse",
            "activo" if self.cfg.langfuse else "desactivado (S20_LANGFUSE=1 y claves para activarlo)",
        )

    def paso_14(self):
        for args, etiqueta in ((["-q"], "uv run pytest"), (["-q", "-m", "db"], "uv run pytest -m db")):
            if "db" in args and not self.pg:
                mal("tests de PostgreSQL omitidos: PostgreSQL no está arrancado")
                continue
            comando(etiqueta)
            r = subprocess.run(
                [sys.executable, "-m", "pytest", *args],
                cwd=RAIZ,
                capture_output=True,
                text=True,
                timeout=300,
            )
            (bien if r.returncode == 0 else mal)(r.stdout.strip().splitlines()[-1])


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Modo clase de S20: el proyecto paso a paso.")
    p.add_argument("--paso", type=int, default=1, help="empezar en este paso")
    p.add_argument("--hasta", type=int, default=len(PASOS), help="terminar en este paso")
    p.add_argument("--solo", type=int, help="ejecutar solo este paso")
    p.add_argument("--lista", action="store_true", help="mostrar los pasos y salir")
    p.add_argument("--sin-pausa", action="store_true", help="no esperar a Enter (ensayo automático)")
    p.add_argument(
        "--sin-postgres", action="store_true", help="usar memoria aunque PostgreSQL esté arrancado"
    )
    p.add_argument(
        "--sin-limpiar", action="store_true", help="no vaciar conversaciones y trabajos al empezar"
    )
    args = p.parse_args(argv)

    if args.lista:
        for n, titulo, diap, archivo, _ in PASOS:
            print(f"{n:>2}. {titulo:<48} diap. {diap:<6} {archivo}")
        return 0
    desde, hasta = (args.solo, args.solo) if args.solo else (args.paso, args.hasta)
    logging.getLogger("agente").propagate = False

    print(negrita(menta("\nS20 · Proyecto final · modo clase")))
    demo = Demo(
        pausa=not args.sin_pausa, usar_postgres=not args.sin_postgres, limpiar=not args.sin_limpiar
    )
    dato("perfil", f"{demo.cfg.perfil} (reglas, sin modelo ni coste)")
    dato(
        "almacén",
        "PostgreSQL" + (" · tablas vaciadas al empezar" if not args.sin_limpiar else "")
        if demo.pg
        else "memoria (PostgreSQL no arrancado o --sin-postgres)",
    )
    dato("fuentes públicas", demo.cfg.fuentes)
    fallos = 0
    try:
        for n, titulo, diap, archivo, decir in PASOS:
            if not desde <= n <= hasta:
                continue
            print("\n" + gris("─" * 78))
            print(negrita(f"PASO {n} de {len(PASOS)} · {titulo}") + gris(f"   diapositiva {diap}"))
            print(gris("  Abre: ") + archivo)
            print(gris("  Di:   ") + decir + "\n")
            try:
                getattr(demo, f"paso_{n}")()
            except Exception as exc:  # un paso que falla no detiene la clase
                fallos += 1
                mal(f"el paso {n} ha fallado: {type(exc).__name__}: {exc}")
            if n < hasta:
                demo.esperar()
    finally:
        demo.s.cerrar()
    print(
        "\n"
        + (
            menta("Fin del recorrido.")
            if not fallos
            else coral(f"Fin del recorrido con {fallos} fallos.")
        )
    )
    if demo.pg:
        print(gris("Al terminar la clase: docker compose down (conserva los datos)."))
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
