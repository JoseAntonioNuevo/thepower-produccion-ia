import fs from 'node:fs/promises';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';
const input=process.argv[2]||'.build/ppt-audit/source-before.pptx';
const out=process.argv[3]||'.build/ppt-audit/updated-draft.pptx';
const p=await PresentationFile.importPptx(await FileBlob.load(input));
const C={bg:'#0F1B22',title:'#EAF1F2',text:'#C3D0D4',mint:'#4FD1A1',muted:'#9AABB1',border:'#33474F',bar:'#133A30'};
function box(sl,x,y,w,h,text,size=21,color=C.text,font='Arial',bold=false){
 const sh=sl.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=text;sh.text.style={typeface:font,fontSize:size,color,bold,insets:0};return sh;
}
function line(sl,x,y,w,color=C.border){sl.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:1},fill:color,line:{fill:'none',width:0}})}
function base(sl,eyebrow,title,sub,number){sl.background.fill=C.bg;box(sl,56,34,1168,26,eyebrow.toUpperCase(),13,C.mint,'Arial',true);box(sl,56,69,1168,60,title,38,C.title,'Georgia');box(sl,56,135,1168,56,sub,18);line(sl,56,668,1168);box(sl,56,681,400,18,'thePower · AI Engineer · S16',11,C.muted);box(sl,690,681,500,18,'AWS · OpenRouter · eu-north-1',11,C.muted);box(sl,1200,681,26,18,String(number),11,C.muted);}
function take(sl,text){sl.shapes.add({geometry:'rect',position:{left:56,top:608,width:1168,height:42},fill:C.bar,line:{fill:'none',width:0}});box(sl,72,619,1135,27,text,18,'#A8F0D0');}
function rows(sl,items,top=212,height=70){items.forEach(([a,b],i)=>{const y=top+i*height;box(sl,64,y,278,height-9,a,21,C.mint,'Arial',true);box(sl,355,y,846,height-9,b,21);if(i<items.length-1)line(sl,64,y+height-9,1137);})}
function code(sl,x,y,w,h,text,size=19){sl.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill:'#18272E',line:{fill:C.border,width:1}});box(sl,x+18,y+18,w-36,h-30,text,size,'#A8F0D0','Courier New');}
const snapshot=await p.inspect({kind:'textbox,shape,image,table,chart',maxChars:1500000});
function clear(index,keepImages=false){const ids=[...new Set(snapshot.records.filter(r=>r.slideIndex===index&&(!keepImages||r.kind!=='image')).map(r=>r.id))];p.delete(ids);}
// Text edits preserve the source's geometry and run styling.
const replacements=[['eu-west-1','eu-north-1'],['euw1-az','eun1-az'],['Irlanda','Estocolmo'],['Ireland','Stockholm'],['s16-lab/anthropic','s16/thepower/openrouter'],['ANTHROPIC_API_KEY','OPENROUTER_API_KEY'],['10.216.0.0/24','172.31.0.0/16'],['10.216.0.0/25','172.31.16.0/20'],['10.216.0.x','172.31.x.x'],['17/10/2026','11/11/2026'],['/thepower/s16-lab','/s16/thepower/api'],['/thepower/<lab>','/s16/thepower/api']];
for(const [i,sl] of p.slides.items.entries())for(const sh of sl.shapes.items){let t=String(sh.text);for(const [a,b]of replacements)if(t.includes(a)){sh.text.replace(a,b);t=t.replaceAll(a,b)}
 const specific=[
 ['Proveedor externo por HTTPS (Anthropic en la referencia de S16)','OpenRouter por HTTPS · GPT-6 Luna'],
 ['Proveedor del modelo\n(Anthropic hoy; Bedrock en S17)','OpenRouter hoy\nBedrock en S17'],
 ['llama a Anthropic;','llama a OpenRouter;'],['Anthropic · modelo','OpenRouter · GPT-6 Luna'],
 ['código de la API: src/','código de la API: app.py'],
 ['API_MODE=demo · 127.0.0.1:8016 → 8000','API_MODE=real · 127.0.0.1:8000 → 8000'],
 ['Misma imagen, distinta configuración y distinto lugar de ejecución.','Mismo código; imagen nativa local e imagen AMD64 para Fargate.'],
 ['docker build --platform linux/amd64 \\\n  --provenance=false …','docker build --platform linux/amd64 \\\n  -t s16-clasificador:1 .'],
 ['Modo, modelo y versión llegan como variables al arrancar.','Modo, modelo y proveedor llegan como variables al arrancar.'],
 ['docker compose up --build -d\n# local: 127.0.0.1:8016 → 8000','docker run --env-file .env \\\n  -p 127.0.0.1:8000:8000 \\\n  s16-clasificador:local'],
 ['Tag immutability: Immutable  ·  Encryption: AES-256  ·  Scan on push: activado','Tag immutability: Immutable  ·  Encryption: AES-256  ·  Registro privado'],
 ['(configuración de nuestra plantilla infra/s16/registro.json)','(esquema ilustrativo; comprobar los valores en la consola)'],
 ['s16-lab · Images (2)','s16-clasificador · Images (2)'],['Repositories  ›  s16-lab','Repositories  ›  s16-clasificador'],['/s16-lab','/s16-clasificador'],
 ['Cluster s16-lab','Cluster s16-thepower'],['Service s16-lab','Service s16-thepower-api'],['s16-lab:3','s16-thepower-api:N'],
 ['request_id localizado en CloudWatch.','Respuesta real y logs de arranque.'],
 ['/health, /clasificar en demo y usuario 10001.','/health, /clasificar real y usuario 10001.'],
 ['Punto de partida  S16-inicio.zip, con la API ya preparada.','Punto de partida  Repo thepower-aws, con la API ya preparada.'],
 ['Ayuda  Guía del alumno con comandos y proyecto de referencia.','Ayuda  README y carpeta docs con guion y prompt del agente.'],
 ['CloudWatch une cada petición con su log; factura, estimación, presupuesto y alerta son cosas distintas.','CloudWatch muestra la salida del contenedor; factura, estimación y presupuesto son distintos.'],
 ['Presentación, guía del alumno, enunciado de la práctica opcional y paquetes S16-inicio y S16-referencia.','Repositorio thepower-aws: README, guion de clase y prompt del agente en docs/.'],
 ['Imagen por digest, X86_64 y secreto por ARN.','Imagen identificada, X86_64 y secreto por ARN.'],
 ['La task definition referencia la imagen por digest: sabemos qué contenido exacto corre aunque alguien publique otra etiqueta.','La etiqueta identifica la versión; el digest identifica el contenido exacto que desplegamos.']
 ];
 for(const[a,b]of specific)if(t.includes(a)){sh.text.replace(a,b);t=t.replaceAll(a,b)}
}
// Match the tiny API response and the reused public subnet topology.
for (const sh of p.slides.items[2].shapes.items) {
 const t=String(sh.text);
 if(t.startsWith('{"resultado":')) sh.text='{ "modo": "real", "modelo": "openai/gpt-6-luna",\n  "resultado": {"categoria": "facturacion",\n                "prioridad": "media",\n                "respuesta": "…"} }';
 if(t==='La metadata la añade el servidor: el modelo no puede inventarla.') sh.text='La API valida el JSON y distingue una respuesta real de una simulada.';
 if(t.includes('Una línea de log por petición')) sh.text='Logs de arranque y errores del contenedor; retención de tres días.';
}
for (const sh of p.slides.items[10].shapes.items) {
 const t=String(sh.text);
 const map={
 'Subred privada (ejemplo)\n10.216.0.128/25':'Otra subred pública\n172.31.32.0/20',
 'Aquí iría una base de datos sin IP pública. No está en el laboratorio.':'Nuestra tarea vive en una zona; no se replica por tener otras subredes.',
 '172.31.0.0/16 → local\nsin ruta a Internet':'172.31.0.0/16 → local\n0.0.0.0/0 → igw-…',
 'Para salir haría falta un NAT gateway, con coste por hora.':'Reutilizamos la red por defecto; esta demo no crea un NAT gateway.'
 };
 if(map[t])sh.text=map[t];
}

// Replace notes so the class no longer follows the retired no-deployment walkthrough.
const notes=[
'Presentar Cloud deployment: AWS basics. Usaremos una API FastAPI pequeña que clasifica incidencias ficticias mediante OpenRouter, GPT-6 Luna. Región del proyecto del profesor: eu-north-1. El despliegue y su retirada se ensayaron realmente el 11/11/2026. El guion y el prompt públicos están en github.com/JoseAntonioNuevo/thepower-aws/tree/main/docs.',
'Un minuto para el QR de la sesión anterior S15. Teoría breve apoyada en consola; después ejecutamos la demo real. Permisos, red, secreto y logs se prepararon antes. Explicar qué creamos durante la clase y cerrar con retirada. No mostrar .env ni valores de secretos.',
'Leer app.py: GET /health comprueba el proceso sin invocar al modelo; POST /clasificar recibe texto ficticio y valida la respuesta JSON. Categorías acceso, facturacion, tecnico, consulta; prioridades alta, media, baja. API_MODE=demo simula explícitamente; real llama a OpenRouter. No añadir RAG, LangGraph, base de datos ni frontend.',
'Recorrer la arquitectura: portátil HTTP 8000 desde /32 hacia la tarea en una subred pública; tarea por HTTPS a OpenRouter. Al arrancar ECS descarga imagen ECR y recupera el secreto con el execution role. Logs a CloudWatch. Reutilizamos VPC por defecto y tres subredes; se ejecuta una sola tarea en una de ellas, sin alta disponibilidad.',
'Comprobar perfil thepower-aws, identidad y región Estocolmo eu-north-1. IAM es global. En la nueva experiencia de AWS, la región del proyecto no se cambia para resolver errores. El servicio MCP usa su endpoint de conexión sin cambiar la región de nuestros recursos.',
'Región: ubicación geográfica. Cada subred ocupa una zona. Podemos ofrecer tres subredes al planificador, pero nuestra única tarea vive en una zona concreta. Eso no da alta disponibilidad. No confundir nombres de zona asignados por proyecto con IDs físicos de zona.',
'AWS opera la infraestructura subyacente de Fargate; nosotros seguimos gestionando imagen, dependencias, aplicación, permisos, red y datos. Usar datos ficticios. La demo HTTP restringida no equivale a publicación de producción.',
'Identidad del operador: crea recursos. Execution role: ECS descarga ECR, lee el secreto y escribe logs al arrancar. Task role: permisos que usaría la app al llamar a AWS; no hace falta en esta API externa. STS get-caller-identity verifica el destino, no crea permisos. Fuente: docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html',
'EC2 y EBS son alternativas que mostramos conceptualmente: no creamos instancias ni volúmenes EBS para la demo. EC2 sería una máquina que administramos. Fargate evita ese trabajo de administración del host.',
'S3 almacena objetos, no es una base de datos ni el disco de una instancia. Lo usamos como comparación conceptual; esta API no necesita bucket propio. No guardar aquí la clave de OpenRouter: se referencia desde Secrets Manager.',
'VPC por defecto reutilizada, subredes públicas, tabla principal y ruta a internet gateway. No se modifican recursos compartidos. Cada tarea Fargate tiene su ENI e IP privada; habilitamos IPv4 pública temporal. Fuente: docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html',
'Para recibir tráfico hacen falta proceso escuchando en 0.0.0.0:8000, IP pública, ruta y security group. Entrada TCP 8000 solo desde IP del profesor /32; salida HTTPS 443 para servicios y OpenRouter. Security groups con estado permiten respuestas del tráfico admitido. DNS de VPC ya preparado. Recalcular IP si cambia la VPN.',
'Enseñar Dockerfile y .dockerignore del repo pequeño. Construcción nativa local: docker build -t s16-clasificador:local . Para AWS: docker build --platform linux/amd64 -t s16-clasificador:1 . La tarea es X86_64. Arrancar con --env-file .env y puerto 127.0.0.1:8000:8000; la clave no entra en el build. Las dependencias están fijadas; reconstruir si cambia el código.',
'ECR guarda imágenes; no ejecuta contenedores. Crear el repositorio propio, login por password-stdin, tag y push. Etiquetas inmutables: no sobrescribir 1; si se repite, retirar antes el repo propio o usar versión nueva. Digest identifica el contenido. El guion manual usa tag inmutable; el agente ensayado usó digest. No afirmar escaneo automático si no está habilitado.',
'Cluster s16-thepower agrupa; task definition es receta versionada; task es ejecución; service mantiene desired count. Fargate aporta cómputo. Registrar nueva revisión no la arranca. Crear servicio con desired 1 y esperar. Si paras solo una tarea, el servicio puede reponerla: para limpiar, desired 0 primero.',
'Explicar operador, execution role y task role. El rol propio s16-thepower-ecs-execution limita ECR, logs y el secreto concreto. No conceder administración general. El rol de servicio AWSServiceRoleForECS lo gestiona ECS y se conserva. Fuente: docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html',
'Secreto cifrado en Secrets Manager con clave administrada de KMS aws/secretsmanager; no hemos creado KMS propia. ECS recupera al arrancar e inyecta OPENROUTER_API_KEY. Dentro del proceso existe como variable; no mostrar inspect del contenedor. Una rotación exige lanzar tareas nuevas. Fuente: docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html',
'CloudWatch Logs recoge stdout/stderr mediante awslogs, grupo /s16/thepower/api, stream api/api/ID_TAREA y retención 3 días. Esta API mínima registra arranque, no una línea por petición ni request_id. No hemos configurado alarmas, SNS ni métricas personalizadas. Salud y clasificación HTTP son la evidencia funcional.',
'Billing consulta consumo; Cost Explorer analiza; Pricing Calculator estima; Budgets puede alertar pero no parar automáticamente. No hemos creado un presupuesto en la preparación. En nueva experiencia revisar también AWS Settings, créditos y plan. OpenRouter factura inferencia fuera de AWS.',
'Cálculo de 730 horas con tarifas guardadas de Estocolmo del 11/11/2026. CPU 0.25*730*0.0445=8.12125; memoria 0.5*730*0.0049=1.7885; IPv4 730*0.005=3.65; subtotal 13.55975; secreto 0.40; total parcial 13.95975. No incluye ECR, logs, tráfico, lecturas de secreto ni inferencia. No es factura ni se descuentan créditos.',
'Demo de 2 horas: cómputo+IPv4=0.25*2*0.0445+0.5*2*0.0049+2*0.005=0.03715 USD. Otros recursos y la inferencia aparte. Tras limpiar preservamos apoyo para repetir clase; secreto y logs pueden seguir costando. No afirmar coste cero.',
'La app consume GPT-6 Luna a través de OpenRouter; endpoint HTTPS /api/v1/responses. OPENROUTER_MODEL=openai/gpt-6-luna; OPENROUTER_PROVIDER=openai/fast. En esta demo no invocamos Bedrock ni Lambda. La siguiente sesión introduce esa alternativa sin cambiar el caso de soporte. Fuentes: openrouter.ai/docs/api/reference/responses/overview; openrouter.ai/docs/guides/features/service-tiers',
'Comparar por función: VM, contenedores, funciones, objetos, red, identidad, relacional, IA gestionada. Son equivalencias orientativas, no APIs idénticas. Bedrock, Microsoft Foundry y Vertex AI son servicios de modelos; nuestra API actual usa OpenRouter externo.',
'Laura pidió desplegar una aplicación con Docker; el ejercicio opcional concretado usa FastAPI, ECR, ECS/Fargate, secretos, red, costes y retirada. La demo de clase enseña el mismo recorrido con una API pequeña. Los alumnos parten del repo público, adaptan perfil y región a su proyecto y consultan docs/guion-clase.md o docs/prompt-agente.md. No exigir RAG, BD o S3.',
'Recapitular la secuencia observada y las pruebas reales. Distinguir RUNNING, health 200 y clasificación real. Al cerrar, comprobar retirada sin borrar recursos de apoyo. Próxima sesión S17: API Gateway, Lambda y Bedrock.',
'Consulta de rutas de la consola. Solo creamos los recursos temporales de la demo; EC2, S3 y Bedrock se muestran como alternativas. Usar los nombres reales del guion y no copiar identificadores de los esquemas. GitHub: JoseAntonioNuevo/thepower-aws.',
'Tarifas de referencia de eu-north-1, leídas 11/11/2026, en material/S16/demo-openrouter/aws/tarifas-2026-11-11.json. Son catálogo y supuestos, no gasto facturado. Ver la tabla y sumar únicamente los recursos realmente utilizados.'
];
p.slides.items.forEach((s,i)=>s.speakerNotes.text=notes[i]);
// Agenda: preserve the original QR image.
clear(1,true);let sl=p.slides.items[1];base(sl,'Antes de empezar','Encuesta de S15 y plan de la sesión','Una API pequeña, los servicios que la rodean y un despliegue real con Docker.',2);
box(sl,76,494,280,46,'Encuesta de la sesión anterior · S15',18,C.title,'Arial',true);box(sl,76,547,280,50,'Formulario de AI Engineer',16,C.muted);
const agenda=[['18:30 · 5 min','QR y caso de soporte'],['18:35 · 15 min','Cuenta, región, IAM y mapa cloud'],['18:50 · 15 min','Cómputo, datos y red'],['19:05 · 10 min','Contenedores, operación y coste'],['19:15 · 35 min','Demo: Docker → ECR → Fargate'],['19:50 · 10 min','Práctica, recapitulación y dudas']];
agenda.forEach(([a,b],i)=>{box(sl,430,215+i*60,205,45,a,20,C.mint,'Arial',true);box(sl,650,215+i*60,565,45,b,21);line(sl,430,263+i*60,780)});take(sl,'Hoy desplegamos, probamos una clasificación real y retiramos los recursos temporales.');
// Replace misleading observability and regional cost examples.
clear(17);sl=p.slides.items[17];base(sl,'Amazon CloudWatch','Ver el arranque y los errores del contenedor','Nuestra demo utiliza CloudWatch Logs; no hemos configurado alarmas ni métricas personalizadas.',18);
rows(sl,[['Grupo','/s16/thepower/api · retención de tres días'],['Stream','api/api/ID_TAREA · una ejecución del contenedor']],204,65);
code(sl,64,353,1137,115,'INFO: Application startup complete.\nINFO: Uvicorn running on http://0.0.0.0:8000',21);
box(sl,64,493,1137,70,'La API mínima no registra cada petición ni el texto de la incidencia.\nLa validación funcional la hacemos con /health y /clasificar.',22);take(sl,'CloudWatch conserva la salida del proceso; una respuesta HTTP prueba su función.');
clear(19);sl=p.slides.items[19];base(sl,'Coste mensual','730 horas: 13,96 USD de coste parcial','Estocolmo · eu-north-1 · tarifas leídas el 11/11/2026 · USD antes de impuestos y créditos.',20);
rows(sl,[['CPU · 8,12125 USD','0,25 vCPU × 730 h × 0,0445 USD/vCPU-h'],['Memoria · 1,78850 USD','0,5 GB × 730 h × 0,0049 USD/GB-h'],['IPv4 · 3,65000 USD','Una IPv4 pública × 730 h × 0,005 USD/h'],['Secreto · 0,40000 USD','Un secreto conservado durante el mes']],210,74);
box(sl,64,522,1120,64,'Sumar ECR, logs, tráfico, lecturas del secreto e inferencia en OpenRouter.\n13,95975 → 13,96 USD es una estimación parcial, no una factura.',20);take(sl,'El coste depende de recursos y tiempo; los créditos se revisan por separado.');
clear(20);sl=p.slides.items[20];base(sl,'Coste de la demo','Dos horas: 0,03715 USD de cómputo e IPv4','Supuesto docente con las mismas tarifas de Estocolmo; no incluye inferencia ni almacenamiento.',21);
rows(sl,[['CPU','0,25 × 2 × 0,0445 = 0,02225 USD'],['Memoria','0,5 × 2 × 0,0049 = 0,00490 USD'],['IPv4','1 × 2 × 0,005 = 0,01000 USD'],['Al terminar','Desired count 0, eliminar servicio y ECR, cerrar entrada /32']],210,72);
box(sl,64,520,1120,60,'Conservamos secreto, rol, cluster y logs para repetir la clase.\nEl secreto y los logs retenidos pueden seguir generando coste.',20);take(sl,'Apagar cómputo y retirar almacenamiento son acciones diferentes.');
clear(26);sl=p.slides.items[26];base(sl,'Consulta','Tarifas de referencia de Estocolmo','eu-north-1 · consulta del 11/11/2026 · catálogo público, USD sin impuestos.',27);
const prices=[['Fargate CPU','0,0445 USD/vCPU-h'],['Fargate memoria','0,0049 USD/GB-h'],['IPv4 pública en uso','0,005 USD/h'],['ECR','0,10 USD/GB-mes'],['Logs · ingesta / retención','0,54 USD/GB / 0,028 USD/GB-mes'],['Secreto / lectura','0,40 USD/mes / 0,000005 USD por llamada']];
rows(sl,prices,200,58);take(sl,'Tráfico e inferencia aparte; fuente y supuestos completos en las notas.');
// New final practical section. Native editable shapes use the original palette and fonts.
function newSlide(eyebrow,title,sub){const s=p.slides.add();base(s,eyebrow,title,sub,0);return s;}
sl=newSlide('Demo en directo','Lo preparado y lo que montamos hoy','Mismo caso de soporte; siete piezas principales de AWS alrededor de una API pequeña.');
rows(sl,[['Apoyo preparado','VPC, subredes, grupo propio, IAM, secreto, logs y cluster vacío'],['Creamos en clase','Repositorio ECR → imagen → revisión de tarea → servicio Fargate'],['Probamos','/health, clasificación real de OpenRouter y logs del contenedor'],['Retiramos','Servicio, imagen remota y acceso temporal; conservamos el apoyo']],210,83);take(sl,'ECR almacena; ECS organiza; Fargate ejecuta; la API consulta el modelo.');
sl.speakerNotes.text='Presentar la demo manual usando GUION-OBSIDIAN.md. Se conservó la infraestructura de apoyo tras el ensayo del 11/11. No crear roles o redes compartidas de nuevo. Explicar que la existencia de un cluster no implica cómputo activo. STS comprueba identidad; KMS cifra el secreto como dependencia administrada. EC2 y S3 fueron conceptos de orientación, no recursos de negocio creados.';
sl=newSlide('Demo · construir y publicar','Del Dockerfile a una imagen en ECR','Dos arquitecturas: nativa para el ordenador y AMD64 para nuestra tarea Fargate X86_64.');
code(sl,64,209,1137,147,'docker build -t s16-clasificador:local .\ndocker build --platform linux/amd64 -t s16-clasificador:1 .',22);
rows(sl,[['Local','Arrancar con --env-file .env; probar salud y una clasificación real.'],['Publicación','Crear ECR, login por stdin, etiquetar y ejecutar docker push.'],['Evidencia','Localizar la etiqueta y el digest en ECR → Images.']],382,65);take(sl,'La imagen contiene código y dependencias; la clave entra al arrancar.');
sl.speakerNotes.text='Abrir app.py, Dockerfile y .dockerignore. Ejecutar los bloques de la guía; no poner claves en comandos ni compartir .env. Mantener imágenes local y AWS con etiquetas distintas. En alumnos Mac/Linux/Windows construir nativamente según README. Si la etiqueta remota es inmutable, usar una nueva versión o limpiar el repo propio antes de repetir. Fuente de comandos: docs/guion-clase.md del repo público.';
sl=newSlide('Demo · ejecutar','La definición, la red y el servicio','La receta describe la tarea; el servicio pide que haya una ejecución disponible.');
rows(sl,[['Definición','Imagen ECR · X86_64 · 0,25 vCPU · 512 MiB · puerto 8000'],['Identidad y clave','Execution role y ARN de Secrets Manager; sin clave en el JSON'],['Red','Subred pública, IP temporal, entrada /32 al 8000 y salida HTTPS'],['Servicio','Desired count 1 → esperar a RUNNING y HEALTHY']],210,83);take(sl,'Registrar una revisión no arranca nada; crear el servicio sí inicia ejecución.');
sl.speakerNotes.text='Enseñar aws/task-definition.json y network.json del profesor; los alumnos usan sus valores. Registrar y guardar el ARN que devuelve AWS, sin suponer que la revisión es :1. Actualizar la IP con el script desde la conexión/VPN del directo. Crear servicio y esperar con límite; leer Events si falla. El rol permite ECR/logs/secreto; el task role se omite porque la API no llama a AWS. No se configura alta disponibilidad con una sola tarea.';
sl=newSlide('Demo · comprobar','Del puerto 8000 a una clasificación real','La petición llega al contenedor; el modelo se consume por API fuera de nuestra infraestructura.');
code(sl,64,210,1137,98,'GET  http://IP_DE_LA_TAREA:8000/health\nPOST http://IP_DE_LA_TAREA:8000/clasificar',22);
code(sl,64,332,1137,153,'{"modo":"real", "modelo":"openai/gpt-6-luna",\n "resultado":{"categoria":"acceso", "prioridad":"media",\n              "respuesta":"…"}}',22);
box(sl,64,514,1120,60,'Abrir /docs y CloudWatch. Una tarea RUNNING no basta:\ncomprobamos salud, respuesta del modelo y versión de imagen.',23);take(sl,'ECR y Secrets Manager intervienen al arrancar, no en cada petición.');
sl.speakerNotes.text='Obtener tarea, ENI e IP actual con el guion. Salud no llama al modelo. POST real consume OpenRouter y debe devolver modo real; no activar simulación automáticamente en caso de fallo. Modelo openai/gpt-6-luna, proveedor openai/fast, autenticación con clave inyectada. Consultar solo logs de arranque del stream de esta tarea: no hay request_id en esta API mínima. No usar datos privados en HTTP de laboratorio.';
sl=newSlide('Demo · retirar','Cerrar la demo y comprobar lo que queda','Primero dejamos de mantener tareas; después retiramos las imágenes y la conexión de entrada.');
rows(sl,[['1 · Parar','Desired count 0 → esperar running=0 y pending=0'],['2 · Retirar','Eliminar servicio y repositorio propio, incluidos manifiestos sin etiqueta'],['3 · Cerrar red','Buscar el ID actual de la regla de entrada y retirarla'],['4 · Verificar','Cero tareas/servicios/ENI, ECR vacío y entrada cerrada']],210,79);take(sl,'Para repetir: conservamos cluster, rol, secreto y logs; pueden quedar costes de retención.');
sl.speakerNotes.text='Seguir limpieza del guion: nunca borrar recursos compartidos. El repo exclusivo de demo puede retirarse con --force para incluir manifiestos OCI sin etiqueta; comprobar el nombre y uso antes. La regla de red tiene un ID nuevo cada vez, no reutilizar IDs del ensayo. Revisiones de tarea no ejecutan cómputo. Un agente debe desregistrar solo su revisión y devolver la red al estado anterior. Verificar estado INACTIVE y ENI liberada.';
sl=newSlide('Demo con un agente','El mismo recorrido con un solo prompt','Un agente con acceso a Docker, al repositorio y a AWS puede ejecutar las mismas operaciones.');
rows(sl,[['Contexto','Carpeta de la API, perfil, ID del proyecto y región autorizados'],['Trabajo','Construir → publicar → desplegar → clasificar → leer logs'],['Límites','Una tarea, datos ficticios, dos inferencias y conservación de recursos previos'],['Resultado','Informe con evidencias y limpieza verificada, sin secretos']],210,79);
box(sl,64,536,1120,40,'github.com/JoseAntonioNuevo/thepower-aws/tree/main/docs',23,C.mint,'Arial',true);take(sl,'El prompt necesita herramientas y credenciales válidas; el agente debe verificar sus resultados.');
sl.speakerNotes.text='Abrir docs/prompt-agente.md del repo público o PROMPT-AGENTE-AWS en Obsidian para el entorno del profesor. El recorrido fue probado por este agente el 11/11: salud y clasificación reales, logs y limpieza final verificados. Hubo que renovar el login AWS antes de la prueba; no prometer que un prompt evita la autenticación humana. No duplicar el despliegue manual si sigue activo: la prueba del agente debe detectar el estado previo. En clase se puede ejecutar el prompt tras limpiar la demo manual, o mostrar el informe real si falta tiempo. El agente usa una imagen por digest y su revisión propia.';
// Save before ordering in OOXML (append API has no documented move operation).
await (await PresentationFile.exportPptx(p)).save(out);
console.log('Exported',p.slides.items.length,'slides to',out);
