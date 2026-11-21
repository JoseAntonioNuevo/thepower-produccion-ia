# Comprobación antes del directo S18 · 25/11/2026

## Autorizaciones de José (antes del 24/11)

- [ ] Publicar el repositorio de la demo en GitHub (público) y crear el environment `staging`.
- [ ] Crear los stacks `…-registro` y `…-staging` en eu-north-1 con el perfil del aula.
- [ ] Ensayo completo: PR roja, publicación A y B, despliegue de B, error localizado, rollback a A y retirada.
- [ ] Decidir si los recursos se mantienen hasta el directo (coste de una tarea Fargate pequeña y logs) o se recrean ese día.

## Ensayo (si está autorizado)

- [ ] `Diagnóstico · OIDC` leído; `SubPublicar` y `SubDesplegar` iguales al `sub` real.
- [ ] Dispatch desde una rama distinta de `main` rechazado por el environment.
- [ ] La PR roja no puede integrarse (ruleset con el check obligatorio).
- [ ] Digest de A y B anotados; el resumen del despliegue muestra Antes/Después.
- [ ] El smoke del workflow pasa contra staging y la regla temporal del puerto se retira.
- [ ] Error de B localizado por `request_id` en CloudWatch; panel con 5xx y p95; alarma en ALARM y de vuelta a OK.
- [ ] Rollback a A: salud y `/clasificar` en 200 con la versión de A.
- [ ] Capturas saneadas guardadas (sin ID de proyecto, IP ni claves) por si falla la red en directo.
- [ ] Retirada comprobada o recursos conservados con decisión explícita.

## El día de la clase

- [ ] Grupo L/X, 18:30–20:00 Madrid; QR de AI Engineer vigente: evalúa **S17 del 23/11**.
- [ ] Presentación `presentaciones/S18-cicd-monitorizacion.pptx` (y PDF) enviada a la escuela para la plataforma.
- [ ] Terminal con letra grande; `uv sync --locked` y las imágenes `s18:A` y `s18:B` construidas (comandos.md, paso 0).
- [ ] Docker arrancado; `uv run pytest -q` → 23 passed.
- [ ] Pestañas: repositorio, Actions, ECR, ECS, panel y Logs Insights (solo si hubo ensayo real).
- [ ] Nada de `.env`, claves, ID de proyecto ni credenciales en pantalla.
- [ ] Rotular como «ilustrativo» cualquier valor que no proceda del ensayo.

## Después

- [ ] Retirar recursos (README de la demo, paso 9) o confirmar que siguen por decisión de José.
- [ ] Anotar en `verificacion.md` qué se ejecutó de verdad en el directo.
