"""Ampliación opcional de S18: migración compatible y prueba de restauración.

Todo ocurre en una carpeta temporal con SQLite y datos ficticios. No toca la API,
ni AWS, ni ninguna base de datos real. Sirve para ver con datos tres ideas:

1. Un cambio «expand» (añadir una columna opcional) no rompe a la versión anterior.
2. Volver al código anterior NO deshace lo que ya se escribió en la base de datos.
3. Una copia de seguridad solo vale si se ha restaurado y comprobado.

    python extras/migracion_y_restauracion.py
"""

import hashlib
import sqlite3
import tempfile
from pathlib import Path


def conectar(ruta: Path) -> sqlite3.Connection:
    conexion = sqlite3.connect(ruta)
    conexion.row_factory = sqlite3.Row
    return conexion


# ------------------------------------------------- dos versiones del código
def guardar_version_a(db: sqlite3.Connection, categoria: str, prioridad: str) -> None:
    """Código de la versión A: no sabe que existe el plazo de atención."""
    db.execute(
        "INSERT INTO incidencias (categoria, prioridad) VALUES (?, ?)", (categoria, prioridad)
    )
    db.commit()


def guardar_version_b(db: sqlite3.Connection, categoria: str, prioridad: str, sla: int) -> None:
    """Código de la versión B: escribe también el plazo."""
    db.execute(
        "INSERT INTO incidencias (categoria, prioridad, sla_horas) VALUES (?, ?, ?)",
        (categoria, prioridad, sla),
    )
    db.commit()


def leer_version_a(db: sqlite3.Connection) -> list[tuple]:
    """A pide las columnas por su nombre: una columna nueva no le afecta."""
    return [tuple(f) for f in db.execute("SELECT id, categoria, prioridad FROM incidencias")]


def huella(db: sqlite3.Connection) -> str:
    """Resumen del contenido: permite comparar el original con lo restaurado."""
    filas = db.execute("SELECT * FROM incidencias ORDER BY id").fetchall()
    return hashlib.sha256(repr([tuple(f) for f in filas]).encode()).hexdigest()[:16]


def main() -> None:
    with tempfile.TemporaryDirectory() as carpeta:
        ruta = Path(carpeta) / "soporte.sqlite3"
        db = conectar(ruta)

        print("1. Esquema inicial y datos ficticios escritos por la versión A")
        db.execute(
            "CREATE TABLE incidencias (id INTEGER PRIMARY KEY, categoria TEXT NOT NULL,"
            " prioridad TEXT NOT NULL)"
        )
        for categoria, prioridad in [
            ("acceso", "media"),
            ("tecnico", "alta"),
            ("consulta", "baja"),
        ]:
            guardar_version_a(db, categoria, prioridad)
        print(f"   filas: {len(leer_version_a(db))}")

        print("2. Copia de seguridad ANTES de migrar, con su huella")
        copia = Path(carpeta) / "copia-antes-de-migrar.sqlite3"
        destino = conectar(copia)
        db.backup(destino)  # copia coherente aunque la base esté en uso
        destino.close()
        huella_copia = huella(db)
        filas_copia = len(leer_version_a(db))
        print(f"   {copia.name}: {filas_copia} filas, huella {huella_copia}")

        print("3. EXPAND: columna nueva opcional. Es compatible con la versión A")
        db.execute("ALTER TABLE incidencias ADD COLUMN sla_horas INTEGER")  # admite NULL
        guardar_version_a(db, "facturacion", "media")  # A sigue escribiendo
        guardar_version_b(db, "acceso", "alta", 4)  # B ya usa la columna
        assert len(leer_version_a(db)) == 5  # y A sigue leyendo
        print("   A y B escriben y leen a la vez: se puede desplegar B poco a poco")

        print("4. Rellenar los datos antiguos (backfill) sin parar el servicio")
        plazos = {"alta": 4, "media": 24, "baja": 72}
        for prioridad, horas in plazos.items():
            db.execute(
                "UPDATE incidencias SET sla_horas = ? WHERE sla_horas IS NULL AND prioridad = ?",
                (horas, prioridad),
            )
        db.commit()
        pendientes = db.execute("SELECT count(*) FROM incidencias WHERE sla_horas IS NULL")
        assert pendientes.fetchone()[0] == 0

        print("5. Rollback del CÓDIGO a la versión A: los datos no retroceden")
        guardar_version_a(db, "consulta", "baja")
        columnas = [c["name"] for c in db.execute("PRAGMA table_info(incidencias)")]
        assert "sla_horas" in columnas and len(leer_version_a(db)) == 6
        print(f"   la columna sigue ahí ({', '.join(columnas)}) y hay 6 filas, no 3")

        print("6. Un cambio INCOMPATIBLE rompería a A (se prueba y se deshace)")
        db.execute("ALTER TABLE incidencias RENAME COLUMN prioridad TO urgencia")
        try:
            leer_version_a(db)
            raise AssertionError("la versión A debería fallar con la columna renombrada")
        except sqlite3.OperationalError as error:
            print(f"   la versión A falla: {error}")
        db.execute("ALTER TABLE incidencias RENAME COLUMN urgencia TO prioridad")
        assert len(leer_version_a(db)) == 6

        print("7. PRUEBA DE RESTAURACIÓN en una base nueva, sin tocar la original")
        restaurada = Path(carpeta) / "restaurada.sqlite3"
        origen = conectar(copia)
        nueva = conectar(restaurada)
        origen.backup(nueva)
        origen.close()
        integridad = nueva.execute("PRAGMA integrity_check").fetchone()[0]
        assert integridad == "ok"
        assert huella(nueva) == huella_copia and len(leer_version_a(nueva)) == filas_copia
        perdidas = len(leer_version_a(db)) - filas_copia
        print(f"   integridad {integridad}, {filas_copia} filas, huella {huella(nueva)}: coincide")
        print(f"   lo escrito después de la copia no está: {perdidas} filas (eso mide el RPO)")
        nueva.close()
        db.close()
    print("CORRECTO: migración compatible y restauración comprobadas con datos ficticios")


if __name__ == "__main__":
    main()
