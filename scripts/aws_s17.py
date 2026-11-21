"""S17: preparación y operaciones explícitas de HTTP API, Lambda y Bedrock.

plan no usa red; preflight/estado/logs/politica-cliente leen AWS. Subir, desplegar,
verificar, medir y limpiar requieren --execute y destino explícito.
"""

import argparse
import base64
import hashlib
import json
import re
import time
from datetime import UTC, datetime

import httpx

from curso_ia.serverless.config import REFERENCE_MODEL
from curso_ia.serverless.evidencia import parse_report, resumir_mediciones, validar_perfil
from curso_ia.serverless.firma import signed_headers, validar_url
from scripts.aws_lab import PROJECT, ROOT, Laboratorio


def version_despliegue(artifact, profile, template):
    """Una configuración nueva también necesita publicar versión, aunque el ZIP sea el mismo."""
    material = json.dumps(
        {
            "zip": artifact["sha256"],
            "profile": profile,
            "template": hashlib.sha256(template.encode()).hexdigest(),
        },
        sort_keys=True,
    ).encode()
    return "s17-" + hashlib.sha256(material).hexdigest()[:16]


class ServerlessLab(Laboratorio):
    """Reutiliza verificación STS, etiquetas, CloudFormation y recibos de la base común."""

    def __init__(self, args):
        if not (args.region or "").startswith("eu-"):
            raise ValueError("S17 requiere una región europea explícita")
        super().__init__(args, prefix="s17")

    def lectura(self, name):
        """Los recibos locales solo se aceptan para esta misma cuenta/región/laboratorio."""
        data = json.loads((self.folder / f"{name}.json").read_text())
        for key, value in (
            ("account", self.args.cuenta),
            ("region", self.args.region),
            ("lab", self.args.lab),
        ):
            if data.get(key) != value:
                raise ValueError(f"Recibo ajeno: {key}")
        return data

    def perfil(self, model):
        if not model.startswith("eu."):
            raise ValueError("No se admite un cambio silencioso a un perfil global")
        data = self.client("bedrock").get_inference_profile(inferenceProfileIdentifier=model)
        return validar_perfil(
            data, account=self.args.cuenta, region=self.args.region, model_id=model
        )

    def preflight(self):
        profile = self.perfil(self.args.modelo or REFERENCE_MODEL)
        quota = self.client("lambda").get_account_settings()["AccountLimit"]
        # AWS deja 100 unidades sin reservar. En una actualización ya existen nuestras 2.
        existing = self.stack("servicio")
        needed = 100 if existing else 102
        if quota.get("UnreservedConcurrentExecutions", 0) < needed:
            raise ValueError("Cuota insuficiente para reservar 2 ejecuciones y mantener 100 libres")
        self.guardar(
            "preflight-s17",
            {**profile, "reserved_concurrency": 2, "inferencia_real_probada": False},
        )
        return {
            "profile_id": profile["profile_id"],
            "regiones_destino": profile["destination_regions"],
            "inferencia_real_probada": False,
        }

    def bootstrap(self):
        self.aplicar("artefactos", {})
        self.guardar("artefactos-s17", self.outputs("artefactos"))

    def subir(self):
        package = json.loads((ROOT / ".build/s17/package.json").read_text())
        archive = ROOT / ".build/s17/lambda-s17.zip"
        content = archive.read_bytes()
        sha = hashlib.sha256(content).digest()
        if (
            package.get("platform") != "linux/amd64"
            or package.get("runtime") != "python3.12"
            or sha.hex() != package.get("sha256")
        ):
            raise ValueError("El paquete no coincide con el manifiesto Linux/Python")
        bucket = self.outputs("artefactos")["Bucket"]
        key = f"code/{sha.hex()}.zip"
        result = self.client("s3").put_object(
            Bucket=bucket, Key=key, Body=content, ChecksumSHA256=base64.b64encode(sha).decode()
        )
        version = result.get("VersionId")
        if not version:
            raise ValueError("S3 no devolvió una versión: revisar antes de desplegar")
        readback = self.client("s3").head_object(
            Bucket=bucket, Key=key, VersionId=version, ChecksumMode="ENABLED"
        )
        if readback.get("ChecksumSHA256") != package["code_sha256_base64"]:
            raise ValueError("S3 no confirma el checksum esperado")
        self.guardar(
            "publicacion-s17", {**package, "bucket": bucket, "key": key, "object_version": version}
        )

    def desplegar(self):
        artifact, previous = self.lectura("publicacion-s17"), self.lectura("preflight-s17")
        if self.args.modelo and self.args.modelo != previous["profile_id"]:
            raise ValueError("Modelo distinto del preflight: revisa primero el perfil nuevo")
        profile = self.perfil(previous["profile_id"])
        release = version_despliegue(
            artifact, profile, (self.infra_dir / "servicio.json").read_text()
        )
        self.aplicar(
            "servicio",
            {
                "CodeBucket": artifact["bucket"],
                "CodeKey": artifact["key"],
                "CodeVersion": artifact["object_version"],
                "CodeSha256": artifact["code_sha256_base64"],
                "AppVersion": release,
                "ProfileId": profile["profile_id"],
                "ProfileArn": profile["profile_arn"],
                "FoundationModelArns": ",".join(profile["model_arns"]),
            },
        )
        self.guardar("despliegue-s17", self.outputs("servicio"))
        print("Stack preparado. Falta verificar IAM, JSON y ejecución real.")

    def estado(self):
        """Verifica el código de la versión publicada que usa el alias y la ruta IAM."""
        out = self.outputs("servicio")
        data = self.client("lambda").get_function(FunctionName=out["AliasArn"])["Configuration"]
        if (
            data["CodeSha256"] != out["CodeSha256"]
            or data["Version"] != out["FunctionVersion"]
            or data["Environment"]["Variables"]["APP_VERSION"] != out["AppVersion"]
            or data["Environment"]["Variables"].get("S17_MODE") != "real"
            or data["Environment"]["Variables"].get("BEDROCK_MODEL_ID") != out["ProfileId"]
            or data["State"] != "Active"
        ):
            raise ValueError("El alias no confirma el código y la configuración real esperados")
        routes = self.client("apigatewayv2").get_routes(ApiId=out["ApiId"])["Items"]
        route = next((r for r in routes if r["RouteKey"] == "POST /clasificar"), None)
        if not route or route.get("AuthorizationType") != "AWS_IAM":
            raise ValueError("La ruta no confirma autorización AWS_IAM")
        integration = self.client("apigatewayv2").get_integration(
            ApiId=out["ApiId"], IntegrationId=route["Target"].split("/", 1)[1]
        )
        if integration.get("IntegrationUri") != out["AliasArn"]:
            raise ValueError("La ruta no usa el alias esperado")
        return out

    def politica_cliente(self):
        """Genera la política exacta sin adjuntarla a identidades del laboratorio."""
        out = self.outputs("servicio")
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {"Effect": "Allow", "Action": "execute-api:Invoke", "Resource": out["InvokeArn"]}
            ],
        }
        self.guardar("politica-cliente-s17", {"policy": policy})
        return policy

    def invocar(self, out, payload, signed=True):
        url = out["Endpoint"]
        validar_url(url, self.args.region)
        body = json.dumps(payload, ensure_ascii=False).encode()
        headers = {"Content-Type": "application/json"}
        if signed:
            credentials = self.session.get_credentials()
            if credentials is None:
                raise ValueError("No hay credenciales temporales disponibles")
            headers = signed_headers(
                url, body, self.args.region, credentials.get_frozen_credentials()
            )
        started = time.perf_counter()
        with httpx.Client(timeout=35, trust_env=False, follow_redirects=False) as client:
            response = client.post(url, content=body, headers=headers)
        duration = round((time.perf_counter() - started) * 1000, 3)
        try:
            data = response.json()
        except ValueError:
            data = {"error": "respuesta_no_json"}
        if response.status_code == 200:
            meta = data.get("metadata", {})
            if (
                meta.get("execution") != "real"
                or meta.get("version") != out["AppVersion"]
                or meta.get("lambda_version") != out["FunctionVersion"]
            ):
                raise ValueError("La respuesta no confirma la versión y ejecución reales")
        return {
            "signed": signed,
            "status": response.status_code,
            "http_duration_ms": duration,
            "body": data,
        }

    def verificar(self):
        out = self.estado()
        payload = json.loads((ROOT / "datos/peticion.json").read_text())
        rows = [self.invocar(out, payload, signed=False)]
        self.guardar("verificacion-s17", {"rows": rows, "complete": False})
        if rows[0]["status"] != 403:
            raise ValueError("La llamada sin firma no produjo el 403 esperado")
        time.sleep(1)
        rows.append(self.invocar(out, {"texto": ""}))
        self.guardar("verificacion-s17", {"rows": rows, "complete": False})
        if rows[-1]["status"] != 422:
            raise ValueError("La petición inválida firmada no produjo 422")
        time.sleep(1)
        rows.append(self.invocar(out, payload))
        self.guardar("verificacion-s17", {"rows": rows, "complete": rows[-1]["status"] == 200})
        if rows[-1]["status"] != 200:
            raise ValueError("La clasificación real falló; evidencia conservada")

    def medir(self):
        """Máximo seis llamadas, sin repetir fallos ni perseguir artificialmente un cold start."""
        out = self.estado()
        rows = []
        start = int(time.time() * 1000) - 5000
        payload = json.loads((ROOT / "datos/peticion.json").read_text())
        for i in range(6):
            if i:
                time.sleep(1.1)
            try:
                row = self.invocar(out, payload)
            except (httpx.HTTPError, ValueError):
                rows.append({"status": None, "error": "cliente_sin_resultado_confirmado"})
                self.guardar(
                    "mediciones-s17",
                    {
                        "rows": rows,
                        "start_ms": start,
                        "log_group": out["LambdaLogGroup"],
                        "reports": [],
                    },
                )
                raise
            rows.append(row)
            self.guardar(
                "mediciones-s17",
                {
                    "rows": rows,
                    "start_ms": start,
                    "log_group": out["LambdaLogGroup"],
                    "reports": [],
                },
            )
            if row["status"] != 200:
                raise ValueError("Lote detenido en el primer fallo; no se reintenta inferencia")
        return self.logs()

    def logs(self):
        """Leer REPORT después del lote; una demora de CloudWatch no implica otra inferencia."""
        receipt = self.lectura("mediciones-s17")
        ids = {r.get("body", {}).get("metadata", {}).get("request_id") for r in receipt["rows"]}
        reports = []
        client = self.client("logs")
        pages = client.get_paginator("filter_log_events").paginate(
            logGroupName=receipt["log_group"],
            startTime=receipt["start_ms"],
            filterPattern='"REPORT RequestId"',
            PaginationConfig={"MaxItems": 200},
        )
        for page in pages:
            for event in page.get("events", []):
                report = parse_report(event["message"])
                if report and report["request_id"] in ids:
                    reports.append(report)
        summary = resumir_mediciones(receipt["rows"], reports)
        self.guardar(
            "mediciones-s17",
            {
                **receipt,
                "reports": reports,
                "summary": summary,
                "logs_read_utc": datetime.now(UTC).isoformat(),
            },
        )
        return summary

    def limpiar(self):
        """Retirar primero servicio y después todas las versiones del bucket propio."""
        for suffix in ("servicio", "artefactos"):
            stack = self.stack(suffix)
            if not stack:
                continue
            if suffix == "artefactos":
                s3 = self.client("s3")
                bucket = self.outputs(suffix)["Bucket"]
                tags = {
                    t["Key"]: t["Value"] for t in s3.get_bucket_tagging(Bucket=bucket)["TagSet"]
                }
                if tags.get("Project") != PROJECT or tags.get("Lab") != self.args.lab:
                    raise ValueError("No se ha confirmado que el bucket sea propio")
                items = []
                for page in s3.get_paginator("list_object_versions").paginate(Bucket=bucket):
                    items.extend(
                        [
                            {"Key": o["Key"], "VersionId": o["VersionId"]}
                            for o in page.get("Versions", []) + page.get("DeleteMarkers", [])
                        ]
                    )
                if any(not re.fullmatch(r"code/[a-f0-9]{64}\.zip", i["Key"]) for i in items):
                    raise ValueError("El bucket contiene objetos ajenos al paquete: no se vacía")
                # Enumerar antes de borrar evita cambiar la colección durante su paginación.
                for offset in range(0, len(items), 1000):
                    result = s3.delete_objects(
                        Bucket=bucket, Delete={"Objects": items[offset : offset + 1000]}
                    )
                    if result.get("Errors"):
                        raise ValueError("Quedan versiones del bucket por retirar")
            self.cf.delete_stack(StackName=stack["StackId"])
            self.cf.get_waiter("stack_delete_complete").wait(
                StackName=stack["StackId"], WaiterConfig={"Delay": 10, "MaxAttempts": 90}
            )
        self.guardar(
            "limpieza-s17",
            {"stacks": "eliminados_o_ausentes", "identidad_cliente_externa": "conservada"},
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = [
        "plan",
        "preflight",
        "bootstrap",
        "subir",
        "desplegar",
        "estado",
        "politica-cliente",
        "verificar",
        "medir",
        "logs",
        "limpiar",
    ]
    parser.add_argument("accion", choices=actions)
    for arg in ("profile", "region", "cuenta", "lab", "modelo"):
        parser.add_argument(f"--{arg}")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    readonly = {"preflight", "estado", "logs", "politica-cliente"}
    if args.accion == "plan" or (args.accion not in readonly and not args.execute):
        print("PLAN SIN RED: perfil/cuota → ZIP Linux → S3 versionado → Lambda + HTTP API IAM.")
        print("Verificar: una inferencia. Medir: máximo seis. Los cambios requieren --execute.")
        return
    try:
        result = getattr(ServerlessLab(args), args.accion.replace("-", "_"))()
        if result is not None:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(f"Operación detenida ({type(exc).__name__}); revisa estado antes de repetir.")
        if isinstance(exc, ValueError):
            print(str(exc))
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
