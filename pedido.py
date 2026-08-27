class Pedido_salida:
    todos = []

    def __init__(self, id_pedido_salida, fecha_emision, materiales, cant_materiales):
        self.id_pedido_salida = id_pedido_salida
        self.fecha_emision = fecha_emision
        self.materiales = materiales
        self.cant_materiales = cant_materiales

        Pedido_salida.todos.append(self)

    def cambiar_fecha_emision(self, nueva_fecha):
        self.fecha_emision = nueva_fecha

    def cambiar_cantidad(self, nueva_cantidad):
        self.cant_materiales = nueva_cantidad

    def agregar_material(self, material):
        self.materiales.append(material)

    def quitar_material(self, material):
        self.materiales.remove(material)

    def informar(self):
        return 'ID Pedido: ' + str(self.id_pedido_salida) + ' Fecha de emision: ' + str(self.fecha_emision) + ' Cantidad de materiales: ' + str(self.cant_materiales)

    @classmethod
    def informar(cls):
        return cls.todos
