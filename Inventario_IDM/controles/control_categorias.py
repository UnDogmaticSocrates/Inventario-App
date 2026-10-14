
import dao.categorias_dao


class CategoriasController:

    def crear_categoria(self, nombre, descripcion):
        return dao.categorias_dao.crear_categoria(
            nombre, descripcion
        )

    def obtener_categorias(self):
        return dao.categorias_dao.obtener_categorias()

    def obtener_categoria_por_id(self, id_categoria):
        return dao.categorias_dao.obtener_categoria_por_id(
            id_categoria
        )

    def actualizar_categoria(
        self, id_categoria, nombre, descripcion
    ):
        return dao.categorias_dao.actualizar_categoria(
            id_categoria, nombre, descripcion
        )

    def desactivar_categoria(self, id_categoria):
        return dao.categorias_dao.desactivar_categoria(
            id_categoria
        )

    def activar_categoria(self, id_categoria):
        return dao.categorias_dao.activar_categoria(
            id_categoria
        )
