from empleado import Empleado
from solicitud_proveedor import Solicitud_proveedor

class Comprador(Empleado):
    def __init__(self, id_empleado, nombre, telefono, dni):
        super().__init__(id_empleado, nombre, telefono, dni)

    def crear_solicitud(self, id_solicitud, proveedor, materiales, cantidades, fecha):
        solicitud = Solicitud_proveedor(id_solicitud, proveedor, materiales, cantidades, fecha)
        return solicitud

    