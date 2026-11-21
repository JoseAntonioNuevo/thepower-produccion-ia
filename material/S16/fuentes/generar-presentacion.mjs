// Presentación editable de S16. Ejecutar con el runtime de artefactos de Codex.
// Copiar este archivo a .build/deck y enlazar allí node_modules del runtime.
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const root = process.env.S16_ROOT;
if (!root) throw new Error('Falta S16_ROOT');
const skill = process.env.S16_PRESENTATION_SKILL;
const python = process.env.S16_RUNTIME_PYTHON;
const build = path.join(root, '.build/deck');
const output = path.join(root, 'material/S16/presentaciones');
await fs.mkdir(build, { recursive: true });
await fs.mkdir(output, { recursive: true });
const p = Presentation.create({ slideSize: { width: 1280, height: 720 } });
p.theme.defaultFont = 'Arial';
const C = { bg: '#081923', ink: '#F5FAFC', mute: '#B5C8D2', mint: '#54E1B8', blue: '#56CBE7', line: '#29424F', table: '#102735' };
const font = 'Arial';

function text(slide, value, x, y, w, h, size=28, color=C.ink, bold=false, mono=false) {
  const shape=slide.shapes.add({ geometry:'textbox', name:`texto-${slide.shapes.items.length}`, position:{left:x,top:y,width:w,height:h}, fill:'none', line:{fill:'none',width:0} });
  shape.text=value;
  shape.text.style={typeface:mono?'Courier New':font,fontSize:size,color,bold};
  shape.text.insets=0;
  return shape;
}
function line(slide,x,y,w) {
  slide.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:2},fill:C.line,line:{fill:'none',width:0}});
}
function slide(title, subtitle='', notes='') {
  const s=p.slides.add();s.background.fill=C.bg;
  const n=p.slides.items.length;
  text(s,'S16 · CLOUD DEPLOYMENT',60,35,1000,25,17,C.mint,true);
  text(s,title,60,86,1160,104,45,C.ink,true);
  if(subtitle)text(s,subtitle,60,158,1160,54,24,C.mute);
  text(s,'thePower · AI Engineer',60,677,1000,22,15,C.mute);
  text(s,String(n),1185,677,40,22,15,C.mute);
  s.speakerNotes.text=notes;
  return s;
}
function rows(s,items,{top=235,gap=104}={}) {
  items.forEach(([head,body],i)=>{text(s,head,60,top+i*gap,310,58,28,C.mint,true);text(s,body,400,top+i*gap,800,76,28);if(i<items.length-1)line(s,60,top+i*gap+88,1140);});
}
function cols(s,items,top=245) {
  const gap=40,w=(1160-gap*(items.length-1))/items.length;
  items.forEach(([head,body],i)=>{const x=60+i*(w+gap);text(s,head,x,top,w,60,34,C.mint,true);text(s,body,x,top+82,w,260,28,C.ink);});
}
function table(s,values,widths,{top=222,height=390,size=24}={}) {
  const t=s.tables.add({rows:values.length,columns:values[0].length,left:60,top,width:1160,height,columnWidths:widths,values});
  t.borders.assign({style:'solid',fill:C.line,width:1});
  for(let r=0;r<values.length;r++){
    t.rows[r].height=height/values.length;
    for(let c=0;c<values[0].length;c++){
      const cell=t.getCell(r,c);cell.fill=r===0?'#193E49':C.table;
      cell.text.style={typeface:font,fontSize:size,color:r===0?C.mint:C.ink,bold:r===0||r===values.length-1&&String(values[r][0]).startsWith('Total')};
    }
  }
  return t;
}
async function image(s,name,x,y,w,h,type='image/png') {
  const bytes=await fs.readFile(path.join(root,'material/S16/assets',name));
  s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:type,alt:name,fit:'contain',position:{left:x,top:y,width:w,height:h}});
}
const AWS='https://docs.aws.amazon.com/AmazonECS/latest/developerguide/';
const price='Fuentes: docs/fuentes/tarifas-aws-2026-10-17.json, catálogo público AWS Price List, eu-west-1. Cantidades supuestas; no es factura.';

// 1. Portada sin resultado de despliegue inventado.
{
 const s=p.slides.add();s.background.fill=C.bg;
 await image(s,'thepower-logo.png',60,40,240,95);
 text(s,'AI ENGINEER · S16',60,175,1100,36,24,C.mint,true);
 text(s,'Cloud deployment',60,244,1160,110,77,C.ink,true);
 text(s,'AWS y Docker',60,355,1100,85,58,C.blue,true);
 text(s,'Una API de IA: imagen, permisos, red, coste y retirada.',60,484,1100,88,31);
 text(s,'José Antonio Nuevo · 12 y 18 noviembre 2026 · 18:30–20:00',60,628,1160,34,23,C.mute);
 s.speakerNotes.text='18:30. Presentar la misma clasificación de soporte de S7/S8. El objetivo de hoy es desplegar la API que consume el modelo y demostrar imagen, servicio y función. No se entrena un modelo. La práctica es opcional; quien la complete debe usar AWS real y aportar evidencias. La misma versión sirve para M/J del 12 y L/X del 18 de noviembre. Referencia: temario AI Engineer del 17/07 y ejercicio S16 enviado el 28/09.';
}
// 2. QR original; el programa y la clase evaluada están identificados.
{
 const s=slide('Antes de empezar','El QR de AI Engineer evalúa la sesión anterior de tu grupo (S15).','18:30–18:35. Dar un minuto para escanear. Usar el QR enviado por Laura el 19/10/2026. La encuesta corresponde a S15 de cada grupo. No fijar la fecha de S15 en esta versión compartida. Fuente: https://mail.google.com/mail/u/0/#all/1a1533d7800144ad . Pedir ejemplos de lo que puede fallar al mover una API del Mac a otra máquina. Reservar diez minutos finales para preguntas. Guion: Apertura y QR.');
 await image(s,'qr-ai-engineer.jpg',60,235,360,360,'image/jpeg');
 text(s,'Al terminar podremos…',480,242,700,65,34,C.mint,true);
 text(s,'Empaquetar la API.\nDesplegar una imagen identificada.\nComprobar salud y función.\nCalcular el coste y retirar lo creado.',480,330,700,245,30);
}
// Ruta guiada de la sesión.
{
 const s=slide('Un recorrido, seis comprobaciones','Partimos de una API preparada y explicamos cada decisión mientras la desplegamos.', '18:33. Presentar el recorrido antes de abrir el repositorio. El alumno empieza por S16-inicio, no por todos los módulos. En cada paso mostrar acción, recurso y resultado esperado. Pedir una predicción o una explicación breve antes de avanzar. La solución completa es material de consulta.');
 rows(s,[['1 · Docker local','Construir → arrancar → comprobar la API.'],['2–3 · Imagen y tarea','Publicar en ECR → configurar la ejecución.'],['4–5 · Red y función','Permitir la conexión → probar y leer logs.'],['6 · Coste y retirada','Estimar → eliminar lo propio → revisar remanentes.']],{top:225,gap:99});
}
// 3. Fundamentos cloud y responsabilidad.
{
 const s=slide('Qué estamos contratando en cloud','Recursos, permisos y facturación dentro de una cuenta y una región.', '18:35. Explicar cuenta, región y zona de disponibilidad. Una región puede contener varias zonas; nuestra tarea única no aporta alta disponibilidad. Responsabilidad compartida: AWS opera infraestructura física, pero nosotros configuramos código, permisos, red, secretos y datos. La nube no elimina administración ni coste. Hacer que un alumno sitúe cuenta, región y recurso en el mapa. Fuente: temario S16 y documentación de AWS ECS.');
 cols(s,[['Cuenta','Identidad y permisos.\nFacturación y recursos.\nSeparar el laboratorio.'],['Región y zona','Dónde se ejecuta.\nDisponibilidad de servicios.\nTarifas y conectividad.'],['Responsabilidad','Proveedor: infraestructura.\nNosotros: aplicación, acceso, secretos y datos.']]);
}
// 4. Comparación funcional editable.
{
 const s=slide('AWS, Azure y Google Cloud','Comparar funciones ayuda a orientarse; las capacidades y APIs no son idénticas.', '18:38. Recorrer por funciones, no memorizar logos. VM: EC2, Azure Virtual Machines y Compute Engine. Contenedores gestionados: Fargate, Container Apps y Cloud Run. Objetos: S3, Blob Storage y Cloud Storage. Redes: VPC/VNet. Identidad y autorización tienen modelos distintos. IA gestionada: Bedrock, Foundry y Vertex AI; verificar catálogo/región antes de elegir un modelo. Fuentes: https://learn.microsoft.com/en-us/azure/architecture/aws-professional/ y https://cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison .');
 table(s,[['Función','AWS','Azure','Google Cloud'],['Máquina virtual','EC2','Virtual Machines','Compute Engine'],['Contenedor gestionado','ECS + Fargate','Container Apps','Cloud Run'],['Objetos','S3','Blob Storage','Cloud Storage'],['Red privada','VPC','Virtual Network','VPC'],['Identidad / permisos','IAM','Entra ID + RBAC','Cloud IAM'],['Modelos gestionados','Bedrock','Foundry','Vertex AI']],[275,270,300,315],{top:215,height:420,size:23});
}
// 20. Primer vistazo obligatorio a IA gestionada.
{
 const s=slide('Servicios de IA gestionada','Consumir un modelo y desplegar la aplicación son decisiones diferentes.', '18:40. Mostrar esta diapositiva en el bloque principal, junto a la comparación cloud. Bedrock, Foundry y VertexAI ofrecen acceso gestionado a modelos/capacidades; pueden incluir herramientas de evaluación/adaptación según servicio. No equivalen a entrenar ni garantizan el mismo catálogo o condiciones. Comparar permisos, región, cuotas, precios y privacidad. Esta API usa Anthropic directamente; S17 enseñará Bedrock con IAM. Fuente: documentación oficial AWS/Azure/Google de la matriz de servicios.');
 [['AWS','Bedrock','Acceso a modelos mediante AWS.\nIdentidad y permisos IAM.\nSe trabajará en S17.'],['Azure','Foundry','Modelos y herramientas de IA.\nIdentidad y recursos Azure.\nRevisar catálogo y región.'],['Google Cloud','Vertex AI','Modelos y servicios gestionados.\nProyecto e IAM.\nRevisar cuotas y ubicación.']].forEach(([cloud,name,body],i)=>{
  const x=60+i*400;
  text(s,cloud,x,245,360,40,24,C.mute);
  text(s,name,x,295,360,60,34,C.mint,true);
  text(s,body,x,390,360,220,28);
 });
}

// 5. Recursos con ejemplos vinculados a la arquitectura.
{
 const s=slide('Cómputo, almacenamiento y red','Cada recurso tiene una función y un coste distintos.', '18:42. Cómputo ejecuta procesos; objetos conservan ficheros, bloque da discos y una base de datos estructura registros. ECR almacena imágenes y CloudWatch logs, ninguno es la BD del producto. La API S16 es stateless y no necesita añadir S3 o PostgreSQL. Un filesystem del contenedor no ofrece persistencia al reemplazarlo. La red necesita rutas, resolución DNS y reglas de entrada/salida. Preguntar dónde se guardaría una conversación tras reiniciar; conectar con S20.');
 cols(s,[['Compute','VM: sistema a administrar.\nContenedor: proceso empaquetado.\nFunción: ejecución por invocación.'],['Storage','Objetos: archivos.\nDiscos: bloques.\nBase de datos: registros.\nECR: imágenes.'],['Networking','VPC y subred.\nIP, ruta y DNS.\nReglas de entrada y salida.\nTLS protege el transporte.']]);
}
// 6. Relación imagen/contenedor; contenido nativo.
{
 const s=slide('Docker: imagen y contenedor','El artefacto que construimos y la ejecución que arrancamos.', '18:47. Abrir Dockerfile y .dockerignore. Una imagen combina base, dependencias y código; un contenedor ejecuta esa imagen con configuración. Cambiar código local no cambia una imagen ya construida. Tags pueden ser nombres; digest identifica el artefacto. Nuestro ECR fija tags inmutables. Un secreto escrito en una capa sigue dentro de la imagen aunque se borre en otra. EXPOSE no abre Internet.');
 rows(s,[['Imagen','Base fijada + dependencias con hashes + código.'],['Contenedor','Proceso, usuario, puertos y configuración de ejecución.'],['Identidad','Etiqueta legible y digest del contenido.'],['Secretos','Se inyectan al arrancar; quedan fuera de Git y del build.']],{top:225,gap:99});
}
// 7. Contrato y modo de ejecución.
{
 const s=slide('La API que vamos a desplegar','Incidencia ficticia → categoría, prioridad y recomendación.', '18:50. Mostrar contratos.py, config.py y api.py. La entrada se valida antes de llamar al proveedor; su salida también se valida. La metadata pertenece al servidor. Health no invoca al modelo. Demo utiliza reglas y se rotula; real exige modelo y clave y no vuelve silenciosamente a demo. Solicitar una clasificación, señalar execution y request_id y probar una entrada vacía.');
 text(s,'GET /health\nPOST /clasificar',60,247,500,130,38,C.blue,true,true);
 text(s,'{"texto": "Factura ficticia duplicada"}',60,440,1100,55,27,C.ink,false,true);
 text(s,'Salud del proceso.\nFunción con entrada y salida validadas.',650,246,560,150,30);
 text(s,'execution: demo / real    ·    request_id    ·    versión    ·    consumo',60,540,1160,65,25,C.mute);
}
// Paso 1. Construcción y comprobación local.
{
 const s=slide('Paso 1 · ejecutar la API en Docker','El puerto 8016 del equipo llega al 8000 del contenedor.', '18:55. Abrir Dockerfile y .dockerignore. Seguir el comando de Compose en la guía; comprobar /health y /clasificar, execution demo y UID10001. Antes de publicar: build linux/amd64 --provenance=false, coherente con Fargate X86_64. Mostrar docker image inspect. Preguntar qué cambia al editar código sin reconstruir la imagen. No interpretar demo como inferencia real.');
 text(s,'docker compose up --build -d\ncurl --fail http://127.0.0.1:8016/health\ndocker compose exec api id',60,232,1160,150,29,C.blue,false,true);
 rows(s,[['Comprobar','Salud ok · clasificación demo · usuario 10001.'],['Antes de AWS','Imagen linux/amd64 y tarea X86_64.']],{top:430,gap:98});
}
// 9. Secuencia de infraestructura.
{
 const s=slide('El recorrido de la imagen en AWS','ECR conserva el artefacto; ECS describe y mantiene la ejecución; Fargate la ejecuta.', `19:02. Seguir dos plantillas: registro primero, servicio después de subir imagen. La task definition declara imagen por digest, CPU, memoria, arquitectura, usuario, puertos, secretos y logs. El servicio mantiene DesiredCount=1. Fargate ejecuta sin administrar hosts. La API llama al proveedor remoto por HTTPS. Fuente: ${AWS}task_execution_IAM_role.html y CloudFormation TaskDefinition.`);
 rows(s,[['1 · ECR','Publicar y leer el digest desde el registro.'],['2 · Task definition','Imagen + recursos + arquitectura + configuración.'],['3 · Servicio / tarea','ECS mantiene una ejecución en Fargate.'],['4 · Observación','Logs, healthcheck y petición funcional.']],{top:225,gap:99});
}
// Paso 2. Publicar y leer el resultado en ECR.
{
 const s=slide('Paso 2 · publicar la imagen en ECR','Consola ECR → repositorio del laboratorio → Images.', '19:02–19:07. Ejecutar bootstrap y publicar con los argumentos de la guía. Mientras se publica, explicar build, autenticación temporal por stdin y push. Abrir Images en ECR y señalar versión, tag y digest; abrir publicacion.json para enlazar esos valores. No enseñar tokens ni afirmar que ya hay un servicio porque exista una imagen. Fuente: https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html .');
 rows(s,[['Acción','Crear el registro y publicar una versión nueva.'],['Mirar en ECR','Etiqueta legible y digest sha256 de la imagen.'],['Resultado esperado','La imagen existe en la cuenta y región elegidas.'],['Pregunta','¿Publicar una imagen significa que la API ya responde?']],{top:225,gap:99});
}
// 11. Roles diferentes.
{
 const s=slide('Tres identidades, tres responsabilidades','El secreto se referencia por ARN y se lee al arrancar la tarea.', `19:10. El operador crea recursos. El execution role obtiene imagen/secreto y publica logs durante el arranque. El task role autoriza llamadas AWS de la aplicación; aquí no necesita permisos. Con KMS propia se necesita kms:Decrypt y key policy compatible. Parameter Store es otra opción del ejercicio con permisos correspondientes. Rotación de secreto inyectado: renovar la tarea para volver a leerlo. Fuente: ${AWS}task_execution_IAM_role.html .`);
 cols(s,[['Operador','Crea y retira recursos.\nCuenta y región verificadas.\nPermisos delegados.'],['Execution role','Descarga desde ECR.\nLee Secrets Manager.\nEscribe en CloudWatch.'],['Task role','Permisos de la aplicación.\nS16 no necesita APIs AWS.\nNo confundir con el anterior.']]);
}
// Paso 3. Configuración visible de la tarea.
{
 const s=slide('Paso 3 · leer la definición de tarea','Leer primero la plantilla; comprobar después ECS → Task definitions.', `19:07–19:10. Leer infra/s16/servicio.json antes de crear la tarea. Después del despliegue abrir la revisión creada por el laboratorio. Relacionar cada valor con infra/s16/servicio.json y los argumentos usados. Mostrar el ARN del secreto, nunca su contenido. El execution role permite inyectarlo al arrancar. Explicar que una definición describe la ejecución; el servicio arranca y mantiene la tarea. Fuente: ${AWS}task_definition_parameters.html .`);
 table(s,[['Campo','Valor de esta práctica','Qué comprobar'],['Imagen','ECR @sha256:…','Digest del paso anterior'],['Recursos','0,25 vCPU · 512 MiB','Linux · X86_64'],['Configuración','API_MODE=real · MODEL_ID','Modelo disponible'],['Secretos','ARN de Secrets Manager','Execution role autorizado'],['Proceso','Puerto 8000 · healthcheck','Logs en CloudWatch']],[260,430,470],{top:225,height:400,size:25});
}
// Paso 4. Comprobar la red en consola.
{
 const s=slide('Paso 4 · revisar red y arrancar','Consola ECS → servicio → tarea → Networking; después, VPC y security group.', `19:10. Ejecutar desplegar con los argumentos de la guía. Abrir los recursos creados por CloudFormation y explicar su finalidad: subred, ruta al internet gateway, ENI/IP y security group. El script automatiza su creación, pero se inspeccionan los valores en consola. La cuenta, región, IPv4 /32 y secreto se preparan antes. Fuente: ${AWS}fargate-task-networking.html .`);
 rows(s,[['Entrada','IPv4 pública de prueba /32 → TCP 8000 → tarea.'],['Ruta y salida','Subred pública + internet gateway; salida HTTPS.'],['Al arrancar','Tarea RUNNING y healthcheck HEALTHY.'],['Si no responde','Comprobar IP, ruta y reglas antes de repetir.']],{top:225,gap:99});
 text(s,'Laboratorio con datos ficticios; para usuarios, añadir HTTPS y autenticación.',60,626,1160,36,22,C.mute);
}
// 12. Evidencia y límites de health.
{
 const s=slide('Paso 5 · comprobar salud y función','Abrir /health, ejecutar /clasificar y localizar el request ID en CloudWatch.', '19:20. Leer publicacion.json, describir tarea y comparar taskDefinitionArn e imageDigest. estado no hace una llamada de IA. verificar añade GET y una petición sintética real, con execution real y versión coherente. No dar un deploy por válido solo por CloudFormation verde. El request ID permite ir a CloudWatch; los logs guardan versión, estado y duración, no texto ni claves. Si se usa replay, indicar fecha y fuente.');
 rows(s,[['Artefacto','Versión de código → digest publicado en ECR.'],['Ejecución','Task definition → imagen observada en ECS.'],['Salud','GET /health: proceso y versión, sin llamar al modelo.'],['Función','POST /clasificar: respuesta real y request ID.']],{top:225,gap:99});
}
// 13. Diagnóstico por capas.
{
 const s=slide('Diagnosticar por la capa que falla','Un error del proveedor no se resuelve abriendo el firewall al mundo.', '19:25. Probar 422 con datos vacíos y usar tests para timeout/fallos remotos. No cambiar credenciales en directo para provocar un fallo. Un 502/503/504 se registra sin cuerpo privado ni reintentos ocultos. Preguntar por dónde empezar con health200 y clasificación504. Mostrar un request ID en logs. Los eventos del stack explican fallos previos al arranque.');
 table(s,[['Síntoma','Primera comprobación','Evidencia'],['No arranca','Imagen / arquitectura / comando','Task + logs'],['No obtiene secreto','Execution role / ARN / KMS','Eventos ECS'],['No entra el Mac','IP /32 / puerto / rutas','Red de la tarea'],['Health 200; IA falla','Modelo / clave / timeout','Request ID + código']],[340,480,340],{height:350,size:25});
}
// 14. Costes, fórmulas y límites de la estimación.
{
 const s=slide('Calcular 730 horas sin dejarlas correr','Cantidad × tarifa de la región; hosting e inferencia por separado.', `19:32. CPU0.25*730*.04048=7.3876; memoria0.5*730*.004445=1.622425; IPv4 730*.005=3.65. Añadir almacenamiento ECR, logs, secreto/lecturas y tráfico facturable. Valores en USD sin impuestos/créditos/descuentos. No añadir NAT/ALB/BD si no se usan; si se añaden sí cuentan. Inferencia por tokens/tarifa del proveedor y con consumo de caché diferenciado. ${price}`);
 rows(s,[['CPU','0,25 vCPU × 730 h × 0,04048 USD/vCPU-h'],['Memoria','0,5 GB × 730 h × 0,004445 USD/GB-h'],['IPv4 pública','1 IP × 730 h × 0,005 USD/IP-h'],['Además','Imagen, logs, secreto, lecturas y tráfico; inferencia aparte.']],{top:225,gap:99});
}
// 15. Tabla numérica nativa.
{
 const s=slide('Coste mensual y demo con recursos retenidos','Irlanda · USD sin inferencia · demo: 90 min de cómputo + 30 días de ECR, logs y secreto.', `19:35. Escenario mes:0.25vCPU,0.5GB,unaIPv4,0.25GB imagen,1GB logs ingesta/almacén,un secreto,dos lecturas,1GB salida facturable. Demo:1.5h compute/IP,imagen y secreto retenidos el mes,0.01GB logs,una lectura,0.001GB salida facturable. El total se calcula antes de redondear:13.78 y0.46. Se usa tráfico después del tramo gratuito global. Parar tarea deja costes de recursos retenidos. ${price}`);
 table(s,[['Concepto','730 h · USD','Demo · USD'],['CPU','7.3876','0.0152'],['Memoria','1.6224','0.0033'],['IPv4','3.6500','0.0075'],['ECR','0.0250','0.0250'],['Logs: ingesta + almacén','0.6000','0.0060'],['Secreto + lecturas','0.4000','0.4000'],['Salida facturable','0.0900','0.0001'],['Total redondeado','13.78','0.46']],[600,250,310],{top:215,height:420,size:24});
}
// Lectura del supuesto que explica los 0,46 USD.
{
 const s=slide('Qué incluye la demo de 0,46 USD','Son 90 minutos de cómputo y un mes de recursos retenidos; la inferencia se suma aparte.', `19:38. Desglosar 0.02601375 USD de CPU/memoria/IP para 1.5 horas, 0.4253 de ECR/secreto/logs retenidos 30 días y 0.005795 de ingesta/lectura/salida. Total sin redondear:0.45710875 USD. No presentar 0.46 como solo 90 minutos de todos los recursos. La tarifa de cada partida y su cantidad están en datos/costes-ejemplo.json. Eliminar recursos reduce el remanente, sin borrar consumo anterior. ${price}`);
 rows(s,[['Cómputo e IP','1,5 horas de CPU, memoria e IPv4: 0,0260 USD.'],['Retención de 30 días','ECR + secreto + logs almacenados: 0,4253 USD.'],['Uso del escenario','Ingesta, lectura y salida: 0,0058 USD.'],['Si retiramos todo','Recalcular por la duración real y revisar el inventario.']],{top:225,gap:99});
}
// 16. Cierre de recursos y optimización.
{
 const s=slide('Paso 6 · retirar y comprobar recursos','ECS → ECR → CloudWatch → VPC → Secrets Manager: revisar el inventario final.', '19:40–19:50. Optimizar tamaño medido, tiempo encendido, retención, imágenes, tokens y reintentos. Alertas de presupuesto no son un interruptor universal. limpiar elimina solo stacks/imagen propios. retirar-secreto programa borrado del secreto propio con siete días, sin tocar compartidos. Revisar ENI/IP, VPC, logs, ECR, secretos, KMS externa y añadidos. Si DELETE_FAILED, investigar el recurso concreto. Guardar inventario eliminado/conservado/programado.');
 rows(s,[['Antes','Identificar cuenta, región, laboratorio y propiedad.'],['Retirar','Servicio y tarea → red/logs/roles → imágenes y ECR.'],['Revisar','Secretos externos, KMS y cualquier recurso añadido.'],['Documentar','Eliminado, conservado o borrado programado; coste residual.']],{top:225,gap:99});
}
// 17. Entrega breve; los detalles ya estaban publicados.
{
 const s=slide('Práctica opcional de S16','Ejercicio voluntario · 4–6 horas con cuenta, permisos y entorno preparados.', '19:50. Laura confirmó el 04/11 que los ejercicios no son obligatorios. Enunciado redactado por José y enviado28/09. Fuente: https://mail.google.com/mail/u/0/#all/1a1a6346ce2eb942 . Entregar código/lock, Docker no root, ECR/Fargate, secretos/roles, arquitectura coherente, salud y función reales, coste730h y limpieza. Opcional ALBHTTPS/tareas privadas; no exige S3 ni BD. Demo offline no cumple la evidencia real. Preguntas: quién lee el secreto, qué prueba digest, qué falta tras health200. Conectar con S17 sin anticipar su práctica.');
 rows(s,[['Código e infraestructura','API, lock, Dockerfile y procedimiento reproducible.'],['Evidencia real','Imagen, task definition, salud y clasificación identificadas.'],['Coste y retirada','Tarifas, cantidades, inferencia separada e inventario final.'],['Ampliación','HTTPS y tareas privadas, con coste y limpieza propios.']],{top:225,gap:99});
}
// 18. Anexo de código; permanece editable.
{
 const s=slide('Consulta · leer el Dockerfile','El secreto se inyecta al ejecutar, no al construir.', 'Anexo. Abrir el Dockerfile real del repo para ver el digest completo. El texto de esta diapositiva resume sus instrucciones. COPY usa contexto permitido; requirements.lock incluye hashes. Usuario sin privilegios, no bytecode y logs sin buffer. S16 no necesita copiar datos privados, tests ni presentaciones a la imagen.');
 text(s,'FROM python:3.12-slim-bookworm@sha256:…\nCOPY requirements.lock ./\nRUN pip install --require-hashes -r requirements.lock\nCOPY --chown=10001:10001 src/ ./src/\nUSER 10001:10001\nEXPOSE 8000\nCMD ["uvicorn", "curso_ia.api:create_app", "--factory", …]',60,245,1160,340,27,C.ink,false,true);
}
// 19. Comandos de apoyo, sin credenciales ni destinos inventados.
{
 const s=slide('Consulta · comandos del laboratorio','La guía del alumno contiene los argumentos completos y los resultados esperados.', 'Anexo. plan es offline. estado lee AWS. bootstrap/publicar/desplegar/verificar/limpiar requieren --execute y destino explícito; verificar consume una inferencia. No ejecutar hasta comprobar cuenta, perfil, región y alcance autorizado. No copiar la elipsis como comando. El script de ensayo local solo acepta loopback y demo.');
 text(s,'uv run python scripts/preflight.py\nuv run python scripts/ensayo_local.py\nuv run python scripts/costes.py\nuv run python scripts/aws_lab.py plan\nuv run python scripts/aws_lab.py --help',60,245,1160,310,29,C.blue,false,true);
 text(s,'Sin secretos en argumentos, capturas ni consultas a una IA de ayuda.',60,580,1160,55,26,C.mute);
}
// Exportar evidencia de cada diapositiva y paquete final verificable.
await fs.writeFile(path.join(build,'contenido.json'),JSON.stringify(p.toProto(),null,2));
const renderOnly=process.env.S16_RENDER_SLIDES?.split(',').map(Number);
for(const [i,s] of (process.env.S16_SKIP_RENDER ? [] : p.slides.items.entries())){
  if(renderOnly&&!renderOnly.includes(i+1))continue;
  const png=await p.export({slide:s,format:'png',scale:1.2});
  await fs.writeFile(path.join(build,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
  console.log(`Diapositiva ${i+1}/${p.slides.items.length} renderizada`);
}
const candidate=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(candidate);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const revision=Date.now();
const validatedPath=path.join(build,'final',`S16-validado-${revision}.pptx`);
const receipt=path.join(build,`validation-${revision}.json`);
await fs.mkdir(path.dirname(validatedPath),{recursive:true});
const result=await finalizePresentation({workspaceDir:root,candidatePath:candidate,
 finalPath:validatedPath,pythonExecutable:python,
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',
  '--require-native-table-slide','5','--require-native-table-slide','14','--require-native-table-slide','17','--require-native-table-slide','19'],
 requiredNativeTableOwnerSlides:[5,14,17,19],fontPolicy:{basis:'design',families:['Arial','Courier New']},
 tableArithmeticContracts:[{slide:19,table:1,label_column:0,total_row:8,value_columns:[1,2],component_rows:[1,2,3,4,5,6,7]}],
 verifyArtifactToolImport:true,receiptPath:receipt});
console.log(JSON.stringify({validado:true,slides:p.slides.items.length,receipt}));
await fs.copyFile(receipt,path.join(build,'validation-latest.json'));
await fs.copyFile(validatedPath,path.join(output,'S16-cloud-docker.pptx'));
// PDF a partir del PPTX validado: LibreOffice usa un perfil temporal propio.
execFileSync(process.env.S16_SOFFICE || 'soffice',[
 '-env:UserInstallation='+pathToFileURL(path.join(build,'lo-profile')).href,
 '--headless','--convert-to','pdf','--outdir',output,path.join(output,'S16-cloud-docker.pptx')
],{stdio:'inherit'});
