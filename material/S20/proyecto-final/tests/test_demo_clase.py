"""Ensayo automático del modo clase: los 13 primeros pasos, en memoria y sin pausas.

    uv run pytest -m demo

El paso 14 ejecuta pytest y se deja fuera para no lanzar pytest dentro de pytest.
"""

import pytest

import demo_clase

pytestmark = pytest.mark.demo


def test_el_modo_clase_recorre_los_pasos_sin_fallos(monkeypatch, capsys):
    monkeypatch.setenv("S20_ALMACEN", "memoria")  # monkeypatch lo restaura al terminar
    monkeypatch.setenv("NO_COLOR", "1")
    assert demo_clase.main(["--sin-pausa", "--sin-postgres", "--hasta", "13"]) == 0
    salida = capsys.readouterr().out
    for n in range(1, 14):
        assert f"PASO {n} de 14" in salida
    assert "todo_ok:" in salida and "true" in salida
    assert (
        "proceso B responde:          En esta conversación todavía no hemos visto ningún ticket."
        in salida
    )
    assert "404 Conversación no encontrada" in salida
    assert "ha fallado" not in salida
