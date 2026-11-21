# thePower Producción de IA

Repositorio independiente del curso AI Engineer. Alcance implementado:
base Python, S16 (FastAPI/Docker/Fargate) y S17 (Lambda/HTTP API IAM/Bedrock),
con código y paquetes docentes. S18–S20 están planificadas.

## Contratos

- La demo vigente de S17 está en `material/S17/demo-bedrock/`: un archivo
  Python, HTTP API con IAM y Nova Lite directo en eu-north-1. Su README
  prevalece sobre el paquete avanzado anterior para el recorrido de clase.
  No tiene fallback demo, clave de proveedor, S3 ni reserva de concurrencia.
  La inferencia real sigue pendiente por cuota cero de Bedrock; no presentarla
  como validada a partir de tests offline o del 503 controlado del ensayo.
- Python 3.12, instalación con `uv sync --frozen --all-extras` y `uv.lock`.
- `API_MODE=demo` es una simulación rotulada; `real` usa Anthropic Messages.
  Un error real nunca activa una simulación ni cambia de proveedor.
- `GET /health` comprueba el proceso; `POST /clasificar` valida entrada y salida.
- S17 reutiliza el contrato en un handler Lambda y usa IAM para Bedrock. El
  handler local de RIE es una demo explícita; la plantilla despliega el real.
- La firma usa credenciales temporales; no guardar headers Authorization.
- Sin datos personales, secretos en Git ni claves dentro de imágenes o materiales.
- Las categorías y prioridades proceden de S7/S8. El nuevo módulo es independiente
  y no requiere acceder a los otros repositorios ni a rutas de este Mac.
- Comentarios y guías en español: explicar finalidad, límites y pasos no triviales.
- No ampliar a RAG, Lambda, MCP o base de datos hasta trabajar su sesión.
- `CLAUDE.md` es un enlace relativo a este archivo.

## Verificación

`uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest`,
`uv run cfn-lint infra/s16/*.json infra/s17/*.json` y el preflight offline.
`scripts/ensayo_local.py` prueba una API de demostración en loopback y guarda un recibo.
La validación de Docker y de AWS es independiente de los tests Python.
No afirmar despliegue, coste real ni inferencia real a partir del modo demo.

## AWS

Los comandos de modificación de `scripts/aws_lab.py` requieren `--execute`, perfil,
región, cuenta esperada y nombre propio del laboratorio. Es una barrera del CLI,
no autorización para que un agente despliegue. Crear recursos, gastar o borrarlos
requiere que José haya autorizado esa operación y destino.
Las plantillas usan IP pública temporal y entrada restringida a una IPv4 /32.
La limpieza conserva los secretos externos y otros recursos compartidos.
S17 se opera con `uv run python -m scripts.aws_s17`: preflight/estado/logs son
lecturas; mutaciones e inferencias exigen `--execute`. El lote tiene seis
intentos como máximo y no reintenta fallos. Regiones, perfil y cuotas se leen
antes del deploy; no hay fallback a un perfil global.

## Memoria y entrega

El selector OpenViking no tiene una cuenta mapeada para este nuevo repositorio.
Conservar decisiones y evidencia local; no atribuir el proyecto a otro tenant.
El contexto completo está en `docs/` y la cobertura docente en `material/S16/`
y `material/S17/`. S17 también tiene un lock de runtime Lambda independiente.
Hacer el trabajo en el agente actual salvo petición explícita de delegación.
Commit, publicación y despliegue son etapas separadas que José debe solicitar.

<!-- BEGIN AWS Agent Toolkit rules -->
# AWS Guidance for the new AWS experience

This user has signed up for the new AWS experience. This experience lets you sign into AWS using a social provider and requires the following additional context.

Where this guidance conflicts with the project's own instructions, the project's instructions take precedence.

## Context

### Terminology:

- Say "project" instead of "account" — a project contains an AWS account and settings for sharing with other collaborators
- Say "team member" instead of "IAM user" — users are invited by email, not created or federated in IAM
- Say "AWS Settings" when referring to management tasks at [settings.aws.com](https://settings.aws.com/) (project management, billing, team members, spend limits). Users view their actual AWS resources in the AWS Management Console.
- Say "selected Region" when referring to the user's Region — not "home Region"
- The user has a managed IAM experience. This includes a managed service control policies (SCP) and resource control policies (RCP) that govern the use of AWS. They will still need to use IAM to create policies to let services work with each other. If there are questions about the SCPs or RCPs, go to the documentation at https://docs.aws.amazon.com/accounts/latest/reference/scps-and-rcps-for-projects.html

### Constraints:

- All projects share a single AWS Region determined by the user's contact address. Resources cannot be created in other Regions
- When developing:
  - MUST create all Regional resources in the project's assigned Region
  - You CAN create AWS WAF and Cloudwatch Logs resources in us-east-1 when there are global resources (like a global WAF instance) that require a connection to dependencies in us-east-1. You should not use these for any other reason, because resources in the selected Region will provide lower cost (due to no cross-Region traffic), increased availability (due to no cross-Region traffic), and easier manageability (due to not needing to look in another Region). When you need to do an inventory of resources, you need to look in both the selected Region and us-east-1 for Cloudwatch Logs or WAF resources.
  - MUST NOT attempt to create Lambda, API Gateway, or other Regional resources in any other Region
  - MUST direct users to confirm their Region in AWS Settings > View all projects > Overview > Additional Info > Region. If the user cannot confirm their Region, check in ~/.aws/config
  - MUST NOT use Lambda@Edge — excluded from both Lambda and CloudFront
  - MUST NOT use CloudFormation StackSets — no multi-account or multi-Region deployments
  - MUST NOT attempt cross-Region actions — no cross-Region replication for DynamoDB/S3/RDS, no multi-Region KMS keys
  - MUST NOT use Route 53 cross-Region routing — geolocation, latency-based, and failover routing policies are not available
  - CloudFront is a global service and its actions ARE allowed in `us-east-1`. A user can create a CloudFront distribution pointing to their project-region Lambda function URL or API Gateway. However, Lambda and API Gateway themselves MUST NOT be created in `us-east-1` — they must be in the project Region.
  - Reduced availability in `eu-north-1` specifically: Amazon Rekognition, Amazon Textract, Amazon Personalize, AWS App Runner are not available in that Region.
- IAM permissions for human access are managed by AWS. Don't assign roles to team members unless absolutely necessary
- The user may have a spend limit if they are on the paid plan. The limit that pauses their project if it's exceeded. If resources suddenly become inaccessible, ask if they have a spend limit configured. Only project owners can modify a spend limit.
- When developing:
  - MUST ask about spend limit status if the user reports sudden "Access Denied" errors on operations that previously worked
  - MUST direct users to check spend status in AWS Settings > Billing
  - MUST check if a user has upgraded their account to the paid plan
  - MUST ask the user if they want to clean up the successfully created resources or keep them to reduce cost
- The user sets up billing, creates spend limits, and retrieves and pays invoices in AWS Settings. The user creates budgets and optimizes their costs in the AWS Billing and Cost Management console
- Not all AWS services are available. If a service isn't working, do the following:
  1. Run the command `aws freetier get-account-plan-state`
  2. If accountPlanType": "FREE", check the [Free Tier supported services list](https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html#supported-services-free-tier) next,
  3. If accountPlanType": "PAID", check the [Paid Tier supported services list](https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html#supported-services-paid-plan).
  4. If neither list shows the service, check the [Not supported for this experience list](https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html#unsupported-services). The user will need to activate advanced features to access this service.
- Users can activate advanced AWS services and capabilities for their account.
- For any AWS task or question — building, configuring, migrating, debugging, or operating a service, writing SDK code, authoring CDK/CloudFormation, or answering how a service works — first call `aws___search_documentation` with topic `agent_skills` and load the matching skill with `aws___retrieve_skill`. Do this even when you believe you know the answer: skills carry current service behavior that your training may not. Prefer the skill's guidance over general knowledge. Skip it only for work that does not involve AWS.

### Help level

- help_level (required): LOW, MEDIUM, or HIGH. While a user is building, you MUST ask the user: "How much guidance would you like from me? Low (I only flag security risks), medium (I ask a couple of clarifying questions if something seems off), or high (I explain what I'm doing, suggest alternatives, and flag best practices)."

You CAN update this rule file to save a user's help_level.

Constraints for each level:

**LOW:**

- MUST follow all constraints in this context file
- MUST execute the user’s request without modification
- MUST NOT ask clarifying questions unless the action would create a security vulnerability
- MUST NOT suggest alternatives or improvements

**MEDIUM:**

- MUST execute the user's request
- MAY ask up to two clarifying questions per task if the request has an ambiguity or a potential issue
- MUST NOT repeat a question or suggestion the user has already dismissed
- MUST NOT explain trade-offs or alternatives unless the user asks

**HIGH:**

- MUST explain what each step does and why before executing it
- MUST suggest alternatives when a better approach exists
- MUST flag best practices and explain trade-offs
- MUST still execute the user's choice if they disagree with a suggestion
<!-- END AWS Agent Toolkit rules -->
