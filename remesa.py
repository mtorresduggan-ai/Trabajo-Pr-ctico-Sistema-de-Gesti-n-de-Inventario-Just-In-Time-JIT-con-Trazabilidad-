class Remesa:
    todos = []

    def __init__(self, id_remesa, materiales, proveedor, saldo_disponible, cant_materiales, fecha_llegada):
        self.id_remesa = id_remesa
        self.materiales = materiales
        self.proveedor = proveedor
        self.saldo_disponible = saldo_disponible
        self.cant_materiales = cant_materiales
        self.fecha_llegada = fecha_llegada

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

