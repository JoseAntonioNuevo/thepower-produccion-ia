"""Barreras de destino y cálculos que pueden producir gasto o una entrega engañosa."""

import argparse
import json
from pathlib import Path

import pytest

from scripts import aws_lab, costes


def destino():
    return argparse.Namespace(
        profile="laboratorio", cuenta="123456789012", region="eu-west-1", lab="s16-prueba"
    )


def test_mutacion_sin_execute_no_inicializa_sdk(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["aws_lab", "limpiar"])
    monkeypatch.setattr(aws_lab, "Laboratorio", lambda _: pytest.fail("No debe acceder a AWS"))
    aws_lab.main()
    assert "PLAN SIN RED" in capsys.readouterr().out


@pytest.mark.parametrize(
    "campo,valor",
    [
        ("account", "999999999999"),
        ("region", "us-east-1"),
        ("image", "registro-ajeno@sha256:" + "a" * 64),
    ],
)
def test_recibo_ajeno_no_se_despliega(campo, valor):
    args = destino()
    receipt = {
        "account": args.cuenta,
        "region": args.region,
        "lab": args.lab,
        "version": "v1",
        "platform": "linux/amd64",
        "image": f"{args.cuenta}.dkr.ecr.eu-west-1.amazonaws.com/s16-prueba@sha256:" + "a" * 64,
    }
    aws_lab.validar_publicacion(receipt, args)
    receipt[campo] = valor
    with pytest.raises(ValueError):
        aws_lab.validar_publicacion(receipt, args)


def test_stack_con_nombre_correcto_pero_propiedad_ajena_se_rechaza():
    class CF:
        def describe_stacks(self, **kwargs):
            return {"Stacks": [{"Tags": [{"Key": "Project", "Value": "otro"}]}]}

    lab = aws_lab.Laboratorio.__new__(aws_lab.Laboratorio)
    lab.args = destino()
    lab.cf = CF()
    with pytest.raises(ValueError, match="no está identificado"):
        lab.stack("registro")


def test_coste_mensual_completo_y_coste_demo_con_remanentes():
    data = json.loads(Path("datos/costes-ejemplo.json").read_text())
    result = costes.calcular(data)
    first, second = result["resultados"]
    assert len(first["conceptos"]) == 9
    assert float(first["total_sin_inferencia_usd"]) > float(second["total_sin_inferencia_usd"])
    data["escenarios"][0]["conceptos"][0]["cantidad"] = -1
    with pytest.raises(ValueError):
        costes.calcular(data)


def test_cuenta_incorrecta_detiene_antes_de_crear_clientes_operativos(monkeypatch):
    import boto3

    calls = []

    class Session:
        def client(self, service, **kwargs):
            calls.append(service)
            assert service == "sts"
            return self

        def get_caller_identity(self):
            return {"Account": "999999999999"}

    monkeypatch.setattr(boto3, "Session", lambda **kwargs: Session())
    with pytest.raises(ValueError, match="no coincide"):
        aws_lab.Laboratorio(destino())
    assert calls == ["sts"]


def test_secreto_compartido_no_se_borra(tmp_path):
    args = destino()
    receipt = {
        "account": args.cuenta,
        "region": args.region,
        "lab": args.lab,
        "SecretArn": "arn:aws:secretsmanager:eu-west-1:123456789012:secret:prueba",
    }
    (tmp_path / "secreto.json").write_text(json.dumps(receipt))

    class Secrets:
        def describe_secret(self, **kwargs):
            return {"Name": "secreto-compartido", "Tags": []}

        def delete_secret(self, **kwargs):
            pytest.fail("No puede borrar un secreto ajeno")

    lab = aws_lab.Laboratorio.__new__(aws_lab.Laboratorio)
    lab.args, lab.folder = args, tmp_path
    lab.client = lambda _: Secrets()
    with pytest.raises(ValueError, match="secreto sea propio"):
        lab.retirar_secreto()
