import customtkinter as ctk


class AgregarProductoView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        productos_controller,
        navegacion_controller
    ):
        super().__init__(master)

        self.productos_controller = productos_controller
        self.navegacion_controller = navegacion_controller

        self.crear_interfaz()

    def crear_interfaz(self):

        self.titulo = ctk.CTkLabel(
            self,
            text="Agregar producto",
            font=("Arial", 24)
        )
        self.titulo.pack(pady=20)

        self.codigo_entry = ctk.CTkEntry(
            self,
            placeholder_text="Código de producto"
        )
        self.codigo_entry.pack(pady=5)

        self.nombre_entry = ctk.CTkEntry(
            self,
            placeholder_text="Nombre"
        )
        self.nombre_entry.pack(pady=5)

        self.precio_entry = ctk.CTkEntry(
            self,
            placeholder_text="Precio"
        )
        self.precio_entry.pack(pady=5)

        self.stock_entry = ctk.CTkEntry(
            self,
            placeholder_text="Stock"
        )
        self.stock_entry.pack(pady=5)

        self.ubicacion_entry = ctk.CTkEntry(
            self,
            placeholder_text="Ubicación (ej: B1C3)"
        )
        self.ubicacion_entry.pack(pady=5)

        self.agregar_button = ctk.CTkButton(
            self,
            text="Agregar producto",
            command=self.agregar_producto
        )
        self.agregar_button.pack(pady=15)

        self.regresar_button = ctk.CTkButton(
            self,
            text="Regresar al menú",
            command=self.navegacion_controller.mostrar_menu
        )
        self.regresar_button.pack(pady=10)

    def agregar_producto(self):

        codigo = self.codigo_entry.get()
        nombre = self.nombre_entry.get()
        precio = self.precio_entry.get()
        stock = self.stock_entry.get()
        ubicacion = self.ubicacion_entry.get()

        self.productos_controller.crear_producto(
            codigo,
            nombre,
            precio,
            stock,
            ubicacion
        )