# S18 · CI/CD + monitorización en producción

**AI Engineer · grupo L/X · miércoles 25/11/2026 · 18:30–20:00 (hora de Madrid).**
Profesor: José Antonio Nuevo. Sesión anterior del grupo: S17 (Bedrock + Lambda, 23/11).

Objetivo del temario: llevar una aplicación de IA a producción con las mismas garantías de
calidad que cualquier sistema de software. En la clase se demuestra que un cambio defectuoso
queda bloqueado, que se despliega exactamente el artefacto probado y que se puede volver a una
versión conocida.

**QR:** evalúa la **S17 del 23/11** (diapositiva 2). La práctica es **opcional** (escuela, 04/11).

## Piezas

1. **[PowerPoint](presentaciones/S18-cicd-monitorizacion.pptx)** y [PDF](presentaciones/S18-cicd-monitorizacion.pdf):
   40 diapositivas con notas del orador (3–5, punto de partida: qué es CI/CD, qué es monitorizar y casos de uso, añadidas el 20/11); diseño de la presentación final de S17 (8, 14 y 15 añadidas el 17/11: qué es una action y alternativas con precios; 27, 29 y 33 añadidas el 17/11: APM, error tracking y cómo se demuestra un despliegue sin corte).
   Fuente editable en [fuentes/presentacion](fuentes/presentacion/README.md).
2. **[demo-cicd](demo-cicd/README.md)**: proyecto autónomo con forma de repositorio publicable.
   API FastAPI, 23 tests, Dockerfile, cinco workflows con acciones fijadas por SHA, plantillas
   de registro y de staging (ECS/Fargate, OIDC, logs, panel y alarma), parches para la demo
   (PR roja, versión B y el test que faltaba) y ampliación de migración y restauración.
3. [Guion de 90 minutos](demo-cicd/docs/guion-clase.md) · [comandos en el orden de la presentación](demo-cicd/docs/comandos.md) ·
   [práctica opcional](demo-cicd/docs/ejercicio.md).
4. [Enunciado](enunciado.md) · [cobertura](cobertura.md) · [verificación](verificacion.md) ·
   [checklist](checklist.md) · [fuentes](fuentes.md).
5. Originales: [temario](fuentes/temario-S18-original.txt), [ejercicio](fuentes/ejercicio-S18-original.txt) e
   [indicaciones de la escuela](fuentes/indicaciones-laura.md) (Gmail, leídos el 16/11/2026).

## Estado real (17/11/2026)

| Comprobado en local | Pendiente de autorización de José |
|---|---|
| `uv sync --locked`, lock = `requirements.lock`, ruff, formato, 23 tests | Publicar el repositorio de la demo en GitHub |
| `cfn-lint` de las dos plantillas (también para eu-north-1) | Crear los stacks en AWS (eu-north-1) |
| `actionlint` de los cinco workflows; SHA de las acciones con `gh api` | Ejecutar los workflows en GitHub Actions |
| `docker build` y smoke de las imágenes A y B | Publicar en ECR, desplegar en ECS, OIDC real |
| PR con fallo en rojo (2 tests), B verde con regresión (500), arreglo (27 tests) | Error en CloudWatch, panel y alarma reales |
| Recorrido A → B → A con Docker; migración y restauración con SQLite | Rollback real en staging y retirada de recursos |
| Despliegue sin corte en loopback (`extras/despliegue_sin_corte.py`): 0 fallos frente a ≈60 | Continuidad real en AWS (requeriría un ALB que el laboratorio no tiene) |

Detalle y comandos: [verificacion.md](verificacion.md). Los pasos exactos para el ensayo real
están en el [README de la demo](demo-cicd/README.md), pasos 4–9. Nada se ha publicado ni desplegado.
