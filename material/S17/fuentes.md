# Fuentes de S17

Revisión: 17/10/2026. Los documentos oficiales informan el diseño; no acreditan el acceso de la cuenta del curso.

- Temario del 17/07: `docs/fuentes/temario-ai-engineer.txt`.
- Ejercicio S17 redactado por José, enviado el 28/09, página 6 de `AI_Engineer_enunciados.docx`: [correo original](https://mail.google.com/mail/u/0/#all/1a0e699466bafc2e). Copia del texto en `docs/fuentes/S17-ejercicio-original.txt`.
- [Nova 2 y herramientas](https://docs.aws.amazon.com/nova/latest/nova2-userguide/using-tools.html): estructura y selección de herramienta concreta. Se consultó la documentación de Nova 2, no se asumió que la de Nova 1 fuese idéntica.
- [Inferencia geográfica entre regiones](https://docs.aws.amazon.com/bedrock/latest/userguide/geographic-cross-region-inference.html): permisos sobre perfil, origen y modelos de destino.
- [IAM en HTTP API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-access-control-iam.html): SigV4 y permiso de invocación de la ruta.
- [Cuotas HTTP API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-quotas.html): límite de integración de 30 segundos.
- [Concurrencia Lambda](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html): reserva, cuota y distinción con provisioned concurrency.
- Modelo de servicio de botocore **1.43.114** instalado: operaciones Converse/GetInferenceProfile, tipos y firma. La prueba con Stubber valida la petición contra ese SDK sin red.
- Tarifas públicas de Irlanda: `docs/fuentes/tarifas-s17-2026-10-17.json` contiene SKU, unidad, importe, fecha de efectividad/publicación y URL del catálogo AWS para cada partida. Se seleccionaron tarifas estándar de Nova 2 Lite, no global/flex/priority/batch.
- [Comparación de servicios cloud](https://cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison) y [AWS/Azure para IA](https://learn.microsoft.com/en-us/azure/architecture/aws-professional/data-ai): alternativas por función.

Logo y QR proceden del material original usado en S16 y se reutilizan sin modificar sus bytes. Las tarifas y modelos deben volver a comprobarse antes de los directos; la disponibilidad de un modelo en documentación no demuestra permiso, cuota ni acceso real.

