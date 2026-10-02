from dao import unidades_dao


class UnidadesController:

    def crear_unidad(self, nombre):

        return unidades_dao.crear_unidad(nombre)

    def obtener_unidades(self):

        return unidades_dao.obtener_unidades()