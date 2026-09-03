from proveedor import Proveedor
from material import Material
from datetime import date

class Solicitud_proveedor:
    todos = []

    def __init__(self, id_solicitud, proveedor, fecha_emision, materiales, cant_materiales):
        self.id_solicitud = id_solicitud
        self.proveedor = proveedor
        self.fecha_emision = fecha_emision
        self.materiales = materiales
        self.cant_materiales = cant_materiales

        self.validar_fecha(fecha_emision)
        self.validar_id_unico(id_solicitud)
        self.validar_proveedor(proveedor)
        self.validar_materiales(materiales)
        self.validar_cant_materiales(cant_materiales)
        self.validar_id(id_solicitud)

        Solicitud_proveedor.todos.append(self)

    def cambiar_fecha_emision(self, nueva_fecha):
        self.validar_fecha(nueva_fecha)
        self.fecha_emision = nueva_fecha

    def cambiar_cantidad(self, nueva_cantidad):
        self.validar_cant_materiales(nueva_cantidad)
        self.cant_materiales = nueva_cantidad

    def cambiar_proveedor(self, nuevo_proveedor):
        self.validar_proveedor(nuevo_proveedor)
        self.proveedor = nuevo_proveedor

    def agregar_material(self, material):
        self.validar_materiales([material])
        self.materiales.append(material)

    def quitar_material(self, material):
        if material not in self.materiales:
            raise ValueError("El material no se encuentra en la lista de materiales de la solicitud")
        self.materiales.remove(material)

    def informar(self):
        return 'ID Solicitud: ' + str(self.id_solicitud) + ' Proveedor: ' + self.proveedor.nombre + ' Fecha de emision: ' + str(self.fecha_emision) + ' Cantidad de materiales: ' + str(self.cant_materiales)

    @classmethod
    def informar_todos(cls):
        return cls.todos

    @classmethod
    def validar_id_unico(cls, id):
        for solicitud in cls.todos:
            if solicitud.id_solicitud == id:
                raise ValueError(f"Ya existe una solicitud con id '{id}'")

    @staticmethod
    def validar_fecha(fecha):
        if fecha is not None:
            if not isinstance(fecha, date):
                raise TypeError(
                    "La fecha de emision debe ser en formato fecha"
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
    def validar_cant_materiales(cantidad):
        if not isinstance(cantidad, (int, float)):
                    raise TypeError("La cantidad debe ser un número")
        if cantidad <= 0:
            raise ValueError("La cantidad pedida debe ser mayor que cero")

    @staticmethod
    def validar_id(id_solicitud):
        if not isinstance(id_solicitud, int):
            raise TypeError("El ID de la solicitud debe ser un entero")
        if id_solicitud <= 0:
            raise ValueError("El ID de la solicitud debe ser mayor a 0")