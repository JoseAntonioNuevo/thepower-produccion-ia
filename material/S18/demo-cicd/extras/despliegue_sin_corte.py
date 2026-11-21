"""Ampliación opcional de S18: cómo se DEMUESTRA un despliegue sin corte.

Todo ocurre en 127.0.0.1, con la API de la demo en modo demo y sin AWS ni red externa.
Un balanceador mínimo hace el papel del ALB: un endpoint estable delante de las tareas.
No cambia app.py, ni las plantillas, ni los workflows: el laboratorio de ECS/Fargate
sigue sin balanceador (IP pública de la tarea), y por eso no puede demostrar continuidad.

El criterio: peticiones continuas al MISMO endpoint antes, durante y después del cambio,
y cero fallos en las tres fases. Se ejecutan dos recorridos para compararlo:

1. Sin corte: B arranca, pasa la comprobación de salud (readiness) y entra en el
   balanceador; A deja de recibir peticiones nuevas, termina las que tenía (drenaje)
   y solo entonces se para.
2. Con corte: se para A y después se arranca B (como recrear la tarea).

En los dos, un smoke posterior contra B sale bien: un smoke después del cambio no dice
nada de lo que pasó durante el cambio. Y un cliente que apuntaba a la «IP» de A falla al
pararse A, aunque el servicio siga vivo.

    uv run python extras/despliegue_sin_corte.py
"""

import asyncio
import os
import socket
import sys
import time
from collections import Counter
from pathlib import Path

import httpx
import uvicorn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import app as api  # noqa: E402  (la misma API de la demo)

# La demo escribe una línea JSON por petición; aquí solo interesa el resumen.
api.registrar = lambda *args, **kwargs: None

TEXTO = "No puedo entrar en mi cuenta desde ayer"  # prioridad media: A y B responden 200
UMBRAL_SANO = 2  # comprobaciones de salud seguidas para pasar de «initial» a «healthy»
DRENAJE_MAX_S = 5.0  # como deregistration_delay, pero corto: la API responde en ms


def puerto_libre() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Tarea:
    """Una «tarea»: la API real con su versión, en su propio puerto (su «IP»)."""

    def __init__(self, version: str):
        self.version = version
        self.puerto = puerto_libre()
        self.url = f"http://127.0.0.1:{self.puerto}"
        os.environ["APP_VERSION"] = version
        os.environ["API_MODE"] = "demo"
        config = uvicorn.Config(
            api.crear_app(), host="127.0.0.1", port=self.puerto, log_level="error"
        )
        self.servidor = uvicorn.Server(config)
        self._tarea: asyncio.Task | None = None

    async def arrancar(self) -> None:
        self._tarea = asyncio.create_task(self.servidor.serve())
        while not self.servidor.started:
            await asyncio.sleep(0.01)

    async def parar(self) -> None:
        # Uvicorn deja de aceptar conexiones y termina las peticiones en curso (SIGTERM).
        self.servidor.should_exit = True
        if self._tarea:
            await self._tarea


class Balanceador:
    """Endpoint estable con destinos en estado initial → healthy → draining (como un ALB)."""

    def __init__(self):
        self.destinos: dict[str, dict] = {}
        self._turno = 0
        self._http = httpx.AsyncClient(timeout=5)

    def registrar(self, tarea: Tarea) -> None:
        self.destinos[tarea.version] = {"tarea": tarea, "estado": "initial", "ok": 0, "en_vuelo": 0}

    def drenar(self, tarea: Tarea) -> None:
        self.destinos[tarea.version]["estado"] = "draining"

    async def comprobar_salud(self) -> None:
        """Readiness: solo recibe tráfico un destino que ha respondido /health varias veces."""
        while True:
            for d in list(self.destinos.values()):
                if d["estado"] not in ("initial", "healthy"):
                    continue
                try:
                    r = await self._http.get(d["tarea"].url + "/health", timeout=0.5)
                    d["ok"] = d["ok"] + 1 if r.status_code == 200 else 0
                except httpx.HTTPError:
                    d["ok"] = 0
                if d["estado"] == "initial" and d["ok"] >= UMBRAL_SANO:
                    d["estado"] = "healthy"
                elif d["estado"] == "healthy" and d["ok"] == 0:
                    d["estado"] = "unhealthy"
            await asyncio.sleep(0.1)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return
        cuerpo = b""
        while True:
            mensaje = await receive()
            cuerpo += mensaje.get("body", b"")
            if not mensaje.get("more_body"):
                break
        sanos = [d for d in self.destinos.values() if d["estado"] == "healthy"]
        if not sanos:
            await self._responder(send, 503, b'{"error":"sin_destinos_sanos"}')
            return
        d = sanos[self._turno % len(sanos)]
        self._turno += 1
        d["en_vuelo"] += 1
        try:
            r = await self._http.request(
                scope["method"],
                d["tarea"].url + scope["path"],
                content=cuerpo,
                headers={"content-type": "application/json"},
            )
            await self._responder(send, r.status_code, r.content)
        except httpx.HTTPError:
            await self._responder(send, 502, b'{"error":"destino_no_responde"}')
        finally:
            d["en_vuelo"] -= 1

    @staticmethod
    async def _responder(send, estado: int, cuerpo: bytes) -> None:
        cabeceras = [(b"content-type", b"application/json")]
        await send({"type": "http.response.start", "status": estado, "headers": cabeceras})
        await send({"type": "http.response.body", "body": cuerpo})

    async def esperar_drenaje(self, tarea: Tarea) -> float:
        inicio = time.perf_counter()
        while (
            self.destinos[tarea.version]["en_vuelo"]
            and time.perf_counter() - inicio < DRENAJE_MAX_S
        ):
            await asyncio.sleep(0.01)
        del self.destinos[tarea.version]
        return time.perf_counter() - inicio


class Cliente:
    """Peticiones continuas a una URL; anota fase, estado y versión que respondió."""

    def __init__(self, url: str, trabajadores: int = 3):
        self.url = url
        self.fase = "antes"
        self.registro: list[tuple[str, str]] = []
        self._seguir = True
        self._trabajadores = trabajadores

    async def _bucle(self) -> None:
        async with httpx.AsyncClient(timeout=2) as http:
            while self._seguir:
                fase = self.fase
                try:
                    r = await http.post(self.url + "/clasificar", json={"texto": TEXTO})
                    ok = r.status_code == 200
                    self.registro.append((fase, r.json()["version"] if ok else str(r.status_code)))
                except (httpx.HTTPError, ValueError):
                    self.registro.append((fase, "sin conexión"))
                await asyncio.sleep(0.02)

    def empezar(self) -> list[asyncio.Task]:
        return [asyncio.create_task(self._bucle()) for _ in range(self._trabajadores)]

    async def terminar(self, tareas: list[asyncio.Task]) -> None:
        self._seguir = False
        await asyncio.gather(*tareas)

    def resumen(self) -> str:
        lineas = []
        for fase in ("antes", "durante", "después"):
            cuenta = Counter(r for f, r in self.registro if f == fase)
            fallos = sum(n for r, n in cuenta.items() if r not in ("A", "B"))
            detalle = ", ".join(f"{r}: {n}" for r, n in sorted(cuenta.items()))
            total = sum(cuenta.values())
            lineas.append(f"   {fase:<8} {total:>4} peticiones · fallos {fallos:>3} · {detalle}")
        return "\n".join(lineas)

    def fallos(self) -> int:
        return sum(1 for _, r in self.registro if r not in ("A", "B"))


async def smoke(url: str) -> str:
    async with httpx.AsyncClient(timeout=2) as http:
        r = await http.post(url + "/clasificar", json={"texto": TEXTO})
        return f"{r.status_code} · versión {r.json().get('version')}"


async def recorrido(sin_corte: bool) -> tuple[int, int]:
    balanceador = Balanceador()
    puerto = puerto_libre()
    servidor = uvicorn.Server(
        uvicorn.Config(balanceador, host="127.0.0.1", port=puerto, log_level="error")
    )
    servicio = asyncio.create_task(servidor.serve())
    salud = asyncio.create_task(balanceador.comprobar_salud())
    while not servidor.started:
        await asyncio.sleep(0.01)
    url = f"http://127.0.0.1:{puerto}"

    a = Tarea("A")
    await a.arrancar()
    balanceador.registrar(a)
    while balanceador.destinos["A"]["estado"] != "healthy":
        await asyncio.sleep(0.02)

    cliente = Cliente(url)  # por el endpoint estable
    directo = Cliente(a.url, trabajadores=1)  # apuntando a la «IP» de la tarea A
    tareas = cliente.empezar() + directo.empezar()
    await asyncio.sleep(1.0)

    cliente.fase = directo.fase = "durante"
    t0 = time.perf_counter()
    b = Tarea("B")
    if sin_corte:
        await b.arrancar()
        balanceador.registrar(b)  # initial: todavía no recibe tráfico
        while balanceador.destinos["B"]["estado"] != "healthy":
            await asyncio.sleep(0.02)
        balanceador.drenar(a)  # draining: sin peticiones nuevas
        drenaje = await balanceador.esperar_drenaje(a)
        await a.parar()
        pasos = f"B sana → A drenada en {drenaje * 1000:.0f} ms → A parada"
    else:
        await a.parar()
        del balanceador.destinos["A"]
        await asyncio.sleep(0.3)  # lo que tarda en arrancar la tarea nueva
        await b.arrancar()
        balanceador.registrar(b)
        while balanceador.destinos["B"]["estado"] != "healthy":
            await asyncio.sleep(0.02)
        pasos = "A parada → B arranca → B sana"
    duracion = time.perf_counter() - t0
    cliente.fase = directo.fase = "después"
    await asyncio.sleep(1.0)
    await cliente.terminar(tareas[:3])
    await directo.terminar(tareas[3:])

    titulo = (
        "1 · SIN CORTE (readiness + drenaje)"
        if sin_corte
        else "2 · CON CORTE (parar y luego arrancar)"
    )
    print(f"\n{titulo}\n   cambio: {pasos} · {duracion * 1000:.0f} ms")
    print(" Endpoint estable (lo que ve el usuario):")
    print(cliente.resumen())
    print(" «IP» directa de la tarea A (lo que haría un cliente sin balanceador):")
    print(directo.resumen())
    print(f" Smoke posterior contra B: {await smoke(b.url)}")

    await b.parar()
    salud.cancel()
    servidor.should_exit = True
    await servicio
    return cliente.fallos(), directo.fallos()


async def principal() -> int:
    print("Despliegue de A a B por el mismo endpoint, con peticiones continuas (local, modo demo)")
    fallos_1, directo_1 = await recorrido(sin_corte=True)
    fallos_2, _ = await recorrido(sin_corte=False)
    print("\nCRITERIO: cero fallos por el endpoint estable antes, durante y después.")
    print(f"   sin corte: {fallos_1} fallos → {'CUMPLE' if fallos_1 == 0 else 'NO CUMPLE'}")
    print(f"   con corte: {fallos_2} fallos → {'CUMPLE' if fallos_2 == 0 else 'NO CUMPLE'}")
    print(f"   la «IP» de A falló {directo_1} veces incluso en el recorrido sin corte")
    print("   y el smoke posterior salió bien en los dos: no prueba la continuidad.")
    return 0 if fallos_1 == 0 and fallos_2 > 0 else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(principal()))
