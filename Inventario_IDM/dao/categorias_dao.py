from base_datos.conection import conectar


def crear_categoria(nombre, descripcion):
    conexion = conectar()

    conexion.execute("""
        INSERT INTO categorias (nombre, descripcion)
        VALUES (?, ?)
    """, (nombre, descripcion))

    conexion.commit()
    conexion.close()


def obtener_categorias():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM categorias")

    categorias = cursor.fetchall()

    conexion.close()

    return categorias


def obtener_categoria_por_id(id_categoria):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM categorias
        WHERE id = ?
    """, (id_categoria,))

    categoria = cursor.fetchone()

    conexion.close()

    return categoria


def actualizar_categoria(id, nombre, descripcion):
    conexion = conectar()

    conexion.execute("""
        UPDATE categorias
        SET nombre = ?,
            descripcion = ?
        WHERE id = ?
    """, (nombre, descripcion, id))

    conexion.commit()
    conexion.close()


def eliminar_categoria(id):
    conexion = conectar()

    conexion.execute("""
        DELETE FROM categorias
        WHERE id = ?
    """, (id,))

    conexion.commit()
    conexion.close()