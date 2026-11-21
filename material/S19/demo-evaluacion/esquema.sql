-- Esquema de S19: un índice vectorial por configuración, reconstruible desde cero.
CREATE EXTENSION IF NOT EXISTS vector;

-- Una fila por índice. Su id es una huella de corpus + fragmentación + modelo de embeddings:
-- si cambia cualquiera de los tres, es OTRO índice y no se mezcla con el anterior.
CREATE TABLE IF NOT EXISTS indices (
  indice_id        TEXT PRIMARY KEY,
  perfil           TEXT NOT NULL,                 -- 'doble' (sin coste) o 'real'
  embedding_modelo TEXT NOT NULL,                 -- el MISMO al indexar y al consultar
  embedding_dim    INTEGER NOT NULL CHECK (embedding_dim = 768),
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
  embedding      vector(768) NOT NULL,
  PRIMARY KEY (indice_id, fragmento_id),
  -- Segunda barrera contra duplicados: el mismo texto no entra dos veces en un índice.
  UNIQUE (indice_id, contenido_hash)
);

-- HNSW con distancia coseno, como en S10. Con decenas de filas no aporta velocidad:
-- la evaluación usa búsqueda exacta para no añadir la aproximación del índice como variable.
CREATE INDEX IF NOT EXISTS fragmentos_embedding_hnsw
  ON fragmentos USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);
