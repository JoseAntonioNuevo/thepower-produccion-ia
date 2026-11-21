# S17 sencilla · 11/11/2026

## Alcance y decisiones

Preparada `material/S17/demo-bedrock/` como recorrido vigente. Conserva el
problema de soporte de S16 y los requisitos del temario: Lambda, Bedrock,
HTTP API con IAM, JSON validado, límites, latencia, coste y alternativas.
Aplicación en un archivo con comentarios españoles. CloudFormation inline
evita Docker, S3, dependencias nativas y alias en la demo del aula.

Se elige Nova Lite directo en eu-north-1 para respetar la región única.
La referencia anterior Nova 2 Lite EU queda histórica y el cambio se explica
en el ejercicio. La cuota regional de Lambda es diez: no se puede reservar
dos dejando cien libres. La demo usa el límite compartido, IAM, throttling
de mejor esfuerzo 1/s y lote secuencial acotado, sin prometer límite por función.

## Evidencia y límites

Despliegue real del stack propio: salud 200, sin firma 403, inválida 422,
modelo 503 por cuota. Nova Lite está autorizado pero sus tres cuotas son cero.
José eligió mantener Free y gestionar revisión con AWS. No hubo cambio de plan,
cuotas ni envío a soporte. Clasificación exitosa y seis medidas pendientes.

Retirada comprobada: stack, API, Lambda, rol y dos grupos de logs ausentes.
Configuración, permisos y logs en `.build/s17-simple/`; informe saneado en
demo-bedrock/ENSAYO.md. Sesenta y cinco tests correctos, veinte nuevos;
cfn-lint y validación AWS correctos. Lint nuevo correcto; global bloqueado
por fuentes de presentaciones preexistentes. Instalación mínima limpia probada.

## Entrega

README, guion, prompt, ejercicio, tarifas y solicitud de cuota preparados.
Power y PDF de S17 actualizados conservando diseño, QR y marca, con 26 notas
y recorrido de 90 minutos. Paquete sencillo para alumnos, sin credenciales.
No se ha creado repo remoto, hecho commit/push ni sustituido una copia de Drive.

OpenViking pendiente: el selector devuelve `unmapped workspace`. No se ha leído
ni escrito otro tenant; esta nota conserva localmente la evidencia y decisiones.
