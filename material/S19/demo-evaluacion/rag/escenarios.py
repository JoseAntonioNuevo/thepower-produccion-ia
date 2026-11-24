"""Versiones del corpus para comparar en clase una sola modificación sin tocar los documentos originales."""

import shutil
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

from rag.ingesta import CORPUS

ESCENARIOS = ("base", "alta", "baja", "actualizacion", "conflicto")
REGLAMENTO = "11-reglamento-nebula"
MANUAL = "12-manual-nebula"


def escribir_plazo(corpus: Path, documento: str, minutos: int):
    """Escribe el mismo documento de prueba que se consulta desde pytest y desde el chat."""
    (corpus / f"{documento}.md").write_text(
        f"# {documento.split('-', 1)[1]}\nLa reserva del telescopio Nébula dura {minutos} minutos.\n",
        encoding="utf-8",
    )


@contextmanager
def corpus_de(escenario: str):
    """Prepara una vista temporal, partiendo siempre de los diez documentos de la clase."""
    if escenario not in ESCENARIOS:
        raise ValueError(f"Corpus desconocido: {escenario}")
    if escenario == "base":
        yield CORPUS
        return
    with TemporaryDirectory(prefix="s19-corpus-") as temporal:
        carpeta = shutil.copytree(CORPUS, Path(temporal) / "corpus")
        if escenario == "baja":
            (carpeta / "04-almacenamiento-y-cifrado-kms.md").unlink()
        else:
            escribir_plazo(carpeta, REGLAMENTO, 45 if escenario == "actualizacion" else 30)
            if escenario == "conflicto":
                escribir_plazo(carpeta, MANUAL, 90)
        yield carpeta
