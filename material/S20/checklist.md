# Lista previa al directo · S20 (02/12/2026, L/X)

## La víspera

- [ ] Confirmar con Laura si la sesión es construcción guiada, revisión o defensa, y si hay
      rúbrica o fecha de entrega. Si las hay, actualizar la diapositiva 23 y `enunciado.md`.
- [ ] Revisar el guion ([proyecto-final/docs/guion-clase.md](proyecto-final/docs/guion-clase.md))
      y hacer un ensayo oral con cronómetro.
- [ ] Desde una copia limpia del proyecto: `uv sync && uv run pytest && uv run python -m agente.cli recorridos`.
- [ ] Docker Desktop arrancado; `docker compose up -d --wait` y `uv run pytest -m db` en verde.
- [ ] Ensayo completo: `uv run python demo_clase.py --sin-pausa` termina en «Fin del recorrido.» sin fallos.
- [ ] Si se quiere enseñar Langfuse: proyecto de laboratorio propio, claves en variables de la
      terminal (nunca en pantalla ni en archivos), y un turno de prueba.
- [ ] Subir la presentación (PPTX/PDF) y el proyecto a la plataforma, según indique la escuela.

## 30 minutos antes

- [ ] Una terminal en `material/S20/proyecto-final/`, fuente grande, tema oscuro.
- [ ] `docker compose up -d --wait`
- [ ] Dejar escrito `uv run python demo_clase.py` sin ejecutar: se lanza en la diapositiva 6.
      Al empezar vacía conversaciones y trabajos e ingesta el corpus.
- [ ] Editor abierto en `agente/grafo.py`; navegador listo para `http://127.0.0.1:8020/docs`.
- [ ] Comprobar si hay internet (para `S20_FUENTES=red`); si no, usar las copias de aula.
- [ ] Presentación en modo presentador con notas visibles solo para el profesor.
- [ ] Reunión, pantalla compartida y grabación comprobadas.

## Durante

- [ ] QR un minuto en la diapositiva 2 (evalúa S19 del 30/11).
- [ ] Decir al empezar que todo corre en el perfil doble (sin modelo ni coste).
- [ ] No mostrar claves, tokens reales ni la URL de la base con contraseña.

## Al terminar

- [ ] Parar `uvicorn` (Ctrl+C) y `docker compose down` (conserva los datos; `-v` los borra).
- [ ] Anotar preguntas de los alumnos que convenga añadir a `docs/ejercicio.md`.
