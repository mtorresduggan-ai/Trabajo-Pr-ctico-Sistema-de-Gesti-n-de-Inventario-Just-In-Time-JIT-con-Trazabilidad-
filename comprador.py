from empleado import Empleado
from solicitud_proveedor import Solicitud_proveedor
from proveedor import Proveedor
from tarea import Tarea

class Comprador(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email, usuario, clave):
        super().__init__(nombre, telefono, dni, fecha_alta, email, usuario, clave)

    def crear_solicitud(self, fecha, materiales, cantidades, proveedor, tareas_pendientes_admin):
        Empleado.validar_fecha(fecha)
        Empleado.validar_cantidades(cantidades)
        Empleado.validar_materiales(materiales)
        self.validar_proveedor(proveedor)
        self.validar_listas(materiales, cantidades)

        solicitud = Solicitud_proveedor(proveedor, fecha, materiales, cantidades, "Pendiente", self)

        tareas_pendientes_admin.agregar(Tarea('solicitud', solicitud))
        
        return solicitud

    def consultar_solicitudes(self):
        return list(filter(lambda s: s.comprador == self, Solicitud_proveedor.todos))

    def consultar_solicitud(self, id_movimiento):
        solicitudes = list(filter(lambda s: s.comprador == self and s.id_movimiento == id_movimiento, Solicitud_proveedor.todos))
        if not solicitudes:
            raise ValueError("No existe esa solicitud")
        return solicitudes[0]

    def cancelar_solicitud(self, id_movimiento):
        solicitud = self.consultar_solicitud(id_movimiento)
        
        if solicitud.estado in ("Entregado", "Cancelado"):
            raise ValueError(f"No se puede cancelar una solicitud en estado '{solicitud.estado}'")
        
        solicitud.estado = "Cancelado"

        return solicitud

    def modificar_solicitud(self, id_movimiento, materiales=None, cantidades=None, fecha=None, proveedor=None, estado=None):
        solicitud = self.consultar_solicitud(id_movimiento)
        
        if solicitud.estado in ("Entregado", "Cancelado"):
            raise ValueError(f"No se puede modificar una solicitud en estado '{solicitud.estado}'")

        if materiales is not None:
            Empleado.validar_materiales(materiales)
            solicitud.materiales = materiales
        if cantidades is not None:
            Empleado.validar_cantidades(cantidades)
            solicitud.cantidades = cantidades
        if fecha is not None:
            Empleado.validar_fecha(fecha)
            solicitud.fecha = fecha
        if proveedor is not None:
            self.validar_proveedor(proveedor)
            solicitud.proveedor = proveedor
        if estado is not None:
            Solicitud_proveedor.validar_estado(estado)
            solicitud.estado = estado

        return solicitud

    @staticmethod
    def validar_proveedor(proveedor):
        if proveedor not in Proveedor.todos:
            raise ValueError("El proveedor no esta registrado")
        
    @staticmethod 
    def validar_listas(materiales, cantidades):
        if len(materiales) != len(cantidades):
            raise ValueError("Debe haber una cantidad por cada material")