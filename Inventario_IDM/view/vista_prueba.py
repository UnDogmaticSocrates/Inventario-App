import customtkinter as ctk


class VistaPrueba(ctk.CTkFrame):

    def __init__(self, master, controller, titulo):
        super().__init__(master)

        self.controller = controller
        self.titulo = titulo

        self.crear_interfaz()

    def crear_interfaz(self):

        self.label = ctk.CTkLabel(
            self,
            text=self.titulo,
            font=("Arial", 24)
        )
        self.label.pack(pady=30)

        self.regresar_button = ctk.CTkButton(
            self,
            text="Regresar al menú",
            command=self.controller.mostrar_menu
        )
        self.regresar_button.pack(pady=10)