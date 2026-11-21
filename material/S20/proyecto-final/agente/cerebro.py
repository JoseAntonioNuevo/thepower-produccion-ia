"""PASO 2 · El «cerebro»: quién decide el siguiente paso del agente.

- Perfil real  -> un modelo de chat con herramientas (LangChain `init_chat_model`).
- Perfil doble -> CerebroDoble: reglas escritas a mano que imitan esas decisiones.

Los dos se usan igual (`bind_tools` + `invoke`), así que el grafo no sabe cuál tiene
delante. El doble NO es un modelo: no entiende lenguaje, solo busca patrones. Existe para
recorrer y probar el proyecto entero sin claves ni coste. Sus respuestas van rotuladas.
"""

import json
import re
import unicodedata

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from .config import Config

ROTULO = "[perfil doble · reglas, sin modelo]"
PATRON_TICKET = r"\bT-\d{3}\b"
# Los patrones se comparan con el texto en minúsculas y sin tildes.
PIDE_DOCUMENTACION = (
    "politica",
    "documentaci",
    "sla",
    "limite",
    "cuota",
    "credito",
    "plan ",
    "factur",
    "cifrado",
    "rollback",
    "canary",
    "severidad",
    "sev-",
    "retenci",
    "token",
    "certificado",
    "region",
    "disponibilidad",
)
SALUDOS = ("hola", "buenas", "gracias", "que puedes hacer", "ayuda")
MEMORIA = ("que ticket", "de que hablabamos", "recuerdas", "estabamos viendo")


def _plano(texto: str) -> str:
    """Minúsculas y sin tildes: «Investígala» -> «investigala»."""
    return unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode()


def _json(mensaje: ToolMessage) -> dict:
    try:
        return json.loads(mensaje.content)
    except (TypeError, ValueError):
        return {"ok": False, "error": str(mensaje.content)[:120]}


class CerebroDoble:
    nombre = "doble-reglas"

    def __init__(self, con_herramientas: bool = False):
        self._con_herramientas = con_herramientas

    def bind_tools(self, herramientas):
        return CerebroDoble(con_herramientas=True)

    def invoke(self, mensajes, config=None) -> AIMessage:
        ultimo = max(i for i, m in enumerate(mensajes) if isinstance(m, HumanMessage))
        pregunta = str(mensajes[ultimo].content)
        texto = _plano(pregunta)
        # Resultados de herramientas de ESTE turno, por nombre.
        hechos: dict[str, list[dict]] = {}
        for m in mensajes[ultimo + 1 :]:
            if isinstance(m, ToolMessage):
                hechos.setdefault(m.name, []).append(_json(m))

        if self._con_herramientas:
            llamada = self._siguiente_llamada(pregunta, texto, hechos)
            if llamada:
                nombre, argumentos = llamada
                numero = sum(len(v) for v in hechos.values()) + 1
                return AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": nombre,
                            "args": argumentos,
                            "id": f"doble-{numero}",
                            "type": "tool_call",
                        }
                    ],
                )
        return AIMessage(content=self._respuesta(pregunta, texto, hechos, mensajes[:ultimo]))

    # --- decidir: ¿qué herramienta falta por usar?
    def _siguiente_llamada(self, pregunta, texto, hechos):
        consultados = {h.get("ticket_id") for h in hechos.get("consultar_ticket", [])}
        for ticket_id in re.findall(PATRON_TICKET, pregunta):
            if ticket_id not in consultados:
                return "consultar_ticket", {"ticket_id": ticket_id}
        tickets = [h["ticket"] for h in hechos.get("consultar_ticket", []) if h.get("ok")]
        quiere_docs = any(clave in texto for clave in PIDE_DOCUMENTACION)
        if quiere_docs and "buscar_documentacion" not in hechos:
            # Con un ticket delante, la búsqueda se hace con el asunto del ticket.
            consulta = f"{tickets[0]['tecnologia']}. {tickets[0]['asunto']}" if tickets else pregunta
            return "buscar_documentacion", {"pregunta": consulta}
        if "investiga" in texto and "investigar" not in hechos:
            tema = tickets[0]["tecnologia"] if tickets else pregunta
            return "investigar", {"tema": tema}
        return None

    # --- redactar: componer la respuesta con lo que devolvieron las herramientas
    def _respuesta(self, pregunta, texto, hechos, historial) -> str:
        lineas = []
        for h in hechos.get("consultar_ticket", []):
            if h.get("ok"):
                t = h["ticket"]
                lineas.append(
                    f"Ticket {h['ticket_id']} ({t['estado']}, plan {t['plan']}): "
                    f"{t['asunto']}. {t['descripcion']}"
                )
            elif h.get("error") == "no_encontrado":
                lineas.append(f"El ticket {h.get('ticket_id')} no existe en el sistema de tickets.")
            else:
                lineas.append("No he podido consultar el ticket: " + str(h.get("error")))
        for h in hechos.get("buscar_documentacion", []):
            if h.get("ok"):
                for f in h["fragmentos"][:2]:
                    lineas.append(f"Política aplicable: {f['texto']} [{f['cita']}]")
            else:
                lineas.append(
                    "No consta en la documentación de AetherCloud: no puedo responder a eso con fuentes."
                )
        for h in hechos.get("investigar", []):
            if h.get("estado") in {"completo", "parcial"}:
                lineas.append(f"Investigación {h['trabajo_id']} ({h['estado']}): {h['resumen']}")
            elif h.get("trabajo_id"):
                lineas.append(
                    f"He registrado la investigación {h['trabajo_id']} "
                    f"(estado: {h['estado']}). Consulta su estado cuando termine."
                )
            else:
                lineas.append("No he podido registrar la investigación: " + str(h.get("error")))
        if not lineas:
            lineas.append(self._directa(texto, historial))
        return "\n".join(lineas) + f"\n{ROTULO}"

    def _directa(self, texto, historial) -> str:
        if any(clave in texto for clave in MEMORIA):
            vistos = re.findall(PATRON_TICKET, " ".join(str(m.content) for m in historial))
            return (
                f"En esta conversación hemos visto el ticket {vistos[-1]}."
                if vistos
                else "En esta conversación todavía no hemos visto ningún ticket."
            )
        if any(clave in texto for clave in SALUDOS):
            return (
                "Hola. Puedo consultar un ticket (por ejemplo T-100), buscar una política en "
                "la documentación de AetherCloud o registrar una investigación."
            )
        return (
            "No tengo una herramienta para eso. Dime un ticket (T-100) o pregunta por una "
            "política de AetherCloud."
        )


def crear_cerebro(cfg: Config):
    if cfg.perfil == "doble":
        return CerebroDoble()
    from langchain.chat_models import init_chat_model

    # "proveedor:modelo", p. ej. google_genai:gemini-3.5-flash-lite. temperature=0: reproducible.
    return init_chat_model(cfg.modelo_chat, temperature=0)
