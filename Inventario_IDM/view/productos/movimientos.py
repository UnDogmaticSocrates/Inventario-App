
import customtkinter as ctk
from tkinter import messagebox


class MovimientosView(ctk.CTkFrame):

    def __init__(self, master, productos_controller, navegacion_controller):
        super().__init__(master)

        self.productos_controller = productos_controller
        self.navegacion_controller = navegacion_controller
        self.productos = []

        ctk.CTkLabel(
            self,
            text="Movimientos de inventario",
            font=("Arial", 24, "bold")
        ).pack(pady=(20, 15))

        ctk.CTkLabel(self, text="Producto").pack(pady=(5, 2))

        self.producto_combo = ctk.CTkComboBox(
            self,
            values=["Cargando productos"],
            command=self.actualizar_stock
        )
        self.producto_combo.pack(pady=5)

        self.stock_label = ctk.CTkLabel(
            self,
            text="Existencia actual: --"
        )
        self.stock_label.pack(pady=8)

        ctk.CTkLabel(self, text="Tipo de movimiento").pack(pady=(10, 2))

        self.tipo_combo = ctk.CTkComboBox(
            self,
            values=["entrada", "salida", "ajuste"]
        )
        self.tipo_combo.set("entrada")
        self.tipo_combo.pack(pady=5)
        self.tipo_combo.configure(command=self.actualizar_etiqueta_cantidad)

        self.cantidad_label = ctk.CTkLabel(
            self,
            text="Cantidad"
        )
        self.cantidad_label.pack(pady=(10, 2))

        self.cantidad_entry = ctk.CTkEntry(
            self,
            placeholder_text="Ej. 5 o 2.5"
        )
        self.cantidad_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Motivo").pack(pady=(10, 2))

        self.motivo_entry = ctk.CTkEntry(
            self,
            placeholder_text="Ej. Compra, consumo o conteo físico"
        )
        self.motivo_entry.pack(pady=5)

        ctk.CTkButton(
            self,
            text="Registrar movimiento",
            command=self.guardar_movimiento
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Ver historial",
            command=self.ver_historial
        ).pack(pady=5)

        self.cargar_productos()

    def cargar_productos(self):
        self.productos = self.productos_controller.obtener_productos()

        if not self.productos:
            self.producto_combo.configure(values=["Sin productos activos"])
            self.producto_combo.set("Sin productos activos")
            return

        valores = [
            f"{producto[0]} | {producto[2]}"
            for producto in self.productos
        ]

        self.producto_combo.configure(values=valores)
        self.producto_combo.set(valores[0])
        self.actualizar_stock(valores[0])

    def obtener_id_producto(self):
        seleccionado = self.producto_combo.get()

        try:
            return int(seleccionado.split("|")[0].strip())
        except (ValueError, IndexError):
            return None

    def actualizar_stock(self, _=None):
        id_producto = self.obtener_id_producto()

        if id_producto is None:
            self.stock_label.configure(text="Existencia actual: --")
            return

        producto = self.productos_controller.obtener_producto_por_id(
            id_producto
        )

        if producto:
            self.stock_label.configure(
                text=f"Existencia actual: {producto[4]:g}"
            )

    def actualizar_etiqueta_cantidad(self, tipo):
        if tipo == "ajuste":
            texto = "Existencia física contada"
        else:
            texto = "Cantidad"

        self.cantidad_label.configure(text=texto)

    def guardar_movimiento(self):
        id_producto = self.obtener_id_producto()

        if id_producto is None:
            messagebox.showwarning(
                "Producto requerido",
                "Selecciona un producto válido.",
                parent=self
            )
            return

        cantidad_texto = self.cantidad_entry.get().strip()

        try:
            cantidad = float(cantidad_texto)
        except ValueError:
            messagebox.showwarning(
                "Cantidad inválida",
                "Introduce una cantidad numérica.",
                parent=self
            )
            return

        tipo = self.tipo_combo.get()
        motivo = self.motivo_entry.get().strip() or None

        try:
            self.productos_controller.registrar_movimiento(
                id_producto, tipo, cantidad, motivo
            )
        except (ValueError, TypeError) as error:
            messagebox.showwarning(
                "Movimiento no registrado",
                str(error),
                parent=self
            )
            return
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo registrar el movimiento:\n{error}",
                parent=self
            )
            return

        messagebox.showinfo(
            "Movimiento registrado",
            "El inventario se actualizó correctamente.",
            parent=self
        )

        self.cantidad_entry.delete(0, "end")
        self.motivo_entry.delete(0, "end")
        self.actualizar_stock()

    def ver_historial(self):
        id_producto = self.obtener_id_producto()

        if id_producto is None:
            messagebox.showwarning(
                "Producto requerido",
                "Selecciona un producto válido.",
                parent=self
            )
            return

        historial = self.productos_controller.obtener_historial_movimientos(
            id_producto
        )

        ventana = ctk.CTkToplevel(self)
        ventana.title("Historial de movimientos")
        ventana.geometry("850x450")

        ctk.CTkLabel(
            ventana,
            text="Historial de movimientos",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        tabla = ctk.CTkScrollableFrame(ventana)
        tabla.pack(fill="both", expand=True, padx=15, pady=10)

        encabezados = (
            "Tipo", "Cantidad/diferencia", "Stock resultante", "Motivo", "Fecha"
        )

        ctk.CTkLabel(
            tabla,
            text=" | ".join(encabezados),
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=5)

        if not historial:
            ctk.CTkLabel(
                tabla,
                text="Este producto no tiene movimientos registrados."
            ).pack(anchor="w", pady=5)
            return

        for movimiento in historial:
            _, tipo, cantidad, stock, motivo, fecha = movimiento

            texto = (
                f"{tipo} | {cantidad:g} | {stock:g} | "
                f"{motivo or '-'} | {fecha}"
            )

            ctk.CTkLabel(
                tabla,
                text=texto,
                anchor="w"
            ).pack(anchor="w", pady=3)
