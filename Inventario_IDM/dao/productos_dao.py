
from base_datos.conection import conectar


def crear_producto(
    codigo, nombre, precio, unidad_id, ubicacion, categoria_id
):
    conexion = conectar()

    try:
        conexion.execute("""
            INSERT INTO productos (
                codigo, nombre, precio, stock,
                unidad_id, ubicacion, categoria_id
            )
            VALUES (?, ?, ?, 0, ?, ?, ?)
        """, (
            codigo,
            nombre,
            precio,
            unidad_id,
            ubicacion,
            categoria_id
        ))

        conexion.commit()
        return True

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def obtener_productos():
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            SELECT
                id, codigo, nombre, precio, stock,
                unidad_id, ubicacion, categoria_id,
                proveedor_id, activo
            FROM productos
            WHERE activo = 1
            ORDER BY nombre COLLATE NOCASE
        """)
        return cursor.fetchall()

    finally:
        conexion.close()


def obtener_producto_por_id(id_producto):
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            SELECT *
            FROM productos
            WHERE id = ?
        """, (id_producto,))
        return cursor.fetchone()

    finally:
        conexion.close()


def actualizar_producto(
    id_producto, codigo, nombre, precio,
    unidad_id, ubicacion, categoria_id
):
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            UPDATE productos
            SET codigo = ?,
                nombre = ?,
                precio = ?,
                unidad_id = ?,
                ubicacion = ?,
                categoria_id = ?
            WHERE id = ?
              AND activo = 1
        """, (
            codigo,
            nombre,
            precio,
            unidad_id,
            ubicacion,
            categoria_id,
            id_producto
        ))

        conexion.commit()
        return cursor.rowcount > 0

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def desactivar_producto(id_producto):
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            UPDATE productos
            SET activo = 0
            WHERE id = ?
              AND activo = 1
        """, (id_producto,))

        conexion.commit()
        return cursor.rowcount > 0

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def activar_producto(id_producto):
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            UPDATE productos
            SET activo = 1
            WHERE id = ?
              AND activo = 0
        """, (id_producto,))

        conexion.commit()
        return cursor.rowcount > 0

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()

def obtener_productos_desactivados():
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            SELECT
                id, codigo, nombre, precio, stock,
                unidad_id, ubicacion, categoria_id,
                proveedor_id, activo
            FROM productos
            WHERE activo = 0
            ORDER BY nombre COLLATE NOCASE
        """)
        return cursor.fetchall()

    finally:
        conexion.close()

