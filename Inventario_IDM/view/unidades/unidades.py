import customtkinter as ctk


class UnidadesView(ctk.CTkFrame):

    def __init__(
        self,
        master,
        unidades_controller,
        navegacion_controller
    ):
        super().__init__(master)

        self.unidades_controller = unidades_controller
        self.navegacion_controller = navegacion_controller

        self.crear_interfaz()

    def crear_interfaz(self):

        self.titulo = ctk.CTkLabel(
            self,
            text="Configurar unidades",
            font=("Arial", 24)
        )
        self.titulo.pack(pady=20)

        self.nombre_entry = ctk.CTkEntry(
            self,
            placeholder_text="Nombre de la unidad"
        )
        self.nombre_entry.pack(pady=5)

        self.agregar_button = ctk.CTkButton(
            self,
            text="Agregar unidad",
            command=self.agregar_unidad
        )
        self.agregar_button.pack(pady=15)

        unidades = self.unidades_controller.obtener_unidades()

        print(unidades)

        self.regresar_button = ctk.CTkButton(
            self,
            text="Regresar al menú",
            command=self.navegacion_controller.mostrar_menu
        )
        self.regresar_button.pack(pady=10)

        self.lista_unidades = ctk.CTkScrollableFrame(
            self,
            width=400,
            height=250
        )

        self.lista_unidades.pack(
            pady=20,
            padx=20,
            fill="both",
            expand=True
        )

        self.mostrar_unidades()

    def agregar_unidad(self):

        nombre = self.nombre_entry.get()

        if not nombre:
            print("El nombre de la unidad es obligatorio")
            return

        resultado = self.unidades_controller.crear_unidad(nombre)

        if resultado:

            self.nombre_entry.delete(0, "end")

            self.mostrar_unidades()

            print("Unidad agregada correctamente")

    def mostrar_unidades(self):

        for widget in self.lista_unidades.winfo_children():
            widget.destroy()

        unidades = self.unidades_controller.obtener_unidades()

        for numero_visual, unidad in enumerate(unidades, start=1):

            fila = ctk.CTkFrame(self.lista_unidades)
            fila.pack(
                fill="x",
                pady=5, 
                padx=5
            )

            label= ctk.CTkLabel(
                fila,
                text= f"{numero_visual}: {unidad[1]}"
            )

            label.pack(
                side="left", 
                padx=10
            )

            editar_button = ctk.CTkButton(
                fila,
                text="Editar",
                command=lambda id_unidad=unidad[0]: self.editar_unidad(id_unidad)
            )

            editar_button.pack(
                side="right",
                padx=10
            )

    def editar_unidad(self, id_unidad):

        for widget in self.lista_unidades.winfo_children():
            widget.destroy()

        unidades = self.unidades_controller.obtener_unidades()

        for unidad in unidades:

            fila = ctk.CTkFrame(
                self.lista_unidades
            )

            fila.pack(
                fill="x",
                pady=5,
                padx=5
            )

            if unidad[0] == id_unidad:

                entrada = ctk.CTkEntry(
                    fila
                )

                entrada.insert(
                    0,
                    unidad[1]
                )

                entrada.pack(
                    side="left",
                    padx=10
                )

                guardar_button = ctk.CTkButton(
                    fila,
                    text="Guardar",
                    command=lambda: self.guardar_edicion(
                        id_unidad,
                        entrada
                    )
                )

                guardar_button.pack(
                    side="right",
                    padx=10
                )

            else:

                label = ctk.CTkLabel(
                    fila,
                    text=f"{unidad[0]}: {unidad[1]}"
                )

                label.pack(
                    side="left",
                    padx=10
                )

                editar_button = ctk.CTkButton(
                    fila,
                    text="Editar",
                    command=lambda id_unidad=unidad[0]: self.editar_unidad(
                        id_unidad
                    )
                )

                editar_button.pack(
                    side="right",
                    padx=10
                )

    def guardar_edicion(self, id_unidad, entrada):

        nombre = entrada.get()

        if not nombre:
            print("El nombre de la unidad es obligatorio")
            return

        resultado = self.unidades_controller.actualizar_unidad(
            id_unidad,
            nombre
        )

        if resultado:

            self.mostrar_unidades()

            print("Unidad actualizada correctamente")

        else:

            print("Ya existe una unidad con ese nombre")
