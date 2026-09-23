import customtkinter as ctk

from base_datos.tablas import crear_tablas
from controles.control_navegacion import NavegacionController

crear_tablas()

app = ctk.CTk()

app.title("Inventario")
app.geometry("1000x700")

NavegacionController(app)

app.mainloop()