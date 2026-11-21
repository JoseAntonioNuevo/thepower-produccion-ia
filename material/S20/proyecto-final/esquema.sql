-- PASO 5 · Esquema de PostgreSQL del proyecto final (idempotente).
-- Tres familias de tablas que NO se mezclan:
--   1. conversaciones  -> quién es dueño de cada thread_id (autorización)
--   2. fragmentos      -> documentación propia con su vector (RAG, pgvector)
--   3. trabajos        -> investigaciones: estado, pasos e informe
-- Las tablas de checkpoints (la memoria del grafo) las crea LangGraph con `setup()`.

CREATE EXTENSION IF NOT EXISTS vector;

-- thread_id identifica una conversación; el propietario decide quién puede leerla.
CREATE TABLE IF NOT EXISTS conversaciones (
  thread_id  TEXT PRIMARY KEY,
  usuario    TEXT NOT NULL,
  creada_en  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Un fragmento = una sección de un documento, con su embedding de 768 dimensiones.
CREATE TABLE IF NOT EXISTS fragmentos (
  fragmento_id TEXT PRIMARY KEY,           -- p. ej. 03-limites-y-cuotas-api#1
  documento    TEXT NOT NULL,
  titulo       TEXT NOT NULL,
  seccion      TEXT NOT NULL,
  contenido    TEXT NOT NULL,
  modelo       TEXT NOT NULL,              -- mismo modelo al indexar y al consultar
  embedding    vector(768) NOT NULL
);
-- Índice aproximado HNSW con distancia coseno (operador <=>).
CREATE INDEX IF NOT EXISTS fragmentos_embedding_hnsw
  ON fragmentos USING hnsw (embedding vector_cosine_ops);

-- Una investigación es un trabajo con estado. `clave` la hace idempotente:
-- pedir dos veces lo mismo en la misma conversación devuelve el mismo trabajo.
CREATE TABLE IF NOT EXISTS trabajos (
  trabajo_id   TEXT PRIMARY KEY,
  clave        TEXT NOT NULL UNIQUE,
  thread_id    TEXT NOT NULL,
  usuario      TEXT NOT NULL,
  tema         TEXT NOT NULL,
  estado       TEXT NOT NULL CHECK (estado IN ('pendiente','en_curso','completo','parcial','error')),
  informe      JSONB,
  creado_en    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actualizado_en TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
