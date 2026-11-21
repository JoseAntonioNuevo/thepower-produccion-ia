"""Ensayo de HTTP real en loopback. Solo acepta una API que declare modo demo."""

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

import httpx


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8016")
    parser.add_argument("--salida", default="evidencias/local/ensayo.json")
    args = parser.parse_args()
    url = urlparse(args.url)
    if url.scheme != "http" or url.hostname not in {"127.0.0.1", "localhost"}:
        parser.error("El ensayo automático solo admite loopback HTTP")
    with httpx.Client(base_url=args.url, timeout=5, trust_env=False) as client:
        health = client.get("/health")
        health.raise_for_status()
        assert health.json()["execution"] == "demo", "No ejecutar llamadas reales desde este ensayo"
        valid = client.post("/clasificar", json={"texto": "Factura ficticia con cobro duplicado"})
        invalid = client.post("/clasificar", json={"texto": ""})
        large = client.post("/clasificar", content=b"x" * 20000)
        assert valid.status_code == 200 and valid.json()["resultado"]["categoria"] == "facturacion"
        assert valid.json()["metadata"]["execution"] == "demo"
        assert invalid.status_code == 422 and large.status_code == 413
    report = {
        "fecha_utc": datetime.now(UTC).isoformat(),
        "url": args.url,
        "execution": "demo",
        "salud": health.json(),
        "respuesta": valid.json(),
        "entrada_invalida": invalid.status_code,
        "limite_bytes": large.status_code,
        "aws_verificado": False,
        "proveedor_real_verificado": False,
    }
    destination = Path(args.salida)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Ensayo HTTP demo correcto. Recibo: {destination}")


if __name__ == "__main__":
    main()
