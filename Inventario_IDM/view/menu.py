
import customtkinter as ctk
from tkinter import messagebox


class MenuView(ctk.CTkFrame):

    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        self.crear_interfaz()

    def crear_interfaz(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ---------- ENCABEZADO ----------
        encabezado = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )
        encabezado.grid(
            row=0, column=0,
            sticky="ew",
            padx=35, pady=(25, 10)
        )
        encabezado.grid_columnconfigure(0, weight=1)

        identidad = ctk.CTkFrame(
            encabezado,
            fg_color="transparent"
        )
        identidad.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            identidad,
            text="Cafetería Astral",
            font=("Arial", 28, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            identidad,
            text="Sistema de inventario",
            font=("Arial", 14),
            text_color="gray"
        ).pack(anchor="w", pady=(3, 0))

        usuario = ctk.CTkFrame(
            encabezado,
            fg_color="transparent"
        )
        usuario.grid(row=0, column=1, sticky="e", padx=(20, 0))

        ctk.CTkLabel(
            usuario,
            text="Sesión iniciada",
            font=("Arial", 12),
            text_color="gray"
        ).pack(anchor="e")

        ctk.CTkLabel(
            usuario,
            text="Carlos",
            font=("Arial", 17, "bold")
        ).pack(anchor="e", pady=(3, 0))

        # ---------- ÁREA CENTRAL ----------
        contenido = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        contenido.grid(
            row=1, column=0,
            sticky="nsew",
            padx=35, pady=10
        )
        
        contenido.anchor("center")

        for columna in range(4):
            contenido.grid_columnconfigure(
                columna, weight=0
            )

        for fila in range(3):
            contenido.grid_rowconfigure(
                fila, weight=0
            )

        ctk.CTkLabel(
            contenido,
            text="¿Qué necesitas hacer?",
            font=("Arial", 24, "bold")
        ).grid(
            row=0, column=0,
            columnspan=4,
            pady=(0, 25)
        )

        opciones = [
            ("📦", "Productos", "mostrar_productos"),
            ("🚚", "Proveedores", None),
            ("📥", "Entradas", None),
            ("📤", "Salidas", None),
            ("📅", "Caducidad", None),
            ("🗂", "Categorías", "mostrar_categorias"),
            ("⚖", "Unidades", "mostrar_unidades"),
            ("📊", "Reportes", None),
        ]

        for indice, (icono, nombre, accion) in enumerate(opciones):
            fila = 1 + indice // 4
            columna = indice % 4

            boton = ctk.CTkButton(
                contenido,
                text=f"{icono}\n\n{nombre}",
                width=105,
                height=120,
                corner_radius=14,
                font=("Arial", 16, "bold"),
                command=lambda n=nombre, a=accion:
                    self.abrir_modulo(n, a)
            )

            boton.grid(
                row=fila,
                column=columna,
                padx=12,
                pady=10
            )

        # ---------- PIE ----------
        pie = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        pie.grid(
            row=2, column=0,
            sticky="ew",
            padx=35, pady=(5, 20)
        )
        pie.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            pie,
            text="Inventario · Gestión diaria",
            font=("Arial", 12),
            text_color="gray"
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            pie,
            text="Salir",
            width=100,
            command=self.controller.salir
        ).grid(row=0, column=1, sticky="e")

    def abrir_modulo(self, nombre, accion):
        if accion is None:
            messagebox.showinfo(
                "Módulo pendiente",
                f"El módulo «{nombre}» todavía no está implementado."
            )
            return

        metodo = getattr(self.controller, accion, None)

        if callable(metodo):
            metodo()
        else:
            messagebox.showwarning(
                "Función no disponible",
                f"No se encontró la función para abrir «{nombre}»."
            )
