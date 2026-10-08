from movimiento import Movimiento

class Pedido_salida(Movimiento):
    todos = []

    def __init__(self, fecha, materiales, cantidades, cliente, estado, vendedor):
        
        self.validar_estado(estado)
        
        super().__init__(fecha, materiales, cantidades)
       
        self.cliente = cliente
        self.estado = estado
        self.vendedor = vendedor

        Pedido_salida.todos.append(self)

    def __str__(self):
        return 'ID Pedido: ' + str(self.id_movimiento) + ' Cliente: ' + self.cliente.nombre + ' Fecha de emision: ' + str(self.fecha) + ' Estado: ' + self.estado

    @classmethod
    def informar_todos(cls):
        return cls.todos

    @staticmethod
    def validar_estado(estado):
        estados_validos = ['Pendiente', 'En preparacion', 'Despachado', 'Entregado', 'Cancelado']
        if estado not in estados_validos:
            raise ValueError(f"Estado no valido. Solo se permiten: {estados_validos}")