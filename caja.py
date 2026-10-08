from datetime import date

class Caja:
    def __init__(self, fecha_vencimineto, cantidad, prox=None):
        self.fecha_vencimineto= fecha_vencimineto
        self.cantidad= cantidad
        self.prox = prox

    def __str__(self):
        return ('Fecha de vencimiento:' + str(self.fecha_vencimineto)
                + 'Cantidad:' + str(self.cantidad))
