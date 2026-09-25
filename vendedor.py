from empleado import Empleado
from pedido import Pedido_salida
from solicitud_proveedor import Solicitud_proveedor
from cliente import Cliente

class Vendedor(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email, usuario, clave):
        super().__init__(nombre, telefono, dni, fecha_alta, email, usuario, clave)

    def crear_pedido_salida(self, fecha, materiales, cantidades, cliente):
        Empleado.validar_fecha(fecha)
        Empleado.validar_cantidades(cantidades)
        Empleado.validar_materiales(materiales)
        self.validar_cliente(cliente)

        id_movimiento= len(Pedido_salida.todos) + len(Solicitud_proveedor.todos) + 1

        pedido = Pedido_salida(id_movimiento, fecha, materiales, cantidades, cliente, "Pendiente", self)
        return pedido

    def consultar_pedido_todos(self):
        return list(filter(lambda p: p.vendedor == self, Pedido_salida.todos))

    def consultar_pedido(self, id_movimiento):
        pedidos = list(filter(
            lambda p: p.vendedor == self and p.id_movimiento == id_movimiento,
            Pedido_salida.todos
        ))

        if not pedidos:
            raise ValueError("No existe ese pedido")

        return pedidos[0]

    def cancelar_pedido(self, id_movimiento):
        pedido = self.consultar_pedido(id_movimiento)
        if pedido.estado in ("Entregado", "Cancelado"):
            raise ValueError(f"No se puede cancelar un pedido en estado '{pedido.estado}'")
        pedido.estado = "Cancelado"
        return pedido

    def modificar_pedido(self, id_movimiento, materiales=None, cantidades=None, fecha=None, cliente=None, estado=None):
        pedido = self.consultar_pedido(id_movimiento)
        if materiales is not None:
            Empleado.validar_materiales(materiales)
            pedido.materiales = materiales
        if cantidades is not None:
            Empleado.validar_cantidades(cantidades)
            pedido.cantidades = cantidades
        if fecha is not None:
            Empleado.validar_fecha(fecha)
            pedido.fecha = fecha
        if pedido.estado in ("Entregado", "Cancelado"):
            raise ValueError(f"No se puede modificar un pedido en estado '{pedido.estado}'")
        if cliente is not None:
            self.validar_cliente(cliente)
            pedido.cambiar_cliente(cliente)
        if estado is not None:
            Pedido_salida.validar_estado(estado)
            pedido.estado = estado

        return pedido

    @staticmethod
    def validar_cliente(cliente):
        if cliente not in Cliente.todos:
            raise ValueError("El cliente no esta registrado")