
import dao.productos_dao


class ProductosController:

    def crear_producto(
        self, codigo, nombre, precio, unidad_id, ubicacion, categoria_id
    ):
        return dao.productos_dao.crear_producto(
            codigo,
            nombre,
            precio,
            unidad_id,
            ubicacion,
            categoria_id
        )

    def obtener_productos(self):
        return dao.productos_dao.obtener_productos()

    def obtener_producto_por_id(self, id_producto):
        return dao.productos_dao.obtener_producto_por_id(id_producto)

    def actualizar_producto(
        self, id_producto, codigo, nombre, precio,
        unidad_id, ubicacion, categoria_id
    ):
        return dao.productos_dao.actualizar_producto(
            id_producto,
            codigo,
            nombre,
            precio,
            unidad_id,
            ubicacion,
            categoria_id
        )

    def desactivar_producto(self, id_producto):
        return dao.productos_dao.desactivar_producto(id_producto)

    def activar_producto(self, id_producto):
        return dao.productos_dao.activar_producto(id_producto)
    
    def obtener_productos_desactivados(self):
        return dao.productos_dao.obtener_productos_desactivados()
