from proveedor import Proveedor

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

        Solicitud_proveedor.todos.append(self)

    def cambiar_fecha_emision(self, nueva_fecha):
        self.fecha_emision = nueva_fecha

    def cambiar_cantidad(self, nueva_cantidad):
        self.cant_materiales = nueva_cantidad

    def cambiar_proveedor(self, nuevo_proveedor):
        self.proveedor = nuevo_proveedor

    def agregar_material(self, material):
        self.materiales.append(material)

    def quitar_material(self, material):
        self.materiales.remove(material)

    def informar(self):
        return 'ID Solicitud: ' + str(self.id_solicitud) + ' Proveedor: ' + self.proveedor.nombre + ' Fecha de emision: ' + str(self.fecha_emision) + ' Cantidad de materiales: ' + str(self.cant_materiales)

    @classmethod
    def informar_todos(cls):
        return cls.todos

    @classmethod
    def validar_id_unico(cls, id):
        for pedido in cls.todos:
            if pedido.id == id:
                raise ValueError(f"Ya existe una solicitud con id '{id}'")

    @staticmethod
    def validar_fecha(fecha):
        if fecha is not None:
            if not isinstance(fecha, str):
                raise TypeError(
                    "La fecha de emision debe ser un texto o None"
                )

    @staticmethod
    def validar_proveedor(proveedor):
        if not isinstance(proveedor, Proveedor.todos):
            raise TypeError("El proveedor debe ser un objeto de la clase Proveedor")

    @staticmethod
    def validar_materiales(materiales):
        if not isinstance(materiales, list):
            raise TypeError("Los materiales deben estar en una lista")

    @staticmethod
    def validar_cant_materiales(cantidad):
        if cantidad <= 0:
            raise ValueError("El cantidad pedida debe ser mayor que cero")
        if not isinstance(cantidad, (int, float)):
                    raise TypeError("La cantidad debe ser un número")
    