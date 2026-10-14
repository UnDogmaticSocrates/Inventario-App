
import customtkinter as ctk
from tkinter import ttk, messagebox


class CategoriasView(ctk.CTkFrame):

    def __init__(self, master, categorias_controller, navegacion_controller):
        super().__init__(master)

        self.categorias_controller = categorias_controller
        self.navegacion_controller = navegacion_controller

        self.crear_interfaz()
        self.cargar_categorias()

    def crear_interfaz(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        encabezado = ctk.CTkFrame(self, fg_color="transparent")
        encabezado.grid(
            row=0, column=0, sticky="ew",
            padx=30, pady=(25, 15)
        )
        encabezado.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="Categorías",
            font=("Arial", 26, "bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            encabezado,
            text="+ Agregar categoría",
            command=self.agregar_categoria
        ).grid(row=0, column=1, padx=(10, 0))

        tabla_frame = ctk.CTkFrame(self)
        tabla_frame.grid(
            row=1, column=0, sticky="nsew",
            padx=30, pady=10
        )
        tabla_frame.grid_columnconfigure(0, weight=1)
        tabla_frame.grid_rowconfigure(0, weight=1)

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=("nombre", "descripcion"),
            show="headings",
            selectmode="browse"
        )

        self.tabla.heading("nombre", text="Categoría")
        self.tabla.heading("descripcion", text="Descripción")
        self.tabla.column("nombre", width=220)
        self.tabla.column("descripcion", width=450)

        scroll = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

        acciones = ctk.CTkFrame(self, fg_color="transparent")
        acciones.grid(
            row=2, column=0, sticky="ew",
            padx=30, pady=10
        )

        ctk.CTkButton(
            acciones,
            text="Editar",
            command=self.editar_categoria
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            acciones,
            text="Desactivar",
            fg_color="#A83232",
            hover_color="#812525",
            command=self.desactivar_categoria
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            acciones,
            text="Actualizar",
            command=self.cargar_categorias
        ).pack(side="left")

        ctk.CTkButton(
            acciones,
            text="Regresar al menú",
            command=self.navegacion_controller.mostrar_menu
        ).pack(side="right")

    def cargar_categorias(self):
        try:
            for elemento in self.tabla.get_children():
                self.tabla.delete(elemento)

            categorias = (
                self.categorias_controller.obtener_categorias()
            )

            for id_categoria, nombre, descripcion in categorias:
                self.tabla.insert(
                    "",
                    "end",
                    iid=str(id_categoria),
                    values=(nombre, descripcion or "")
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible cargar las categorías.\n\n{error}",
                parent=self
            )

    def obtener_id_seleccionado(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selecciona una categoría",
                "Primero selecciona una categoría de la tabla.",
                parent=self
            )
            return None

        return int(seleccion[0])

    def agregar_categoria(self):
        self.abrir_formulario()

    def editar_categoria(self):
        id_categoria = self.obtener_id_seleccionado()

        if id_categoria is not None:
            self.abrir_formulario(id_categoria)

    def abrir_formulario(self, id_categoria=None):
        ventana = ctk.CTkToplevel(self)
        ventana.title(
            "Editar categoría"
            if id_categoria is not None
            else "Agregar categoría"
        )
        ventana.geometry("420x300")
        ventana.resizable(False, False)
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        ctk.CTkLabel(
            ventana,
            text=(
                "Editar categoría"
                if id_categoria is not None
                else "Nueva categoría"
            ),
            font=("Arial", 22, "bold")
        ).pack(pady=(20, 15))

        nombre_entry = ctk.CTkEntry(
            ventana,
            placeholder_text="Nombre de la categoría",
            width=320
        )
        nombre_entry.pack(pady=8)

        descripcion_entry = ctk.CTkEntry(
            ventana,
            placeholder_text="Descripción (opcional)",
            width=320
        )
        descripcion_entry.pack(pady=8)

        if id_categoria is not None:
            try:
                categoria = (
                    self.categorias_controller
                    .obtener_categoria_por_id(id_categoria)
                )

                if categoria is None or categoria[3] != 1:
                    messagebox.showerror(
                        "Categoría no disponible",
                        "La categoría no existe o está desactivada.",
                        parent=ventana
                    )
                    ventana.destroy()
                    return

                nombre_entry.insert(0, categoria[1])
                descripcion_entry.insert(
                    0, categoria[2] or ""
                )

            except Exception as error:
                messagebox.showerror(
                    "Error",
                    f"No fue posible cargar la categoría.\n\n{error}",
                    parent=ventana
                )
                ventana.destroy()
                return

        def guardar():
            nombre = nombre_entry.get().strip()
            descripcion = descripcion_entry.get().strip()

            if not nombre:
                messagebox.showwarning(
                    "Nombre obligatorio",
                    "Escribe el nombre de la categoría.",
                    parent=ventana
                )
                return

            try:
                if id_categoria is None:
                    resultado = (
                        self.categorias_controller
                        .crear_categoria(nombre, descripcion)
                    )
                else:
                    resultado = (
                        self.categorias_controller
                        .actualizar_categoria(
                            id_categoria, nombre, descripcion
                        )
                    )

                if resultado:
                    ventana.destroy()
                    self.cargar_categorias()
                else:
                    messagebox.showwarning(
                        "Sin cambios",
                        "No se encontró una categoría activa para modificar.",
                        parent=ventana
                    )

            except Exception as error:
                messagebox.showerror(
                    "Error al guardar",
                    f"No fue posible guardar la categoría.\n\n{error}",
                    parent=ventana
                )

        ctk.CTkButton(
            ventana,
            text="Guardar",
            command=guardar,
            width=150
        ).pack(pady=18)

    def desactivar_categoria(self):
        id_categoria = self.obtener_id_seleccionado()

        if id_categoria is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar desactivación",
            "La categoría dejará de aparecer en el catálogo activo.\n"
            "Los registros se conservarán.\n\n"
            "¿Deseas continuar?",
            parent=self
        )

        if not confirmar:
            return

        try:
            resultado = (
                self.categorias_controller
                .desactivar_categoria(id_categoria)
            )

            if resultado:
                self.cargar_categorias()
                messagebox.showinfo(
                    "Categoría desactivada",
                    "La categoría se desactivó correctamente.",
                    parent=self
                )
            else:
                messagebox.showwarning(
                    "Sin cambios",
                    "La categoría ya no está activa o no existe.",
                    parent=self
                )
                self.cargar_categorias()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No fue posible desactivar la categoría.\n\n{error}",
                parent=self
            )
