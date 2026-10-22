
from empleado import Empleado
from solicitud_proveedor import Solicitud_proveedor
from proveedor import Proveedor
from tarea import Tarea


class Comprador(Empleado):

    def __init__(self, nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja=None, id_manual=None):
        super().__init__(nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja, id_manual)
    

    def crear_solicitud(self, fecha, materiales, cantidades, proveedor, tareas_pendientes_admin):
        Empleado.validar_fecha(fecha)
        Empleado.validar_cantidades(cantidades)
        Empleado.validar_materiales(materiales)
        self.validar_proveedor(proveedor)
        self.validar_listas(materiales, cantidades)

        solicitud = Solicitud_proveedor(proveedor, fecha, materiales, cantidades, "Pendiente", self)

        tareas_pendientes_admin.agregar(Tarea('solicitud', solicitud))

        proveedor.agregar_material(solicitud.get_material(),solicitud.get_precio_unitario())

        return solicitud

    def consultar_solicitudes_todas(self):
        return list(
            filter(lambda s: s.get_comprador() == self, Solicitud_proveedor.todos))


    def consultar_solicitud(self, id_movimiento):
        solicitudes = list(filter(lambda s: (s.get_comprador() == self and s.get_id_movimiento() == id_movimiento), Solicitud_proveedor.todos))

        if not solicitudes:
            raise ValueError("No existe esa solicitud")
        return solicitudes[0]

    def cancelar_solicitud(self, id_movimiento):
        solicitud = self.consultar_solicitud(id_movimiento)

        if solicitud.get_estado() in ("Recibido", "Cancelado"):
            raise ValueError(
                f"No se puede cancelar una solicitud en estado "
                f"'{solicitud.get_estado()}'")

        solicitud.set_estado("Cancelado")
        return solicitud

    def modificar_solicitud(self, id_movimiento, materiales=None, cantidades=None, fecha=None, proveedor=None, estado=None):
        solicitud = self.consultar_solicitud(id_movimiento)

        if solicitud.get_estado() in ("Recibido", "Cancelado"):
            raise ValueError(f"No se puede modificar una solicitud en estado '{solicitud.get_estado()}'")

        parametros = {"materiales": (materiales, self.validar_materiales, solicitud.set_materiales),
            "cantidades": (cantidades, self.validar_cantidades, solicitud.set_cantidades),
            "fecha": (fecha, self.validar_fecha, solicitud.set_fecha),
            "proveedor": (proveedor, self.validar_proveedor, solicitud.set_proveedor),
            "estado": (estado, Solicitud_proveedor.validar_estado, solicitud.set_estado)}

        for valor, validar, set_valor in parametros.values():
            if valor is not None:
                validar(valor)
                set_valor(valor)

        return solicitud

    def ejecutar_siguiente_tarea(self, tareas_pendientes_comprador, fecha, proveedor, tareas_pendientes_admin):
        tarea = tareas_pendientes_comprador.ver_primera()

        if tarea is None:
            raise ValueError("No hay tareas pendientes")

        if tarea.get_tipo() == "reponer":
            material = tarea.get_objeto()

            self.crear_solicitud(
                fecha,
                [material],
                [material.get_punto_reposicion()],
                proveedor,
                tareas_pendientes_admin
            )
        
        else:
            raise ValueError('Tipo de tarea desconocido')

        tareas_pendientes_comprador.sacar()

    @staticmethod
    def validar_proveedor(proveedor):
        if proveedor not in Proveedor.todos:
            raise ValueError("El proveedor no esta registrado")

    @staticmethod
    def validar_listas(materiales, cantidades):
        if len(materiales) != len(cantidades):
            raise ValueError("Debe haber una cantidad por cada material")
