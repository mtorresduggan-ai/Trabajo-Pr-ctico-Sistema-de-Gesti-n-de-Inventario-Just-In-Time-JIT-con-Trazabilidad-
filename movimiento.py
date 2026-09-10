from datetime import date

class Movimiento:
    def __init__(self, id_movimiento, fecha, materiales, cantidades_movidas):
        self.id_movimiento = id_movimiento
        self.fecha = fecha
        self.materiales = materiales
        self.cantidades_movidas = cantidades_movidas

        self.validar_id_unico(id_movimiento)
        self.validar_id(id_movimiento)
        self.validar_fecha(fecha)
        self.validar_cant_movidas(cantidades_movidas)

    @classmethod
    def validar_id_unico(cls, id):
        for solicitud in cls.todos:
            if solicitud.id_solicitud == id:
                raise ValueError(f"Ya existe un empleado con id '{id}'")

    @staticmethod
    def validar_fecha(fecha):
        if fecha is not None:
            if not isinstance(fecha, date):
                raise TypeError(
                    "La fecha de inicio debe ser en formato fecha"
                )

    @staticmethod
    def validar_id(id):
        if not isinstance(id, int):
            raise TypeError("El ID del empleado debe ser un entero")
        if id <= 0:
            raise ValueError("El ID del empleado debe ser mayor a 0")

    @staticmethod 
    def validar_cant_movidas(cant):
        if not isinstance(cant, int):
            raise TypeError("La cantidad de movimietnos debe ser un entero")
        if cant < 0:
            raise ValueError("La cantidad de movimientos no puede ser negativa")