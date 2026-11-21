# Imagen del agente: la misma sirve para la API y para el ejecutor de investigaciones.
#   docker build -t thepower-s20-agente .
#   docker run --rm -p 8020:8020 thepower-s20-agente
# Sin variables arranca en el perfil doble y en memoria: no lleva claves dentro.
FROM python:3.12-slim

# uv instala exactamente lo que fija uv.lock (misma versión aquí que en tu portátil).
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /usr/local/bin/uv
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONUNBUFFERED=1

# Primero solo las dependencias: esta capa se reutiliza mientras no cambie uv.lock.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY esquema.sql ./
COPY agente ./agente
COPY servidor_mcp ./servidor_mcp
COPY datos ./datos

# El proceso no corre como root.
RUN useradd --create-home agente
USER agente
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8020

# API por defecto. El ejecutor usa la misma imagen con otro comando:
#   python -m agente.cli investigar
CMD ["uvicorn", "agente.api:app", "--host", "0.0.0.0", "--port", "8020"]
