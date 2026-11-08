from gestor import Gestor
from gestor_archivos import GestorArchivos
from solicitud_proveedor import Solicitud_proveedor


class GestorSolicitudes(Gestor):

    def __init__(self, gestor_materiales, gestor_proveedores, gestor_empleados):
        super().__init__()
        self._gestor_materiales = gestor_materiales
        self._gestor_proveedores = gestor_proveedores
        self._gestor_empleados = gestor_empleados

    def agregar_solicitud(self, solicitud):
        self.registrar(solicitud.get_id_solicitud(), solicitud, "solicitud")

    def get_solicitudes(self):
        return list(self._elementos.values())

    def guardar_solicitudes(self):
        solicitudes = self.get_solicitudes()
        filas = list(map(lambda solicitud: solicitud.a_fila(), solicitudes))
        filas_items = []

        for solicitud in solicitudes:
            materiales = solicitud.get_materiales()
            cantidades = solicitud.get_cantidades()
            precios = solicitud.get_precios_unitarios()

            filas_items += list(map(lambda i: [solicitud.get_id_solicitud(), materiales[i].get_id_material(),
                cantidades[i], precios[i]], range(len(materiales))))

        GestorArchivos.escribir_csv("solicitudes.csv",
            ["id", "fecha", "proveedor_id", "estado", "comprador_id", "fecha_envio"], filas)

        GestorArchivos.escribir_csv("solicitudes_items.csv",
            ["solicitud_id", "material_id", "cantidad", "precio_unitario"], filas_items)

    def cargar_solicitudes(self):
        filas = GestorArchivos.leer_csv_dict("solicitudes.csv")
        filas_items = GestorArchivos.leer_csv_dict("solicitudes_items.csv")

        for fila in filas:
            items = list(filter(lambda item: item["solicitud_id"] == fila["id"]
                and self._gestor_materiales.buscar_id(item["material_id"]) is not None, filas_items))

            materiales = list(map(lambda item: self._gestor_materiales.buscar_id(item["material_id"]), items))
            cantidades = list(map(lambda item: float(item["cantidad"]), items))
            precios = list(map(lambda item: float(item["precio_unitario"]), items))

            self.agregar_solicitud(Solicitud_proveedor(
                self._gestor_proveedores.buscar_id(fila["proveedor_id"]),
                GestorArchivos.convertir_fecha(fila["fecha"]), materiales, cantidades,
                fila["estado"],
                self._gestor_empleados.buscar_id(fila["comprador_id"]),
                id_manual=fila["id"],
                fecha_envio_manual=GestorArchivos.convertir_fecha(fila["fecha_envio"]),
                precios_unitarios=precios))