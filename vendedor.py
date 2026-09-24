from empleado import Empleado
from pedido import Pedido_salida
from solicitud_proveedor import Solicitud_proveedor

class Vendedor(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email, usuario, clave):
        super().__init__(nombre, telefono, dni, fecha_alta, email, usuario, clave)

    def crear_pedido_salida(self, fecha, materiales, cantidades, cliente):
        Empleado.validar_fecha(fecha)
        Empleado.validar_cantidades(cantidades)
        Empleado.validar_materiales(materiales)

        id_movimiento= len(Pedido_salida.todos) + len(Solicitud_proveedor.todos) + 1

        pedido = Pedido_salida(id_movimiento, fecha, materiales, cantidades, cliente, "Pendiente", self)
        return pedido

    def consultar_pedido(self):
        return list(filter(lambda p: p.vendedor == self, Pedido_salida.todos))

    def cancelar_pedido(self, id_movimiento):
        pedido = self.consultar_pedido(id_movimiento)
        if pedido.estado in ("Entregado", "Cancelado"):
            raise ValueError(f"No se puede cancelar un pedido en estado '{pedido.estado}'")
        pedido.estado = "Cancelado"
        return pedido

    def modificar_pedido(self, id_movimiento, materiales=None, cantidades=None, fecha=None, cliente=None, estado=None):
        pedido = self.consultar_pedido(id_movimiento)
        Empleado.validar_fecha(fecha)
        Empleado.validar_cantidades(cantidades)
        Empleado.validar_materiales(materiales)
        
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