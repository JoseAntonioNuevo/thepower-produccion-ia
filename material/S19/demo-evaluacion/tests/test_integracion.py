"""Tests que NO se ejecutan por defecto: PostgreSQL real (`db`) y modelos de pago (`llm`).

uv run pytest -m db                       necesita `docker compose up -d` (sin coste)
S19_EJECUTAR_REAL=1 uv run pytest -m llm  consume la API: solo con el gasto autorizado
"""

import os

import pytest

from rag.almacen import AlmacenPg
from rag.config import cargar_config
from rag.consulta import responder
from rag.ingesta import reconstruir_indice
from rag.proveedores import EmbeddingsDoble, GeneradorDoble, Proveedores, crear_proveedores
from tests.conftest import config


@pytest.mark.db
def test_pgvector_reconstruye_sin_duplicar_y_busca_por_coseno():
    # chunk_size propio del test: su índice no pisa los de la práctica (A=320, B=900).
    cfg = config(chunk_size=333, database_url=cargar_config().database_url)
    almacen, prov = AlmacenPg(cfg.database_url), Proveedores(EmbeddingsDoble(), GeneradorDoble())
    try:
        primero = reconstruir_indice(cfg, almacen, prov.embeddings)
        segundo = reconstruir_indice(cfg, almacen, prov.embeddings)
        assert primero == segundo == almacen.leer_indice(primero.indice_id)
        assert almacen.contar(primero.indice_id) == primero.n_fragmentos
        r = responder(
            cfg,
            almacen,
            prov,
            primero.indice_id,
            "¿Qué crédito corresponde si la disponibilidad mensual es inferior al 99,00 %?",
        )
        assert r.documentos_recuperados[0] == "05-sla-y-creditos-servicio"
        assert 0.0 < r.mejor_similitud <= 1.0
    finally:
        with almacen._conectar() as con:
            con.execute("DELETE FROM indices WHERE chunk_size = 333")


@pytest.mark.db
def test_indices_de_distinta_dimension_conviven_en_la_misma_base():
    """Cambiar de modelo de embeddings en .env no obliga a vaciar la base: cada índice guarda
    su dimensión y la búsqueda solo compara vectores de ese índice."""
    from rag.almacen import Indice
    from rag.corpus import Fragmento

    almacen = AlmacenPg(cargar_config().database_url)
    almacen.preparar_esquema()
    indices = []
    try:
        for dim in (768, 1536):
            indice = Indice(f"idx-prueba-dim-{dim}", "real", f"modelo-{dim}", dim, 100, 0, 1, 2)
            filas = [
                (
                    Fragmento(f"doc#{i}", "doc", i, "t", f"texto {dim} {i}", f"h-{dim}-{i}"),
                    [float(i + 1)] + [0.0] * (dim - 1),
                )
                for i in range(2)
            ]
            almacen.reconstruir(indice, filas)
            indices.append(indice)
        for indice in indices:
            hallazgos = almacen.buscar(indice.indice_id, [1.0] + [0.0] * (indice.embedding_dim - 1), 5)
            assert {h.contenido.split()[1] for h in hallazgos} == {str(indice.embedding_dim)}
            assert almacen.leer_indice(indice.indice_id).embedding_dim == indice.embedding_dim
    finally:
        with almacen._conectar() as con:
            con.execute("DELETE FROM indices WHERE indice_id LIKE 'idx-prueba-dim-%'")


@pytest.mark.llm
def test_rag_real_responde_con_fuente_y_rechaza_lo_que_no_consta():
    if os.environ.get("S19_EJECUTAR_REAL") != "1" or os.environ.get("S19_PERFIL") != "real":
        pytest.skip("evaluación real: exige S19_PERFIL=real, OPENROUTER_API_KEY y S19_EJECUTAR_REAL=1")
    from rag.config import aplicar_variante, cargar_calibracion
    from rag.ingesta import indice_esperado

    cfg = cargar_calibracion(aplicar_variante(cargar_config(), "A"))
    almacen, prov = AlmacenPg(cfg.database_url), crear_proveedores(cfg, execute=True)
    indice_id = indice_esperado(cfg)  # el índice real se crea antes con `ingestar --execute`
    si = responder(cfg, almacen, prov, indice_id, "¿Qué versión de TLS exigen las pasarelas perimetrales?")
    assert not si.rechazo and "1.3" in si.texto and si.fuentes
    no = responder(cfg, almacen, prov, indice_id, "¿Cuál es el teléfono de guardia de AetherCloud en Lisboa?")
    assert no.rechazo
