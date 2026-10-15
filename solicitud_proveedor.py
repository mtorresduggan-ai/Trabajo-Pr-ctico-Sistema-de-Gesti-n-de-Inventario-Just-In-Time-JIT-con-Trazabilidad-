from movimiento import Movimiento


class Solicitud_proveedor(Movimiento):
    todos = []

    def __init__(self, proveedor, fecha, materiales, cantidades, estado, comprador):
        self.validar_estado(estado)

        super().__init__(fecha, materiales, cantidades)

        self._proveedor = proveedor
        self._estado = estado
        self._comprador = comprador
        self._fecha_envio = None

        Solicitud_proveedor.todos.append(self)

    def get_proveedor(self):
        return self._proveedor
    def get_estado(self):
        return self._estado
    def get_comprador(self):
        return self._comprador
    def get_fecha_envio(self):
        return self._fecha_envio
    
    def set_proveedor(self, nuevo_proveedor):
        self._proveedor = nuevo_proveedor
    def set_estado(self, nuevo_estado):
        self.validar_estado(nuevo_estado)
        self._estado = nuevo_estado
    def set_comprador(self, nuevo_comprador):
        self._comprador = nuevo_comprador
    def set_fecha_envio(self, nueva_fecha):
        self._fecha_envio = nueva_fecha

    
    def __str__(self):
        return (
            'ID Solicitud: ' + str(self.get_id_movimiento())
            + ' Proveedor: ' + self.get_proveedor().get_nombre()
            + ' Fecha de emision: ' + str(self.get_fecha())
            + ' Estado: ' + self.get_estado()
        )

    @classmethod
    def informar_todos(cls):
        return cls.todos.copy()

    @staticmethod
    def validar_estado(estado):
        estados_validos = ['Pendiente', 'Solicitado', 'Recibido', 'Cancelado']

        if estado not in estados_validos:
            raise ValueError(
                f"Estado no valido. Solo se permiten: {estados_validos}"
            )