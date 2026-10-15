from movimiento import Movimiento

class Pedido_salida(Movimiento):
    todos = []

    def __init__(self, fecha, materiales, cantidades, cliente, estado, vendedor):
        
        self.validar_estado(estado)
        
        super().__init__(fecha, materiales, cantidades)
       
        self._cliente = cliente
        self._estado = estado
        self._vendedor = vendedor
        self._fecha_aceptacion= None
        self._fecha_envio= None

        Pedido_salida.todos.append(self)

    def get_cliente(self):
        return self._client
    def get_estado(self):
        return self._estado
    def get_vendedor(self):
        return self._vendedor
    def get_fecha_aceptacion(self):
        return self._fecha_aceptacion
    def get_fecha_envio(self):
        return self._fecha_envio

    def set_cliente(self, nuevo_cliente):
        self._cliente = nuevo_cliente
    def set_estado(self, nuevo_estado):
        self.validar_estado(nuevo_estado)
        self._estado = nuevo_estado
    def set_vendedor(self, nuevo_vendedor):
        self._vendedor = nuevo_vendedor
    def set_fecha_aceptacion(self, nueva_fecha):
        self._fecha_aceptacion = nueva_fecha
    def set_fecha_envio(self, nueva_fecha):
        self._fecha_envio = nueva_fecha

    def __str__(self):
        return 'ID Pedido: ' + str(self.get_id_movimiento) + ' Cliente: ' + self.get_cliente().get_nombre() + ' Fecha de emision: ' + str(self._fecha) + ' Estado: ' + self._estado

    @classmethod
    def informar_todos(cls):
        return cls.todos

    @staticmethod
    def validar_estado(estado):
        estados_validos = ['Pendiente', 'En preparacion', 'Despachado', 'Entregado' 'Cancelado']
        if estado not in estados_validos:
            raise ValueError(f"Estado no valido. Solo se permiten: {estados_validos}")