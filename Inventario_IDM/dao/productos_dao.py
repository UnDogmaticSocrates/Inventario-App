from base_datos.conection import conectar

def crear_producto(codigo, nombre, precio, stock):
    conexion =conectar()

    conexion.execute("""
        INSERT INTO productos (codigo, nombre, precio, stock)
        VALUES (?, ?, ?, ?)
    """, (codigo, nombre, precio, stock))

    conexion.commit()
    conexion.close()

print("Producto agregado")

def obtener_productos ():
    conexion = conectar()
    cursor = conexion.cursor()

    conexion.execute("SELECT * FROM productos")

    productos = cursor.fetchall()

    conexion.close()

    return productos

def obtener_producto_por_id (id_producto):
    conexion = conectar()
    cursor = conexion.cursor()

    conexion.execute("""
        SELECT *
        FROM productos
        WHERE id = ?
    """, (id_producto,))

    producto = cursor.fetchone()

    conexion.close()

    return producto

def actualizar_producto(id, codigo, nombre, precio, stock, descripcion):
    conexion = conectar()

    conexion.execute("""
        UPDATE productos
        SET codigo = ?, 
            nombre = ?, 
            precio = ?, 
            stock = ?,
            descripcion = ?
        WHERE id = ?
    """, (id, codigo, nombre, precio, stock, descripcion))

    conexion.commit()
    conexion.close()

def eliminar_producto (id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id = ?
    """, (id,))

    conexion.commit()
    conexion.close()

