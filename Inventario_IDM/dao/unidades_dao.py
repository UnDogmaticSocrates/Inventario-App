from base_datos.conection import conectar


def crear_unidad(nombre):

    conexion = conectar()

    conexion.execute("""
        INSERT INTO unidades (nombre)
        VALUES (?)
    """, (nombre,))

    conexion.commit()
    conexion.close()

    return True

def obtener_unidades():

    conexion = conectar()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre
        FROM unidades
        ORDER BY id
    """)

    unidades = cursor.fetchall()

    conexion.close()

    return unidades