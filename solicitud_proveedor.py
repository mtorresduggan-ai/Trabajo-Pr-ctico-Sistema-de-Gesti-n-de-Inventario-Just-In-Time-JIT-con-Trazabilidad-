class Solicitud_proveedor:
    todos = []

    def __init__(self, id_solicitud, proveedor, fecha_emision, materiales, cant_materiales):
        self.id_solicitud = id_solicitud
        self.proveedor = proveedor
        self.fecha_emision = fecha_emision
        self.materiales = materiales
        self.cant_materiales = cant_materiales

        Solicitud_proveedor.todos.append(self)