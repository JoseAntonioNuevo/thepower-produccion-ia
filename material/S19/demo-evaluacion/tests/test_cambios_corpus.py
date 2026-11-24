"""Taller S19: misma pregunta, corpus distinto. Perfil doble local con el grafo real e índice en memoria."""

import shutil

import pytest

from rag.almacen import AlmacenMemoria
from rag.consulta import responder
from rag.escenarios import MANUAL, REGLAMENTO, escribir_plazo
from rag.ingesta import CORPUS, reconstruir_indice
from rag.proveedores import EmbeddingsDoble, GeneradorDoble, Proveedores

PREGUNTA_NEBULA = "¿Cuántos minutos dura la reserva del telescopio Nébula?"


@pytest.fixture
def corpus(tmp_path):
    """Copia los documentos de clase para poder añadir, retirar y editar fuentes en cada prueba."""
    return shutil.copytree(CORPUS, tmp_path / "corpus")


@pytest.fixture
def consultar(corpus, cfg):
    """Mantiene la configuración y los proveedores fijos para aislar el efecto de cambiar el corpus."""
    almacen = AlmacenMemoria()
    proveedores = Proveedores(EmbeddingsDoble(), GeneradorDoble())

    def consulta(pregunta):
        """Reconstruye el índice y muestra qué documentos llegan al generador junto a la respuesta observada."""
        indice = reconstruir_indice(cfg, almacen, proveedores.embeddings, corpus)
        r = responder(cfg, almacen, proveedores, indice.indice_id, pregunta)
        print(f"\n{indice.indice_id} · {indice.n_documentos} documentos · similitud {r.mejor_similitud}")
        print("Documentos recuperados:", ", ".join(r.documentos_recuperados))
        print("Contexto del generador:", ", ".join(c["fragmento_id"] for c in r.contextos) or "rechazo previo")
        print("Respuesta:", r.texto)
        return r

    return consulta


def test_alta(corpus, consultar):
    """Comprueba que una pregunta inicialmente sin respuesta obtiene el nuevo dato y la cita tras la ingesta."""
    assert consultar(PREGUNTA_NEBULA).rechazo
    escribir_plazo(corpus, REGLAMENTO, 30)
    r = consultar(PREGUNTA_NEBULA)
    assert not r.rechazo and "30 minutos" in r.texto and REGLAMENTO in r.fuentes


def test_baja(corpus, consultar):
    """Retira la única fuente sobre el borrado de claves y comprueba que el índice reconstruido deja de servirla."""
    pregunta = "¿Cuánto dura el periodo de enfriamiento de una CMK antes de su borrado irreversible?"
    fuente = "04-almacenamiento-y-cifrado-kms"
    antes = consultar(pregunta)
    assert "72 horas" in antes.texto and fuente in antes.fuentes
    (corpus / f"{fuente}.md").unlink()
    despues = consultar(pregunta)
    assert fuente not in despues.documentos_recuperados
    assert despues.rechazo and not despues.fuentes and "72 horas" not in despues.texto


def test_actualizacion(corpus, consultar):
    """Sustituye el plazo en el mismo archivo y comprueba que desaparece el valor antiguo de la respuesta y el contexto."""
    escribir_plazo(corpus, REGLAMENTO, 30)
    assert "30 minutos" in consultar(PREGUNTA_NEBULA).texto
    escribir_plazo(corpus, REGLAMENTO, 45)
    r = consultar(PREGUNTA_NEBULA)
    assert REGLAMENTO in r.fuentes and "45 minutos" in r.texto and "30 minutos" not in r.texto
    plazos_del_reglamento = [c["contenido"] for c in r.contextos if c["documento_id"] == REGLAMENTO]
    assert any("45 minutos" in texto for texto in plazos_del_reglamento)
    assert all("30 minutos" not in texto for texto in plazos_del_reglamento)


@pytest.fixture
def conflicto(corpus, consultar):
    """Crea dos fuentes sin fecha ni prioridad que dan plazos incompatibles para la misma reserva."""
    escribir_plazo(corpus, REGLAMENTO, 30)
    escribir_plazo(corpus, MANUAL, 90)
    return consultar(PREGUNTA_NEBULA)


def test_conflicto_llega_al_contexto(conflicto):
    """Comprueba por documento y contenido que las dos afirmaciones enfrentadas llegaron al generador."""
    for fuente, plazo in ((REGLAMENTO, "30 minutos"), (MANUAL, "90 minutos")):
        assert any(c["documento_id"] == fuente and plazo in c["contenido"] for c in conflicto.contextos)


@pytest.mark.xfail(
    strict=True, raises=AssertionError, reason="El generador doble copia frases y carece de regla de conflicto"
)
def test_conflicto_sin_precedencia_debe_abstenerse(conflicto):
    """Evalúa la política propuesta para el taller: abstenerse cuando dos fuentes de igual autoridad discrepan."""
    assert conflicto.rechazo, f"Esperábamos una abstención ante plazos incompatibles. Salida: {conflicto.texto}"
