import dao.proveedores_dao

class ControlProveedores:
    
    def crear_proveedor(self, nombre, telefono, email):
        return dao.proveedores_dao.crear_proveedor(
            nombre,
            telefono,
            email
        )

    def obtener_proveedores(self):
        return dao.proveedores_dao.obtener_proveedores()

    def obtener_proveedor_por_id(self, id_proveedor):
        return dao.proveedores_dao.obtener_proveedor_por_id(id_proveedor)

    def actualizar_proveedor(self, id, nombre, telefono, email):
        return dao.proveedores_dao.actualizar_proveedor(
            id,
            nombre,
            telefono,
            email
        )

    def eliminar_proveedor(self, id):
        return dao.proveedores_dao.eliminar_proveedor(id)