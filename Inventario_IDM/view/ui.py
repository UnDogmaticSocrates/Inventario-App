import customtkinter as ctk
from tkinter import ttk


class ProductosView(ctk.CTkFrame):

    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        self.crear_interfaz()
        self.cargar_productos()

    def crear_interfaz(self):

        # -------------------------
        # FORMULARIO
        # -------------------------

        self.codigo_entry = ctk.CTkEntry(
            self,
            placeholder_text= "Código de producto"
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

        # -------------------------
        # BOTONES
        # -------------------------

        self.crear_btn = ctk.CTkButton(
            self,
            text="Agregar producto",
            command=self.crear_producto
        )
        self.crear_btn.pack(pady=5)

        self.actualizar_btn = ctk.CTkButton(
            self,
            text="Actualizar",
            command=self.actualizar_producto
        )
        self.actualizar_btn.pack(pady=5)

        self.eliminar_btn = ctk.CTkButton(
            self,
            text="Eliminar",
            command=self.eliminar_producto
        )
        self.eliminar_btn.pack(pady=5)

        # -------------------------
        # TABLA
        # -------------------------

        self.tabla = ttk.Treeview(
            self,
            columns=("id", "codigo", "nombre", "precio", "stock"),
            show="headings"
        )

        self.tabla.heading("id", text="ID")
        self.tabla.heading("codigo", text = "Código de producto")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("stock", text="Stock")

        self.tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.tabla.bind(
            "<ButtonRelease-1>",
            self.seleccionar_producto
        )

    # -------------------------
    # CRUD
    # -------------------------

    def crear_producto(self):

        codigo = self.codigo_entry.get()
        nombre = self.nombre_entry.get()
        precio = self.precio_entry.get()
        stock = self.stock_entry.get()

        self.controller.crear_producto(
            codigo,
            nombre,
            precio,
            stock
        )

        self.limpiar_formulario()
        self.cargar_productos()

    def cargar_productos(self):

        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        productos = self.controller.obtener_productos()

        for producto in productos:
            self.tabla.insert(
                "",
                "end",
                values=producto
            )

    def seleccionar_producto(self, event):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado)

        valores = datos["values"]

        self.nombre_entry.delete(0, "end")
        self.nombre_entry.insert(0, valores[1])

        self.precio_entry.delete(0, "end")
        self.precio_entry.insert(0, valores[2])

        self.stock_entry.delete(0, "end")
        self.stock_entry.insert(0, valores[3])

    def actualizar_producto(self):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado)
        id_producto = datos["values"][0]

        nombre = self.nombre_entry.get()
        precio = self.precio_entry.get()
        stock = self.stock_entry.get()

        self.controller.actualizar_producto(
            id_producto,
            nombre,
            precio,
            stock
        )

        self.limpiar_formulario()
        self.cargar_productos()

    def eliminar_producto(self):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado)
        id_producto = datos["values"][0]

        self.controller.eliminar_producto(
            id_producto
        )

        self.limpiar_formulario()
        self.cargar_productos()

    def limpiar_formulario(self):

        self.nombre_entry.delete(0, "end")
        self.precio_entry.delete(0, "end")
        self.stock_entry.delete(0, "end")