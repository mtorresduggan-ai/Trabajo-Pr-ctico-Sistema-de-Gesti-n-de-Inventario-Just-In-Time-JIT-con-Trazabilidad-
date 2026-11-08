from gestor import Gestor
from gestor_archivos import GestorArchivos
from deposito import Deposito


class GestorDepositos(Gestor):

    def __init__(self, gestor_materiales):
        super().__init__()
        self._gestor_materiales = gestor_materiales

    def agregar_deposito(self, deposito):
        self.registrar(deposito.get_nombre(), deposito, "depósito")

    def get_depositos(self):
        return list(self._elementos.values())

    def buscar_deposito(self, nombre):
        return self._elementos.get(nombre)

    def guardar_depositos(self):
        filas = list(map(lambda deposito: [deposito.get_nombre()], self.get_depositos()))
        GestorArchivos.escribir_csv("depositos.csv", ["nombre"], filas)

    def cargar_depositos(self):
        self._elementos = {}
        filas = GestorArchivos.leer_csv_dict("depositos.csv")

        for fila in filas:
            self.agregar_deposito(Deposito(fila["nombre"]))

    def guardar_stock(self):
        filas = []

        for deposito in self.get_depositos():
            for material in deposito.get_materiales():
                filas += list(map(lambda caja: [deposito.get_nombre(), material.get_id_material(), caja[0], caja[1]],
                    deposito.obtener_cajas(material)))

        GestorArchivos.escribir_csv("stock.csv", ["deposito", "material_id", "fecha_vencimiento", "cantidad"], filas)

    def cargar_stock(self):
        filas = GestorArchivos.leer_csv_dict("stock.csv")

        for fila in filas:
            deposito = self.buscar_deposito(fila["deposito"])
            material = self._gestor_materiales.buscar_id(fila["material_id"])

            if deposito is None:
                raise ValueError("No se encontró el depósito")

            if material is None:
                raise ValueError("No se encontró el material")

            deposito.ingresar(material,
                GestorArchivos.convertir_fecha(fila["fecha_vencimiento"]),
                float(fila["cantidad"]))