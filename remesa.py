from proveedor import Proveedor

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

        Remesa.todos.append(self)

    def cambiar_saldo(self, nuevo_saldo):
        self.saldo_disponible = nuevo_saldo

    def cambiar_cantidad(self, nueva_cantidad):
        self.cant_materiales = nueva_cantidad

    def agregar_material(self, material):
        self.materiales.append(material)

    def quitar_material(self, material):
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
        if cantidad <= 0:
            raise ValueError("El cantidad recibida debe ser mayor que cero")
        if not isinstance(cantidad, (int, float)):
                    raise TypeError("La cantidad debe ser un número")

    @staticmethod
    def validar_saldo_disponible(saldo_disponible):
        if saldo_disponible < 0:
            raise ValueError("El saldo disponible debe ser mayor o igual a cero")
        if not isinstance(saldo_disponible, (int, float)):
                            raise TypeError("El saldo debe ser un número")

    @staticmethod
    def validar_cant_y_saldo(saldo_disponible,cant_recibida):
        if saldo_disponible > cant_recibida:
            raise ValueError("El saldo disponible debe ser menor o igual a la cantidad recibida")

    @staticmethod
    def validar_proveedor(proveedor):
        if not isinstance(proveedor, Proveedor.todos):
            raise TypeError("El proveedor debe ser un objeto de la clase Proveedor")

    @staticmethod
    def validar_materiales(materiales):
        if not isinstance(materiales, list):
            raise TypeError("Los materiales deben estar en una lista")

    @staticmethod
    def validar_fecha(fecha):
        if fecha is not None:
            if not isinstance(fecha, str):
                raise TypeError(
                    "La fecha de llegada debe ser un texto o None"
                )
