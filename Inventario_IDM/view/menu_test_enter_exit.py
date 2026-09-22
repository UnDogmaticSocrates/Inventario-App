import customtkinter as ctk


class MenuView(ctk.CTkFrame):

    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        self.crear_interfaz()

    def crear_interfaz(self):

        self.label = ctk.CTkLabel(
            self,
            text="Menú Principal",
            font=("Arial", 24)
        )
        self.label.pack(pady=20)

        self.salir_button = ctk.CTkButton(
            self,
            text="Salir",
            command=self.controller.salir
        )
        self.salir_button.pack(pady=10)