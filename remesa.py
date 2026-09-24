from proveedor import Proveedor
from material import Material
from datetime import date

class Remesa:
    todos = []

    def __init__(self, id_remesa, materiales, proveedor, saldo_disponible,
                 cantidades, fechas_vencimiento, fecha_llegada):

        self.id_remesa = id_remesa
        self.materiales = materiales
        self.proveedor = proveedor
        self.saldo_disponible = saldo_disponible
        self.cantidades = cantidades
        self.fechas_vencimiento = fechas_vencimiento
        self.fecha_llegada = fecha_llegada

        self.validar_id_unico(id_remesa)
        self.validar_cantidades(cantidades)
        self.validar_saldo_disponible(saldo_disponible)
        self.validar_cant_y_saldo(saldo_disponible, cantidades)
        self.validar_proveedor(proveedor)
        self.validar_fecha(fecha_llegada)
        self.validar_materiales(materiales)
        self.validar_fechas_vencimiento(fechas_vencimiento)
        self.validar_id(id_remesa)

        Remesa.todos.append(self)

    def set_saldo(self, nuevo_saldo):
        self.validar_saldo_disponible(nuevo_saldo)
        self.validar_cant_y_saldo(nuevo_saldo, self.cantidades)
        self.saldo_disponible = nuevo_saldo

    def agregar_material(self, material, cantidad, fecha_vencimiento):
        self.validar_materiales([material])
        self.validar_cantidades([cantidad])
        self.validar_fechas_vencimiento([fecha_vencimiento])

        self.materiales.append(material)
        self.cantidades.append(cantidad)
        self.fechas_vencimiento.append(fecha_vencimiento)

    def quitar_material(self, material):
        if material not in self.materiales:
            raise ValueError("El material no se encuentra en la remesa")

        posicion = self.materiales.index(material)

        self.materiales.pop(posicion)
        self.cantidades.pop(posicion)
        self.fechas_vencimiento.pop(posicion)

    def __str__(self):
        return (
            'ID Remesa: ' + str(self.id_remesa) +
            ' Proveedor: ' + self.proveedor.nombre +
            ' Saldo disponible: ' + str(self.saldo_disponible) +
            ' Materiales: ' + str(self.materiales) +
            ' Cantidades: ' + str(self.cantidades) +
            ' Fecha de llegada: ' + str(self.fecha_llegada)
        )

    @classmethod
    def informar(cls):
        return cls.todos

    @classmethod
    def validar_id_unico(cls, id_remesa):
        for remesa in cls.todos:
            if remesa.id_remesa == id_remesa:
                raise ValueError(
                    f"Ya existe una remesa con id '{id_remesa}'"
                )

    @staticmethod
    def validar_cantidades(cantidades):
        if not isinstance(cantidades, list):
            raise TypeError("Las cantidades deben estar en una lista")

        for cantidad in cantidades:
            if not isinstance(cantidad, (int, float)):
                raise TypeError("Cada cantidad debe ser un número")

            if cantidad <= 0:
                raise ValueError(
                    "Cada cantidad debe ser mayor que cero"
                )

    @staticmethod
    def validar_saldo_disponible(saldo_disponible):
        if not isinstance(saldo_disponible, (int, float)):
            raise TypeError("El saldo debe ser un número")

        if saldo_disponible < 0:
            raise ValueError(
                "El saldo disponible debe ser mayor o igual a cero"
            )

    @staticmethod
    def validar_cant_y_saldo(saldo_disponible, cantidades):
        if saldo_disponible > sum(cantidades):
            raise ValueError(
                "El saldo disponible debe ser menor o igual "
                "a la cantidad total recibida"
            )

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
    def validar_fechas_vencimiento(fechas):
        if not isinstance(fechas, list):
            raise TypeError(
                "Las fechas de vencimiento deben estar en una lista"
            )

        for fecha in fechas:
            if fecha is not None and not isinstance(fecha, date):
                raise TypeError(
                    "Las fechas de vencimiento deben ser fechas"
                )

    @staticmethod
    def validar_id(id_remesa):
        if not isinstance(id_remesa, int):
            raise TypeError("El ID de la remesa debe ser un entero")

        if id_remesa <= 0:
            raise ValueError(
                "El ID de la remesa debe ser mayor a 0"
            )