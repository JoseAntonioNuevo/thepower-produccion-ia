"""Estimar 1.000 peticiones sin ejecutarlas. Tarifas y origen de cantidades explícitos."""

import argparse
import json
import statistics
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def estimar(data, prices):
    """Separar inferencia, infraestructura por uso y artefacto retenido; no simular una factura."""
    if data["region"] != prices["region"] or data["profile_id"] != prices["profile_id"]:
        raise ValueError("Las tarifas no corresponden a la región/modelo de la muestra")
    numeric = {k: Decimal(str(v)) for k, v in data.items() if isinstance(v, (int, float, Decimal))}
    if any(not v.is_finite() or v < 0 for v in numeric.values()):
        raise ValueError("Cantidades inválidas")
    if not 0 <= numeric["cold_fraction"] <= 1:
        raise ValueError("Fracción fría fuera de [0,1]")
    n, f = numeric["requests"], numeric["cold_fraction"]
    billed = numeric["warm_billed_ms"] * (1 - f) + numeric["cold_billed_ms"] * f
    quantities = {
        "lambda_gbs": n * numeric["memory_mb"] / 1024 * billed / 1000,
        "lambda_request": n,
        "api_request": n,
        "input_1k": n * numeric["input_tokens"] / 1000,
        "output_1k": n * numeric["output_tokens"] / 1000,
        "logs_ingest_gb": numeric["logs_ingest_gb"],
        "logs_store_gb_month": numeric["logs_store_gb_month"],
        "s3_gb_month": numeric["s3_gb_month"],
        "s3_put": numeric["s3_puts"],
        "s3_get": numeric["s3_gets"],
        "egress_gb": numeric["billable_egress_gb"],
    }
    rows = []
    for key, quantity in quantities.items():
        rate = Decimal(prices["rates"][key]["usd"])
        if not rate.is_finite() or rate < 0:
            raise ValueError("Tarifa inválida")
        cost = quantity * rate
        rows.append(
            {
                "concepto": key,
                "cantidad": str(quantity),
                "unidad": prices["rates"][key]["unit"],
                "tarifa_usd": str(rate),
                "coste_usd": str(cost.quantize(Decimal("0.00000001"))),
            }
        )
    total = sum(Decimal(r["coste_usd"]) for r in rows)
    return {
        "tipo": "estimacion_no_factura",
        "origen_cantidades": data["origen_cantidades"],
        "region": data["region"],
        "modelo": data["profile_id"],
        "peticiones": int(n),
        "frecuencia_frio": "supuesto de escenario, no inferida del lote de 6",
        "sin_impuestos_creditos_descuentos": True,
        "peticiones_ejecutadas_por_calculadora": 0,
        "filas": rows,
        "total_usd": str(total.quantize(Decimal("0.0001"))),
    }


def incorporar_mediciones(example, receipt, cold_fraction):
    """Duración facturada desde REPORT; no sumar Init Duration otra vez a Billed Duration."""
    data = dict(example)
    good = [r for r in receipt["rows"] if r.get("status") == 200]
    if len(good) != len(receipt["rows"]):
        raise ValueError("La muestra tiene errores: no se descarta su posible gasto")
    reports = {r["request_id"]: r for r in receipt.get("reports", [])}
    warm, cold, inputs, outputs, memories = [], [], [], [], set()
    for row in good:
        meta = row["body"]["metadata"]
        if meta.get("execution") != "real" or meta["modelo_solicitado"] != data["profile_id"]:
            raise ValueError("No se mezclan demo, otro modelo y tarifas reales")
        report = reports.get(meta["request_id"])
        if not report or report.get("billed_ms") is None or report.get("memory_mb") is None:
            raise ValueError("Faltan REPORT facturables; relee logs sin repetir inferencia")
        memories.add(report["memory_mb"])
        if report.get("init_ms") is not None:
            cold.append(report["billed_ms"])
        elif meta.get("first_in_environment") is False:
            warm.append(report["billed_ms"])
        usage = meta["consumo"]
        if any(usage.get(k) for k in ("cacheReadInputTokens", "cacheWriteInputTokens")):
            raise ValueError("La muestra usa caché; incorpora sus tarifas antes de estimar")
        if type(usage.get("inputTokens")) is not int or type(usage.get("outputTokens")) is not int:
            raise ValueError("Faltan tokens observados; no sustituirlos por cero")
        inputs.append(usage["inputTokens"])
        outputs.append(usage["outputTokens"])
    if len(warm) < 5 or len(memories) != 1:
        raise ValueError("Se requieren cinco warm y una configuración de memoria comparable")
    fraction = example["cold_fraction"] if cold_fraction is None else cold_fraction
    if not cold and fraction > 0:
        raise ValueError(
            "No hay cold confirmado; usa --fraccion-fria 0 para un escenario solo warm"
        )
    data.update(
        origen_cantidades="duracion_y_tokens_observados; frecuencia_frio/logs/S3/trafico_supuestos",
        memory_mb=next(iter(memories)),
        warm_billed_ms=statistics.mean(warm),
        cold_billed_ms=statistics.mean(cold) if cold else 0,
        cold_fraction=fraction,
        input_tokens=statistics.mean(inputs),
        output_tokens=statistics.mean(outputs),
    )
    if receipt.get("region") != data["region"]:
        raise ValueError("La muestra no corresponde a la región tarifada")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mediciones", type=Path)
    parser.add_argument("--fraccion-fria", type=float)
    args = parser.parse_args()
    data = json.loads((ROOT / "datos/s17/costes-ejemplo.json").read_text())
    rates = json.loads((ROOT / "docs/fuentes/tarifas-s17-2026-10-17.json").read_text())
    if args.mediciones:
        data = incorporar_mediciones(
            data, json.loads(args.mediciones.read_text()), args.fraccion_fria
        )
    elif args.fraccion_fria is not None:
        data["cold_fraction"] = args.fraccion_fria
    print(json.dumps(estimar(data, rates), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
