# S18 · CI/CD + monitorización en producción

**AI Engineer · grupo L/X · miércoles 25/11/2026 · 18:30–20:00 (Madrid).**
Textos originales: [temario](fuentes/temario-S18-original.txt) e [ejercicio](fuentes/ejercicio-S18-original.txt),
leídos en Gmail el 16/11/2026 por la sesión anterior de preparación (solo lectura).

## Temario (correo de la escuela del 17/07/2026)

**Objetivo:** llevar una aplicación de IA a producción con las mismas garantías de calidad que
cualquier sistema de software.

**Contenidos:**

1. Conceptos básicos de CI/CD y entornos.
2. CI/CD con GitHub Actions.
3. Logging, monitoring y APM.
4. Error tracking.
5. Gestión de variables de entorno y secretos en despliegue.
6. Migraciones de base de datos en producción y despliegues sin downtime.
7. Disaster recovery y backups.

**Ejercicio:** montar un pipeline de CI/CD con tests automáticos.

## Ejercicio (adjunto `ejercicios.docx` del 29/09/2026)

Automatiza las pruebas, la construcción y el despliegue de una pequeña API de IA. Un cambio con
errores debe quedar bloqueado antes de desplegarse. Demuestra además cómo detectar un fallo y
volver a una versión anterior en un entorno de pruebas.

Resumen de los requisitos (texto completo en la fuente):

| # | Requisito |
|---|---|
| E1 | FastAPI con `/health` y endpoint de IA; configuración local y de staging; modelos y secretos fuera del código; GitHub + ECS/Fargate |
| E2 | En cada PR: dependencias bloqueadas, análisis de código, pytest y build Docker |
| E3 | Tests de entrada inválida, respuesta válida y fallo del proveedor con respuestas simuladas |
| E4 | Fallo deliberado detectado por el workflow |
| E5 | Acciones externas fijadas al SHA completo (40 caracteres) de un commit verificado |
| E6 | Tras integrar en main: repetir checks sobre ese commit, publicar en ECR y registrar el digest |
| E7 | Desplegar a staging con `workflow_dispatch` desde main, por digest o tag inmutable, sin reconstruir |
| E8 | Verificar `/health` y una petición funcional; un job correcto no basta |
| E9 | OIDC: job con `environment: staging`, `sub` del entorno real, `aud = sts.amazonaws.com` |
| E10 | Environment `staging` solo desde main; las PR sin credenciales de despliegue; credenciales temporales |
| E11 | Logs en CloudWatch con request ID, versión, duración y estado, sin secretos |
| E12 | Localizar un error de prueba; panel básico de errores y latencia |
| E13 | Segunda versión y rollback al digest anterior; comprobar el endpoint |
| E14 | README: despliegue progresivo, cambios de BD compatibles, backups con prueba de restauración |
| E15 | Ampliación opcional: alerta automática o migración compatible y restauración con datos ficticios |
| E16 | Entrega: app, workflows, tests, evidencias de bloqueo/despliegue/rollback y limpieza |

Dedicación orientativa del enunciado: 6–8 horas con la infraestructura del laboratorio preparada.
La práctica es **opcional** según la aclaración de la escuela del 04/11/2026
([indicaciones](fuentes/indicaciones-laura.md)).
