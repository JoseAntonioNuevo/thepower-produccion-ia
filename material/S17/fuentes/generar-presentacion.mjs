// Presentación editable de S17. Ejecutar con el runtime de artefactos de Codex.
// Copiar este archivo a .build/s17/deck y enlazar allí node_modules del runtime.
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const root = process.env.S17_ROOT;
if (!root) throw new Error('Falta S17_ROOT');
const skill = process.env.S17_PRESENTATION_SKILL;
const python = process.env.S17_RUNTIME_PYTHON;
const build = path.join(root, '.build/s17/deck');
const output = path.join(root, 'material/S17/presentaciones');
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
  text(s,'S17 · SERVERLESS AI',60,35,1000,25,17,C.mint,true);
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
  items.forEach(([head,body],i)=>{const x=60+i*(w+gap);text(s,head,x,top,w,60,34,C.mint,true);text(s,body,x,top+82,w,Math.min(260,640-(top+82)),28,C.ink);});
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
  const bytes=await fs.readFile(path.join(root,'material/S17/assets',name));
  s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:type,alt:name,fit:'contain',position:{left:x,top:y,width:w,height:h}});
}
const AWS='https://docs.aws.amazon.com/bedrock/latest/userguide/';
const price='Fuentes: docs/fuentes/tarifas-s17-2026-10-17.json, catálogo público AWS Price List, eu-west-1. Cantidades supuestas; no es factura.';

// 1. Portada común a las dos promociones.
{
 const s=p.slides.add();s.background.fill=C.bg;
 await image(s,'thepower-logo.png',60,40,240,95);
 text(s,'AI ENGINEER · S17',60,175,1100,36,24,C.mint,true);
 text(s,'Serverless AI',60,244,1160,110,77,C.ink,true);
 text(s,'Bedrock y Lambda',60,355,1100,85,58,C.blue,true);
 text(s,'La misma incidencia: identidad, límites, latencia y coste.',60,484,1100,88,31);
 text(s,'José Antonio Nuevo · 17 noviembre M/J · 23 noviembre L/X',60,614,1160,34,23,C.mute);
 text(s,'18:30–20:00 · hora de Madrid',60,655,1160,30,21,C.mute);
}
// 2. Contexto de la encuesta de cada grupo.
{
 const s=slide('Antes de empezar','El QR de AI Engineer evalúa S16, la sesión anterior de tu grupo.');
 await image(s,'qr-ai-engineer.jpg',60,235,360,360,'image/jpeg');
 text(s,'M/J · S16 del 12 noviembre\nL/X · S16 del 18 noviembre',480,245,700,110,31,C.mint,true);
 text(s,'Hoy: firmar una petición,\nvalidar el JSON y los permisos,\nmedir frío y caliente,\ny estimar 1.000 solicitudes.',480,395,700,210,30);
}
// 3. Recorrido del caso conocido.
{
 const s=slide('El mismo contrato, otro recorrido','Incidencia ficticia → categoría, prioridad y recomendación JSON.');
 rows(s,[['Cliente','Credenciales temporales + petición SigV4.'],['HTTP API','HTTPS, autorización IAM y límite de integración.'],['Lambda','Entrada y salida validadas; una llamada al SDK.'],['Bedrock','Modelo gestionado y perfil europeo configurado.']],{top:225,gap:99});
}
// 4. Semántica de serverless.
{
 const s=slide('Qué cambia con serverless','Gestionar menos infraestructura sigue dejando decisiones de aplicación.');
 cols(s,[['Proveedor','Aprovisiona y opera\nlos servidores.\nEjecuta invocaciones\ny gestiona entornos.'],['Aplicación','Código y dependencias.\nMemoria y timeouts.\nPermisos y validación.\nCoste y observabilidad.'],['Límites','Cuotas finitas.\nArranques fríos.\nDuración máxima.\nUn estado efímero.']]);
}
// 5. Comparación funcional de nubes.
{
 const s=slide('Alternativas en Azure y Google Cloud','Las funciones y los modelos son dos componentes distintos.');
 table(s,[['Papel','AWS','Azure','Google Cloud'],['Código por invocación','Lambda','Functions','Cloud Run functions'],['Acceso a modelos','Bedrock','Foundry','Vertex AI'],['Entrada y control','API Gateway + IAM','Gateway + identidad','Gateway + IAM'],['Contenedor gestionado','ECS + Fargate','Container Apps','Cloud Run']],[275,270,300,315],{height:345,size:23});
 text(s,'Revisar latencia, duración, carga, streaming, permisos y coste del plan.',60,600,1160,55,25,C.mute);
}
// 6. Perfil y procedencia de inferencia.
{
 const s=slide('Bedrock y el perfil europeo','La región de origen y las posibles regiones de destino no son lo mismo.');
 text(s,'BEDROCK_MODEL_ID\neu.amazon.nova-2-lite-v1:0',60,240,1160,125,34,C.blue,true,true);
 cols(s,[['Origen','Región de la petición.\nCuenta del laboratorio.\nIdentidad que invoca.'],['Destinos','Se leen desde el perfil.\nPermisos sobre los modelos de esas regiones.'],['Comprobación','Perfil activo ≠ inferencia probada.\nNo hay fallback global.']],385);
}
// 7. Las tres comprobaciones de acceso.
{
 const s=slide('Tres comprobaciones de permisos','Converse es el método; bedrock:InvokeModel es la acción IAM.');
 cols(s,[['Cliente → API','SigV4 temporal.\nexecute-api:Invoke\nsobre la ruta exacta.'],['API → Lambda','Servicio API Gateway.\nPermiso sobre el alias.\nOrigen y cuenta acotados.'],['Lambda → modelo','Rol de ejecución.\nbedrock:InvokeModel\nPerfil + modelos de origen/destino.']]);
}
// 8. Firma.
{
 const s=slide('Qué firma SigV4','Método, ruta, headers y los mismos bytes que se envían por HTTPS.');
 text(s,'firma = SigV4Auth(credenciales, "execute-api", region)\nfirma.add_auth(peticion)',60,247,1160,125,29,C.blue,false,true);
 rows(s,[['Credenciales','Access key + secret + session token, fuera del código.'],['Permiso','Una firma válida no concede acceso por sí misma.']],{top:445,gap:103});
}
// 9. JSON y protocolo pedagógico.
{
 const s=slide('Solicitar estructura y volver a validar','Una salida que parece JSON todavía debe cumplir el contrato.');
 cols(s,[['Solicitud','toolConfig\n+ inputSchema\n+ toolChoice.tool'],['Respuesta','stopReason: tool_use\nUna herramienta conocida.\nInput con el JSON.'],['Servidor','Categorías permitidas.\nPrioridades permitidas.\nTexto acotado.\nError si no cumple.']]);
}
// 10. Flujo de código.
{
 const s=slide('Leer el handler en cuatro pasos','Validar antes de gastar; medir y devolver una respuesta controlada.');
 rows(s,[['1 · Entrada','Evento HTTP v2, JSON y contrato compartido.'],['2 · Margen','No empezar Bedrock si el plazo restante es insuficiente.'],['3 · Modelo','Un intento, salida estructurada y validación.'],['4 · Respuesta','JSON + identidad + tiempos + consumo observado.']],{top:225,gap:99});
}
// 11. Márgenes de tiempo explícitos.
{
 const s=slide('Un timeout en cada capa','La HTTP API tiene un máximo de integración de 30 segundos.');
 rows(s,[['Cliente · 35 s','Espera el resultado de la API; no reintenta automáticamente.'],['HTTP · 29 s','El plazo HTTP incluye la inicialización fría.'],['Lambda · 24 s','Tiempo máximo de ejecución configurado.'],['SDK · 2 / 15 s','Conexión / lectura. Se exige margen antes de invocar.']],{top:225,gap:99});
}
// 12. Controles de carga y consumo.
{
 const s=slide('Límites antes de gastar','Son decisiones explícitas del laboratorio, no valores universales.');
 cols(s,[['Tamaños','8 KiB de cuerpo.\n2.000 caracteres.\n300 tokens de salida.'],['Intentos','Una llamada al SDK.\nSin reparación oculta.\nSin cambio de modelo.'],['Concurrencia','2 ejecuciones reservadas.\nRuta con ritmo acotado.\nCuota de cuenta comprobada.']]);
}
// 13. Errores por capa.
{
 const s=slide('Localizar la capa del error','La prueba sin firma debe quedarse en API Gateway.');
 table(s,[['Respuesta','Capa','Primera revisión'],['403 sin firma','API Gateway','Resultado esperado'],['403 con firma','API Gateway','Token, firma y permiso de ruta'],['400 / 413 / 415 / 422','Handler','Formato, tamaño y contrato'],['502','Bedrock / salida','Rol, perfil o esquema devuelto'],['503 / 504','Límites / tiempo','Cuota, plazo y request ID']],[315,310,535],{height:390,size:23});
}
// 14. Despliegue reproducible.
{
 const s=slide('El ZIP y la versión que se invoca','Código Linux, checksum, objeto S3 versionado y alias Lambda.');
 rows(s,[['Construir','Dependencias nativas para Linux, no las del Mac.'],['Publicar','S3 privado: checksum y versión del objeto.'],['Desplegar','Lambda publicada → alias aula → integración HTTP.'],['Leer de vuelta','Código, configuración y ruta; después una petición real.']],{top:225,gap:99});
}
// 15. Qué mide cada reloj.
{
 const s=slide('Medir cuatro tiempos diferentes','Los tiempos se superponen; no hay que sumarlos todos.');
 rows(s,[['HTTP del cliente','Red, gateway, inicialización y ejecución hasta la respuesta.'],['Handler','Lo que ocurre dentro de nuestra función.'],['Paso de modelo','SDK observado y latencia informada por Bedrock.'],['REPORT','Duración, facturación, memoria e Init Duration.']],{top:225,gap:99});
}
// 16. Evidencia de init.
{
 const s=slide('La primera petición puede estar caliente','Cold start se acredita con el registro, no con su posición en la tabla.');
 cols(s,[['Cold confirmado','Request ID asociado.\nInit Duration en REPORT.\nConservar el registro.'],['Warm observado','Entorno reutilizado.\nAl menos cinco respuestas.\nMismas condiciones.'],['Sin cold capturado','Declararlo.\nPresentar lo observado.\nNo inventar una duración.']]);
}
// 17. Fórmulas.
{
 const s=slide('Estimar 1.000 peticiones','La calculadora hace cero invocaciones.');
 rows(s,[['Lambda','N × memoria en GB × segundos facturados + solicitudes.'],['API Gateway','N × tarifa por petición HTTP API.'],['Bedrock','Tokens de entrada y salida × sus respectivas tarifas.'],['Adicionales','Logs, tráfico facturable y artefacto S3 retenido.']],{top:225,gap:99});
}
// 18. Tabla editable calculada.
{
 const s=slide('Ejemplo de coste del laboratorio','Irlanda · tarifas 17/10/2026 · cantidades hipotéticas · USD sin impuestos.');
 table(s,[['Partida','USD','Supuesto'],['Lambda','0.012825','757,5 GB-s + 1.000 invocaciones'],['HTTP API','0.001110','1.000 solicitudes'],['Bedrock · entrada','0.093500','250 tokens por solicitud'],['Bedrock · salida','0.315700','100 tokens por solicitud'],['CloudWatch logs','0.001154','Ingesta y retención previstas'],['Artefacto S3','0.000465','ZIP un mes + publicación'],['Tráfico facturable','0.000180','Volumen posterior a franquicia'],['Total','0.4249','Estimación, no factura']],[380,230,550],{top:207,height:435,size:23});
}
// 19. Elección de arquitectura.
{
 const s=slide('Cuándo elegir otra arquitectura','Medir la carga y la experiencia esperada antes de decidir.');
 cols(s,[['Proceso largo','Trabajo asíncrono.\nIdentificador y estado.\nPlazo independiente del HTTP.'],['Carga sostenida','Comparar con Fargate.\nMedir coste y latencia.\nContar operación y límites.'],['Streaming','Transporte compatible.\nModelo y permisos propios.\nAmpliación opcional.']]);
}
// 20. Entrega y retirada.
{
 const s=slide('Entregar y retirar el laboratorio','4–6 horas de práctica autónoma con accesos preparados.');
 rows(s,[['Función y acceso','Petición válida, firma, permisos y errores controlados.'],['Medidas','Frío observado o declarado ausente; cinco warm.'],['Coste','1.000 peticiones calculadas con región y supuestos.'],['Retirada','API, Lambda, logs, rol y versiones del bucket propio.']],{top:225,gap:99});
}
// 21. Anexo IAM.
{
 const s=slide('Consulta · permisos del perfil','El preflight construye la lista desde la respuesta de AWS.');
 text(s,'bedrock:InvokeModel\n  → ARN del perfil europeo\n  → ARN del modelo en origen y destinos\n  → condición bedrock:InferenceProfileArn\n\nexecute-api:Invoke\n  → ARN exacto de POST /clasificar',60,240,1160,330,29,C.blue,false,true);
}
// 22. Comandos y alcance.
{
 const s=slide('Consulta · recorrido de comandos','La guía contiene destino, argumentos, permisos y resultados esperados.');
 text(s,'uv run python scripts/demo_s17.py\nuv run python scripts/build_lambda_s17.py\nuv run python scripts/ensayo_s17.py\nuv run python -m scripts.aws_s17 plan\nuv run python scripts/costes_s17.py',60,245,1160,310,29,C.blue,false,true);
 text(s,'preflight → artefacto → despliegue → medir / verificar → limpiar',60,580,1160,55,26,C.mute);
}

const notas=JSON.parse(await fs.readFile(path.join(root,'material/S17/fuentes/notas.json'),'utf8'));
if(notas.length!==p.slides.items.length)throw new Error('Notas incompletas');
p.slides.items.forEach((s,i)=>{s.speakerNotes.text=notas[i];});
// Exportar evidencia de cada diapositiva y paquete final verificable.
await fs.writeFile(path.join(build,'contenido.json'),JSON.stringify(p.toProto(),null,2));
const renderOnly=process.env.S17_RENDER_SLIDES?.split(',').map(Number);
for(const [i,s] of (process.env.S17_SKIP_RENDER ? [] : p.slides.items.entries())){
  if(renderOnly&&!renderOnly.includes(i+1))continue;
  const png=await p.export({slide:s,format:'png',scale:1.2});
  await fs.writeFile(path.join(build,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
  console.log(`Diapositiva ${i+1}/22 renderizada`);
}
const candidate=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(candidate);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const revision=Date.now();
const validatedPath=path.join(build,'final',`S17-validado-${revision}.pptx`);
const receipt=path.join(build,`validation-${revision}.json`);
await fs.mkdir(path.dirname(validatedPath),{recursive:true});
const result=await finalizePresentation({workspaceDir:root,candidatePath:candidate,
 finalPath:validatedPath,pythonExecutable:python,
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',
  '--require-native-table-slide','5','--require-native-table-slide','13','--require-native-table-slide','18'],
 requiredNativeTableOwnerSlides:[5,13,18],fontPolicy:{basis:'design',families:['Arial','Courier New']},
 tableArithmeticContracts:[{slide:18,table:1,label_column:0,total_row:8,value_columns:[1],component_rows:[1,2,3,4,5,6,7]}],
 verifyArtifactToolImport:true,receiptPath:receipt});
console.log(JSON.stringify({validado:true,slides:22,receipt}));
await fs.copyFile(receipt,path.join(build,'validation-latest.json'));
await fs.copyFile(validatedPath,path.join(output,'S17-serverless-ai.pptx'));
// PDF a partir del PPTX validado: LibreOffice usa un perfil temporal propio.
execFileSync(process.env.S17_SOFFICE || 'soffice',[
 '-env:UserInstallation='+pathToFileURL(path.join(build,'lo-profile')).href,
 '--headless','--convert-to','pdf','--outdir',output,path.join(output,'S17-serverless-ai.pptx')
],{stdio:'inherit'});
