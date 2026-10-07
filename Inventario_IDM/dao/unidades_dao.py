import sqlite3

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
        WHERE activa = 1
        ORDER BY id
    """)

    unidades = cursor.fetchall()

    conexion.close()

    return unidades

def actualizar_unidad(id_unidad, nombre):

    conexion = conectar()

    try:

        conexion.execute("""
            UPDATE unidades
            SET nombre = ?
            WHERE id = ?
        """, (nombre, id_unidad))

        conexion.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conexion.close()

def desactivar_unidad(id_unidad):

    conexion = conectar()

    conexion.execute("""
        UPDATE unidades
        SET activa = 0
        WHERE id = ?
    """, (id_unidad,))

    conexion.commit()
    conexion.close()

    return True