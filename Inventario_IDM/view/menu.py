import customtkinter as ctk

class MenuView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.crear_interfaz()

    def crear_interfaz(self):
        self.label = ctk.CTkLabel(self, text="Menú Principal", font=("Arial", 24))
        self.label.pack(pady=20)

        self.add_productos_button = ctk.CTkButton(self, text="Agregar Productos", command=self.controller.show_agregar_productos)
        self.add_productos_button.pack(pady=10)

        self.del_productos_button = ctk.CTkButton(self, text="Eliminar productos", command=self.controller.show_eliminar_productos)
        self.del_productos_button.pack(pady=10)

        self.where_productos_button = ctk.CTkButton(self, text="Localizar productos", command=self.controller.show_localizar_productos)
        self.where_productos_button.pack(pady=10)

        self.salir_button = ctk.CTkButton(self, text="Salir", command=self.controller.salir)
        self.salir_button.pack(pady=10)