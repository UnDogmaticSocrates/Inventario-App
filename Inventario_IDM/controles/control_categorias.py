import dao.categorias_dao

class ControlCategorias:
    
    def crear_categoria(self, nombre, descripcion):
        return dao.categorias_dao.crear_categoria(
            nombre,
            descripcion
        )

    def obtener_categorias(self):
        return dao.categorias_dao.obtener_categorias()

    def obtener_categoria_por_id(self, id_categoria):
        return dao.categorias_dao.obtener_categoria_por_id(id_categoria)

    def actualizar_categoria(self, id, nombre, descripcion):
        return dao.categorias_dao.actualizar_categoria(
            id,
            nombre,
            descripcion
        )

    def eliminar_categoria(self, id):
        return dao.categorias_dao.eliminar_categoria(id)