from .conection import conectar

def crear_tablas():
    conexion = conectar()

    cursor = conexion.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE, 
            nombre TEXT NOT NULL,
            precio REAL NOT NULL, 
            stock INTEGER DEFAULT 0,
            ubicacion TEXT
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