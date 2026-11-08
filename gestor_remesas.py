from gestor import Gestor
from gestor_archivos import GestorArchivos
from remesa import Remesa


class GestorRemesas(Gestor):

    def __init__(self, gestor_materiales, gestor_proveedores, gestor_solicitudes):
        super().__init__()
        self._gestor_materiales = gestor_materiales
        self._gestor_proveedores = gestor_proveedores
        self._gestor_solicitudes = gestor_solicitudes

    def agregar_remesa(self, remesa):
        self.registrar(remesa.get_id_remesa(), remesa, "remesa")

    def get_remesas(self):
        return list(self._elementos.values())

    def guardar_remesas(self):
        remesas = self.get_remesas()
        filas = list(map(lambda remesa: remesa.a_fila(), remesas))
        filas_items = []

        for remesa in remesas:
            materiales = remesa.get_materiales()
            cantidades = remesa.get_cantidades()
            fechas = remesa.get_fechas_vencimiento()

            filas_items += list(map(lambda i: [remesa.get_id_remesa(), materiales[i].get_id_material(),
                cantidades[i], fechas[i]], range(len(materiales))))

        GestorArchivos.escribir_csv("remesas.csv",
            ["id", "proveedor_id", "solicitud_id", "fecha_llegada"], filas)
        GestorArchivos.escribir_csv("remesas_items.csv",
            ["remesa_id", "material_id", "cantidad", "fecha_vencimiento"], filas_items)

    def cargar_remesas(self):
        filas = GestorArchivos.leer_csv_dict("remesas.csv")
        filas_items = GestorArchivos.leer_csv_dict("remesas_items.csv")

        for fila in filas:
            items = list(filter(lambda item: item["remesa_id"] == fila["id"]
                and self._gestor_materiales.buscar_id(item["material_id"]) is not None, filas_items))

            materiales = list(map(lambda item: self._gestor_materiales.buscar_id(item["material_id"]), items))
            cantidades = list(map(lambda item: float(item["cantidad"]), items))
            fechas = list(map(lambda item: GestorArchivos.convertir_fecha(item["fecha_vencimiento"]), items))

            self.agregar_remesa(Remesa(materiales,
                self._gestor_proveedores.buscar_id(fila["proveedor_id"]),
                self._gestor_solicitudes.buscar_id(fila["solicitud_id"]),
                cantidades, fechas, None, None,
                GestorArchivos.convertir_fecha(fila["fecha_llegada"]),
                id_manual=fila["id"], cargando=True))