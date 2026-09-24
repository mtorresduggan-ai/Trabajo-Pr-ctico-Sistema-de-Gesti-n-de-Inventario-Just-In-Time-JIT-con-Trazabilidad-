from empleado import Empleado
from solicitud_proveedor import Solicitud_proveedor
from pedido import Pedido_salida
from proveedor import Proveedor

class Comprador(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email, usuario, clave):
        super().__init__(nombre, telefono, dni, fecha_alta, email, usuario, clave)

    def crear_solicitud(self, id_movimiento, fecha, materiales, cantidades, proveedor):
        Empleado.validar_fecha(fecha)
        Empleado.validar_cantidades(cantidades)
        Empleado.validar_materiales(materiales)
        self.validar_proveedor(proveedor)

        id_movimiento= len(Pedido_salida.todos) + len(Solicitud_proveedor.todos) + 1

        solicitud = Solicitud_proveedor(id_movimiento, proveedor, fecha, materiales, cantidades, "Pendiente", self)
        return solicitud

    def consultar_solicitudes(self):
        return list(filter(lambda s: s.comprador == self, Solicitud_proveedor.todos))

    def cancelar_solicitud(self, id_movimiento):
        solicitud = self.consultar_solicitud(id_movimiento)
        if solicitud.estado in ("Recibida", "Cancelada"):
            raise ValueError(f"No se puede cancelar una solicitud en estado '{solicitud.estado}'")
        solicitud.estado = "Cancelada"
        return solicitud

    def modificar_solicitud(self, id_movimiento, materiales=None, cantidades=None, fecha=None, proveedor=None, estado=None):
        solicitud = self.consultar_solicitud(id_movimiento)
        Empleado.validar_fecha(fecha)
        Empleado.validar_cantidades(cantidades)
        Empleado.validar_materiales(materiales)

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

    @staticmethod
    def validar_proveedor(proveedor):
        if proveedor not in Proveedor.todos:
            raise ValueError("El proveedor no esta registrado")
    
