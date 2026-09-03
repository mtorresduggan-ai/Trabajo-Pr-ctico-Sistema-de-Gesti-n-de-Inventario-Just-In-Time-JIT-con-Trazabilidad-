from proveedor import Proveedor
from material import Material
from datetime import date

class Remesa:
    todos = []

    def __init__(self, id_remesa, materiales, proveedor, saldo_disponible, cant_materiales, fecha_llegada):
        self.id_remesa = id_remesa
        self.materiales = materiales
        self.proveedor = proveedor
        self.saldo_disponible = saldo_disponible
        self.cant_materiales = cant_materiales
        self.fecha_llegada = fecha_llegada

        self.validar_id_unico(id_remesa)
        self.validar_cant_recibida(cant_materiales)
        self.validar_saldo_disponible(saldo_disponible)
        self.validar_cant_y_saldo(saldo_disponible,cant_materiales)
        self.validar_proveedor(proveedor)
        self.validar_fecha(fecha_llegada)
        self.validar_materiales(materiales)
        self.validar_id(id_remesa)

        Remesa.todos.append(self)

    def set_saldo(self, nuevo_saldo):
        self.validar_saldo_disponible(nuevo_saldo)
        self.validar_cant_y_saldo(nuevo_saldo, self.cant_materiales)
        self.saldo_disponible = nuevo_saldo

    def set_cantidad(self, nueva_cantidad):
        self.validar_cant_recibida(nueva_cantidad)
        self.validar_cant_y_saldo(self.saldo_disponible, nueva_cantidad)
        self.cant_materiales = nueva_cantidad

    def agregar_material(self, material):
        self.validar_materiales([material])
        self.materiales.append(material)

    def quitar_material(self, material):
        if material not in self.materiales:
            raise ValueError("El material no se encuentra en la remesa")
        self.materiales.remove(material)

    def __str__(self):
        return 'ID Remesa: ' + str(self.id_remesa) + ' Proveedor: ' + self.proveedor.nombre + ' Saldo disponible: ' + str(self.saldo_disponible) + ' Cantidad de materiales: ' + str(self.cant_materiales) + ' Fecha de llegada: ' + str(self.fecha_llegada)
    
    @classmethod
    def informar(cls):
        return cls.todos

    @classmethod
    def validar_id_unico(cls, id_remesa):
        for remesa in cls.todos:
            if remesa.id_remesa == id_remesa:
                raise ValueError(f"Ya existe una remesa con id '{id_remesa}'")

    @staticmethod
    def validar_cant_recibida(cantidad):
        if not isinstance(cantidad, (int, float)):
            raise TypeError("La cantidad debe ser un número")
        if cantidad <= 0:
            raise ValueError("El cantidad recibida debe ser mayor que cero")

    @staticmethod
    def validar_saldo_disponible(saldo_disponible):
        if not isinstance(saldo_disponible, (int, float)):
                            raise TypeError("El saldo debe ser un número")
        if saldo_disponible < 0:
            raise ValueError("El saldo disponible debe ser mayor o igual a cero")

    @staticmethod
    def validar_cant_y_saldo(saldo_disponible,cant_recibida):
        if saldo_disponible > cant_recibida:
            raise ValueError("El saldo disponible debe ser menor o igual a la cantidad recibida")

    @staticmethod
    def validar_proveedor(proveedor):
        if proveedor not in Proveedor.todos:
            raise ValueError("El proveedor no esta registrado")

    @staticmethod
    def validar_materiales(materiales):
        if not isinstance(materiales, list):
            raise TypeError("Los materiales deben estar en una lista")
        for material in materiales:
            if material not in Material.todos:
                raise ValueError("El material no esta registrado")

    @staticmethod
    def validar_fecha(fecha):
        if fecha is not None:
            if not isinstance(fecha, date):
                raise TypeError(
                    "La fecha de llegada debe ser en formato fecha"
                )

    @staticmethod
    def validar_id(id_remesa):
        if not isinstance(id_remesa, int):
            raise TypeError("El ID de la remesa debe ser un entero")
        if id_remesa <= 0:
            raise ValueError("El ID de la remesa debe ser mayor a 0")