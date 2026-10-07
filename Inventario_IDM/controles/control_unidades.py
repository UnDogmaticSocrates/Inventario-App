from dao import unidades_dao


class UnidadesController:

    def crear_unidad(self, nombre):

        return unidades_dao.crear_unidad(nombre)

    def obtener_unidades(self):

        return unidades_dao.obtener_unidades()

    def actualizar_unidad(self, id_unidad, nombre):

        return unidades_dao.actualizar_unidad(
            id_unidad,
            nombre
        )

    def desactivar_unidad(self, id_unidad):

        return unidades_dao.desactivar_unidad(
            id_unidad
        )

    def activar_unidad(self, id_unidad):

        return unidades_dao.activar_unidad(
            id_unidad
        )

if __name__ == "__main__":

    controller = UnidadesController()

    resultado = controller.crear_unidad("kg")

    print(resultado)
    
    resultado = controller.crear_unidad("lt")

    print(resultado)

    resultado = controller.crear_unidad("toneladas")

    print(resultado)