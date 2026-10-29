from view.productos.movimientos import MovimientosView
from view.menu import MenuView
from view.productos.catalogo import CatalogoProductosView
from view.productos.agregar import AgregarProductoView
from view.unidades.unidades import UnidadesView

from controles.control_productos import ProductosController
from controles.control_unidades import UnidadesController

from view.categorias.catalogo import CategoriasView
from controles.control_categorias import CategoriasController

from controles.control_productos_criticos import ProductosCriticosController
from view.productos.criticos import ProductosCriticosView


class NavegacionController:

    def __init__(self, root):
        self.root = root
        self.vista_actual = None

        self.productos_controller = ProductosController()
        self.unidades_controller = UnidadesController()
        self.categorias_controller = CategoriasController()
        self.productos_criticos_controller = ProductosCriticosController()
        self.mostrar_menu()

    def limpiar_vista(self):
        if self.vista_actual is not None:
            self.vista_actual.destroy()
            self.vista_actual = None

    def mostrar_menu(self):
        self.limpiar_vista()

        self.vista_actual = MenuView(self.root, self)
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_productos(self):
        self.limpiar_vista()

        self.vista_actual = CatalogoProductosView(
            self.root,
            self.productos_controller,
            self.unidades_controller,
            self.categorias_controller,
            self
        )
        self.vista_actual.pack(fill="both", expand=True)


    def mostrar_movimientos(self):
            self.limpiar_vista()
    
            self.vista_actual = MovimientosView(
                self.root,
                self.productos_controller,
                self
            )
            self.vista_actual.pack(fill="both", expand=True)

    def mostrar_agregar_producto(self, producto_id=None):
        self.limpiar_vista()

        self.vista_actual = AgregarProductoView(
            self.root,
            self.productos_controller,
            self.unidades_controller,
            self.categorias_controller,
            self,
            producto_id=producto_id
        )
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_unidades(self):
        self.limpiar_vista()

        self.vista_actual = UnidadesView(
            self.root,
            self.unidades_controller,
            self
        )
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_categorias(self):
        self.limpiar_vista()

        self.vista_actual = CategoriasView(
            self.root,
            self.categorias_controller,
            self
        )
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_eliminar_producto(self):
        self.mostrar_productos()

    def mostrar_localizar_producto(self):
        self.mostrar_productos()

    def salir(self):
        self.root.destroy()

    def mostrar_productos_criticos(self):
        self.limpiar_vista()

        self.vista_actual = ProductosCriticosView(
            self.root,
            self.productos_criticos_controller,
            self.productos_controller,
            self
        )
        self.vista_actual.pack(fill="both", expand=True)
