
from .conection import conectar


def crear_tablas():
    conexion = conectar()

    try:
        conexion.executescript("""
            CREATE TABLE IF NOT EXISTS unidades(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                activa INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS proveedores(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                email TEXT
            );

            CREATE TABLE IF NOT EXISTS categorias(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT
            );

            CREATE TABLE IF NOT EXISTS productos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                stock REAL DEFAULT 0,
                unidad_id INTEGER,
                ubicacion TEXT,
                categoria_id INTEGER,
                proveedor_id INTEGER,

                FOREIGN KEY (unidad_id)
                    REFERENCES unidades(id),

                FOREIGN KEY (categoria_id)
                    REFERENCES categorias(id),

                FOREIGN KEY (proveedor_id)
                    REFERENCES proveedores(id)
            );
        """)

        cursor = conexion.cursor()

        # Migración: estado de los productos.
        cursor.execute("PRAGMA table_info(productos)")
        columnas = [columna[1] for columna in cursor.fetchall()]

        if "activo" not in columnas:
            cursor.execute("""
                ALTER TABLE productos
                ADD COLUMN activo INTEGER NOT NULL DEFAULT 1
            """)

        # Migración: estado de las categorías.
        cursor.execute("PRAGMA table_info(categorias)")
        columnas_categorias = [
            columna[1] for columna in cursor.fetchall()
        ]

        if "activo" not in columnas_categorias:
            cursor.execute("""
                ALTER TABLE categorias
                ADD COLUMN activo INTEGER NOT NULL DEFAULT 1
            """)

        conexion.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_categorias_nombre_unico
            ON categorias(LOWER(TRIM(nombre)))
        """)

        # Historial de movimientos de inventario.
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS movimientos_inventario(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL CHECK (
                    tipo IN (
                        'existencia_inicial',
                        'entrada',
                        'salida',
                        'ajuste'
                    )
                ),
                cantidad REAL NOT NULL CHECK (cantidad >= 0),
                stock_resultante REAL NOT NULL,
                motivo TEXT,
                fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (producto_id)
                    REFERENCES productos(id)
            )
        """)

        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()
