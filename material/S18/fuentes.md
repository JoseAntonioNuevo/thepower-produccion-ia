# Fuentes de S18

## Origen de la clase

- Temario de AI Engineer, correo de la escuela del 17/07/2026 (id `19f6f7569cc093d9`):
  [copia del bloque de S18](fuentes/temario-S18-original.txt).
- Ejercicio de S18, adjunto `ejercicios.docx` del 29/09/2026 (id `1a0ebc9b585e70bc`, hilo
  `1a0d7bb5a23dc200`): [copia literal](fuentes/ejercicio-S18-original.txt).
- Indicaciones de la escuela en ese hilo (25/09–16/11/2026): [resumen](fuentes/indicaciones-laura.md).
- Los tres se leyeron en Gmail el 16/11/2026, en solo lectura, por la sesión anterior de esta
  preparación. El 17/11 el conector de Gmail no estaba autorizado y no se volvió a leer.

## Documentación técnica oficial

Consultada el 16/11/2026 (copias en `.build/s18/investigacion/`) y revisada el 17/11/2026. La
documentación describe el servicio; no demuestra que el proyecto del aula tenga acceso o cuota.

**GitHub**

- [Uso seguro de Actions](https://docs.github.com/en/actions/reference/security/secure-use): fijar acciones al SHA completo del commit.
- [OIDC · referencia](https://docs.github.com/en/actions/reference/security/oidc): claims, formato del `sub`, `sub` inmutable para repositorios creados desde el 15/07/2026.
- [OIDC en AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws): `aud = sts.amazonaws.com`, `id-token: write`.
- [Gestionar environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) y [referencia](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments): ramas permitidas; disponibles en repositorios públicos con cualquier plan.
- [Eventos que lanzan workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows): `pull_request`, `push`, `workflow_dispatch`.
- [Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets): checks obligatorios; repositorios públicos en GitHub Free.
- [Facturación de Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions): runners estándar gratuitos en repositorios públicos.
- [Desplegar en ECS](https://docs.github.com/en/actions/how-tos/deploy/deploy-to-third-party-platforms/amazon-elastic-container-service).
- API REST: [environments](https://docs.github.com/en/rest/deployments/environments), [ramas de despliegue](https://docs.github.com/en/rest/deployments/branch-policies) y [reglas](https://docs.github.com/en/rest/repos/rules).
- SHA de las acciones comprobados con `gh api repos/<acción>/git/ref/tags/<versión>` el 17/11/2026 (`.build/s18/logs/acciones-sha.txt`).

**AWS**

- ECR: [inmutabilidad de etiquetas](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-tag-mutability.html) y [uso desde ECS por digest](https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_on_ECS.html).
- ECS: [rolling update](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html), [circuit breaker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html), [blue/green](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-blue-green.html), [canary](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/canary-deployment.html), [lineal](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-linear.html), [secretos](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html).
- IAM: [proveedor OIDC](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html); acciones y recursos admitidos de ECS, ECR, EC2, IAM y Logs según la [referencia de autorización de servicios](https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html) (JSON descargado el 16/11).
- CloudWatch: [sintaxis de filtros de métricas](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntaxForMetricFilters.html), [estructura de paneles](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Dashboard-Body-Structure.html), [Application Signals](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Monitoring-Sections.html), [precios y capa gratuita](https://aws.amazon.com/cloudwatch/pricing/).
- RDS: [copias automáticas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html), [retención 0–35 días](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.BackupRetention.html) y [restauración a un punto en el tiempo](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html) (crea una instancia nueva).

**Otros**

- [Sentry para FastAPI](https://docs.sentry.io/platforms/python/integrations/fastapi/): ejemplo de error tracking; no se integra en la demo.
- Diapositivas 32, 34 y 28 (17/11/2026, Context7 y web de AWS; copias en `.build/s18/investigacion/ctx7-*.txt`,
  `aws-ecs-connection-draining.txt` y `w3c-trace-context.html`):
  OpenTelemetry [trazas](https://opentelemetry.io/docs/concepts/signals/traces/) y [visión general](https://opentelemetry.io/docs/specs/otel/overview/) (TraceId 16 bytes, SpanId 8);
  [W3C Trace Context](https://www.w3.org/TR/trace-context/) (`traceparent`; el trace_id de la diapositiva es su ejemplo);
  Sentry: [agrupación por huella](https://docs.sentry.io/concepts/data-management/event-grouping/), [releases](https://docs.sentry.io/product/releases/) y [estados de una incidencia](https://docs.sentry.io/product/issues/states-triage/);
  ALB: [atributos del grupo de destinos, deregistration delay](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html) y [health checks y estados](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html);
  ECS: [drenaje de conexiones con balanceador](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/load-balancer-connection-draining.html).
- [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) 1.57.2 y [actionlint](https://github.com/rhysd/actionlint) 1.7.12 para la validación offline.

**Punto de partida (diapositivas 3–5, consultadas el 20/11/2026)**

- Google SRE, [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/): las cuatro señales doradas (latencia, tráfico, errores y saturación).
- DORA, [métricas de entrega de software](https://dora.dev/guides/dora-metrics/) e [historia de las métricas](https://dora.dev/insights/dora-metrics-history): cinco métricas en dos grupos, throughput (tiempo de entrega del cambio, frecuencia de despliegue, tiempo de recuperación de un despliegue fallido) e instability (tasa de fallos del cambio y tasa de retrabajo).
- GitHub, [integración continua](https://docs.github.com/en/actions/get-started/continuous-integration), y AWS, [entrega continua](https://aws.amazon.com/devops/continuous-delivery/), para las definiciones de CI y CD.
- Copias en `.build/s18/investigacion/` (`dora-metrics.md`, `sre-monitoring.md` y las dos páginas de definiciones).

**Alternativas y precios (diapositivas 11, 17 y 18, consultadas el 17/11/2026)**

- GitHub: [acciones personalizadas (tipos y action.yml)](https://docs.github.com/en/actions/concepts/workflows-and-actions/custom-actions), [runners self-hosted](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners), [facturación de Actions](https://docs.github.com/en/billing/concepts/product-billing/github-actions) (uso incluido: 12 USD Free, 18 USD Pro/Team, 300 USD Enterprise Cloud) y [precio por runner](https://docs.github.com/en/billing/reference/actions-runner-pricing) (Linux 2 núcleos 0,006 USD/min; macOS 0,062). `action.yml` de configure-aws-credentials leído con `gh api` en el commit `e1253824…` (v6.3.0).
- Cloudflare: [Workers Builds](https://developers.cloudflare.com/workers/ci-cd/builds/) y [límites y precios](https://developers.cloudflare.com/workers/ci-cd/builds/limits-and-pricing/) (Free 3.000 min, 1 build; de pago 6.000 min, 6 builds, +0,005 USD/min; 20 min por build); [precio de Workers Paid](https://developers.cloudflare.com/workers/platform/pricing/) (mínimo 5 USD/mes).
- GitLab: [precios](https://about.gitlab.com/pricing/) (Free 400 min; Premium 29 USD/usuario/mes, 10.000 min; 10 USD por 1.000 min).
- AWS: [precios de CodeBuild](https://aws.amazon.com/codebuild/pricing/) (capa gratuita de 100 min; ejemplo oficial 0,005 USD/min en general1.small).
- Hetzner: [Cloud](https://www.hetzner.com/cloud/) (Regular Performance desde 5,49 €/mes sin IVA).

## Imágenes de la presentación

Procedencia de cada imagen en [fuentes/presentacion/README.md](fuentes/presentacion/README.md).
