# Cobertura de S18

Cada punto del temario (17/07/2026) y del ejercicio (29/09/2026) con la diapositiva, la parte de
la demo o el documento que lo cubre, y su evidencia. «Local» = ejecutado el 17/11/2026 sin cuentas;
«pendiente» = requiere el ensayo autorizado en GitHub y AWS.

## Temario

| Punto | Diapositivas | Demo o documento | Evidencia |
|---|---|---|---|
| Objetivo: garantías de calidad en producción | 1, 6, 40 | README de la demo | — |
| Qué es CI/CD y qué es monitorizar, con casos de uso (añadido a petición de José, 20/11) | 3, 4, 5 | — | Señales doradas (Google SRE) y métricas DORA leídas el 20/11/2026 |
| Conceptos básicos de CI/CD y entornos | 3, 7, 8, 9 | `.env.example`, `infra/02-staging.yaml` | Conceptual + plantillas validadas |
| CI/CD con GitHub Actions | 10, 11, 12, 13, 15, 16, 23, 24 | `.github/workflows/` (5) | actionlint ✓; ejecución pendiente |
| Qué es una GitHub Action y dónde se ejecuta (añadido a petición de José, 17/11) | 11 | `action.yml` real de configure-aws-credentials v6.3.0 | `gh api` ✓ |
| Alternativas a GitHub Actions con precios, ventajas e inconvenientes (añadido a petición de José, 17/11) | 17, 18 | — | Precios oficiales consultados 17/11/2026 (`.build/s18/investigacion/`) |
| APM, error tracking y despliegue sin corte en profundidad (añadido a petición de José, 17/11) | 28, 32, 34 | `extras/despliegue_sin_corte.py` | Documentación oficial con Context7 (`.build/s18/investigacion/ctx7-*`); demo local real |
| Logging, monitoring y APM | 30, 31, 32, 35 | `app.py` (`registrar`, `observar`), filtros, panel; cascada de spans con el proveedor del caso (32) | Logs reales en local; CloudWatch pendiente; traza ilustrativa (OpenTelemetry no integrado) |
| Error tracking | 30, 33, 34 | línea `excepcion`, alarma de 5xx; incidencia agrupada por huella con frecuencia, usuarios y release (34) | Error localizado en local por request_id; esquema rotulado (Sentry no integrado) |
| Variables de entorno y secretos en despliegue | 8, 20, 21, 22 | `.env.example`, `Secrets` de la tarea, OIDC | Plantillas validadas; OIDC real pendiente |
| Migraciones de BD en producción y despliegues sin downtime | 25, 27, 28, 37 | `extras/migracion_y_restauracion.py`, `extras/despliegue_sin_corte.py`, rolling 100/200 % | Scripts ejecutados (sin corte: 0 fallos frente a ≈60); rolling real pendiente; sin ALB en el laboratorio |
| Disaster recovery y backups | 38 | `extras/`, README de la demo («Copias de seguridad») | Restauración con SQLite ✓ |
| Ejercicio: pipeline de CI/CD con tests automáticos | 13–15, 39 | `docs/ejercicio.md` | — |

## Ejercicio

| # | Requisito | Diapositivas | Dónde en la demo | Evidencia |
|---|---|---|---|---|
| E1 | FastAPI con /health y endpoint de IA; local y staging; secretos fuera del código; GitHub + ECS/Fargate | 6, 8, 20 | `app.py`, `.env.example`, `infra/02-staging.yaml` | Tests y plantillas ✓ |
| E2 | En cada PR: lock, análisis, pytest y build | 13 | `comprobaciones.yml`, `ci-pr.yml` | Mismos comandos en local ✓ |
| E3 | Entrada inválida, respuesta válida y fallo del proveedor con dobles | 14 | `tests/test_api.py` | 23 passed ✓ |
| E4 | Fallo deliberado detectado | 15 | `cambios/01-pr-con-fallo.patch` | 2 failed en local ✓; PR real pendiente |
| E5 | Acciones por SHA completo verificado | 16 | los 5 workflows | `gh api` ✓ (`.build/s18/logs/acciones-sha.txt`) |
| E6 | Main repite checks, publica en ECR y registra el digest | 19, 23 | `publicar-main.yml`, `infra/01` | Pendiente |
| E7 | workflow_dispatch desde main, por digest, sin reconstruir | 24, 29 | `desplegar-staging.yml` | Pendiente |
| E8 | /health y petición funcional; un job verde no basta | 25, 26 | `scripts/smoke.sh` | Smoke local de A y B ✓; staging pendiente |
| E9 | OIDC: environment staging, sub real, aud | 21, 22 | `diagnostico-oidc.yml`, `RolDesplegar` | Plantilla ✓; sub real pendiente |
| E10 | Staging solo desde main; PR sin credenciales; credenciales temporales | 15, 22 | README de la demo (paso 4), `ci-pr.yml` | Pendiente |
| E11 | Logs en CloudWatch con request ID, versión, duración y estado, sin secretos | 31 | `app.py`, `awslogs` en la tarea | Formato y test ✓; CloudWatch pendiente |
| E12 | Localizar un error; panel de errores y latencia | 33, 35 | filtros, `Panel`, `docs/comandos.md` | Local ✓; panel real pendiente |
| E13 | Segunda versión y rollback al digest anterior | 29, 36 | `cambios/02`, `desplegar-staging.yml` | A → B → A con Docker ✓; staging pendiente |
| E14 | README: progresivo, BD compatible, backups con restauración | 27, 28, 37, 38 | README de la demo («Plan para proteger los datos») | Escrito ✓ |
| E15 | Ampliación: alerta o migración y restauración ficticias | 35, 37, 38 | `AlarmaErrores`, `extras/` | Script ✓; alarma pendiente |
| E16 | Entrega con evidencias y limpieza | 39 | README de la demo (paso 9), `docs/ejercicio.md` | Pasos escritos; retirada real pendiente |

## Indicaciones de la escuela

| Indicación | Dónde |
|---|---|
| QR al inicio, el correcto, explicar para qué sirve; insistir en la encuesta | Diapositiva 2 y notas; recordatorio en la 40 |
| Diapositivas que se entiendan solas, intercaladas con la práctica | Frases completas; cinco momentos de demo (15, 23, 29, 33, 36) y la demostración local de la 28 |
| Práctica opcional, pasos claros, repositorio menos denso | Diapositiva 39; demo de un archivo de app y cinco workflows cortos |
| Enviar la presentación antes de la clase | Checklist (no se ha enviado nada) |
