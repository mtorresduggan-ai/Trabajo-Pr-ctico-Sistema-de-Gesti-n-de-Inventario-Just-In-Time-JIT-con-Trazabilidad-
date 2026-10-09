from movimiento import Movimiento

class Solicitud_proveedor(Movimiento):
    todos = []

    def __init__(self, proveedor, fecha, materiales, cantidades, estado, comprador):
        
        self.validar_estado(estado)
        
        super().__init__(fecha, materiales, cantidades)

        self.proveedor = proveedor
        self.estado = estado
        self.comprador = comprador
        self.fecha_envio = None

        Solicitud_proveedor.todos.append(self)

    def __str__(self):
        return 'ID Solicitud: ' + str(self.id_movimiento) + ' Proveedor: ' + self.proveedor.nombre + ' Fecha de emision: ' + str(self.fecha) + ' Estado: ' + self.estado

    @classmethod
    def informar_todos(cls):
        return cls.todos

    @staticmethod
    def validar_estado(estado):
        estados_validos = ['Pendiente', 'Solicitado', 'Recibido', 'Cancelado']
        if estado not in estados_validos:
            raise ValueError(f"Estado no valido. Solo se permiten: {estados_validos}")
