
import customtkinter as ctk
from tkinter import ttk, messagebox


class CatalogoProductosView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        productos_controller,
        unidades_controller,
        categorias_controller,
        navegacion_controller
    ):
        super().__init__(master)

        self.productos_controller = productos_controller
        self.unidades_controller = unidades_controller
        self.categorias_controller = categorias_controller
        self.navegacion_controller = navegacion_controller

        self.productos = []
        self.unidades = {}
        self.categorias = {}

        self.crear_interfaz()
        self.cargar_productos()

    def crear_interfaz(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Encabezado
        encabezado = ctk.CTkFrame(self, fg_color="transparent")
        encabezado.grid(
            row=0, column=0, sticky="ew",
            padx=30, pady=(25, 10)
        )
        encabezado.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="Catálogo de productos",
            font=("Arial", 26, "bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            encabezado,
            text="+ Agregar producto",
            width=160,
            height=38,
            command=self.navegacion_controller.mostrar_agregar_producto
        ).grid(row=0, column=1, padx=(10, 0))

        # Búsqueda
        barra_busqueda = ctk.CTkFrame(self, fg_color="transparent")
        barra_busqueda.grid(
            row=1, column=0, sticky="ew",
            padx=30, pady=10
        )
        barra_busqueda.grid_columnconfigure(0, weight=1)

        self.busqueda_entry = ctk.CTkEntry(
            barra_busqueda,
            placeholder_text="Buscar por código, nombre o categoría..."
        )
        self.busqueda_entry.grid(
            row=0, column=0, sticky="ew", padx=(0, 10)
        )
        self.busqueda_entry.bind(
            "<KeyRelease>", self.filtrar_productos
        )

        ctk.CTkButton(
            barra_busqueda,
            text="Actualizar",
            width=110,
            command=self.cargar_productos
        ).grid(row=0, column=1)

        # Tabla
        tabla_frame = ctk.CTkFrame(self)
        tabla_frame.grid(
            row=2, column=0, sticky="nsew",
            padx=30, pady=10
        )
        tabla_frame.grid_columnconfigure(0, weight=1)
        tabla_frame.grid_rowconfigure(0, weight=1)

        columnas = (
            "codigo", "nombre", "categoria", "precio",
            "stock", "unidad", "ubicacion"
        )

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        encabezados = {
            "codigo": "Código",
            "nombre": "Producto",
            "categoria": "Categoría",
            "precio": "Precio",
            "stock": "Existencia",
            "unidad": "Unidad",
            "ubicacion": "Ubicación"
        }

        anchos = {
            "codigo": 110,
            "nombre": 190,
            "categoria": 150,
            "precio": 90,
            "stock": 90,
            "unidad": 100,
            "ubicacion": 130
        }

        for columna in columnas:
            self.tabla.heading(
                columna, text=encabezados[columna]
            )
            self.tabla.column(
                columna,
                width=anchos[columna],
                anchor="w"
            )

        scroll = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

                # Panel de detalles del producto seleccionado
        self.detalles_frame = ctk.CTkFrame(self)
        self.detalles_frame.grid(
            row=3, column=0, sticky="ew",
            padx=30, pady=(5, 10)
        )
        self.detalles_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.detalles_frame,
            text="Detalles del producto seleccionado",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

        self.descripcion_label = ctk.CTkLabel(
            self.detalles_frame,
            text="Selecciona un producto para ver sus especificaciones.",
            justify="left",
            anchor="w",
            wraplength=800      
        )
        self.descripcion_label.grid(
            row=1, column=0, sticky="ew",
            padx=15, pady=(0, 10)
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.mostrar_detalles_producto
        )

        # Acciones
        acciones = ctk.CTkFrame(self, fg_color="transparent")
        acciones.grid(
            row=3, column=0, sticky="ew",
            padx=30, pady=(5, 5)
        )

        ctk.CTkButton(
            acciones,
            text="Editar producto",
            command=self.editar_producto
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            acciones,
            text="Desactivar producto",
            fg_color="#A83232",
            hover_color="#812525",
            command=self.desactivar_producto
        ).pack(side="left")
        
        ctk.CTkButton(
            acciones,
            text="Productos desactivados",
            command=self.mostrar_productos_desactivados
        ).pack(side="left", padx=(10, 0))

        # Pie
        pie = ctk.CTkFrame(self, fg_color="transparent")
        pie.grid(
            row=4, column=0, sticky="ew",
            padx=30, pady=(5, 20)
        )
        pie.grid_columnconfigure(0, weight=1)

        self.total_label = ctk.CTkLabel(
            pie, text="Productos mostrados: 0"
        )
        self.total_label.grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            pie,
            text="Regresar al menú",
            width=140,
            command=self.navegacion_controller.mostrar_menu
        ).grid(row=0, column=1, sticky="e")

    def cargar_productos(self):
        try:
            self.productos = (
                self.productos_controller.obtener_productos()
            )

            unidades = self.unidades_controller.obtener_unidades()
            self.unidades = {
                id_unidad: nombre
                for id_unidad, nombre in unidades
            }

            categorias = (
                self.categorias_controller.obtener_categorias()
            )
            self.categorias = {
                id_categoria: nombre
                for id_categoria, nombre, descripcion in categorias
            }

            self.filtrar_productos()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible cargar el catálogo.\n\n{error}",
                parent=self
            )

    def filtrar_productos(self, evento=None):
        texto = self.busqueda_entry.get().strip().lower()

        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        total = 0

        for producto in self.productos:
            # id, codigo, nombre, precio, stock,
            # unidad_id, ubicacion, categoria_id,
            # proveedor_id, activo
            if len(producto) < 10:
                continue

            id_producto = producto[0]
            codigo = producto[1] or ""
            nombre = producto[2] or ""
            precio = producto[3]
            stock = producto[4]
            unidad_id = producto[5]
            ubicacion = producto[6] or ""
            categoria_id = producto[7]

            nombre_unidad = self.unidades.get(
                unidad_id, "Sin unidad"
            )
            nombre_categoria = self.categorias.get(
                categoria_id, "Sin categoría"
            )

            descripcion = producto[11] or ""

            if texto not in (
                f"{codigo} {nombre} {nombre_categoria} {descripcion}".lower()
            ):
                continue

            self.tabla.insert(
                "",
                "end",
                iid=str(id_producto),
                values=(
                    codigo,
                    nombre,
                    nombre_categoria,
                    precio,
                    stock,
                    nombre_unidad,
                    ubicacion
                )
            )

            total += 1

        self.total_label.configure(
            text=f"Productos mostrados: {total}"
        )

    def obtener_id_seleccionado(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selecciona un producto",
                "Primero selecciona un producto de la tabla.",
                parent=self
            )
            return None

        return int(seleccion[0])

    def editar_producto(self):
        id_producto = self.obtener_id_seleccionado()

        if id_producto is None:
            return

        self.navegacion_controller.mostrar_agregar_producto(
            producto_id=id_producto
        )

    def desactivar_producto(self):
        id_producto = self.obtener_id_seleccionado()

        if id_producto is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar desactivación",
            "El producto dejará de aparecer en el catálogo activo.\n"
            "El registro se conservará en la base de datos.\n\n"
            "¿Deseas continuar?",
            parent=self
        )

        if not confirmar:
            return

        try:
            resultado = (
                self.productos_controller.desactivar_producto(
                    id_producto
                )
            )

            if resultado:
                messagebox.showinfo(
                    "Producto desactivado",
                    "El producto se desactivó correctamente.",
                    parent=self
                )

            else:
                messagebox.showwarning(
                    "Sin cambios",
                    "El producto ya no está activo o no existe.",
                    parent=self
                )

            self.cargar_productos()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible desactivar el producto.\n\n{error}",
                parent=self
            )

    
    def mostrar_productos_desactivados(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Productos desactivados")
        ventana.geometry("850x450")
        ventana.transient(self.winfo_toplevel())

        ventana.grid_columnconfigure(0, weight=1)
        ventana.grid_rowconfigure(0, weight=1)

        columnas = ("codigo", "nombre", "stock", "unidad", "categoria")

        tabla = ttk.Treeview(
            ventana,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        encabezados = {
            "codigo": "Código",
            "nombre": "Producto",
            "stock": "Existencia",
            "unidad": "Unidad",
            "categoria": "Categoría"
        }

        anchos = {
            "codigo": 100,
            "nombre": 220,
            "stock": 100,
            "unidad": 120,
            "categoria": 180
        }

        for columna in columnas:
            tabla.heading(columna, text=encabezados[columna])
            tabla.column(columna, width=anchos[columna], anchor="w")

        tabla.grid(
            row=0, column=0, columnspan=2,
            sticky="nsew", padx=15, pady=15
        )

        ctk.CTkButton(
            ventana,
            text="Reactivar producto",
            command=lambda: self.reactivar_producto(ventana, tabla)
        ).grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")

        ctk.CTkButton(
            ventana,
            text="Actualizar lista",
            command=lambda: self.cargar_productos_desactivados(tabla)
        ).grid(row=1, column=1, padx=15, pady=(0, 15), sticky="e")

        self.cargar_productos_desactivados(tabla)


    def cargar_productos_desactivados(self, tabla):
        try:
            productos = (
                self.productos_controller.obtener_productos_desactivados()
            )

            for elemento in tabla.get_children():
                tabla.delete(elemento)

            for producto in productos:
                # id, codigo, nombre, precio, stock,
                # unidad_id, ubicacion, categoria_id,
                # proveedor_id, activo
                if len(producto) < 10:
                    continue

                id_producto = producto[0]
                codigo = producto[1] or ""
                nombre = producto[2] or ""
                stock = producto[4]
                unidad_id = producto[5]
                categoria_id = producto[7]

                nombre_unidad = self.unidades.get(
                    unidad_id, "Sin unidad"
                )
                nombre_categoria = self.categorias.get(
                    categoria_id, "Sin categoría"
                )

                tabla.insert(
                    "",
                    "end",
                    iid=str(id_producto),
                    values=(
                        codigo,
                        nombre,
                        stock,
                        nombre_unidad,
                        nombre_categoria
                    )
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible cargar los productos desactivados.\n\n{error}",
                parent=tabla.winfo_toplevel()
            )


    def reactivar_producto(self, ventana, tabla):
        seleccion = tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selecciona un producto",
                "Selecciona el producto que deseas reactivar.",
                parent=ventana
            )
            return

        id_producto = int(seleccion[0])

        confirmar = messagebox.askyesno(
            "Confirmar reactivación",
            "¿Deseas reactivar este producto?",
            parent=ventana
        )

        if not confirmar:
            return

        try:
            resultado = self.productos_controller.activar_producto(
                id_producto
            )

            if resultado:
                messagebox.showinfo(
                    "Producto reactivado",
                    "El producto vuelve a estar disponible en el catálogo.",
                    parent=ventana
                )

                self.cargar_productos()
                self.cargar_productos_desactivados(tabla)

            else:
                messagebox.showwarning(
                    "Sin cambios",
                    "El producto ya estaba activo o no existe.",
                    parent=ventana
                )

                self.cargar_productos_desactivados(tabla)

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible reactivar el producto.\n\n{error}",
                parent=ventana
        )

    def mostrar_detalles_producto(self, evento=None):
        seleccion = self.tabla.selection()

        if not seleccion:
            self.descripcion_label.configure(
                text="Selecciona un producto para ver sus especificaciones."
            )
            return

        id_producto = int(seleccion[0])

        producto = next(
            (
                producto for producto in self.productos
                if producto[0] == id_producto
            ),
            None
        )

        if producto is None:
            return

        # descripcion es la columna 11, después de stock_minimo.
        descripcion = producto[11] or "Sin descripción registrada."

        self.descripcion_label.configure(
            text=f"{producto[2]}\n\n{descripcion}"
        )
        