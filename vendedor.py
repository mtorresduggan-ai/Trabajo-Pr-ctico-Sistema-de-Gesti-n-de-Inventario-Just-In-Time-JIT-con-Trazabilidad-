from empleado import Empleado
from pedido import Pedido_salida

class Vendedor(Empleado):
    def __init__(self, id_empleado, nombre, telefono, dni):
        super().__init__(id_empleado, nombre, telefono, dni)

    def crear_pedido_salida(self, id_pedido, materiales, cantidades, fecha, cliente):
        pedido = Pedido_salida(self, id_pedido, materiales, cantidades, fecha, cliente)
        return pedido

    
