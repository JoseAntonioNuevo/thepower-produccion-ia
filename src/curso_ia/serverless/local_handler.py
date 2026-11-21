"""Entrada exclusiva de ensayo RIE local: no es el handler desplegado por CloudFormation."""

from curso_ia.serverless.config import Settings
from curso_ia.serverless.demo import DemoClient
from curso_ia.serverless.handler import handle


def lambda_handler(event, context):
    return handle(
        event,
        context,
        cfg=Settings(mode="demo", version="s17-rie-demo"),
        client=DemoClient(),
        first=False,
    )
