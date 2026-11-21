# Práctica opcional S18 · Pipeline de CI/CD con tests automáticos

Enunciado original (29/09/2026): automatiza las pruebas, la construcción y el despliegue de una
pequeña API de IA. Un cambio con errores debe quedar bloqueado antes de desplegarse. Demuestra
además cómo detectar un fallo y volver a una versión anterior en un entorno de pruebas.

La práctica es **opcional** (aclaración de la escuela del 04/11). Esta carpeta es una solución
completa de referencia; puedes partir de ella o de tu propia API de la sesión 16. Usa solo
incidencias ficticias. Dedicación orientativa: 6–8 horas con el proveedor OIDC, el rol y los
recursos del laboratorio preparados.

## Pasos

1. **API y configuración.** FastAPI con `/health` y un endpoint de IA. Configuración local
   (`.env`, fuera de Git) y de staging (variables de la tarea y Secrets Manager). Ningún modelo
   ni clave en el código.
2. **Tests sin APIs de pago.** Con un doble del proveedor: entrada inválida, respuesta válida y
   fallo del proveedor. `uv run pytest` debe pasar sin red.
3. **CI en cada pull request.** Dependencias bloqueadas (`uv sync --locked`), análisis
   (ruff), pytest y `docker build`. Sin credenciales de AWS en ese workflow.
4. **Bloqueo demostrado.** Una PR con un fallo deliberado queda roja y no se puede integrar
   (regla de rama con el check obligatorio). Guarda captura o enlace.
5. **Acciones por SHA.** Cada `uses:` externo con el SHA completo de 40 caracteres de un commit
   verificado y la versión en un comentario.
6. **Publicar desde main.** Repite las comprobaciones sobre el commit integrado; si pasan,
   construye una vez, publica en ECR (etiquetas inmutables) y registra el digest.
7. **OIDC bien configurado.** Lee el `sub` real con un job de diagnóstico. El rol de despliegue
   confía en `…:environment:staging` y `aud = sts.amazonaws.com`, con `StringEquals`.
8. **Solo main despliega.** El environment `staging` admite únicamente la rama `main`.
9. **Desplegar por digest.** `workflow_dispatch` desde `main` con `repo@sha256:…`, sin
   reconstruir. Comprueba `/health` y una petición funcional contra el servicio real.
10. **Observar.** Logs en CloudWatch con `request_id`, versión, duración y estado, sin secretos.
    Provoca un error de prueba, localízalo por su `request_id` y revisa errores y latencia en un panel.
11. **Rollback.** Despliega una segunda versión y vuelve a la anterior con su digest. Repite la
    comprobación del endpoint.
12. **Datos.** En el README: despliegue progresivo, cambios de base de datos compatibles con la
    versión anterior y copias con prueba de restauración (no hace falta añadir una base de datos).
13. **Limpieza.** Elimina tus recursos y documenta los pasos.

## Entrega

Aplicación, workflows, tests, evidencias (PR bloqueada, digest publicado, despliegue, error
localizado, rollback) y los pasos de limpieza. Se valoran el bloqueo de cambios defectuosos, el
uso del mismo artefacto, los secretos protegidos y la recuperación comprobable.

**Ampliación opcional:** una alarma automática (la plantilla de staging incluye una) o una
migración compatible y una restauración con datos ficticios (`extras/`). Nunca sobre producción real.

## Comprobación rápida antes de entregar

- [ ] La PR defectuosa está en rojo y su workflow no declara `id-token: write`.
- [ ] El digest desplegado es el que publicó `Publicar · main` para ese commit.
- [ ] Un `workflow_dispatch` desde otra rama no llega a obtener credenciales.
- [ ] El `sub` de la confianza es exactamente el que emite tu repositorio.
- [ ] Después del despliegue y del rollback, `/health` y `/clasificar` responden con la versión esperada.
- [ ] Ningún log contiene el texto de la incidencia ni una clave.
- [ ] No queda ningún recurso tuyo en AWS.
