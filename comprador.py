from empleado import Empleado
from solicitud_proveedor import Solicitud_proveedor
from proveedor import Proveedor
from tarea import Tarea


class Comprador(Empleado):

    def __init__(self, nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja=None, id_manual=None):
        super().__init__(nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja, id_manual)
    
    def crear_solicitud(self, fecha, materiales, cantidades, proveedor, tareas_pendientes_admin, precios_unitarios, precios):
        Empleado.validar_fecha(fecha)
        Empleado.validar_cantidades(cantidades)
        Empleado.validar_materiales(materiales)
        self.validar_proveedor(proveedor)
        self.validar_listas(materiales, cantidades)

        if len(materiales) != len(precios_unitarios):
            raise ValueError("Debe haber un precio por cada material")

        for precio in precios_unitarios:
            proveedor.validar_precio(precio)

        solicitud = Solicitud_proveedor(proveedor, fecha, materiales, cantidades, "Pendiente", self, precios_unitarios=precios_unitarios)

        tareas_pendientes_admin.agregar(Tarea('solicitud', solicitud))

        for material, precio in zip(materiales, precios_unitarios):
            proveedor.agregar_material(material, precio)
            precios.agregar_precio(material, proveedor)
        
        return solicitud


    def consultar_solicitudes_todas(self, solicitudes):
        return [s for s in solicitudes if s.get_comprador() == self]


    def consultar_solicitud(self, id_solicitud, solicitudes):
        for solicitud in solicitudes:
            if (solicitud.get_comprador() == self
                    and solicitud.get_id_solicitud() == id_solicitud):
                return solicitud

        raise ValueError("No existe esa solicitud")


    def cancelar_solicitud(self, id_solicitud, solicitudes):
        solicitud = self.consultar_solicitud(id_solicitud, solicitudes)

        if solicitud.get_estado() in ("Recibido", "Cancelado"):
            raise ValueError(f"No se puede cancelar una solicitud en estado "f"'{solicitud.get_estado()}'")

        solicitud.set_estado("Cancelado")
        return solicitud


    def modificar_solicitud(self, id_solicitud, solicitudes, materiales=None,cantidades=None, fecha=None, proveedor=None, estado=None):
        solicitud = self.consultar_solicitud(id_solicitud, solicitudes)

        if solicitud.get_estado() in ("Recibido", "Cancelado"):
            raise ValueError(f"No se puede modificar una solicitud en estado "f"'{solicitud.get_estado()}'")

        parametros = {
            "materiales": (materiales, self.validar_materiales, solicitud.set_materiales),
            "cantidades": (cantidades, self.validar_cantidades, solicitud.set_cantidades),
            "fecha": (fecha, self.validar_fecha, solicitud.set_fecha),
            "proveedor": (proveedor, self.validar_proveedor, solicitud.set_proveedor),
            "estado": (estado, Solicitud_proveedor.validar_estado, solicitud.set_estado)}

        for valor, validar, set_valor in parametros.values():
            if valor is not None:
                validar(valor)
                set_valor(valor)

        return solicitud


    @staticmethod
    def validar_proveedor(proveedor, proveedores):
        if proveedor not in proveedores:
            raise ValueError("El proveedor no esta registrado")


    def ejecutar_siguiente_tarea(self, tareas_pendientes_comprador, fecha, proveedor, tareas_pendientes_admin, precios):
        tarea = tareas_pendientes_comprador.ver_primera()

        if tarea is None:
            raise ValueError("No hay tareas pendientes")

        if tarea.get_tipo() == "reponer":
            material = tarea.get_objeto()

            precio = proveedor.obtener_precio(material)

            self.crear_solicitud(fecha,
                [material],
                [material.get_punto_reposicion()],
                proveedor,
                tareas_pendientes_admin,
                [precio],
                precios)
        
        else:
            raise ValueError('Tipo de tarea desconocido')

        tareas_pendientes_comprador.sacar()

    @staticmethod
    def validar_listas(materiales, cantidades):
        if len(materiales) != len(cantidades):
            raise ValueError("Debe haber una cantidad por cada material")
