from empleado import Empleado
from pedido import Pedido_salida

class Vendedor(Empleado):
    def __init__(self, id_empleado, nombre, telefono, dni):
        super().__init__(id_empleado, nombre, telefono, dni)

    def crear_pedido_salida(self, id_movimiento, fecha, materiales, cantidades, cliente):
        pedido = Pedido_salida(id_movimiento, fecha, materiales, cantidades,cliente, "Pendiente", self)
        return pedido

    def consultar_pedidos(self):
        return list(filter(lambda p: p.vendedor == self, Pedido_salida.todos))

    def cancelar_pedido(self, id_movimiento):
        pedido = self.consultar_pedido(id_movimiento)
        if pedido.estado in ("Entregado", "Cancelado"):
            raise ValueError(f"No se puede cancelar un pedido en estado '{pedido.estado}'")
        pedido.estado = "Cancelado"
        return pedido

    def modificar_pedido(self, id_movimiento, materiales=None, cantidades=None, fecha=None, cliente=None, estado=None):
        pedido = self.consultar_pedido(id_movimiento)
        if pedido.estado in ("Entregado", "Cancelado"):
            raise ValueError(f"No se puede modificar un pedido en estado '{pedido.estado}'")

        if materiales is not None:
            pedido.materiales = materiales
        if cantidades is not None:
            pedido.cantidades = cantidades
        if fecha is not None:
            pedido.fecha = fecha
        if cliente is not None:
            pedido.cambiar_cliente(cliente)
        if estado is not None:
            Pedido_salida.validar_estado(estado)
            pedido.estado = estado

        return pedido