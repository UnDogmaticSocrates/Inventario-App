from view.menu import MenuView


class NavegacionController:

    def __init__(self, root):
        self.root = root
        self.vista_actual = None

        self.mostrar_menu()

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

    def salir(self):

        self.root.destroy()