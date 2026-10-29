
from base_datos.conection import conectar


def crear_producto_critico(
    producto_id,
    motivo="esencial",
    frecuencia_reporte="semanal",
    alertas_activas=True
):
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            INSERT INTO productos_criticos (
                producto_id,
                motivo,
                frecuencia_reporte,
                alertas_activas
            )
            VALUES (?, ?, ?, ?)
        """, (
            producto_id,
            motivo,
            frecuencia_reporte,
            int(alertas_activas)
        ))

        conexion.commit()
        return cursor.lastrowid

    finally:
        conexion.close()


def obtener_productos_criticos(solo_activos=True):
    conexion = conectar()

    try:
        consulta = """
            SELECT
                pc.id,
                pc.producto_id,
                p.codigo,
                p.nombre,
                p.descripcion,
                p.stock,
                p.stock_minimo,
                p.unidad_id,
                u.nombre AS unidad,
                pc.motivo,
                pc.frecuencia_reporte,
                pc.alertas_activas,
                pc.activo,
                pc.fecha_creacion
            FROM productos_criticos pc
            INNER JOIN productos p
                ON p.id = pc.producto_id
            LEFT JOIN unidades u
                ON u.id = p.unidad_id
        """

        if solo_activos:
            consulta += """
                WHERE pc.activo = 1
                  AND p.activo = 1
            """

        consulta += " ORDER BY p.nombre COLLATE NOCASE"

        cursor = conexion.execute(consulta)
        return cursor.fetchall()

    finally:
        conexion.close()


def obtener_producto_critico_por_producto_id(producto_id):
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            SELECT *
            FROM productos_criticos
            WHERE producto_id = ?
        """, (producto_id,))

        return cursor.fetchone()

    finally:
        conexion.close()


def actualizar_producto_critico(
    producto_id,
    motivo,
    frecuencia_reporte,
    alertas_activas,
    activo=True
):
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            UPDATE productos_criticos
            SET motivo = ?,
                frecuencia_reporte = ?,
                alertas_activas = ?,
                activo = ?
            WHERE producto_id = ?
        """, (
            motivo,
            frecuencia_reporte,
            int(alertas_activas),
            int(activo),
            producto_id
        ))

        conexion.commit()
        return cursor.rowcount > 0

    finally:
        conexion.close()


def desactivar_producto_critico(producto_id):
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            UPDATE productos_criticos
            SET activo = 0
            WHERE producto_id = ?
        """, (producto_id,))

        conexion.commit()
        return cursor.rowcount > 0

    finally:
        conexion.close()


def registrar_alerta(producto_id, stock_detectado, stock_minimo):
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            INSERT INTO alertas_inventario (
                producto_id,
                stock_detectado,
                stock_minimo
            )
            VALUES (?, ?, ?)
        """, (
            producto_id,
            stock_detectado,
            stock_minimo
        ))

        conexion.commit()
        return cursor.lastrowid

    finally:
        conexion.close()


def obtener_alertas_pendientes():
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            SELECT
                a.id,
                a.producto_id,
                p.codigo,
                p.nombre,
                a.stock_detectado,
                a.stock_minimo,
                a.fecha_deteccion,
                a.estado
            FROM alertas_inventario a
            INNER JOIN productos p
                ON p.id = a.producto_id
            WHERE a.estado = 'pendiente'
            ORDER BY a.fecha_deteccion
        """)

        return cursor.fetchall()

    finally:
        conexion.close()


def marcar_alerta_notificada(id_alerta):
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            UPDATE alertas_inventario
            SET estado = 'notificada',
                fecha_notificacion = CURRENT_TIMESTAMP
            WHERE id = ?
              AND estado = 'pendiente'
        """, (id_alerta,))

        conexion.commit()
        return cursor.rowcount > 0

    finally:
        conexion.close()


def resolver_alerta(id_alerta):
    conexion = conectar()

    try:
        cursor = conexion.execute("""
            UPDATE alertas_inventario
            SET estado = 'resuelta'
            WHERE id = ?
              AND estado != 'resuelta'
        """, (id_alerta,))

        conexion.commit()
        return cursor.rowcount > 0

    finally:
        conexion.close()

def revisar_stock_productos_criticos():
    conexion = conectar()

    resultado = {
        "revisados": 0,
        "alertas_creadas": 0,
        "alertas_actualizadas": 0,
        "alertas_resueltas": 0
    }

    try:
        cursor = conexion.cursor()

        productos = cursor.execute("""
            SELECT
                pc.producto_id,
                p.nombre,
                p.stock,
                p.stock_minimo,
                pc.alertas_activas,
                pc.activo,
                p.activo
            FROM productos_criticos pc
            INNER JOIN productos p
                ON p.id = pc.producto_id
        """).fetchall()

        for producto in productos:
            (
                producto_id,
                nombre,
                stock,
                stock_minimo,
                alertas_activas,
                critico_activo,
                producto_activo
            ) = producto

            # Solo se revisan productos activos con alertas habilitadas.
            if not critico_activo or not producto_activo or not alertas_activas:
                continue

            resultado["revisados"] += 1

            # Buscamos una alerta que todavía no esté resuelta.
            alerta = cursor.execute("""
                SELECT id, estado
                FROM alertas_inventario
                WHERE producto_id = ?
                  AND estado IN ('pendiente', 'notificada')
                ORDER BY id DESC
                LIMIT 1
            """, (producto_id,)).fetchone()

            if stock < stock_minimo:
                if alerta is None:
                    cursor.execute("""
                        INSERT INTO alertas_inventario (
                            producto_id,
                            stock_detectado,
                            stock_minimo
                        )
                        VALUES (?, ?, ?)
                    """, (producto_id, stock, stock_minimo))

                    resultado["alertas_creadas"] += 1

                elif alerta[1] == "pendiente":
                    cursor.execute("""
                        UPDATE alertas_inventario
                        SET stock_detectado = ?,
                            stock_minimo = ?
                        WHERE id = ?
                    """, (stock, stock_minimo, alerta[0]))

                    resultado["alertas_actualizadas"] += 1

                # Si ya fue notificada, no se genera otra alerta
                # mientras siga abierta la misma situación.

            elif alerta is not None:
                cursor.execute("""
                    UPDATE alertas_inventario
                    SET estado = 'resuelta'
                    WHERE producto_id = ?
                      AND estado IN ('pendiente', 'notificada')
                """, (producto_id,))

                resultado["alertas_resueltas"] += cursor.rowcount

        conexion.commit()
        return resultado

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()
