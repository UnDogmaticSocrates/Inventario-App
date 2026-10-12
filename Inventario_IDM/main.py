import customtkinter as ctk

from base_datos.tablas import crear_tablas
from controles.control_navegacion import NavegacionController

crear_tablas()

app = ctk.CTk()

app.title("Inventario")
app.geometry("1500x800")
app.minsize(1000, 650)

NavegacionController(app)

app.mainloop()