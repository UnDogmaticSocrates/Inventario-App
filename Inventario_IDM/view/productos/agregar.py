
import customtkinter as ctk
from tkinter import messagebox


class AgregarProductoView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        productos_controller,
        unidades_controller,
        navegacion_controller,
        producto_id=None
    ):
        super().__init__(master)

        self.productos_controller = productos_controller
        self.unidades_controller = unidades_controller
        self.navegacion_controller = navegacion_controller
        self.producto_id = producto_id

        self.unidades_disponibles = {}

        self.crear_interfaz()

        if self.producto_id is not None:
            self.cargar_producto()

    def crear_interfaz(self):
        es_edicion = self.producto_id is not None

        self.titulo = ctk.CTkLabel(
            self,
            text="Editar producto" if es_edicion else "Agregar producto",
            font=("Arial", 24, "bold")
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
            self.unidad_selector.set(unidades[0][1])
        else:
            self.unidad_selector.set("No hay unidades disponibles")
            self.unidad_selector.configure(state="disabled")

        self.ubicacion_entry = ctk.CTkEntry(
            self,
            placeholder_text="Ubicación (ej. B1C3)"
        )
        self.ubicacion_entry.pack(pady=5)

        self.guardar_button = ctk.CTkButton(
            self,
            text="Guardar cambios" if es_edicion else "Agregar producto",
            command=self.guardar_producto
        )
        self.guardar_button.pack(pady=15)

        self.regresar_button = ctk.CTkButton(
            self,
            text="Regresar al catálogo",
            command=self.navegacion_controller.mostrar_productos
        )
        self.regresar_button.pack(pady=10)

    def cargar_producto(self):
        try:
            producto = (
                self.productos_controller.obtener_producto_por_id(
                    self.producto_id
                )
            )

            if producto is None or producto[9] != 1:
                messagebox.showerror(
                    "Producto no disponible",
                    "El producto no existe o está desactivado.",
                    parent=self
                )
                self.navegacion_controller.mostrar_productos()
                return

            # Orden del registro:
            # id, codigo, nombre, precio, stock,
            # unidad_id, ubicacion, categoria_id,
            # proveedor_id, activo

            self.codigo_entry.insert(0, producto[1] or "")
            self.nombre_entry.insert(0, producto[2] or "")
            self.precio_entry.insert(0, str(producto[3]))
            self.stock_entry.insert(0, str(producto[4]))

            unidad_id = producto[5]
            for nombre, id_unidad in self.unidades_disponibles.items():
                if id_unidad == unidad_id:
                    self.unidad_selector.set(nombre)
                    break

            self.ubicacion_entry.insert(0, producto[6] or "")

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible cargar el producto.\n\n{error}",
                parent=self
            )
            self.navegacion_controller.mostrar_productos()

    def guardar_producto(self):
        codigo = self.codigo_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        precio_texto = self.precio_entry.get().strip()
        stock_texto = self.stock_entry.get().strip()
        ubicacion = self.ubicacion_entry.get().strip()

        if not codigo or not nombre or not precio_texto or not stock_texto:
            messagebox.showwarning(
                "Campos obligatorios",
                "Completa el código, nombre, precio y stock.",
                parent=self
            )
            return

        if not self.unidades_disponibles:
            messagebox.showwarning(
                "Sin unidades",
                "Primero registra una unidad en Configurar unidades.",
                parent=self
            )
            return

        nombre_unidad = self.unidad_selector.get()
        unidad_id = self.unidades_disponibles.get(nombre_unidad)

        if unidad_id is None:
            messagebox.showwarning(
                "Unidad inválida",
                "Selecciona una unidad válida.",
                parent=self
            )
            return

        try:
            precio = float(precio_texto)
            stock = float(stock_texto)

            if precio < 0 or stock < 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Valores inválidos",
                "El precio y el stock deben ser números válidos y no negativos.",
                parent=self
            )
            return

        try:
            if self.producto_id is None:
                resultado = self.productos_controller.crear_producto(
                    codigo,
                    nombre,
                    precio,
                    stock,
                    unidad_id,
                    ubicacion
                )
                accion = "agregó"
            else:
                resultado = self.productos_controller.actualizar_producto(
                    self.producto_id,
                    codigo,
                    nombre,
                    precio,
                    stock,
                    unidad_id,
                    ubicacion
                )
                accion = "actualizó"

            if resultado:
                messagebox.showinfo(
                    "Operación exitosa",
                    f"Se {accion} correctamente el producto '{nombre}'.",
                    parent=self
                )
                self.navegacion_controller.mostrar_productos()
            else:
                messagebox.showwarning(
                    "Sin cambios",
                    "No se encontró un producto activo para modificar.",
                    parent=self
                )

        except Exception as error:
            messagebox.showerror(
                "Error al guardar",
                "No fue posible guardar el producto.\n\n"
                f"Detalle: {error}",
                parent=self
            )

        