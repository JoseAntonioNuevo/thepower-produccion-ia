"""Operaciones S16 de AWS: plan por defecto, destino explícito y recibos sin secretos.

Uso sin red: `uv run python scripts/aws_lab.py plan`.
Las modificaciones requieren --execute. `estado` solo lee; `verificar` hace una
inferencia real y también exige --execute. No se crea ni selecciona una cuenta.
"""

import argparse
import base64
import ipaddress
import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

PROJECT = "thepower-produccion-ia"
ROOT = Path(__file__).resolve().parents[1]


def validar_destino(args, prefix="s16"):
    """Validamos identificadores antes de pedir credenciales o construir comandos."""
    if not args.profile or not re.fullmatch(r"\d{12}", args.cuenta or ""):
        raise ValueError("Indica --profile y --cuenta (12 dígitos)")
    if not re.fullmatch(r"[a-z]{2}-[a-z]+-\d", args.region or ""):
        raise ValueError("Indica --region, por ejemplo eu-west-1")
    if prefix not in {"s16", "s17"}:
        raise ValueError("Sesión de laboratorio no admitida")
    if not re.fullmatch(rf"{prefix}-[a-z0-9-]{{3,30}}", args.lab or ""):
        raise ValueError(f"--lab debe ser {prefix}- seguido de 3 a 30 letras, números o guiones")


def validar_publicacion(data, args):
    """No desplegar un recibo de otra cuenta, región o laboratorio."""
    if data.get("platform") != "linux/amd64":
        raise ValueError("La publicación debe ser linux/amd64 para esta task definition")
    for key, value in (("account", args.cuenta), ("region", args.region), ("lab", args.lab)):
        if data.get(key) != value:
            raise ValueError(f"El recibo no corresponde al destino: {key}")
    expected = f"{args.cuenta}.dkr.ecr.{args.region}.amazonaws.com/{args.lab}@sha256:"
    if not str(data.get("image", "")).startswith(expected):
        raise ValueError("La imagen no pertenece al ECR del laboratorio")
    if not re.fullmatch(r"[a-f0-9]{64}", data["image"][len(expected) :]):
        raise ValueError("El digest no es SHA-256")
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", data.get("version", "")):
        raise ValueError("Versión de aplicación inválida")


class Laboratorio:
    """La sesión verifica STS antes de operar; los stacks deben tener nuestras etiquetas."""

    def __init__(self, args, prefix="s16"):
        import boto3
        from botocore.config import Config

        validar_destino(args, prefix)
        self.infra_dir = ROOT / "infra" / prefix
        self.args = args
        self.session = boto3.Session(profile_name=args.profile, region_name=args.region)
        self.config = Config(connect_timeout=8, read_timeout=30, retries={"max_attempts": 2})
        actual = self.client("sts").get_caller_identity()["Account"]
        if actual != args.cuenta:
            raise ValueError(
                "La cuenta autenticada no coincide con --cuenta; no se ha modificado nada"
            )
        self.cf = self.client("cloudformation")
        self.tags = [{"Key": "Project", "Value": PROJECT}, {"Key": "Lab", "Value": args.lab}]
        self.folder = ROOT / "evidencias/aws" / args.lab

    def client(self, service):
        return self.session.client(service, config=self.config)

    def guardar(self, name, data):
        """Los recibos identifican ejecución y destino, nunca valores de secretos."""
        self.folder.mkdir(parents=True, exist_ok=True)
        data = {
            "account": self.args.cuenta,
            "region": self.args.region,
            "lab": self.args.lab,
            "fecha_utc": datetime.now(UTC).isoformat(),
            **data,
        }
        # Cada ejecución conserva su original; el nombre corto apunta a la última lectura.
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
        text = json.dumps(data, ensure_ascii=False, indent=2, default=str) + "\n"
        (self.folder / f"{name}-{stamp}.json").write_text(text)
        target = self.folder / f"{name}.json"
        pending = self.folder / f".{name}.tmp"
        pending.write_text(text)
        pending.replace(target)
        print(f"Recibo: {target.relative_to(ROOT)}")

    def stack(self, suffix):
        """Una coincidencia de nombre no basta: exigimos Project y Lab correctos."""
        from botocore.exceptions import ClientError

        try:
            stack = self.cf.describe_stacks(StackName=f"{self.args.lab}-{suffix}")["Stacks"][0]
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "ValidationError" and "does not exist" in str(exc):
                return None
            raise
        tags = {item["Key"]: item["Value"] for item in stack.get("Tags", [])}
        if tags.get("Project") != PROJECT or tags.get("Lab") != self.args.lab:
            raise ValueError("El stack existente no está identificado como este laboratorio")
        return stack

    def aplicar(self, suffix, parameters):
        """Crear/actualizar el stack; un fallo debe investigarse antes de repetir la operación."""
        from botocore.exceptions import ClientError

        existing = self.stack(suffix)
        kwargs = {
            "StackName": f"{self.args.lab}-{suffix}",
            "TemplateBody": (self.infra_dir / f"{suffix}.json").read_text(),
            "Parameters": [
                {"ParameterKey": k, "ParameterValue": v}
                for k, v in {"Lab": self.args.lab, **parameters}.items()
            ],
            "Capabilities": ["CAPABILITY_IAM"],
            "Tags": self.tags,
        }
        action = "update" if existing else "create"
        try:
            getattr(self.cf, f"{action}_stack")(**kwargs)
        except ClientError as exc:
            if "No updates are to be performed" in str(exc):
                return
            raise
        self.cf.get_waiter(f"stack_{action}_complete").wait(
            StackName=kwargs["StackName"], WaiterConfig={"Delay": 10, "MaxAttempts": 90}
        )

    def outputs(self, suffix):
        stack = self.stack(suffix)
        if not stack:
            raise ValueError(f"Falta el stack {suffix}")
        return {o["OutputKey"]: o["OutputValue"] for o in stack.get("Outputs", [])}

    def bootstrap(self):
        self.aplicar("registro", {})
        self.guardar("registro", self.outputs("registro"))

    def crear_secreto(self):
        """Entrada oculta: la clave no aparece en argumentos, Git ni el recibo."""
        import getpass
        import sys

        if not sys.stdin.isatty():
            raise ValueError(
                "Crear el secreto requiere una terminal interactiva con entrada oculta"
            )
        if self.args.kms_arn and not self.args.kms_arn.startswith(
            f"arn:aws:kms:{self.args.region}:{self.args.cuenta}:key/"
        ):
            raise ValueError("KMS propia debe pertenecer a la cuenta y región seleccionadas")

        value = getpass.getpass("Clave de Anthropic (no se mostrará): ").strip()
        if not value or len(value) > 4096:
            raise ValueError("Clave vacía o demasiado larga")
        kwargs = {"Name": f"{self.args.lab}/anthropic", "SecretString": value, "Tags": self.tags}
        if self.args.kms_arn:
            kwargs["KmsKeyId"] = self.args.kms_arn
        result = self.client("secretsmanager").create_secret(**kwargs)
        self.guardar("secreto", {"SecretArn": result["ARN"], "creado_por_este_laboratorio": True})

    def retirar_secreto(self):
        """Solo programa el borrado del secreto registrado y etiquetado como propio."""
        receipt = json.loads((self.folder / "secreto.json").read_text())
        for key, value in (
            ("account", self.args.cuenta),
            ("region", self.args.region),
            ("lab", self.args.lab),
        ):
            if receipt.get(key) != value:
                raise ValueError("El recibo del secreto pertenece a otro destino")
        client = self.client("secretsmanager")
        meta = client.describe_secret(SecretId=receipt["SecretArn"])
        tags = {t["Key"]: t["Value"] for t in meta.get("Tags", [])}
        if (
            meta["Name"] != f"{self.args.lab}/anthropic"
            or tags.get("Project") != PROJECT
            or tags.get("Lab") != self.args.lab
        ):
            raise ValueError("No se ha verificado que el secreto sea propio")
        result = client.delete_secret(SecretId=meta["ARN"], RecoveryWindowInDays=7)
        self.guardar(
            "secreto-retirada",
            {"SecretArn": meta["ARN"], "borrado_programado": result["DeletionDate"]},
        )

    def publicar(self):
        """Construir amd64, subir y leer el digest desde ECR. La contraseña va por stdin."""
        version = self.args.version or ""
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", version):
            raise ValueError("Indica --version con un identificador único (por ejemplo ensayo-01)")
        uri = self.outputs("registro")["RepositoryUri"]
        ecr = self.client("ecr")
        token = ecr.get_authorization_token(registryIds=[self.args.cuenta])["authorizationData"][0]
        user, password = base64.b64decode(token["authorizationToken"]).decode().split(":", 1)
        subprocess.run(
            ["docker", "login", "--username", user, "--password-stdin", uri.split("/")[0]],
            input=password,
            text=True,
            check=True,
            capture_output=True,
        )
        tagged = f"{uri}:{version}"
        subprocess.run(
            [
                "docker",
                "build",
                "--platform",
                "linux/amd64",
                "--provenance=false",
                "--build-arg",
                f"APP_VERSION={version}",
                "-t",
                tagged,
                ".",
            ],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(["docker", "push", tagged], check=True)
        details = ecr.describe_images(
            repositoryName=self.args.lab, imageIds=[{"imageTag": version}]
        )["imageDetails"][0]
        self.guardar(
            "publicacion",
            {
                "image": f"{uri}@{details['imageDigest']}",
                "version": version,
                "platform": "linux/amd64",
            },
        )

    def desplegar(self):
        """Inyecta un ARN existente; nunca recibe el valor del secreto."""
        receipt = json.loads((self.folder / "publicacion.json").read_text())
        validar_publicacion(receipt, self.args)
        cidr = ipaddress.ip_network(self.args.ip or "", strict=True)
        if cidr.version != 4 or cidr.prefixlen != 32 or not cidr.network_address.is_global:
            raise ValueError("--ip debe ser la IPv4 pública del profesor seguida de /32")
        prefix = f"arn:aws:secretsmanager:{self.args.region}:{self.args.cuenta}:secret:"
        if not (self.args.secret_arn or "").startswith(prefix) or not self.args.modelo:
            raise ValueError("Indica --secret-arn de esta cuenta/región y --modelo disponible")
        if self.args.kms_arn and not self.args.kms_arn.startswith(
            f"arn:aws:kms:{self.args.region}:{self.args.cuenta}:key/"
        ):
            raise ValueError("KMS propia debe pertenecer a la cuenta y región seleccionadas")
        self.aplicar(
            "servicio",
            {
                "ImageUri": receipt["image"],
                "AppVersion": receipt["version"],
                "AllowedCidr": str(cidr),
                "SecretArn": self.args.secret_arn,
                "ModelId": self.args.modelo,
                "KmsKeyArn": self.args.kms_arn or "",
            },
        )
        self.guardar("despliegue", self.outputs("servicio"))
        print("Stack listo. Falta verificar salud y una petición funcional real.")

    def estado(self):
        """Lee la tarea y su ENI; no infiere disponibilidad de la API ni del modelo."""
        out = self.outputs("servicio")
        ecs = self.client("ecs")
        arns = ecs.list_tasks(
            cluster=out["Cluster"], serviceName=out["Service"], desiredStatus="RUNNING"
        )["taskArns"]
        if len(arns) != 1:
            raise ValueError(f"Se esperaba una tarea RUNNING; se observaron {len(arns)}")
        reply = ecs.describe_tasks(cluster=out["Cluster"], tasks=arns)
        if reply.get("failures"):
            raise ValueError("ECS no confirmó la lectura de la tarea")
        task = reply["tasks"][0]
        if task["taskDefinitionArn"] != out["TaskDefinition"]:
            raise ValueError("La tarea activa no usa la task definition esperada")
        eni = next(
            d["value"]
            for a in task["attachments"]
            for d in a["details"]
            if d["name"] == "networkInterfaceId"
        )
        interface = self.client("ec2").describe_network_interfaces(NetworkInterfaceIds=[eni])[
            "NetworkInterfaces"
        ][0]
        ip = interface.get("Association", {}).get("PublicIp")
        if not ip or not ipaddress.ip_address(ip).is_global:
            raise ValueError("La tarea no tiene una IPv4 pública confirmada")
        digest = task["containers"][0].get("imageDigest")
        if digest != out["ImageUri"].split("@", 1)[1]:
            raise ValueError("El digest observado en ECS no coincide con la imagen esperada")
        return {
            **out,
            "task": arns[0],
            "digest_observado": digest,
            "url": f"http://{ip}:8000",
            "lastStatus": task["lastStatus"],
        }

    def verificar(self):
        """Una sola inferencia sintética; no envía credenciales de cliente por HTTP."""
        import httpx

        state = self.estado()
        with httpx.Client(
            base_url=state["url"], timeout=30, trust_env=False, follow_redirects=False
        ) as client:
            health = client.get("/health")
            health.raise_for_status()
            if (
                health.json().get("version") != state["AppVersion"]
                or health.json().get("execution") != "real"
            ):
                raise ValueError("La salud no confirma la versión real esperada; no se invoca IA")
            response = client.post(
                "/clasificar", json=json.loads((ROOT / "datos/peticion.json").read_text())
            )
            response.raise_for_status()
            data = response.json()
            if (
                data["metadata"].get("execution") != "real"
                or data["metadata"].get("version") != state["AppVersion"]
            ):
                raise ValueError("La respuesta no corresponde a la ejecución real esperada")
        self.guardar("verificacion", {**state, "health": health.json(), "respuesta": data})

    def limpiar(self):
        """Retira las dos pilas propias y sus imágenes. Conserva siempre el secreto externo."""
        for suffix in ("servicio", "registro"):
            stack = self.stack(suffix)
            if not stack:
                continue
            if suffix == "registro":
                ecr = self.client("ecr")
                # Vaciar únicamente el repositorio identificado por el stack de este laboratorio.
                name = self.outputs("registro")["RepositoryName"]
                if name != self.args.lab:
                    raise ValueError("Repositorio inesperado: limpieza detenida")
                ids = []
                for page in ecr.get_paginator("list_images").paginate(repositoryName=name):
                    ids.extend(page["imageIds"])
                digests = sorted({i["imageDigest"] for i in ids})
                for offset in range(0, len(digests), 100):
                    result = ecr.batch_delete_image(
                        repositoryName=name,
                        imageIds=[{"imageDigest": d} for d in digests[offset : offset + 100]],
                    )
                    if result.get("failures"):
                        raise ValueError("No se pudieron retirar todas las imágenes; revisar ECR")
            self.cf.delete_stack(StackName=stack["StackId"])
            self.cf.get_waiter("stack_delete_complete").wait(
                StackName=stack["StackId"], WaiterConfig={"Delay": 10, "MaxAttempts": 90}
            )
        self.guardar(
            "limpieza",
            {
                "stacks": "eliminados_o_ausentes",
                "secreto_externo": "conservado_revisar_manualmente",
            },
        )
        print("Revisa el secreto externo, KMS si procede y el inventario de recursos cobrables.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "accion",
        choices=[
            "plan",
            "bootstrap",
            "publicar",
            "desplegar",
            "estado",
            "verificar",
            "limpiar",
            "crear-secreto",
            "retirar-secreto",
        ],
    )
    for option in (
        "profile",
        "region",
        "cuenta",
        "lab",
        "version",
        "ip",
        "modelo",
        "secret-arn",
        "kms-arn",
    ):
        parser.add_argument(f"--{option}")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if args.accion == "plan" or (args.accion != "estado" and not args.execute):
        print("PLAN SIN RED: ECR → build amd64 → push/digest → Fargate → GET + POST → limpieza.")
        print("Usa --execute y un destino explícito para ejecutar la operación autorizada.")
        print("Secreto: crear o seleccionar fuera del stack; conservar o retirar según propiedad.")
        return
    try:
        lab = Laboratorio(args)
        result = getattr(lab, args.accion.replace("-", "_"))()
        if result is not None:
            print(json.dumps(result, indent=2))
    except Exception as exc:
        # No imprimir respuestas de SDK o subprocess: podrían contener datos sensibles.
        print(f"Operación detenida ({type(exc).__name__}). Revisa el estado antes de repetir.")
        if isinstance(exc, ValueError):
            print(str(exc))
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
