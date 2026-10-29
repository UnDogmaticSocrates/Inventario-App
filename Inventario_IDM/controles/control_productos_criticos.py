
import dao.productos_criticos_dao


class ProductosCriticosController:

    def crear_producto_critico(
        self,
        producto_id,
        motivo="esencial",
        frecuencia_reporte="semanal",
        alertas_activas=True
    ):
        return dao.productos_criticos_dao.crear_producto_critico(
            producto_id,
            motivo,
            frecuencia_reporte,
            alertas_activas
        )

    def obtener_productos_criticos(self, solo_activos=True):
        return dao.productos_criticos_dao.obtener_productos_criticos(
            solo_activos
        )

    def obtener_producto_critico_por_producto_id(self, producto_id):
        return (
            dao.productos_criticos_dao
            .obtener_producto_critico_por_producto_id(producto_id)
        )

    def actualizar_producto_critico(
        self,
        producto_id,
        motivo,
        frecuencia_reporte,
        alertas_activas,
        activo=True
    ):
        return dao.productos_criticos_dao.actualizar_producto_critico(
            producto_id,
            motivo,
            frecuencia_reporte,
            alertas_activas,
            activo
        )

    def desactivar_producto_critico(self, producto_id):
        return dao.productos_criticos_dao.desactivar_producto_critico(
            producto_id
        )

    def obtener_alertas_pendientes(self):
        return dao.productos_criticos_dao.obtener_alertas_pendientes()

    def marcar_alerta_notificada(self, id_alerta):
        return dao.productos_criticos_dao.marcar_alerta_notificada(
            id_alerta
        )

    def resolver_alerta(self, id_alerta):
        return dao.productos_criticos_dao.resolver_alerta(id_alerta)

    
    def revisar_stock_productos_criticos(self):
        return (
            dao.productos_criticos_dao
            .revisar_stock_productos_criticos()
        )
