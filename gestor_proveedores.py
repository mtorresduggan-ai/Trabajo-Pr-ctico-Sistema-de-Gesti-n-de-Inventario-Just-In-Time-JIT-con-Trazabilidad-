from gestor import Gestor
from gestor_archivos import GestorArchivos
from proveedor import Proveedor


class GestorProveedores(Gestor):

    def __init__(self, gestor_materiales):
        super().__init__()
        self._gestor_materiales = gestor_materiales

    def agregar_proveedor(self, proveedor):
        self.registrar(proveedor.get_id(), proveedor, "proveedor")

    def get_proveedores(self):
        return list(self._elementos.values())

    def guardar_proveedores(self):
        self.guardar_csv("proveedores.csv",
            ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja", "plazo_estimado", "puntaje"],
            self.get_proveedores())

    def cargar_proveedores(self):
        filas = GestorArchivos.leer_csv_dict("proveedores.csv")

        for fila in filas:
            self.agregar_proveedor(Proveedor(fila["nombre"],
                int(fila["plazo_estimado"]),
                fila["telefono"],
                int(fila["dni"]),
                fila["email"],
                GestorArchivos.convertir_fecha(fila["fecha_alta"]),
                fecha_baja=GestorArchivos.convertir_fecha(fila["fecha_baja"]),
                id_manual=fila["id"],
                puntaje_manual=fila["puntaje"]))

    def guardar_precios_proveedores(self):
        filas = []

        for proveedor in self.get_proveedores():
            precios = proveedor.get_precios_materiales()
            filas += list(map(lambda par: [proveedor.get_id(), par[0], par[1]], precios.items()))

        GestorArchivos.escribir_csv("proveedores_precios.csv",
            ["proveedor_id", "material_id", "precio"], filas)

    def cargar_precios_proveedores(self):
        filas = GestorArchivos.leer_csv_dict("proveedores_precios.csv")

        for fila in filas:
            proveedor = self.buscar_id(fila["proveedor_id"])
            material = self._gestor_materiales.buscar_id(fila["material_id"])

            if proveedor is not None and material is not None:
                proveedor.agregar_material(material, float(fila["precio"]))