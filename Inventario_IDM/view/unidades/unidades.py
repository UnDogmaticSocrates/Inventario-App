import customtkinter as ctk


class UnidadesView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        unidades_controller,
        navegacion_controller
    ):
        super().__init__(master)

        self.unidades_controller = unidades_controller
        self.navegacion_controller = navegacion_controller

        self.crear_interfaz()

    def crear_interfaz(self):

        self.titulo = ctk.CTkLabel(
            self,
            text="Configurar unidades",
            font=("Arial", 24)
        )
        self.titulo.pack(pady=20)

        self.nombre_entry = ctk.CTkEntry(
            self,
            placeholder_text="Nombre de la unidad"
        )
        self.nombre_entry.pack(pady=5)

        self.agregar_button = ctk.CTkButton(
            self,
            text="Agregar unidad",
            command=self.agregar_unidad
        )
        self.agregar_button.pack(pady=15)

        unidades = self.unidades_controller.obtener_unidades()

        print(unidades)

        self.regresar_button = ctk.CTkButton(
            self,
            text="Regresar al menú",
            command=self.navegacion_controller.mostrar_menu
        )
        self.regresar_button.pack(pady=10)

    def agregar_unidad(self):

        nombre = self.nombre_entry.get()

        if not nombre:
            print("El nombre de la unidad es obligatorio")
            return

        resultado = self.unidades_controller.crear_unidad(nombre)

        if resultado:

            self.nombre_entry.delete(0, "end")

            print("Unidad agregada correctamente")