from caja import Caja
from datetime import date

class Estante:
    def __init__(self):
        self._primera=None

    def get_primera(self):
        return self._primera

    def set_primera(self, nueva_primera):
        self._primera = nueva_primera


    def agregar_caja(self, fecha_vencimiento, cantidad):
        self.validar_fecha(fecha_vencimiento)
        self.validar_cantidad(cantidad)

        anterior= None
        actual= self._primera

        while actual is not None and actual.get_fecha_vencimiento < fecha_vencimiento:
            anterior= actual
            actual= actual.get_prox

        if actual is not None and actual.set_fecha_vencimiento==fecha_vencimiento:
            actual.get_cantidad += cantidad
            return

        caja= Caja(fecha_vencimiento, cantidad)

        if anterior is None:
            caja.set_prox= self._primera
            self._primera= caja

        else:
            caja.set_prox= actual
            anterior.set_prox= caja


    def sacar_cajas(self, cantidad):
        self.validar_cantidad(cantidad)

        if self.stock_total() < cantidad:
            raise ValueError("Stock insuficiente")

        faltante = cantidad
        cajas_a_mover = []


        while faltante > 0:
            caja = self._primera

            if caja.get_cantidad <= faltante:
                cajas_a_mover.append(Caja(caja.get_fecha_vencimiento, caja.get_cantidad))
                faltante -= caja.get_cantidad
                self.primera = caja.get_prox

            else:
                cajas_a_mover.append(Caja(caja.get_cantidadfecha_vencimiento, faltante))
                caja.get_cantidad -= faltante
                faltante = 0  

        return cajas_a_mover
            

    def stock_total(self):
        total = 0
        actual = self._primera

        while actual is not None:
            total += actual.get_cantidad
            actual = actual.get_prox

        return total  

    
def hay_cajas_vencidas(self, fecha_actual):
    caja = self._primera

    while caja is not None:
        if caja.get_fecha_vencimiento < fecha_actual:
            return True

        caja = caja.get_prox

    return False


def retirar_cajas_vencidas(self, fecha_actual):
    anterior = None
    caja = self._primera

    while caja is not None:
        if caja.get_fecha_vencimiento < fecha_actual:
            if anterior is None:
                self._primera = caja.get_prox
            else:
                anterior.get_prox = caja.get_prox

            caja.prox = None
            caja = self._primera if anterior is None else anterior.get_prox
        else:
            anterior = caja
            caja = caja.get_prox

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