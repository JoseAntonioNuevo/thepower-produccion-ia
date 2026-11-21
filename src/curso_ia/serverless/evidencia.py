"""Perfiles europeos y métricas: comprobar lo observado sin atribuir un cold start al orden."""

import re
import statistics


def validar_perfil(data, *, account, region, model_id):
    """Solo el perfil pedido y sus modelos europeos; añadir el origen a la política si falta."""
    expected = f"arn:aws:bedrock:{region}:{account}:inference-profile/{model_id}"
    if data.get("inferenceProfileArn") != expected or data.get("status") != "ACTIVE":
        raise ValueError("El perfil devuelto no es el solicitado/activo en la cuenta y región")
    models = {item.get("modelArn", "") for item in data.get("models", [])}
    if not models:
        raise ValueError("El perfil no declara modelos de destino")
    regions, names = set(), set()
    for arn in models:
        match = re.fullmatch(r"arn:aws:bedrock:(eu-[a-z]+-\d)::foundation-model/(.+)", arn)
        if not match:
            raise ValueError("El perfil incluye un modelo fuera del ámbito europeo esperado")
        regions.add(match[1])
        names.add(match[2])
    if names != {model_id.removeprefix("eu.")}:
        raise ValueError("El modelo base no coincide con el perfil seleccionado")
    model_name = next(iter(names))
    # IAM también evalúa el modelo en la región de origen de la invocación.
    models.add(f"arn:aws:bedrock:{region}::foundation-model/{model_name}")
    return {
        "profile_id": model_id,
        "profile_arn": expected,
        "model_arns": sorted(models),
        "destination_regions": sorted(regions),
        "source_region": region,
    }


def parse_report(line):
    """Extrae campos de REPORT textual; no conserva el mensaje completo de CloudWatch."""
    match = re.search(r"REPORT RequestId:\s*([A-Za-z0-9-]+)", line)
    if not match:
        return None
    report = {"request_id": match[1]}
    for label, key, unit in (
        ("Duration", "duration_ms", "ms"),
        ("Billed Duration", "billed_ms", "ms"),
        ("Memory Size", "memory_mb", "MB"),
        ("Max Memory Used", "max_memory_mb", "MB"),
        ("Init Duration", "init_ms", "ms"),
    ):
        # El tabulador separa campos; evita confundir Duration con Billed/Init Duration.
        value = re.search(rf"(?:^|\t)\s*{label}:\s*([0-9.]+)\s+{unit}", line)
        report[key] = float(value[1]) if value else None
    return report


def resumir_mediciones(rows, reports):
    """Un lote pequeño describe su muestra; no estima por sí solo la frecuencia de cold starts."""
    by_id = {r["request_id"]: r for r in reports}
    successes = [
        r
        for r in rows
        if r.get("status") == 200
        and r.get("body", {}).get("metadata", {}).get("execution") == "real"
    ]
    warm, cold = [], []
    for row in successes:
        meta = row["body"]["metadata"]
        ident = meta["request_id"]
        if by_id.get(ident, {}).get("init_ms") is not None:
            cold.append(ident)
        elif meta.get("first_in_environment") is False:
            warm.append(ident)
    times = [r["http_duration_ms"] for r in successes]
    return {
        "attempts": len(rows),
        "successes": len(successes),
        "errors": len(rows) - len(successes),
        "warm_observed": len(warm),
        "cold_confirmed_by_report": len(cold),
        "cold_request_ids": cold,
        "warm_request_ids": warm,
        "report_coverage": len(
            set(by_id) & {r["body"]["metadata"]["request_id"] for r in successes}
        ),
        "http_median_ms": statistics.median(times) if times else None,
        "cold_evidence": "observado" if cold else "no_capturado",
        "five_warm_complete": len(warm) >= 5,
    }
