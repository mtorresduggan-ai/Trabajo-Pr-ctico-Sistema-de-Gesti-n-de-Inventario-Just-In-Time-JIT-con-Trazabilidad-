from caja import Caja
from datetime import date

class Estante:
    def __init__(self):
        self.prox_a_vencer=None

    def agregar_caja(self, fecha_vencimiento, cantidad):
        self.validar_fecha(fecha_vencimiento)
        self.validar_cantidad(cantidad)

        anterior= None
        actual= self.primera

        while actual is not None and actual.fecha_vencimiento < fecha_vencimiento:
            anterior= actual
            actual= actual.prox

        if actual is not None and actual.fecha_vencimiento==fecha_vencimiento:
            actual.cantidad += cantidad
            return

        caja= Caja(fecha_vencimiento, cantidad)

        if anterior is None:
            caja.prox= self.primera
            self.primera= caja

        else:
            caja.prox= actual
            anterior.prox= caja


    def sacar_cajas(self, cantidad):
        faltante = cantidad

        while faltante > 0:
            caja = self.primera

            if caja.cantidad <= faltante:
                faltante -= caja.cantidad
                self.primera = caja.prox

            else:
                caja.cantidad -= faltante
                faltante = 0        

    @staticmethod
    def validar_fecha(fecha):
        if fecha is not None:
            if not isinstance(fecha, date):
                raise TypeError("La fecha debe ser en formato fecha")

    @staticmethod 
    def validar_cantidad(cantidad):
        if not isinstance(cantidad, (int, float)):
            raise TypeError("Cada cantidad debe ser un numero")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")