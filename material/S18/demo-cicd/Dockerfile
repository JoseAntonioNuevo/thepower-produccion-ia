# Imagen base fijada por digest: índice multi-arquitectura de python:3.12-slim-bookworm
# (Python 3.12.16) leído el 16/11/2026. Un tag puede moverse; un digest no.
FROM python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
# Dependencias con versión y hash fijados; copiarlas primero permite reutilizar la capa.
COPY requirements.lock .
RUN pip install --no-cache-dir --require-hashes -r requirements.lock \
    && groupadd --gid 10001 api && useradd --uid 10001 --gid api --no-create-home api
COPY --chown=10001:10001 app.py .
# La versión es el commit: la escribe el workflow al construir y la API la muestra.
ARG APP_VERSION=desarrollo-local
ENV APP_VERSION=${APP_VERSION} API_MODE=demo
# La aplicación no necesita permisos de administrador ni escribir en disco.
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app:crear_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
