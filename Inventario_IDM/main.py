import customtkinter as ctk

from controles.control_navegacion import NavegacionController


app = ctk.CTk()

app.title("Inventario")
app.geometry("1000x700")

NavegacionController(app)

app.mainloop()