
from controles.control_productos_criticos import (
    ProductosCriticosController
)

controller = ProductosCriticosController()

# Registrar el producto 11 como crítico.
producto_critico = controller.obtener_producto_critico_por_producto_id(11)

if producto_critico is None:
    controller.crear_producto_critico(
        producto_id=11,
        motivo="esencial",
        frecuencia_reporte="semanal",
        alertas_activas=True
    )
    print("Producto registrado como crítico.")
else:
    print("El producto ya estaba registrado como crítico.")

# Revisar los niveles de stock.
resultado = controller.revisar_stock_productos_criticos()
print("\nResultado de la revisión:")
print(resultado)

# Consultar las alertas pendientes.
print("\nAlertas pendientes:")
for alerta in controller.obtener_alertas_pendientes():
    print(alerta)
