from view.menu import MenuView
from view.productos.agregar import AgregarProductoView
from controles.control_productos import ProductosController
from view.unidades.unidades import UnidadesView
from controles.control_unidades import UnidadesController

class NavegacionController:

    def __init__(self, root):
        self.unidades_controller = UnidadesController()
        self.root = root
        self.vista_actual = None

        self.productos_controller = ProductosController()
        self.mostrar_menu()

    def mostrar_unidades(self):

        self.limpiar_vista()

        self.vista_actual = UnidadesView(
            self.root,
            self.unidades_controller,
            self
        )

        self.vista_actual.pack(
            fill="both",
            expand=True
        )

    def limpiar_vista(self):

        if self.vista_actual is not None:
            self.vista_actual.destroy()

    def mostrar_menu(self):

        self.limpiar_vista()

        self.vista_actual = MenuView(
            self.root,
            self
        )

        self.vista_actual.pack(
            fill="both",
            expand=True
        )

    def mostrar_agregar_producto(self):

        self.limpiar_vista()

        self.vista_actual = AgregarProductoView(
            self.root,
            self.productos_controller,
            self.unidades_controller,
            self
        )

        self.vista_actual.pack(
            fill="both",
            expand=True
        )

    def mostrar_eliminar_producto(self):

       pass  # Implementación pendiente

    def mostrar_localizar_producto(self):

        pass  # Implementación pendiente

    def salir(self):

        self.root.destroy()