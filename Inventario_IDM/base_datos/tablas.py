from .conection import conectar

def crear_tablas():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS unidades(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
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
    """)

    conexion.commit()
    conexion.close()