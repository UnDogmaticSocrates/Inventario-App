import customtkinter as ctk


class AgregarProductoView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        productos_controller,
        unidades_controller,
        navegacion_controller
    ):
        super().__init__(master)

        self.productos_controller = productos_controller
        self.unidades_controller = unidades_controller
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

        unidades = self.unidades_controller.obtener_unidades()
        self.unidades_disponibles = {
            nombre: id_unidad
            for id_unidad, nombre in unidades
        }

        self.unidad_selector = ctk.CTkComboBox(
            self,
            values=list(self.unidades_disponibles.keys()),
            state="readonly"
        )

        self.unidad_selector.pack(pady=5)

        if unidades:
            
            self.unidad_selector.set(unidades[0][1])  # Establece la primera unidad como seleccionada por defecto
        else:
            self.unidad_selector.set("No hay unidades disponibles")
            self.unidad_selector.configure(state="disabled")

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

        codigo = self.codigo_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        precio_texto = self.precio_entry.get().strip()
        stock_texto = self.stock_entry.get().strip()
        ubicacion = self.ubicacion_entry.get().strip()

        # Validar campos obligatorios
        if not codigo or not nombre or not precio_texto or not stock_texto:
            self.mostrar_mensaje(
                "Campos obligatorios",
                "Completa el código, nombre, precio y stock."
            )
            return

        # Verificar que haya unidades disponibles
        if not self.unidades_disponibles:
            self.mostrar_mensaje(
                "Sin unidades",
                "Primero debes registrar una unidad en Configurar unidades."
            )
            return

        # Obtener el ID real de la unidad seleccionada
        nombre_unidad = self.unidad_selector.get()
        unidad_id = self.unidades_disponibles.get(nombre_unidad)

        if unidad_id is None:
            self.mostrar_mensaje(
                "Unidad inválida",
                "Selecciona una unidad válida."
            )
            return

        # Validar y convertir los valores numéricos
        try:
            precio = float(precio_texto)
            stock = float(stock_texto)

            if precio < 0 or stock < 0:
                raise ValueError

        except ValueError:
            self.mostrar_mensaje(
                "Valores inválidos",
                "El precio y el stock deben ser números válidos y no negativos."
            )
            return

        # Crear el producto
        resultado = self.productos_controller.crear_producto(
            codigo,
            nombre,
            precio,
            stock,
            unidad_id,
            ubicacion
        )

        if resultado:

            self.codigo_entry.delete(0, "end")
            self.nombre_entry.delete(0, "end")
            self.precio_entry.delete(0, "end")
            self.stock_entry.delete(0, "end")
            self.ubicacion_entry.delete(0, "end")

            self.mostrar_mensaje(
                "Producto agregado",
                f"El producto '{nombre}' se agregó correctamente."
            )


    def mostrar_mensaje(self, titulo, mensaje):

        ventana = ctk.CTkToplevel(self)

        ventana.title(titulo)
        ventana.geometry("350x160")
        ventana.resizable(False, False)

        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        etiqueta = ctk.CTkLabel(
            ventana,
            text=mensaje,
            wraplength=300
        )
        etiqueta.pack(pady=25, padx=15)

        boton_aceptar = ctk.CTkButton(
            ventana,
            text="Aceptar",
            command=ventana.destroy
        )
        boton_aceptar.pack(pady=10)
        