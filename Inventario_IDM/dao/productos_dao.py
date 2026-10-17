import math
from base_datos.conection import conectar


def crear_producto(
    codigo, nombre, precio, unidad_id, ubicacion, categoria_id,
    cantidad_inicial = None, registrar_existencia_inicial = True
):
    if registrar_existencia_inicial:
        if cantidad_inicial is None:
            raise ValueError("Indica la existencia inicial.")
        
        cantidad_inicial= float(cantidad_inicial)
        
        if not math.isfinite(cantidad_inicial) or cantidad_inicial < 0:
            raise ValueError(
                "Ingrese un número válido que no sea negativo."
            )
            
    else:
        cantidad_inicial = 0
        
        
    conexion = conectar()
    
    
    try:
        cursor = conexion.execute("""
            INSERT INTO productos (
                codigo, nombre, precio, stock,
                unidad_id, ubicacion, categoria_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            codigo,
            nombre,
            precio,
            cantidad_inicial,
            unidad_id,
            ubicacion,
            categoria_id
        ))
        
        id_producto = cursor.lastrowid
        
        if registrar_existencia_inicial:
            conexion.execute("""
                INSERT INTO movimientos_inventario (
                    producto_id, 
                    tipo,
                    cantidad,
                    stock_resultante,
                    motivo
                )
                VALUES(?, 'existencia_inicial', ?, ?, ?)
            """, (
                id_producto,
                cantidad_inicial,
                cantidad_inicial,
                "conteo inicial"
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
        
def registrar_movimiento(id_producto, tipo, cantidad, motivo=None):
    tipos_validos = {"entrada", "salida", "ajuste"}

    if tipo not in tipos_validos:
        raise ValueError("El tipo de movimiento no es válido.")

    try:
        cantidad = float(cantidad)
    except (TypeError, ValueError):
        raise ValueError("La cantidad debe ser numérica.")

    if not math.isfinite(cantidad) or cantidad < 0:
        raise ValueError("La cantidad debe ser válida y no negativa.")

    if tipo in {"entrada", "salida"} and cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor que cero.")

    conexion = conectar()

    try:
        # Evita que dos operaciones simultáneas lean el mismo stock.
        conexion.execute("BEGIN IMMEDIATE")

        cursor = conexion.execute(
            """
            SELECT stock
            FROM productos
            WHERE id = ? AND activo = 1
            """,
            (id_producto,)
        )

        producto = cursor.fetchone()

        if producto is None:
            raise ValueError("El producto no existe o está inactivo.")

        stock_actual = float(producto[0])

        if tipo == "entrada":
            stock_nuevo = stock_actual + cantidad

        elif tipo == "salida":
            if cantidad > stock_actual:
                raise ValueError(
                    f"Existencia insuficiente. Stock actual: {stock_actual:g}."
                )
            stock_nuevo = stock_actual - cantidad

        else:  # ajuste: cantidad representa el stock físico contado
            stock_nuevo = cantidad
            cantidad = abs(stock_nuevo - stock_actual)

        conexion.execute(
            """
            UPDATE productos
            SET stock = ?
            WHERE id = ?
            """,
            (stock_nuevo, id_producto)
        )

        conexion.execute(
            """
            INSERT INTO movimientos_inventario (
                producto_id, tipo, cantidad, stock_resultante, motivo
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (id_producto, tipo, cantidad, stock_nuevo, motivo)
        )

        conexion.commit()
        return True

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()
        
def obtener_historial_movimientos(id_producto):
    conexion = conectar()

    try:
        cursor = conexion.execute(
            """
            SELECT id, tipo, cantidad, stock_resultante, motivo, fecha
            FROM movimientos_inventario
            WHERE producto_id = ?
            ORDER BY id DESC
            """,
            (id_producto,)
        )

        return cursor.fetchall()

    finally:
        conexion.close()

