from datetime import date

class Caja:
    def __init__(self, fecha_vencimineto, cantidad, proximo=None):
        self.fecha_fecha_vencimineto= fecha_vencimineto
        self.cantidad= cantidad
        self.prox = proximo

        self.validar_fecha(fecha_vencimineto)
        self.validar_cantidad(cantidad)

    def __str__(self):
        return ('Fecha de vencimiento:' + str(self.fecha_vencimineto)
                + 'Cantidad:' + str(self.cantidad))

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