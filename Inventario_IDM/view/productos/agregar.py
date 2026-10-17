import math
import customtkinter as ctk
from tkinter import messagebox


class AgregarProductoView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        productos_controller,
        unidades_controller,
        categorias_controller,
        navegacion_controller,
        producto_id=None
    ):
        super().__init__(master)

        self.productos_controller = productos_controller
        self.unidades_controller = unidades_controller
        self.categorias_controller = categorias_controller
        self.navegacion_controller = navegacion_controller
        self.producto_id = producto_id

        self.unidades_disponibles = {}
        self.categorias_disponibles = {}

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
            self, placeholder_text="Código de producto"
        )
        self.codigo_entry.pack(pady=5)

        self.nombre_entry = ctk.CTkEntry(
            self, placeholder_text="Nombre"
        )
        self.nombre_entry.pack(pady=5)

        # Categorías disponibles
        categorias = self.categorias_controller.obtener_categorias()

        self.categorias_disponibles = {
            nombre: id_categoria
            for id_categoria, nombre, descripcion in categorias
        }

        self.categoria_selector = ctk.CTkComboBox(
            self,
            values=list(self.categorias_disponibles.keys()),
            state="readonly"
        )
        self.categoria_selector.pack(pady=5)

        if categorias:
            self.categoria_selector.set(categorias[0][1])
        else:
            self.categoria_selector.set("Registra una categoría primero")
            self.categoria_selector.configure(state="disabled")

        # Precio
        self.precio_entry = ctk.CTkEntry(
            self, placeholder_text="Precio"
        )
        self.precio_entry.pack(pady=5)

        # Unidades disponibles
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
            self.unidad_selector.set("Registra una unidad primero")
            self.unidad_selector.configure(state="disabled")

        self.ubicacion_entry = ctk.CTkEntry(
            self, placeholder_text="Ubicación (ej. B1C3)"
        )
        self.ubicacion_entry.pack(pady=5)
        
        # Existencia inicial: solo se solicita al crear productos.
        self.cantidad_inicial_entry = None
        self.omitir_existencia_var = None

        if not es_edicion:
            ctk.CTkLabel(
                self,
                text="Existencia inicial",
                font=("Arial", 14, "bold")
            ).pack(pady=(12, 3))

            self.cantidad_inicial_entry = ctk.CTkEntry(
                self,
                placeholder_text="Cantidad inicial"
            )
            self.cantidad_inicial_entry.pack(pady=5)
            self.cantidad_inicial_entry.insert(0, "0")

            self.omitir_existencia_var = ctk.BooleanVar(value=False)

            self.omitir_existencia_checkbox = ctk.CTkCheckBox(
                self,
                text="Omitir existencia inicial",
                variable=self.omitir_existencia_var,
                command=self.actualizar_campo_existencia
            )
            self.omitir_existencia_checkbox.pack(pady=5)


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

            # id, codigo, nombre, precio, stock, unidad_id,
            # ubicacion, categoria_id, proveedor_id, activo

            self.codigo_entry.insert(0, producto[1] or "")
            self.nombre_entry.insert(0, producto[2] or "")
            self.precio_entry.insert(0, str(producto[3]))

            categoria_id = producto[7]
            for nombre, id_categoria in self.categorias_disponibles.items():
                if id_categoria == categoria_id:
                    self.categoria_selector.set(nombre)
                    break

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
        ubicacion = self.ubicacion_entry.get().strip()

        if not codigo or not nombre or not precio_texto:
            messagebox.showwarning(
                "Campos obligatorios",
                "Completa el código, nombre y precio.",
                parent=self
            )
            return

        categoria_id = self.categorias_disponibles.get(
            self.categoria_selector.get()
        )
        unidad_id = self.unidades_disponibles.get(
            self.unidad_selector.get()
        )

        if categoria_id is None:
            messagebox.showwarning(
                "Categoría inválida",
                "Registra y selecciona una categoría válida.",
                parent=self
            )
            return

        if unidad_id is None:
            messagebox.showwarning(
                "Unidad inválida",
                "Registra y selecciona una unidad válida.",
                parent=self
            )
            return

        try:
            precio = float(precio_texto)
            if not math.isfinite(precio) or precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Precio inválido",
                "El precio debe ser un número válido y no negativo.",
                parent=self
            )
            return
        
        
        cantidad_inicial = None
        registrar_existencia_inicial = False

        if self.producto_id is None:
            registrar_existencia_inicial = (
                not self.omitir_existencia_var.get()
            )

            if registrar_existencia_inicial:
                cantidad_texto = (
                    self.cantidad_inicial_entry.get().strip()
                )

                try:
                    cantidad_inicial = float(cantidad_texto)

                    if (
                        not math.isfinite(cantidad_inicial)
                        or cantidad_inicial < 0
                    ):
                        raise ValueError

                except ValueError:
                    messagebox.showwarning(
                        "Cantidad inválida",
                        "La existencia inicial debe ser un número "
                        "válido y no negativo.",
                        parent=self
                    )
                    return


        try:
            if self.producto_id is None:
                resultado = self.productos_controller.crear_producto(
                    codigo,
                    nombre,
                    precio,
                    unidad_id,
                    ubicacion,
                    categoria_id,
                    cantidad_inicial,
                    registrar_existencia_inicial
                )
                accion = "agregó"
            else:
                resultado = self.productos_controller.actualizar_producto(
                    self.producto_id,
                    codigo,
                    nombre,
                    precio,
                    unidad_id,
                    ubicacion,
                    categoria_id
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
                f"No fue posible guardar el producto.\n\nDetalle: {error}",
                parent=self
            )

    
    def actualizar_campo_existencia(self):
        if self.omitir_existencia_var.get():
            self.cantidad_inicial_entry.configure(state="disabled")
        else:
            self.cantidad_inicial_entry.configure(state="normal")
    