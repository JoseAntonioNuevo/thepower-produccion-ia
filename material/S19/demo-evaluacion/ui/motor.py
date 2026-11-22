"""Lo que hace el chat, sin pantalla: comandos, perfiles, consultas y trazas de Langfuse.

La TUI (`ui/rag_tui.py`) solo pinta; toda la lógica está aquí y se prueba sin terminal en
`tests/test_tui.py`. Cada pregunta ejecuta el MISMO grafo que el lote (`rag/grafo.py`) y,
con Langfuse activo, deja una traza con la misma forma: sesión = esta apertura del chat.
"""

from __future__ import annotations

import datetime as dt
import os
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from evaluacion import conjuntos
from evaluacion.metricas import evaluar_caso
from rag.almacen import AlmacenPg, ErrorIndice
from rag.config import (
    RAIZ,
    VARIABLE_ARCHIVO_ENV,
    ErrorConfiguracion,
    aplicar_variante,
    cargar_calibracion,
    cargar_config,
    cargar_env,
    modelos_evaluador,
    ruta_env,
)
from rag.consulta import Respuesta, responder
from rag.ingesta import indice_esperado
from rag.observabilidad import Trazador
from rag.proveedores import crear_proveedores
from ui.lineas import AYUDA, GUION, ChatLine, fila_de_respuesta, lista_de_casos

SALIR = {"salir", "exit", "q"}
_CASO = re.compile(r"[TtVv]\d{2}")


@dataclass(frozen=True)
class Orden:
    """Qué pidió el usuario: una pregunta (libre o del test) o un comando."""

    tipo: str  # pregunta | ayuda | casos | perfil | config | salir | desconocido
    argumento: str = ""
    pregunta: str = ""
    caso: dict | None = None


class MotorChat:
    def __init__(
        self,
        execute: bool,
        config_id: str = "A",
        fabrica_almacen: Callable[[str], object] = AlmacenPg,
        sesion: str | None = None,
        carpeta_env: Path = RAIZ,
    ):
        self.execute, self.config_id, self._fabrica_almacen = execute, config_id, fabrica_almacen
        self.carpeta_env = carpeta_env  # dónde busca `/perfil` los archivos .env.*
        self.sesion = sesion or f"chat-{dt.datetime.now():%Y%m%d-%H%M%S}"
        self.casos = {c["caso_id"]: c for c in conjuntos.cargar("test")}
        self.n_preguntas, self.coste_sesion, self.coste_completo = 0, 0.0, True
        self.cargar()

    # ------------------------------------------------------------ configuración
    def cargar(self) -> None:
        """Lee el archivo de entorno activo y prepara configuración, proveedores, índice y trazas."""
        cfg = cargar_calibracion(aplicar_variante(cargar_config(), self.config_id))
        proveedores = crear_proveedores(cfg, self.execute)  # el perfil real exige --execute
        almacen = self._fabrica_almacen(cfg.database_url)
        indice_id = indice_esperado(cfg)
        if almacen.leer_indice(indice_id) is None:
            orden = f"python s19.py ingestar --config {self.config_id}" + (" --execute" if cfg.perfil == "real" else "")
            raise ErrorIndice(f"el índice {indice_id} está vacío: ejecuta antes `{orden}`")
        self.cfg, self.proveedores, self.almacen, self.indice_id = cfg, proveedores, almacen, indice_id
        self.trazador = Trazador.desde_entorno()
        self.juez = modelos_evaluador()[0] if cfg.perfil == "real" else "doble (sin modelo)"

    @property
    def perfil(self) -> str:
        return ruta_env().name

    def perfiles(self) -> list[str]:
        return sorted(p.name for p in self.carpeta_env.glob(".env*") if p.is_file() and p.name != ".env.example")

    def cambiar_perfil(self, nombre: str) -> list[ChatLine]:
        destino = self.carpeta_env / (nombre if nombre.startswith(".env") else f".env.{nombre}")
        if not destino.is_file():
            return [ChatLine("error", f"No existe {destino.name}. Disponibles: {', '.join(self.perfiles())}")]
        anterior = os.environ.get(VARIABLE_ARCHIVO_ENV)
        try:
            self._usar_archivo(str(destino))
            self.cargar()
        except (ErrorConfiguracion, ErrorIndice) as exc:
            self._usar_archivo(anterior)
            self.cargar()
            return [ChatLine("error", f"No se cambió de perfil: {exc}")]
        return [ChatLine("hint", f"Perfil {destino.name}: genera {self.cfg.gen_modelo} · perfil {self.cfg.perfil}")]

    def _usar_archivo(self, ruta: str | None) -> None:
        if ruta:
            os.environ[VARIABLE_ARCHIVO_ENV] = ruta
        else:
            os.environ.pop(VARIABLE_ARCHIVO_ENV, None)
        cargar_env(sustituir=True)  # retira lo del archivo anterior y carga el nuevo

    def cambiar_config(self, config_id: str) -> list[ChatLine]:
        anterior = self.config_id
        try:
            self.config_id = config_id
            self.cargar()
        except (ErrorConfiguracion, ErrorIndice) as exc:
            self.config_id = anterior
            self.cargar()
            return [ChatLine("error", f"No se cambió de configuración: {exc}")]
        return [
            ChatLine("hint", f"Configuración {config_id}: fragmentos de {self.cfg.chunk_size} · índice {self.indice_id}")
        ]

    # ------------------------------------------------------------ órdenes
    def interpretar(self, texto: str) -> Orden:
        texto = texto.strip()
        if texto.lower() in SALIR:
            return Orden("salir")
        if texto.startswith("/"):
            partes = texto[1:].split(maxsplit=1)
            comando = partes[0].lower() if partes else ""
            argumento = partes[1].strip() if len(partes) > 1 else ""
            if comando in {"ayuda", "casos", "perfil", "config"}:
                return Orden(comando, argumento)
            return Orden("desconocido", comando)
        if texto.isdigit() and 1 <= int(texto) <= len(GUION):
            caso = self.casos[GUION[int(texto) - 1]]
            return Orden("pregunta", pregunta=caso["pregunta"], caso=caso)
        if _CASO.fullmatch(texto) and texto.upper() in self.casos:
            caso = self.casos[texto.upper()]
            return Orden("pregunta", pregunta=caso["pregunta"], caso=caso)
        return Orden("pregunta", pregunta=texto)

    def comando(self, orden: Orden) -> list[ChatLine]:
        if orden.tipo == "ayuda":
            return [ChatLine("hint", AYUDA)]
        if orden.tipo == "casos":
            return [ChatLine("hint", lista_de_casos(list(self.casos.values())))]
        if orden.tipo == "perfil":
            if not orden.argumento:
                marcas = [("→ " if p == self.perfil else "  ") + p for p in self.perfiles()]
                return [ChatLine("hint", "Archivos de entorno (/perfil <nombre>):\n" + "\n".join(marcas))]
            return self.cambiar_perfil(orden.argumento)
        if orden.tipo == "config":
            if not orden.argumento:
                return [ChatLine("hint", f"Configuración actual: {self.config_id}. Usa /config A, B, MH o MS.")]
            return self.cambiar_config(orden.argumento.upper())
        return [ChatLine("error", f"Comando desconocido: /{orden.argumento}. Escribe /ayuda.")]

    # ------------------------------------------------------------ consulta
    def preguntar(self, pregunta: str, caso: dict | None, al_paso: Callable[[dict], None]) -> Respuesta:
        """Ejecuta el grafo y deja la traza en Langfuse (si está activo), igual que el lote."""
        self.n_preguntas += 1
        caso_id = f"{self.n_preguntas:02d}-{caso['caso_id'] if caso else 'libre'}"
        with self.trazador.consulta(self.sesion, caso_id, self.cfg, pregunta) as traza:
            r = responder(self.cfg, self.almacen, self.proveedores, self.indice_id, pregunta, traza, al_paso)
            puntuaciones = {"rechazo": float(r.rechazo)}
            if caso:
                e = evaluar_caso(caso, fila_de_respuesta(r))
                puntuaciones |= {
                    "precision_at_5": e["precision_at_5"],
                    "recall_at_5": e["recall_at_5"],
                    "acierto_criterio": None if e["acierto"] is None else float(e["acierto"]),
                }
            traza.cerrar(
                salida={"respuesta": r.texto, "fuentes": r.fuentes, "rechazo": r.rechazo},
                metadatos={
                    "origen": "chat",
                    "perfil_env": self.perfil,
                    "caso_test": caso["caso_id"] if caso else None,
                    "documentos_recuperados": r.documentos_recuperados,
                    "latencia_ms": r.latencia_ms,
                    "coste_usd": r.coste_usd,
                    "coste_fuente": r.coste_fuente,
                },
                puntuaciones=puntuaciones,
            )
        self.trazador.cerrar()  # envía ya: la traza aparece en Langfuse sin esperar al final
        if r.coste_usd is None:
            self.coste_completo = False
        else:
            self.coste_sesion += r.coste_usd
        return r
