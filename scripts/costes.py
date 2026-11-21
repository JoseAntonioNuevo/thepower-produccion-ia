"""Calculadora de S16: cantidades x tarifas explícitas, sin consultar cuentas AWS."""

import argparse
import json
from decimal import Decimal
from pathlib import Path


def calcular(data):
    """Los conceptos son aditivos y cada tarifa tiene unidad y procedencia en el JSON."""
    result = []
    for scenario in data["escenarios"]:
        rows = []
        total = Decimal("0")
        for item in scenario["conceptos"]:
            quantity = Decimal(str(item["cantidad"]))
            rate = Decimal(str(item["tarifa_usd"]))
            if not quantity.is_finite() or not rate.is_finite() or quantity < 0 or rate < 0:
                raise ValueError("Cantidades y tarifas deben ser finitas y no negativas")
            cost = quantity * rate
            total += cost
            rows.append(
                {
                    "concepto": item["concepto"],
                    "unidad": item["unidad"],
                    "cantidad": str(quantity),
                    "tarifa_usd": str(rate),
                    "coste_usd": str(cost.quantize(Decimal("0.0001"))),
                }
            )
        result.append(
            {
                "escenario": scenario["nombre"],
                "conceptos": rows,
                "total_sin_inferencia_usd": str(total.quantize(Decimal("0.01"))),
            }
        )
    return {
        "tipo": data["tipo"],
        "region": data["region"],
        "fecha_tarifas": data["fecha_tarifas"],
        "inferencia": "se calcula aparte con consumo, proveedor y tarifas verificadas",
        "resultados": result,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archivo", nargs="?", default="datos/costes-ejemplo.json")
    args = parser.parse_args()
    print(
        json.dumps(
            calcular(json.loads(Path(args.archivo).read_text())), ensure_ascii=False, indent=2
        )
    )


if __name__ == "__main__":
    main()
