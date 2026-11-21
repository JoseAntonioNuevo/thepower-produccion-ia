"""Ensayo del emulador oficial Lambda en loopback, con handler de demo explícito."""

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

import httpx

from curso_ia.serverless.demo import event_for


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:9017")
    args = parser.parse_args()
    parsed = urlsplit(args.url)
    if parsed.scheme != "http" or parsed.hostname not in {"localhost", "127.0.0.1"}:
        parser.error("El emulador se comprueba únicamente en loopback HTTP")
    url = args.url.rstrip("/") + "/2015-03-31/functions/function/invocations"
    rows = []
    with httpx.Client(timeout=20, trust_env=False) as client:
        for event, expected in [(event_for(), 200), (event_for(""), 422)]:
            reply = client.post(url, json=event)
            reply.raise_for_status()
            result = reply.json()
            if result.get("statusCode") != expected:
                raise ValueError("El handler no devolvió el contrato proxy esperado")
            body = json.loads(result["body"])
            if expected == 200 and body.get("metadata", {}).get("execution") != "demo":
                raise ValueError("El ensayo solo admite el handler local de demo")
            rows.append(
                {"invoke_http_status": reply.status_code, "proxy_status": expected, "body": body}
            )
    target = Path("evidencias/local/s17-rie.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(
            {
                "fecha_utc": datetime.now(UTC).isoformat(),
                "execution": "demo",
                "runtime": "Lambda Python 3.12 Linux amd64 RIE",
                "iam_gateway_verificado": False,
                "bedrock_real": False,
                "rows": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    print(f"Contrato Lambda verificado en emulador; no acredita IAM ni Bedrock real: {target}")


if __name__ == "__main__":
    main()
