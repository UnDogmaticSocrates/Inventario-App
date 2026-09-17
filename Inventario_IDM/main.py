import customtkinter as ctk

from base_datos.tablas import crear_tablas
from controles.control_productos import ProductosController
from view.ui import ProductosView

crear_tablas()
print("Base de datos lista")

# Inicializar aplicación
app = ctk.CTk()

app.title("Inventario")
app.geometry("1000x700")


# Controlador
productos_controller = ProductosController()


# Vista
productos_view = ProductosView(
    app,
    productos_controller
)

productos_view.pack(
    fill="both",
    expand=True
)


# Ejecutar aplicación
app.mainloop()