
import customtkinter as ctk
from tkinter import messagebox


class ProductosCriticosView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        controller,
        productos_controller,
        navegacion_controller
    ):
        super().__init__(master)

        self.controller = controller
        self.productos_controller = productos_controller
        self.navegacion_controller = navegacion_controller

        self.productos = []
        self.productos_por_opcion = {}
        self.productos_criticos = []
        self.producto_critico_seleccionado = None

        self.crear_interfaz()
        self.cargar_productos()
        self.cargar_productos_criticos()
        self.cargar_alertas()

    def crear_interfaz(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Encabezado
        encabezado = ctk.CTkFrame(self, fg_color="transparent")
        encabezado.grid(
            row=0, column=0, sticky="ew",
            padx=25, pady=(20, 10)
        )
        encabezado.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="Productos críticos",
            font=("Arial", 26, "bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            encabezado,
            text="Volver al menú",
            width=130,
            command=self.navegacion_controller.mostrar_menu
        ).grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(
            self,
            text=(
                "Administra materiales esenciales, difíciles de conseguir "
                "y sus alertas de inventario."
            ),
            text_color="gray",
            wraplength=850,
            justify="left"
        ).grid(
            row=1, column=0, sticky="w",
            padx=25, pady=(0, 15)
        )

        # Área principal
        principal = ctk.CTkFrame(self, fg_color="transparent")
        principal.grid(
            row=2, column=0, sticky="nsew",
            padx=25, pady=(0, 15)
        )
        principal.grid_columnconfigure(0, weight=1)
        principal.grid_columnconfigure(1, weight=2)
        principal.grid_rowconfigure(0, weight=1)

        # Formulario
        formulario = ctk.CTkFrame(principal)
        formulario.grid(
            row=0, column=0, sticky="nsew",
            padx=(0, 10), pady=0
        )

        ctk.CTkLabel(
            formulario,
            text="Configurar producto",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=15, pady=(15, 12))

        ctk.CTkLabel(
            formulario,
            text="Producto existente"
        ).pack(anchor="w", padx=15)

        self.selector_producto = ctk.CTkComboBox(
            formulario,
            values=["Cargando productos..."],
            command=self.seleccionar_producto
        )
        self.selector_producto.pack(
            fill="x", padx=15, pady=(5, 12)
        )

        ctk.CTkLabel(
            formulario,
            text="Motivo"
        ).pack(anchor="w", padx=15)

        self.selector_motivo = ctk.CTkOptionMenu(
            formulario,
            values=[
                "esencial",
                "dificil_conseguir",
                "ambos"
            ]
        )
        self.selector_motivo.pack(
            fill="x", padx=15, pady=(5, 12)
        )

        ctk.CTkLabel(
            formulario,
            text="Periodicidad del reporte"
        ).pack(anchor="w", padx=15)

        self.selector_frecuencia = ctk.CTkOptionMenu(
            formulario,
            values=[
                "cada_3_dias",
                "semanal",
                "desactivado"
            ]
        )
        self.selector_frecuencia.pack(
            fill="x", padx=15, pady=(5, 12)
        )

        self.checkbox_alertas = ctk.CTkCheckBox(
            formulario,
            text="Activar alertas de stock bajo"
        )
        self.checkbox_alertas.pack(
            anchor="w", padx=15, pady=(5, 15)
        )
        self.checkbox_alertas.select()

        self.boton_guardar = ctk.CTkButton(
            formulario,
            text="Registrar como crítico",
            command=self.guardar_producto_critico
        )
        self.boton_guardar.pack(
            fill="x", padx=15, pady=(0, 8)
        )

        ctk.CTkButton(
            formulario,
            text="Limpiar formulario",
            fg_color="gray",
            hover_color="dim gray",
            command=self.limpiar_formulario
        ).pack(fill="x", padx=15, pady=(0, 15))

        # Tabla y controles
        panel_lista = ctk.CTkFrame(principal)
        panel_lista.grid(
            row=0, column=1, sticky="nsew",
            padx=(10, 0), pady=0
        )
        panel_lista.grid_columnconfigure(0, weight=1)
        panel_lista.grid_rowconfigure(1, weight=1)

        barra = ctk.CTkFrame(
            panel_lista,
            fg_color="transparent"
        )
        barra.grid(
            row=0, column=0, sticky="ew",
            padx=12, pady=12
        )
        barra.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            barra,
            text="Productos registrados",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            barra,
            text="Revisar stock",
            width=115,
            command=self.revisar_stock
        ).grid(row=0, column=1, padx=(5, 0))

        ctk.CTkButton(
            barra,
            text="Actualizar",
            width=90,
            command=self.actualizar_pantalla
        ).grid(row=0, column=2, padx=(5, 0))

        self.lista = ctk.CTkScrollableFrame(panel_lista)
        self.lista.grid(
            row=1, column=0, sticky="nsew",
            padx=12, pady=(0, 12)
        )
        self.lista.grid_columnconfigure(0, weight=1)

        # Alertas pendientes
        panel_alertas = ctk.CTkFrame(self)
        panel_alertas.grid(
            row=3, column=0, sticky="ew",
            padx=25, pady=(0, 20)
        )
        panel_alertas.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel_alertas,
            text="Alertas pendientes",
            font=("Arial", 17, "bold")
        ).grid(
            row=0, column=0, sticky="w",
            padx=15, pady=(12, 5)
        )

        self.lista_alertas = ctk.CTkScrollableFrame(
            panel_alertas,
            height=100
        )
        self.lista_alertas.grid(
            row=1, column=0, sticky="ew",
            padx=12, pady=(0, 12)
        )
        self.lista_alertas.grid_columnconfigure(0, weight=1)

    def cargar_productos(self):
        self.productos = self.productos_controller.obtener_productos()
        self.productos_por_opcion = {}

        opciones = []

        for producto in self.productos:
            producto_id = producto[0]
            codigo = producto[1]
            nombre = producto[2]

            opcion = f"{codigo} | {nombre} (ID: {producto_id})"
            opciones.append(opcion)
            self.productos_por_opcion[opcion] = producto_id

        if opciones:
            self.selector_producto.configure(values=opciones)
            self.selector_producto.set(opciones[0])
        else:
            self.selector_producto.configure(
                values=["No hay productos disponibles"]
            )
            self.selector_producto.set("No hay productos disponibles")

    def seleccionar_producto(self, opcion):
        producto_id = self.productos_por_opcion.get(opcion)

        if producto_id is None:
            return

        producto_critico = (
            self.controller.obtener_producto_critico_por_producto_id(
                producto_id
            )
        )

        if producto_critico:
            self.cargar_en_formulario(producto_id, producto_critico)
        else:
            self.producto_critico_seleccionado = None
            self.selector_motivo.set("esencial")
            self.selector_frecuencia.set("semanal")
            self.checkbox_alertas.select()
            self.boton_guardar.configure(
                text="Registrar como crítico"
            )

    def cargar_en_formulario(self, producto_id, registro):
        self.producto_critico_seleccionado = producto_id

        # Columnas de productos_criticos:
        # 0 id, 1 producto_id, 2 motivo, 3 frecuencia,
        # 4 alertas_activas, 5 activo, 6 fecha_creacion.
        self.selector_motivo.set(registro[2])
        self.selector_frecuencia.set(registro[3])

        if registro[4]:
            self.checkbox_alertas.select()
        else:
            self.checkbox_alertas.deselect()

        self.boton_guardar.configure(
            text="Guardar cambios"
        )

    def guardar_producto_critico(self):
        opcion = self.selector_producto.get()
        producto_id = self.productos_por_opcion.get(opcion)

        if producto_id is None:
            messagebox.showwarning(
                "Producto requerido",
                "Selecciona un producto existente."
            )
            return

        motivo = self.selector_motivo.get()
        frecuencia = self.selector_frecuencia.get()
        alertas_activas = bool(self.checkbox_alertas.get())

        try:
            existente = (
                self.controller
                .obtener_producto_critico_por_producto_id(producto_id)
            )

            if existente is None:
                self.controller.crear_producto_critico(
                    producto_id=producto_id,
                    motivo=motivo,
                    frecuencia_reporte=frecuencia,
                    alertas_activas=alertas_activas
                )
                mensaje = "El producto se registró como crítico."

            else:
                resultado = self.controller.actualizar_producto_critico(
                    producto_id=producto_id,
                    motivo=motivo,
                    frecuencia_reporte=frecuencia,
                    alertas_activas=alertas_activas,
                    activo=True
                )

                if not resultado:
                    messagebox.showerror(
                        "Error",
                        "No se pudo actualizar el producto crítico."
                    )
                    return

                mensaje = "Se actualizaron los datos del producto crítico."

            self.producto_critico_seleccionado = producto_id
            self.cargar_productos_criticos()
            self.cargar_alertas()

            self.boton_guardar.configure(
                text="Guardar cambios"
            )

            messagebox.showinfo("Productos críticos", mensaje)

        except Exception as error:
            messagebox.showerror(
                "No se pudo guardar",
                f"Ocurrió un error al guardar el producto crítico:\n{error}"
            )

    def cargar_productos_criticos(self):
        for widget in self.lista.winfo_children():
            widget.destroy()

        self.productos_criticos = (
            self.controller.obtener_productos_criticos(
                solo_activos=True
            )
        )

        if not self.productos_criticos:
            ctk.CTkLabel(
                self.lista,
                text="Todavía no hay productos críticos registrados.",
                text_color="gray"
            ).grid(row=0, column=0, padx=10, pady=15, sticky="w")
            return

        for fila, producto in enumerate(self.productos_criticos):
            (
                registro_id,
                producto_id,
                codigo,
                nombre,
                descripcion,
                stock,
                stock_minimo,
                unidad_id,
                unidad,
                motivo,
                frecuencia,
                alertas_activas,
                activo,
                fecha
            ) = producto

            tarjeta = ctk.CTkFrame(self.lista)
            tarjeta.grid(
                row=fila, column=0, sticky="ew",
                padx=3, pady=5
            )
            tarjeta.grid_columnconfigure(0, weight=1)

            unidad_texto = unidad or "sin unidad"

            ctk.CTkLabel(
                tarjeta,
                text=f"{codigo} · {nombre}",
                font=("Arial", 15, "bold"),
                anchor="w"
            ).grid(
                row=0, column=0, sticky="ew",
                padx=10, pady=(8, 2)
            )

            ctk.CTkLabel(
                tarjeta,
                text=(
                    f"Motivo: {motivo} | Reporte: {frecuencia}\n"
                    f"Stock: {stock:g} {unidad_texto} | "
                    f"Mínimo: {stock_minimo:g} {unidad_texto}\n"
                    f"Alertas: {'activas' if alertas_activas else 'desactivadas'}"
                ),
                anchor="w",
                justify="left",
                text_color="gray"
            ).grid(
                row=1, column=0, sticky="ew",
                padx=10, pady=(0, 8)
            )

            acciones = ctk.CTkFrame(
                tarjeta,
                fg_color="transparent"
            )
            acciones.grid(
                row=0, column=1, rowspan=2,
                padx=8, pady=8
            )

            ctk.CTkButton(
                acciones,
                text="Editar",
                width=75,
                command=lambda pid=producto_id: self.editar_producto(pid)
            ).pack(pady=(0, 5))

            ctk.CTkButton(
                acciones,
                text="Desactivar",
                width=75,
                fg_color="gray",
                hover_color="dim gray",
                command=lambda pid=producto_id: self.desactivar_producto(pid)
            ).pack()

    def editar_producto(self, producto_id):
        for opcion, pid in self.productos_por_opcion.items():
            if pid == producto_id:
                self.selector_producto.set(opcion)
                break

        registro = self.controller.obtener_producto_critico_por_producto_id(
            producto_id
        )

        if registro is None:
            messagebox.showwarning(
                "Registro no encontrado",
                "Este producto ya no está registrado como crítico."
            )
            self.cargar_productos_criticos()
            return

        self.cargar_en_formulario(producto_id, registro)

    def desactivar_producto(self, producto_id):
        confirmar = messagebox.askyesno(
            "Desactivar producto crítico",
            "¿Deseas desactivar este producto crítico?\n"
            "El producto seguirá existiendo en el inventario."
        )

        if not confirmar:
            return

        resultado = self.controller.desactivar_producto_critico(
            producto_id
        )

        if resultado:
            self.limpiar_formulario()
            self.cargar_productos_criticos()
            self.cargar_alertas()
            messagebox.showinfo(
                "Productos críticos",
                "El producto dejó de estar en la lista de críticos."
            )
        else:
            messagebox.showwarning(
                "Sin cambios",
                "No se encontró un registro activo para desactivar."
            )

    def revisar_stock(self):
        try:
            resultado = self.controller.revisar_stock_productos_criticos()

            self.cargar_productos_criticos()
            self.cargar_alertas()

            messagebox.showinfo(
                "Revisión terminada",
                "Productos revisados: "
                f"{resultado['revisados']}\n"
                "Alertas creadas: "
                f"{resultado['alertas_creadas']}\n"
                "Alertas actualizadas: "
                f"{resultado['alertas_actualizadas']}\n"
                "Alertas resueltas: "
                f"{resultado['alertas_resueltas']}"
            )

        except Exception as error:
            messagebox.showerror(
                "Error en la revisión",
                f"No se pudo revisar el stock:\n{error}"
            )

    def cargar_alertas(self):
        for widget in self.lista_alertas.winfo_children():
            widget.destroy()

        alertas = self.controller.obtener_alertas_pendientes()

        if not alertas:
            ctk.CTkLabel(
                self.lista_alertas,
                text="No hay alertas pendientes.",
                text_color="gray"
            ).grid(row=0, column=0, sticky="w", padx=8, pady=8)
            return

        for fila, alerta in enumerate(alertas):
            (
                alerta_id,
                producto_id,
                codigo,
                nombre,
                stock,
                stock_minimo,
                fecha,
                estado
            ) = alerta

            renglon = ctk.CTkFrame(self.lista_alertas)
            renglon.grid(
                row=fila, column=0, sticky="ew",
                padx=3, pady=4
            )
            renglon.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                renglon,
                text=(
                    f"{codigo} · {nombre}: stock {stock:g}, "
                    f"mínimo {stock_minimo:g} · {fecha}"
                ),
                anchor="w",
                wraplength=550
            ).grid(
                row=0, column=0, sticky="ew",
                padx=8, pady=8
            )

            ctk.CTkButton(
                renglon,
                text="Resolver",
                width=85,
                command=lambda aid=alerta_id: self.resolver_alerta(aid)
            ).grid(row=0, column=1, padx=8, pady=5)

    def resolver_alerta(self, alerta_id):
        if not messagebox.askyesno(
            "Resolver alerta",
            "¿Marcar esta alerta como resuelta?"
        ):
            return

        resultado = self.controller.resolver_alerta(alerta_id)

        if resultado:
            self.cargar_alertas()
            messagebox.showinfo(
                "Alertas",
                "La alerta se marcó como resuelta."
            )

    def limpiar_formulario(self):
        self.producto_critico_seleccionado = None

        if self.productos_por_opcion:
            primera_opcion = next(iter(self.productos_por_opcion))
            self.selector_producto.set(primera_opcion)

        self.selector_motivo.set("esencial")
        self.selector_frecuencia.set("semanal")
        self.checkbox_alertas.select()
        self.boton_guardar.configure(
            text="Registrar como crítico"
        )

    def actualizar_pantalla(self):
        self.cargar_productos()
        self.cargar_productos_criticos()
        self.cargar_alertas()
