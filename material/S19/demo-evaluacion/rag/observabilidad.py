"""Observabilidad con Langfuse: una traza por consulta y el evaluador en trazas aparte.

Qué queda en cada traza de consulta: pregunta, respuesta, fuentes, documentos recuperados,
configuración, latencia de cada paso, tokens y coste de la generación, y las métricas como
puntuaciones (precision@5, recall@5, rechazo, faithfulness, answer_relevancy).

El consumo del EVALUADOR va en otra traza (`evaluador-ragas`, etiqueta `evaluador`): así el
coste de responder y el coste de juzgar no se suman en la misma cifra.

Está apagado por defecto. Se enciende con S19_LANGFUSE=on y las claves LANGFUSE_*.
"""

from __future__ import annotations

import os
from contextlib import contextmanager

from rag.config import Config, ErrorConfiguracion


class _PasoNulo:
    def update(self, **_):
        return None


class TrazaNula:
    """Traza que no hace nada: el código de consulta es el mismo con y sin Langfuse."""

    trace_id = None

    @contextmanager
    def paso(self, nombre: str, tipo: str = "span", **_):
        yield _PasoNulo()

    def cerrar(self, **_):
        return None


class _Traza:
    def __init__(self, cliente, raiz, trace_id: str):
        self._cliente, self._raiz, self.trace_id = cliente, raiz, trace_id

    @contextmanager
    def paso(self, nombre: str, tipo: str = "span", **campos):
        # Hija EXPLÍCITA de la raíz `consulta-rag`: los nodos del grafo de LangGraph pueden
        # ejecutarse en otro hilo y así la observación no depende del contexto del hilo.
        with self._raiz.start_as_current_observation(name=nombre, as_type=tipo, **campos) as obs:
            yield obs

    def cerrar(self, *, salida, metadatos: dict, puntuaciones: dict):
        self._raiz.update(output=salida, metadata=metadatos)
        for nombre, valor in puntuaciones.items():
            if valor is None:  # una métrica que no se puede calcular no se publica como 0
                continue
            self._cliente.create_score(trace_id=self.trace_id, name=nombre, value=float(valor), data_type="NUMERIC")


class Trazador:
    def __init__(self, cliente=None):
        self._cliente = cliente

    @property
    def activo(self) -> bool:
        return self._cliente is not None

    @classmethod
    def desde_entorno(cls) -> Trazador:
        if os.environ.get("S19_LANGFUSE", "off").lower() != "on":
            return cls(None)
        faltan = [k for k in ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY") if not os.environ.get(k)]
        if faltan:
            raise ErrorConfiguracion(f"S19_LANGFUSE=on pero faltan {', '.join(faltan)}")
        from langfuse import Langfuse

        return cls(Langfuse(environment="thepower-s19", timeout=20))

    def id_traza(self, run_id: str, caso_id: str, sufijo: str = "") -> str:
        """Id determinista: el evaluador, que corre después, puntúa la MISMA traza."""
        from langfuse import Langfuse

        return Langfuse.create_trace_id(seed=f"{run_id}:{caso_id}{sufijo}")

    @contextmanager
    def consulta(self, run_id: str, caso_id: str, cfg: Config, pregunta: str):
        if not self.activo:
            yield TrazaNula()
            return
        from langfuse import propagate_attributes

        trace_id = self.id_traza(run_id, caso_id)
        etiquetas = ["s19", f"config:{cfg.config_id}", f"perfil:{cfg.perfil}"]
        with propagate_attributes(session_id=run_id, tags=etiquetas, trace_name="consulta-rag"):
            with self._cliente.start_as_current_observation(
                trace_context={"trace_id": trace_id},
                name="consulta-rag",
                as_type="span",
                input={"pregunta": pregunta},
                metadata={"caso_id": caso_id, **cfg.publica()},
            ) as raiz:
                yield _Traza(self._cliente, raiz, trace_id)

    def registrar_evaluador(self, run_id: str, caso_id: str, cfg: Config, filas: list[dict]) -> None:
        """Publica las puntuaciones de Ragas en la traza de la consulta y su consumo aparte."""
        if not self.activo or not filas:
            return
        from langfuse import propagate_attributes

        traza_consulta = self.id_traza(run_id, caso_id)
        for fila in filas:
            if fila["evaluable"]:
                self._cliente.create_score(
                    trace_id=traza_consulta,
                    name=fila["metrica"],
                    value=float(fila["valor"]),
                    data_type="NUMERIC",
                    comment=f"ragas {fila['evaluador'].get('ragas')}",
                )
        ev = filas[0]["evaluador"]
        usos = [f["consumo"] for f in filas]
        tokens = {
            k: sum(u[k] for u in usos) if all(u.get(k) is not None for u in usos) else None
            for k in ("tokens_entrada", "tokens_salida")
        }
        uso = {"input": tokens["tokens_entrada"], "output": tokens["tokens_salida"]} if None not in tokens.values() else None
        # El coste solo se envía si TODAS las filas del caso lo tienen; nunca se rellena con 0.
        coste = (
            {"total": round(sum(u["coste_usd"] for u in usos), 8)}
            if all(u.get("coste_usd") is not None for u in usos)
            else None
        )
        etiquetas = ["s19", "evaluador", f"config:{cfg.config_id}", f"perfil:{ev.get('modo')}"]
        with propagate_attributes(session_id=run_id, tags=etiquetas, trace_name="evaluador-ragas"):
            with self._cliente.start_as_current_observation(
                trace_context={"trace_id": self.id_traza(run_id, caso_id, ":evaluador")},
                name="evaluador-ragas",
                as_type="evaluator",
                model=ev.get("llm"),
                input={"caso_id": caso_id, "traza_consulta": traza_consulta},
                output={f["metrica"]: f["valor"] if f["evaluable"] else f["motivo"] for f in filas},
                usage_details=uso,
                cost_details=coste,
                metadata={"llamadas_llm": sum(u.get("llamadas_llm", 0) for u in usos), **ev},
            ):
                pass

    def cerrar(self) -> None:
        if self.activo:
            self._cliente.flush()
