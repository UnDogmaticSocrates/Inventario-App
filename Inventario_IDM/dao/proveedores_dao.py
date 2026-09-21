from base_datos.conection import conectar

def crear_proveedor(nombre, telefono, email):
    conexion = conectar()

    conexion.execute("""
        INSERT INTO proveedores (nombre, telefono, email)
        VALUES (?, ?, ?)
    """, (nombre, telefono, email))

    conexion.commit()
    conexion.close()

def obtener_proveedores():
    conexion = conectar()
    cursor = conexion.cursor()

    conexion.execute("SELECT * FROM proveedores")

    proveedores = cursor.fetchall()

    conexion.close()

    return proveedores

def obtener_proveedor_por_id(id_proveedor):
    conexion = conectar()
    cursor = conexion.cursor()

    conexion.execute("""
        SELECT *
        FROM proveedores
        WHERE id = ?
    """, (id_proveedor,))

    proveedor = cursor.fetchone()

    conexion.close()

    return proveedor

def actualizar_proveedor(id, nombre, telefono, email):
    conexion = conectar()

    conexion.execute("""
        UPDATE proveedores
        SET nombre = ?, 
            telefono = ?, 
            email = ?
        WHERE id = ?
    """, (nombre, telefono, email, id))

def eliminar_proveedor(id):
    conexion = conectar()

    conexion.execute("""
        DELETE FROM proveedores
        WHERE id = ?
    """, (id,))

    conexion.commit()
    conexion.close()

def obtener_proveedor_por_nombre(nombre):
    conexion = conectar()
    cursor = conexion.cursor()

    conexion.execute("""
        SELECT *
        FROM proveedores
        WHERE nombre = ?
    """, (nombre,))

    proveedor = cursor.fetchone()

    conexion.close()

    return proveedor

