from datetime import date

class Caja:
    def __init__(self, fecha_vencimiento, cantidad,  prox=None):
        self._validar_fecha_vencimiento(fecha_vencimiento)
        self._validar_cantidad(cantidad)

        self._fecha_vencimiento = fecha_vencimiento
        self._cantidad = cantidad
        self._prox = prox

    def get_fecha_vencimiento(self):
        return self._fecha_vencimiento

    def get_cantidad(self):
        return self._cantidad

    def get_prox(self):
        return self._prox

    def set_fecha_vencimiento(self, nueva_fecha):
        self._validar_fecha_vencimiento(nueva_fecha)
        self._fecha_vencimiento = nueva_fecha

    def set_cantidad(self, nueva_cantidad):
        self._validar_cantidad(nueva_cantidad)
        self._cantidad = nueva_cantidad

    def set_prox(self, nueva_prox):
        self._prox = nueva_prox

    def __str__(self):
        return ('Fecha de vencimiento: ' + str(self._fecha_vencimiento) + ', Cantidad: ' + str(self._cantidad))
    
    @staticmethod
    def _validar_fecha_vencimiento(fecha):
        if not isinstance(fecha, date):
            raise TypeError("La fecha de vencimiento debe ser una fecha")

    @staticmethod
    def _validar_cantidad(cantidad):
        if not isinstance(cantidad, (int, float)) or isinstance(cantidad, bool):
            raise TypeError("La cantidad debe ser un número")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")