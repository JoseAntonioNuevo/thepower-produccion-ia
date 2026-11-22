-- Esquema de S19: un índice vectorial por configuración, reconstruible desde cero.
CREATE EXTENSION IF NOT EXISTS vector;

-- Una fila por índice. Su id es una huella de corpus + fragmentación + modelo de embeddings:
-- si cambia cualquiera de los tres, es OTRO índice y no se mezcla con el anterior.
CREATE TABLE IF NOT EXISTS indices (
  indice_id        TEXT PRIMARY KEY,
  perfil           TEXT NOT NULL,                 -- 'doble' (sin coste) o 'real'
  embedding_modelo TEXT NOT NULL,                 -- el MISMO al indexar y al consultar
  embedding_dim    INTEGER NOT NULL CHECK (embedding_dim > 0),  -- la decide el modelo de .env
  chunk_size       INTEGER NOT NULL,
  chunk_overlap    INTEGER NOT NULL,
  n_documentos     INTEGER NOT NULL,
  n_fragmentos     INTEGER NOT NULL,
  creado           TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fragmentos (
  indice_id      TEXT NOT NULL REFERENCES indices(indice_id) ON DELETE CASCADE,
  fragmento_id   TEXT NOT NULL,                   -- '<documento>#<ordinal>'
  documento_id   TEXT NOT NULL,                   -- unidad de precision@5 y recall@5
  ordinal        INTEGER NOT NULL,
  titulo         TEXT NOT NULL,
  contenido      TEXT NOT NULL,
  contenido_hash TEXT NOT NULL,
  embedding      vector NOT NULL,                 -- sin dimensión fija: cada índice guarda la suya
  PRIMARY KEY (indice_id, fragmento_id),
  -- Segunda barrera contra duplicados: el mismo texto no entra dos veces en un índice.
  UNIQUE (indice_id, contenido_hash)
);

-- Sin índice HNSW. En S10 se usó uno, pero HNSW exige una dimensión fija y aquí el modelo de
-- embeddings (y por tanto la dimensión) se cambia desde .env. Con decenas de filas la búsqueda
-- exacta es instantánea y además evita que la aproximación del índice sea otra variable al
-- evaluar. En producción, con el modelo ya decidido, se fija vector(N) y se crea el HNSW.

-- Migración de bases creadas con la versión anterior (vector(768) fijo). Idempotente.
DROP INDEX IF EXISTS fragmentos_embedding_hnsw;
ALTER TABLE fragmentos ALTER COLUMN embedding TYPE vector;
ALTER TABLE indices DROP CONSTRAINT IF EXISTS indices_embedding_dim_check;
ALTER TABLE indices ADD CONSTRAINT indices_embedding_dim_check CHECK (embedding_dim > 0);
