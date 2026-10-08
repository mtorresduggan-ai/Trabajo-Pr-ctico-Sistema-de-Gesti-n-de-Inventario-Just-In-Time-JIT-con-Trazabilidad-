from datetime import date

class Caja:
    def __init__(self, fecha_vencimiento, cantidad, prox=None):
        self.fecha_vencimineto= fecha_vencimiento
        self.cantidad= cantidad
        self.prox = prox

    def __str__(self):
        return ('Fecha de vencimiento:' + str(self.fecha_vencimineto)
                + 'Cantidad:' + str(self.cantidad))
