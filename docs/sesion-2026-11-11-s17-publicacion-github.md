# Publicación de thepower-bedrock · 11/11/2026

## Alcance y entrega

Creado repositorio público JoseAntonioNuevo/thepower-bedrock, en la identidad
personal verificada por el conector. La creación se hizo desde el navegador
porque el conector no ofrece crear repositorios. Los dieciocho archivos se
publicaron mediante GitHub Git Data, en main, conservando el commit inicial.

Commit de entrega: `1702eaa43c6350955dd6fd731f3a3003467d6414`.
Incluye aplicación, plantilla, cliente, calculadora, tarifas, README, guías,
informe, configuración local y veinte pruebas independientes. No se subieron
credenciales, recibos operativos, rutas privadas, entornos o ID del profesor.

## Validación

Antes de publicar: veinte pruebas independientes y las 65 del curso correctas.
Se corrigió el comando documental de cfn-lint: el paquete no admite ejecutarse
como python -m cfnlint; se usa su ejecutable cfn-lint.

Después: clonación pública limpia del commit exacto; dieciocho archivos
idénticos a la fuente, enlaces internos correctos, veinte tests, Ruff lint y
formato, preparación de plantilla, cfn-lint y coste offline correctos.

El código Lambda conserva el SHA-256 del ensayo AWS anterior, por lo que su
evidencia de despliegue, health, IAM, validación, error controlado y limpieza
sigue siendo aplicable. No se crearon recursos ni repitieron inferencias.

Releídas STS, plan Free y tres cuotas de Nova Lite en eu-north-1: siguen a cero
y no ajustables. No se puede acreditar clasificación exitosa o lote cold/warm.
El README lo destaca al principio. No se cambiaron cuotas, plan o facturación.

OpenViking pendiente: workspace sin mapeo. Decisiones y evidencia conservadas
localmente, sin acceso a otro tenant.
