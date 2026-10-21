from empleado import Empleado
from pedido import Pedido_salida
from cliente import Cliente
from tarea import Tarea

class Vendedor(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja=None, id_manual=None):
        super().__init__(nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja, id_manual)

    def crear_pedido_salida(self, fecha, materiales, cantidades, cliente, tareas_pendientes_admin):
        Empleado.validar_fecha(fecha)
        Empleado.validar_cantidades(cantidades)
        Empleado.validar_materiales(materiales)
        self.validar_cliente(cliente)
        self.validar_listas(materiales, cantidades)

        pedido = Pedido_salida(fecha, materiales, cantidades, cliente, "Pendiente", self)
        
        tareas_pendientes_admin.agregar(Tarea('pedido', pedido))
        
        return pedido

    def consultar_pedido_todos(self):
        return list(filter(lambda p: p.get_vendedor() == self, Pedido_salida.todos))

    def consultar_pedido(self, id_movimiento):
        pedidos = list(filter(lambda p: p.get_vendedor() == self and p.get_id_movimiento() == id_movimiento, Pedido_salida.todos))

        if not pedidos:
            raise ValueError("No existe ese pedido")

        return pedidos[0]

    def cancelar_pedido(self, id_movimiento):
        pedido = self.consultar_pedido(id_movimiento)
        if pedido.get_estado() in ("Entregado", "Cancelado"):
            raise ValueError(f"No se puede cancelar un pedido en estado '{pedido.get_estado()}'")
        pedido.set_estado("Cancelado")
        return pedido

    def modificar_pedido(self, id_movimiento, materiales=None, cantidades=None, fecha=None, cliente=None, estado=None):
        pedido = self.consultar_pedido(id_movimiento)
        
        if pedido.get_estado() in ("Entregado", "Cancelado"):
            raise ValueError(f"No se puede modificar un pedido en estado '{pedido.get_estado()}'")
        
        campos = {"materiales": (materiales, Empleado.validar_materiales, pedido.set_materiales),
            "cantidades": (cantidades, Empleado.validar_cantidades, pedido.set_cantidades),
            "fecha": (fecha, Empleado.validar_fecha, pedido.set_fecha),
            "cliente": (cliente, self.validar_cliente, pedido.set_cliente),
            "estado": (estado, Pedido_salida.validar_estado, pedido.set_estado),}

        for valor, validar, set_valor in campos.values():
            if valor is not None:
                validar(valor)
                set_valor(valor)

        return pedido

    @staticmethod
    def validar_cliente(cliente):
        if cliente not in Cliente.todos:
            raise ValueError("El cliente no esta registrado")

    @staticmethod
    def validar_listas(materiales, cantidades):
        if len(materiales) != len(cantidades):
            raise ValueError("Debe haber una cantidad por cada material")