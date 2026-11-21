# Preparación AWS S16 · 11/11/2026

## Alcance y resultado

Preparación autorizada del apoyo para `material/S16/demo-openrouter`, separada del laboratorio Anthropic de la raíz y de S17. Proyecto AWS verificado por MCP y SDK local: For Each and Every, ID 123456789012, perfil thepower-aws, región eu-north-1. MCP cargado con AWS_MCP_PROXY_PROFILES=thepower-aws y sesión STS coincidente. Plan FREE activo, crédito informado 100 USD; no es una factura ni una promesa de saldo futuro.

Se crearon secreto s16/thepower/openrouter, rol s16-thepower-ecs-execution con política s16-runtime-only, grupo de logs /s16/thepower/api con retención de 3 días, security group s16-thepower-api y cluster vacío s16-thepower. También se creó AWSServiceRoleForECS, gestionado por ECS a nivel de proyecto; se conservará en la limpieza. La creación inicial del cluster falló por propagación de ese rol; tras su lectura, el segundo intento tuvo éxito. No quedaron clusters duplicados.

Reutilizados sin modificaciones: VPC predeterminada, tres subredes públicas, DNS, rutas, internet gateway y ACL. No existían workloads, ENI, NAT, endpoints ni EIP en la región. El grupo propio sigue sin entrada y con salida TCP 443; la IP /32 se configura justo antes del directo. No se creó ECR, definición de tarea, servicio, tarea, balanceador, NAT ni IPv4 pública.

La clave se transfirió directamente desde el archivo privado local mediante SDK, sin pasar su valor a herramientas remotas, argumentos de proceso, repositorio o recibos. Se comparó en memoria el secreto creado con el origen; coincidencia verificada sin revelar el valor. El archivo local sigue excluido de Git y del contexto Docker. SDK login requirió el extra botocore[crt], instalado por uv en un entorno efímero sin modificar pyproject/lock ni credenciales.

## Entrega local

- CLASE-AWS.md: ventanas, comandos por paso, resultados, modelo/proveedor, costes, IP, diagnóstico y retirada propia.
- aws/contexto.sh y actualizar-ip.sh: perfil/región explícitos, comprobación de proyecto y grupo; regla única /32 reemplazable.
- aws/task-definition.json y network.json: plantillas preparadas, nunca registradas en AWS.
- aws/execution-policy.json y execution-trust.json: políticas leídas de AWS, útiles para explicar el execution role.
- aws/preparacion-2026-11-11.json, tarifas-2026-11-11.json y verificacion-2026-11-11.json: recibos sin claves.
- README: enlace a la guía específica; el README público de alumnos sigue con su ejemplo genérico eu-west-1. App, Dockerfile y requirements.lock coinciden por hash de blob con main del repositorio público en la lectura realizada.

No hubo commit ni push; no se modificó el repositorio público. El checkout ya tenía archivos sin seguimiento al comenzar. No se cambió facturación, plan, límites de gasto o roles humanos/compartidos existentes. Se mantienen el secreto y los demás recursos de apoyo para el directo, tal como se solicitó.

## Evidencia

Disponibilidad regional confirmada por catálogo y llamadas reales a los servicios; cuota Fargate On-Demand 12 vCPU. Políticas y metadatos leídos después de crearlos. Access Analyzer ValidatePolicy sin hallazgos. Simulación IAM positiva para login/pull ECR, logs y secreto; negativa para otro secreto, push y borrado. PassRole y operaciones del operador del directo permitidas en simulación. Se requiere contexto aws:RequestedRegion=eu-north-1: sin él el simulador informa denegación por Organizations en servicios regionales. Esto no justifica modificar SCP ni ampliar permisos.

Docker Desktop se abrió; build linux/amd64 completado, /health y /clasificar en demo respondieron correctamente, entrada vacía devolvió 422 y contenedor temporal detenido. No se ejecutó inferencia real en esta sesión. No se publicaron imágenes ni se probó el camino de datos Fargate, capacidad efectiva, inyección de secretos, logs de tarea, HTTP remoto o limpieza. Los JSON validan contra los esquemas del SDK, sin llamadas de registro/despliegue.

Validación del actualizador de IP: sintaxis bash/zsh y cuatro escenarios offline con dobles (alta, sustitución, rechazo de /0, rechazo de otro proyecto); no hubo llamadas reales ni regla añadida. 45 tests del repositorio pasan; cfn-lint S16/S17 y preflight offline pasan. Ruff y formato de app.py pasan. Ruff global y formato global fallan en archivos preexistentes de generación de presentaciones ajenos a esta preparación (4.733 avisos, 19 archivos por formatear). No se aplicaron fixes fuera de alcance.

Price List API eu-north-1 consultada el 11/11: una tarea 0,25 vCPU + 0,5 GB e IPv4 cuesta 0,018575 USD/h de catálogo, sin secreto/imagen/logs/tráfico/inferencia/impuestos ni créditos. El secreto añade 0,40 USD/mes prorrateados y llamadas API; es el coste persistente preparado ahora. No se ha consultado una factura final ni supuesto coste real cero. La consulta de precios usó el endpoint global us-east-1 sin crear recursos allí. Logs de us-east-1 también inspeccionados: vacíos.

## Pendiente para clase y memoria

Revisar sesión/identidad/plan/créditos/saldo OpenRouter, comprobar región en AWS Settings, actualizar IP desde la red de clase. En directo: Docker local real, crear ECR/push, explicar/registrar tarea, crear servicio Fargate de una tarea, probar salud/clasificación remotas, mostrar logs/costes y retirar recursos propios según la guía. La limpieza preserva la red y AWSServiceRoleForECS, programa secreto a 7 días y no revoca la clave de OpenRouter.

OpenViking pendiente: el selector indicó workspace sin cuenta mapeada tanto para la demo como para la raíz real del repo. No se accedió a otra cuenta ni se creó tenant. Esta nota conserva el traspaso local sin secretos.
