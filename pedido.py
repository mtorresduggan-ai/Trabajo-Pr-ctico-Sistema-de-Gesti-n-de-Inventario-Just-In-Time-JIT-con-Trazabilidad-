from movimiento import Movimiento

class Pedido_salida(Movimiento):
    contador=0

    def __init__(self, fecha, materiales, cantidades, cliente, estado, vendedor, id_manual=None, fecha_aceptacion_manual=None, fecha_envio_manual=None):
        self.validar_estado(estado)

        super().__init__(fecha, materiales, cantidades)

        if id_manual is not None:
            self._id_movimiento = int(id_manual)
            if self._id_movimiento > Pedido_salida.contador:
                Pedido_salida.contador = self._id_movimiento
        else:
            Pedido_salida.contador += 1
            self._id_movimiento = Pedido_salida.contador

        self._cliente = cliente
        self._estado = estado
        self._vendedor = vendedor
        self._fecha_aceptacion = fecha_aceptacion_manual
        self._fecha_envio = fecha_envio_manual


    def a_fila(self):
        fecha_aceptacion = ""
        fecha_envio = ""

        if self.get_fecha_aceptacion() is not None:
            fecha_aceptacion = self.get_fecha_aceptacion()

        if self.get_fecha_envio() is not None:
            fecha_envio = self.get_fecha_envio()

        return [self.get_id_movimiento(), self.get_fecha(), self.get_cliente().get_id(), self.get_estado(), self.get_vendedor().get_id(), fecha_aceptacion, fecha_envio]

    def get_cliente(self):
        return self._cliente
    def get_estado(self):
        return self._estado
    def get_vendedor(self):
        return self._vendedor
    def get_fecha_aceptacion(self):
        return self._fecha_aceptacion
    def get_fecha_envio(self):
        return self._fecha_envio
    def get_id_movimiento(self):
        return self._id_movimiento

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
        return 'ID Pedido: ' + str(self.get_id_movimiento()) + ' Cliente: ' + self.get_cliente().get_nombre() + ' Fecha de emision: ' + str(self._fecha) + ' Estado: ' + self._estado

    @staticmethod
    def validar_estado(estado):
        estados_validos = ['Pendiente', 'En preparacion', 'Despachado', 'Entregado', 'Cancelado']
        if estado not in estados_validos:
            raise ValueError(f"Estado no valido. Solo se permiten: {estados_validos}")