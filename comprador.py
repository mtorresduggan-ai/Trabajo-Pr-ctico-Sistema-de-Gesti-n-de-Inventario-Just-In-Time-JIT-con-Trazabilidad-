from empleado import Empleado
from solicitud_proveedor import Solicitud_proveedor


class Comprador(Empleado):
    def __init__(self, id_empleado, nombre, telefono, dni):
        super().__init__(id_empleado, nombre, telefono, dni)

    def crear_solicitud(self, id_movimiento, fecha, materiales, cantidades, proveedor):
        solicitud = Solicitud_proveedor(
            id_movimiento, proveedor, fecha, materiales,
            cantidades, "Pendiente", self
        )
        return solicitud

    def consultar_solicitudes(self):
        return list(filter(lambda s: s.comprador == self, Solicitud_proveedor.todos))

    def cancelar_solicitud(self, id_movimiento):
        solicitud = self.consultar_solicitud(id_movimiento)
        if solicitud.estado in ("Recibida", "Cancelada"):
            raise ValueError(f"No se puede cancelar una solicitud en estado '{solicitud.estado}'")
        solicitud.estado = "Cancelada"
        return solicitud

    def modificar_solicitud(self, id_movimiento, materiales=None, cantidades=None,
                             fecha=None, proveedor=None, estado=None):
        solicitud = self.consultar_solicitud(id_movimiento)
        if solicitud.estado in ("Recibida", "Cancelada"):
            raise ValueError(f"No se puede modificar una solicitud en estado '{solicitud.estado}'")

        if materiales is not None:
            solicitud.materiales = materiales
        if cantidades is not None:
            solicitud.cantidades = cantidades
        if fecha is not None:
            solicitud.fecha = fecha
        if proveedor is not None:
            solicitud.cambiar_proveedor(proveedor)
        if estado is not None:
            Solicitud_proveedor.validar_estado(estado)
            solicitud.estado = estado

        return solicitud

    