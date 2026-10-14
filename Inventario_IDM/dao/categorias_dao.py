
from base_datos.conection import conectar


def crear_categoria(nombre, descripcion):
    conexion = conectar()
    try:
        cursor = conexion.execute("""
            SELECT id, activo
            FROM categorias
            WHERE nombre = ? COLLATE NOCASE
            LIMIT 1
        """, (nombre.strip(),))

        categoria = cursor.fetchone()

        if categoria is not None:
            id_categoria, activo = categoria 

            if not activo:
                conexion.execute("""
                    UPDATE categorias
                    SET activo = 1,
                        descripcion = ?
                    WHERE id = ?
                """, (descripcion, id_categoria))

                conexion.commit()
                return True

            return False

        conexion.execute("""
            INSERT INTO categorias (nombre, descripcion)
            VALUES (?, ?)
        """, (nombre.strip(), descripcion))

        conexion.commit()
        return True

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def obtener_categorias():
    conexion = conectar()
    try:
        cursor = conexion.execute("""
            SELECT id, nombre, descripcion
            FROM categorias
            WHERE activo = 1
            ORDER BY nombre COLLATE NOCASE
        """)
        return cursor.fetchall()
    finally:
        conexion.close()


def obtener_categoria_por_id(id_categoria):
    conexion = conectar()
    try:
        cursor = conexion.execute("""
            SELECT id, nombre, descripcion, activo
            FROM categorias
            WHERE id = ?
        """, (id_categoria,))
        return cursor.fetchone()
    finally:
        conexion.close()


def actualizar_categoria(id_categoria, nombre, descripcion):
    conexion = conectar()
    try:
        cursor = conexion.execute("""
            UPDATE categorias
            SET nombre = ?, descripcion = ?
            WHERE id = ? AND activo = 1
        """, (nombre, descripcion, id_categoria))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def desactivar_categoria(id_categoria):
    conexion = conectar()
    try:
        cursor = conexion.execute("""
            UPDATE categorias
            SET activo = 0
            WHERE id = ? AND activo = 1
        """, (id_categoria,))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception:
        conexion.rollback()
        raise


def activar_categoria(id_categoria):
    conexion = conectar()
    try:
        cursor = conexion.execute("""
            UPDATE categorias
            SET activo = 1
            WHERE id = ? AND activo = 0
        """, (id_categoria,))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
