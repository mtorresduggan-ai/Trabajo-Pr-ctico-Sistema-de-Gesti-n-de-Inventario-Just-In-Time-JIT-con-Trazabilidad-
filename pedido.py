from movimiento import Movimiento
from cliente import Cliente

class Pedido_salida(Movimiento):
    todos = []

    def __init__(self, id_movimiento, fecha, materiales, cantidades, cliente, estado, vendedor):
        super().__init__(id_movimiento, fecha, materiales, cantidades)
        self.cliente = cliente
        self.estado = estado
        self.estado = vendedor

        Pedido_salida.todos.append(self)

    def cambiar_cliente(self, nuevo_cliente):
        if nuevo_cliente not in Cliente.todos:
            raise ValueError("El cliente no se encuentra en la lista de clientes registrados en el sistema")
        self.cliente = nuevo_cliente

    def informar(self):
        return 'ID Pedido: ' + str(self.id_movimiento) + ' Cliente: ' + self.cliente.nombre + ' Fecha de emision: ' + str(self.fecha) + ' Cantidad de materiales: ' + str(self.cantidades)

    @classmethod
    def informar_todos(cls):
        return cls.todos

    @staticmethod
    def validar_estado(estado):
        estados_validos = ['Pendiente', 'En preparacion', 'Despachado', 'Entregado', 'Cancelado']
        if estado not in estados_validos:
            raise ValueError(f"Estado no valido. Solo se permiten: {estados_validos}")