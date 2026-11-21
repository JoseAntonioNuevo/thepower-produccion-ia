"""Ingesta: reconstrucción desde documentos en bruto, sin duplicados y con identidad estable."""

import shutil

import pytest

from rag.almacen import AlmacenMemoria, ErrorIndice, Indice
from rag.consulta import recuperar
from rag.corpus import cargar_documentos, fragmentar, preparar
from rag.ingesta import CORPUS, indice_esperado, reconstruir_indice
from rag.proveedores import EmbeddingsDoble
from tests.conftest import config


def test_el_corpus_tiene_al_menos_ocho_documentos_ficticios():
    documentos = cargar_documentos(CORPUS)
    assert len(documentos) >= 8
    assert all(d.documento_id[:2].isdigit() for d in documentos)  # PROCEDENCIA.md no se indexa


def test_el_tamano_de_fragmento_cambia_el_numero_de_fragmentos():
    _, pequenos = preparar(CORPUS, 320, 0)
    _, grandes = preparar(CORPUS, 900, 0)
    assert len(pequenos) > len(grandes)
    assert max(len(f.contenido) for f in grandes) <= 900
    # Una frase más larga que chunk_size no se corta por la mitad: queda sola en su fragmento.
    largos = [f for f in pequenos if len(f.contenido) > 320]
    assert all(len(f.contenido) < 640 for f in largos)
    assert len({f.fragmento_id for f in pequenos}) == len(pequenos)


def test_reconstruir_dos_veces_no_duplica(cfg):
    almacen, emb = AlmacenMemoria(), EmbeddingsDoble()
    primero = reconstruir_indice(cfg, almacen, emb)
    segundo = reconstruir_indice(cfg, almacen, emb)
    assert primero == segundo
    assert almacen.contar(primero.indice_id) == primero.n_fragmentos


def test_un_documento_copiado_con_otro_nombre_no_entra_dos_veces(cfg, tmp_path):
    shutil.copytree(CORPUS, tmp_path / "corpus")
    original = almacen_n = reconstruir_indice(cfg, AlmacenMemoria(), EmbeddingsDoble(), tmp_path / "corpus")
    shutil.copy(tmp_path / "corpus" / "05-sla-y-creditos-servicio.md", tmp_path / "corpus" / "11-copia.md")
    con_copia = reconstruir_indice(cfg, AlmacenMemoria(), EmbeddingsDoble(), tmp_path / "corpus")
    assert (con_copia.n_documentos, con_copia.n_fragmentos) == (original.n_documentos, almacen_n.n_fragmentos)


def test_el_almacen_rechaza_fragmentos_repetidos(cfg):
    doc = cargar_documentos(CORPUS)[0]
    frag = fragmentar(doc, 320)[0]
    indice = Indice("idx-x", "doble", "doble-hash-768", 768, 320, 0, 1, 2)
    with pytest.raises(ErrorIndice, match="duplicados"):
        AlmacenMemoria().reconstruir(indice, [(frag, [0.0] * 768), (frag, [0.0] * 768)])


def test_menos_de_ocho_documentos_es_un_error(cfg, tmp_path):
    for ruta in sorted(CORPUS.glob("0[1-5]-*.md")):
        shutil.copy(ruta, tmp_path / ruta.name)
    with pytest.raises(ErrorIndice, match="al menos 8"):
        reconstruir_indice(cfg, AlmacenMemoria(), EmbeddingsDoble(), tmp_path)


def test_cambiar_la_fragmentacion_cambia_la_identidad_del_indice(cfg):
    assert indice_esperado(cfg) != indice_esperado(config(chunk_size=900))
    assert indice_esperado(cfg) == indice_esperado(config(prompt_version="v2"))  # el prompt no reindexa


def test_no_se_consulta_con_un_modelo_distinto_al_del_indice(cfg, sistema):
    almacen, _, indice_id = sistema
    otro = EmbeddingsDoble()
    otro.nombre = "otro-modelo"
    with pytest.raises(ErrorIndice, match="se creó con"):
        recuperar(cfg, almacen, otro, indice_id, "¿Qué TLS se exige?")


def test_consultar_un_indice_vacio_es_un_error_claro(cfg):
    with pytest.raises(ErrorIndice, match="ingestar"):
        recuperar(cfg, AlmacenMemoria(), EmbeddingsDoble(), "idx-no-existe", "¿hola?")
