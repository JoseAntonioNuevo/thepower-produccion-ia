# Índice multi-arquitectura verificado el 17/10/2026: Python 3.12.15, Debian bookworm.
FROM python:3.12-slim-bookworm@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258
# Evita escrituras de bytecode y muestra logs inmediatamente en CloudWatch.
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app/src
WORKDIR /app
# El lock exportado incluye versiones y hashes de todas las dependencias de ejecución.
COPY requirements.lock ./
RUN pip install --no-cache-dir --require-hashes -r requirements.lock \
    && groupadd --gid 10001 curso && useradd --uid 10001 --gid curso --no-create-home curso
COPY --chown=10001:10001 src/ ./src/
ARG APP_VERSION=desarrollo-local
ENV APP_VERSION=${APP_VERSION} API_MODE=demo
# La aplicación no necesita escribir archivos ni elevar privilegios.
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"
CMD ["uvicorn", "curso_ia.api:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]

