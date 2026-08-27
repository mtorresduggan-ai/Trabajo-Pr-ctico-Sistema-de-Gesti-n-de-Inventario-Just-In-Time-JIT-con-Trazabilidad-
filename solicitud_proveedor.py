class Solicitud_proveedor:
    todos = []

    def __init__(self, id_solicitud, proveedor, fecha_emision, materiales, cant_materiales):
        self.id_solicitud = id_solicitud
        self.proveedor = proveedor
        self.fecha_emision = fecha_emision
        self.materiales = materiales
        self.cant_materiales = cant_materiales

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
    