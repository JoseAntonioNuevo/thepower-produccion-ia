# Entorno de construcción y ensayo Lambda oficial, fijado por digest el 17/10/2026.
FROM public.ecr.aws/lambda/python:3.12@sha256:3856536f53e945debf4c90d0ff301cbaa837c07a4ab9b0e2c102c6e54ceb9762
WORKDIR /asset
ENV PYTHONPATH=/asset PYTHONDONTWRITEBYTECODE=1 AWS_EC2_METADATA_DISABLED=true
COPY infra/s17/requirements.lock /tmp/requirements.lock
RUN python -m pip install --require-hashes --no-compile --no-cache-dir \
    --target /asset -r /tmp/requirements.lock
COPY src/curso_ia/__init__.py src/curso_ia/contratos.py /asset/curso_ia/
COPY src/curso_ia/serverless/ /asset/curso_ia/serverless/
# Comprueba que las dependencias nativas cargan en Linux y que la demo no necesita claves.
RUN python -c "from curso_ia.serverless.demo import DemoContext,event_for; from curso_ia.serverless.local_handler import lambda_handler; r=lambda_handler(event_for(),DemoContext()); assert r['statusCode']==200"
CMD ["curso_ia.serverless.handler.lambda_handler"]
