# S16 · Guía pública alineada con el ensayo

La alumna señaló diferencias entre el repo público y los comandos de clase. Se confirmó que el README mezclaba consola y comandos, enlazaba CLASE-AWS.md ausente del repo y la guía omitía la recuperación del identificador de tarea. Los auxiliares privados del profesor no estaban publicados.

Se publicó en JoseAntonioNuevo/thepower-aws y se sincronizó la copia local: README con una ruta única, docs/preparar-aws.md con comandos para recursos propios, docs/guion-clase.md con el orden del ensayo y correcciones, docs/limpieza-completa.md, prompt actualizado y seis auxiliares en scripts/. Estos generan JSON con IDs propios y guardan solo referencias en .demo-aws/ (ya ignorado). .gitattributes conserva LF para Bash en Windows. Los scripts privados aws/ y el guion de Obsidian se conservaron.

Diferencias deliberadas respecto del profesor: cada alumno usa su perfil y proyecto, red independiente con una subred, y scripts/ en lugar de aws/. Configuración de ejecución igual al ensayo: Linux X86_64, 256 CPU, 512 MiB, puerto 8000, OpenRouter real, Luna, proveedor rápido, ejecución sin servidor EC2 y acceso IPv4 /32. La limpieza del directo mantiene los apoyos; la limpieza completa los retira y programa el borrado del secreto con siete días de recuperación.

Verificación: sintaxis de bloques Bash y auxiliares; lint y formato de Python nuevo; recorrido de 75 comandos AWS simulado de preparación a limpieza; JSON de tarea y servicio contra el modelo ECS del SDK; prueba ficticia de secreto sin impresión y retirada del temporal en éxito/error; enlaces locales y ausencia de IDs/rutas privadas; 65 tests del curso pasan (aviso Starlette previo). Clon público nuevo verificado con los once archivos de contenido idénticos a la copia local. Commit posterior de atributos LF confirmado por fetch y lectura del archivo desde origin/main.

Publicación: 8ae4718ab384e730199231a8fc93ab57a964dba5 (guías y auxiliares) y 15abcea8350dbe9d38da9693cd88db859442e544 (LF); actualizaciones main sin force y con expected_sha. Perfil conector y propietario verificados antes de escribir. No se publicó .env ni se modificó la API.

Límite: no se creó infraestructura ni se hicieron inferencias en esta tarea. El despliegue real ensayado anteriormente es la referencia del recorrido del directo; la preparación nueva de recursos propios se verificó offline, no mediante un nuevo despliegue. AWS se conserva en el estado limpio para clase.

Lección: el material público debe incluir los auxiliares y la preparación que necesita un alumno; no basta con copiar el recorrido desde un entorno del profesor ya configurado. Mantener una guía canónica evita divergencias del README.

OpenViking: workspace sin cuenta mapeada, memoria pendiente; nota local guardada sin atribuirla a otro tenant.
