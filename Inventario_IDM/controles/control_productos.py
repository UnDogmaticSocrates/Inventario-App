import dao.productos_dao

class ProductosController:

    def crear_producto(self, codigo, nombre, precio, stock):
        return dao.productos_dao.crear_producto(
            codigo,
            nombre,
            precio,
            stock
        )

    def obtener_productos(self):
        return dao.productos_dao.obtener_productos()

    def obtener_producto_por_id(self, id_producto):
        return dao.productos_dao.obtener_producto_por_id(id_producto)

    def actualizar_producto(self, id, codigo, nombre, precio, stock, descripcion):
        return dao.productos_dao.actualizar_producto(
            id, 
            codigo,
            nombre,
            precio,
            stock,
            descripcion 
        )

    def eliminar_producto(self, id):
        return dao.productos_dao.eliminar_producto(id)