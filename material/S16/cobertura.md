# Matriz de cobertura de S16

Los **26 puntos de cobertura** del temario y de la práctica opcional tienen una ubicación explícita en presentación y guion. La última columna distingue cobertura docente y evidencia técnica: disponer de una explicación y una plantilla no acredita haberlas ejecutado en AWS. La ampliación opcional se cuenta aparte.

Fuente del temario: `docs/fuentes/temario-ai-engineer.txt`. Fuente del ejercicio: `AI_Engineer_enunciados.docx`, página 5, enviado el 28/09/2026. T = temario; E = ejercicio; O = opcional.

| ID | Requisito | Diapositivas | Bloque del guion | Evidencia y límite |
|---|---|---|---|---|
| T01 | Introducción a proveedores cloud | 4,5 | Cloud y mapa de servicios | Explicación |
| T02 | AWS básico: cuenta, región, zonas y recursos | 4,11 | Cloud y mapa de servicios | Explicación |
| T03 | Comparación AWS, Azure y Google Cloud | 5 | Cloud y mapa de servicios | Explicación |
| T04 | Compute: VM, contenedor y función | 7,11 | Cloud y mapa de servicios | Explicación |
| T05 | Storage: objetos, disco, BD, imágenes y logs | 7 | Cloud y mapa de servicios | Explicación |
| T06 | Networking: VPC, subred, rutas, IP, DNS y SG | 15 | Publicación y Fargate | Plantilla validada; ensayo AWS pendiente |
| T07 | Seguridad: identidad, permisos, red y responsabilidad | 4,13,15 | Cloud y mapa de servicios; Publicación y Fargate | Explicación y plantillas |
| T08 | Optimización de costes | 18,19,20,21 | Costes y optimización | Calculadora ejecutada; consumos supuestos |
| T09 | Docker: imagen, contenedor, puertos, capas y configuración | 8,10,23 | API y Docker local | Contenedor amd64 y HTTP verificados |
| T10 | Primer vistazo a IA gestionada en cada nube | 5,6 | Cloud y mapa de servicios | Explicación con servicios oficiales |
| E01 | FastAPI con salud y endpoint que invoque IA | 9,16 | API y Docker local; Evidencia funcional | HTTP demo y adaptador con transporte simulado; inferencia real pendiente |
| E02 | Modelo por variable y dependencias fijadas | 9,10 | API y Docker local | Lock instalado y configuración comprobada |
| E03 | Dockerfile, dockerignore y usuario no root | 8,10,23 | API y Docker local | Build e id 10001 verificados |
| E04 | Probar ambos endpoints localmente | 9,16 | API y Docker local | Ensayo HTTP demo correcto; proveedor real pendiente |
| E05 | Publicar imagen identificable en ECR | 11,12,16 | Publicación y Fargate | CLI y guardas probados; push AWS pendiente |
| E06 | Desplegar ECS/Fargate | 11,14,15,16 | Publicación y Fargate | CloudFormation validada estáticamente; deploy pendiente |
| E07 | Compatibilidad Apple Silicon, amd64 o ARM64 | 10 | API y Docker local | Build linux/amd64 y tarea X86_64 alineados |
| E08 | Secrets Manager o Parameter Store referenciados en tarea | 13,14 | Publicación y Fargate | Secrets Manager implementado; SSM explicado; remoto pendiente |
| E09 | Execution role, task role y KMS propia si se usa | 13,14 | Publicación y Fargate | Políticas y condición KMS validadas estáticamente |
| E10 | IP temporal, puerto/IP restringidos, salida, datos ficticios y sin claves por HTTP | 15 | Publicación y Fargate | /32 exigido, salida TLS; lectura AWS pendiente |
| E11 | 730 horas: CPU, memoria, ECR, logs, IPv4 y tráfico | 18,19 | Costes y optimización | Tarifas públicas leídas; cálculo reproducido |
| E12 | Inferencia separada, supuestos/tarifas y extras solo si se usan | 18,19,20 | Costes y optimización | Modelo de costes documentado; consumo real pendiente |
| E13 | Retirar tareas, imágenes, secretos, logs y red | 21 | Limpieza e inventario | Procedimiento preparado; retirada AWS pendiente |
| E14 | Revisar remanentes y conservar recursos compartidos | 21 | Limpieza e inventario | Guardas de propiedad probadas; inventario AWS pendiente |
| E15 | Comparar mes completo con demo y apagado | 19,20,21 | Costes y optimización | 13,78 USD y 0,46 USD con supuestos explícitos |
| E16 | Entrega: código, infraestructura/instrucciones, evidencias, coste y limpieza | 22 | Ejercicio y preguntas | Paquete local preparado; evidencia AWS pendiente |
| O01 | Opcional: HTTPS con balanceador y tareas privadas; coste/limpieza incluidos | 15,22 | Ejercicio y preguntas | Explicado como ampliación; no implementado |

Las diapositivas 3, 12, 14 y 20 añaden recorrido, publicación en ECR, lectura de la tarea y desglose de costes. La práctica es voluntaria; la matriz describe los criterios para completarla.

## Cierre docente y cierre operativo

La preparación documental cubre los 26 puntos. El cierre operativo exige, además, un ensayo de la versión final con cuenta, permisos y presupuesto del laboratorio: push a ECR, despliegue, inferencia real, readback de identidad, limpieza e inventario. El ensayo oral de José y la comprobación de reunión/grabación se realizan antes del directo.

Los archivos de referencia de S17–S20 se encuentran en `docs/cobertura-S16-S20.md`; no se consideran clases ya preparadas por existir esta base.
