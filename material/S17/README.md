# S17 Serverless AI con Bedrock y Lambda

**AI Engineer · M/J: 17/11/2026 · L/X: 23/11/2026 · 18:30–20:00 Europe/Madrid.**

La sesión conserva el contrato de soporte de S16 y cambia el recorrido a HTTP API con IAM, Lambda y Bedrock. Cada grupo puede utilizar este paquete sin tener el repositorio de otro profesor.

## Versión vigente · clase del 17/11/2026

Antes del directo, consulta la [revisión de preparación](revision-2026-11-16.md).
La demo conserva el código ensayado el 11/11; la presentación vigente es la
versión ampliada de 34 diapositivas del 12/11.

Repositorio público: [JoseAntonioNuevo/thepower-bedrock](https://github.com/JoseAntonioNuevo/thepower-bedrock).
Incluye la demo independiente, README, guías y veinte pruebas sin credenciales.

1. **[README paso a paso](demo-bedrock/README.md)**: instalación en Mac/Linux/Windows,
   identidad, cuotas, despliegue, peticiones firmadas, medidas, coste y retirada.
2. **[PowerPoint actualizado](presentaciones/S17-serverless-ai-rediseno-visual.pptx)**
   y [PDF](presentaciones/S17-serverless-ai-rediseno-visual.pdf): 34 diapositivas,
   33 para clase y una de consulta; mismo diseño y QR, demo intercalada con conceptos.
3. [Guion corto](demo-bedrock/docs/guion-clase.md),
   [comandos en el orden de la presentación](demo-bedrock/docs/comandos.md),
   [prompt para un agente](demo-bedrock/docs/prompt-agente.md) y
   [ejercicio opcional](demo-bedrock/docs/ejercicio.md).
4. [Aplicación comentada](demo-bedrock/lambda_function.py) y
   [plantilla de infraestructura](demo-bedrock/plantilla.json).
5. [Resultado real del ensayo](demo-bedrock/ENSAYO.md) y
   [cuota pendiente con AWS](demo-bedrock/docs/cuotas-aws.md).
6. [ZIP de la demo vigente](paquetes/S17-demo-bedrock.zip) y
   [manifiesto](paquetes/demo-manifiesto.json), para trabajar sin clonar GitHub.

Usamos Nova Lite directo en **eu-north-1**. No hace falta Docker, S3 ni ECR:
CloudFormation empaqueta un archivo Python. La aplicación usa el rol de
Lambda, no la clave OpenRouter de S16. No se reserva concurrencia que esta
cuenta no permite; se documenta su cuota compartida de diez ejecuciones.

El ensayo confirmó creación, salud 200, rechazo IAM 403, validación 422,
error controlado 503 de Bedrock y retirada de todos los recursos temporales.
**La clasificación real y el lote de seis siguen pendientes: la cuota de
Bedrock es cero.** Se mantiene el plan Free por decisión de José.

El QR evalúa S16 del 12/11 en M/J o del 18/11 en L/X. La práctica de S17 es
opcional según la aclaración de Laura del 04/11.

## Paquete avanzado anterior · histórico

Los enlaces siguientes documentan la versión anterior (perfil europeo Nova 2
Lite, ZIP Linux, S3, alias y reserva de concurrencia). Se conservan para
consulta; **no son los pasos de la nueva demo ni están adaptados al proyecto actual**.

1. [Base visual del 06/11](fuentes/rediseno-visual/referencias/S17-base-2026-11-06.pptx). La presentación original de octubre se conserva como [PPTX](presentaciones/S17-serverless-ai.pptx) y [PDF](presentaciones/S17-serverless-ai.pdf).
2. [Guion completo del profesor](guion-profesor.md) y [PDF](guion-profesor.pdf).
3. [Guía del alumno](guia-alumno.md) y [PDF](guia-alumno.pdf).
4. [Enunciado](enunciado.md), [cobertura](cobertura.md), [verificación](verificacion.md) y [checklist](checklist.md).
5. [Fuentes](fuentes.md), [paquete de inicio](paquetes/S17-inicio.zip) y [referencia completa](paquetes/S17-referencia.zip).
6. [ZIP Lambda compilado](paquetes/lambda-s17.zip) y [manifiesto del runtime](paquetes/lambda-manifiesto.json). Está construido para Linux amd64; no está desplegado.

El QR de AI Engineer evalúa **S16 del 12/11 en M/J** o **S16 del 18/11 en L/X**. La fecha del grupo se anuncia al comenzar. La presentación se intercalará con código, terminal y evidencias; los anexos amplían permisos y comandos.

La demo y el emulador local no consumen modelos y se identifican como tales. La firma sin conexión no acredita que IAM autorice una llamada. Antes del directo se debe completar un ensayo AWS con la cuenta, permisos y presupuesto del laboratorio, conservar resultados reales y comprobar su retirada.

