import sqlite3

from base_datos.conection import conectar


def crear_unidad(nombre):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, activa
        FROM unidades
        WHERE nombre = ?
    """, (nombre,))

    unidad = cursor.fetchone()

    if unidad:
        id_unidad = unidad[0]
        activa = unidad[1]

        if activa == 0:

            return{
                "estado": "desactivada",
                "id": id_unidad
            }
        return{
            "estado": "existe"
        }

    conexion.execute("""
        INSERT INTO unidades (nombre)
        VALUES (?)
    """, (nombre,))

    conexion.commit()
    conexion.close()

    return {
        "estado": "creada",
    }

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

def activar_unidad(id_unidad):

    conexion = conectar()

    conexion.execute("""
        UPDATE unidades
        SET activa = 1
        WHERE id = ?
    """, (id_unidad,))

    conexion.commit()
    conexion.close()

    return True