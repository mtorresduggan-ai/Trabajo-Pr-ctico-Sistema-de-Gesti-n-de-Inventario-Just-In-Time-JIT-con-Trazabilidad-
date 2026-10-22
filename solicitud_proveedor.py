from movimiento import Movimiento


class Solicitud_proveedor(Movimiento):
    contador=0

    def __init__(self, proveedor, fecha, materiales, cantidades, estado, comprador, id_manual=None, fecha_envio_manual=None, precio_unitario=0):
        self.validar_estado(estado)

        super().__init__(fecha, materiales, cantidades)

        self._proveedor = proveedor
        self._estado = estado
        self._comprador = comprador
        self._fecha_envio = fecha_envio_manual 

        if id_manual is not None:
            self._id_movimiento = int(id_manual)
            if self._id_movimiento > Solicitud_proveedor.contador:
                Solicitud_proveedor.contador = self._id_movimiento
        else:
            Solicitud_proveedor.contador += 1
            self._id_movimiento = Solicitud_proveedor.contador

    def a_fila(self):
        fecha_envio = ""

        if self.get_fecha_envio() is not None:
            fecha_envio = self.get_fecha_envio()

        return [self.get_id_movimiento(), self.get_fecha(), self.get_proveedor().get_id(), self.get_estado(), self.get_comprador().get_id(), fecha_envio]

    def get_proveedor(self):
        return self._proveedor
    def get_estado(self):
        return self._estado
    def get_comprador(self):
        return self._comprador
    def get_fecha_envio(self):
        return self._fecha_envio
    def get_id_movimiento(self):
        return self._id_movimiento
    
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
            + ' Estado: ' + self.get_estado())


    @staticmethod
    def validar_estado(estado):
        estados_validos = ['Pendiente', 'Solicitado', 'Recibido', 'Cancelado']

        if estado not in estados_validos:
            raise ValueError(f"Estado no valido. Solo se permiten: {estados_validos}")