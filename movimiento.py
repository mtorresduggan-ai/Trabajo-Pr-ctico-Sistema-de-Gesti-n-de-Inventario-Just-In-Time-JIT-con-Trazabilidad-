from datetime import date
from material import Material

class Movimiento:
    todos=[]

    def __init__(self, id_movimiento, fecha, materiales, cantidades):
        self.id_movimiento = id_movimiento
        self.fecha = fecha
        self.materiales = materiales
        self.cantidades = cantidades

        self.validar_id_unico(id_movimiento)
        self.validar_id(id_movimiento)
        self.validar_fecha(fecha)
        self.validar_cantidades(cantidades)
        self.validar_materiales(materiales)

    def cambiar_fecha(self, nueva_fecha):
            self.validar_fecha(nueva_fecha)
            self.fecha = nueva_fecha
    
    def cambiar_cantidad(self, nueva_cantidad):
        self.validar_cantidades(nueva_cantidad)
        self.cantidades = nueva_cantidad

    def agregar_material(self, material):
        if material not in Material.todos:
            raise ValueError("El material no esta registrado")
        self.materiales.append(material)

    def quitar_material(self, material):
        if material not in self.materiales:
            raise ValueError("El material no se encuentra en la lista de materiales del pedido")
        self.materiales.remove(material)

    @classmethod
    def validar_id_unico(cls, id):
        for movimiento in cls.todos:
            if movimiento.id_movimiento == id:
                raise ValueError(f"Ya existe un movimiento con id '{id}'")

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
    def validar_cantidades(cant):
        if not isinstance(cant, float):
            raise TypeError("La cantidad debe ser un numero real")
        if cant < 0:
            raise ValueError("La cantidad no puede ser negativa")

    @staticmethod
    def validar_materiales(materiales):
        if not isinstance(materiales, list):
            raise TypeError("Los materiales deben estar en una lista")

        for material in materiales:
            if material not in Material.todos:
                raise ValueError("El material no esta registrado")

