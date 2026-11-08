from gestor import Gestor
from gestor_archivos import GestorArchivos
from cliente import Cliente


class GestorClientes(Gestor):

    def agregar_cliente(self, cliente):
        self.registrar(cliente.get_id(), cliente, "cliente")

    def get_clientes(self):
        return list(self._elementos.values())

    def guardar_clientes(self):
        self.guardar_csv("clientes.csv",
            ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja"],
            self.get_clientes())

    def cargar_clientes(self):
        filas = GestorArchivos.leer_csv_dict("clientes.csv")

        for fila in filas:
            self.agregar_cliente(Cliente(fila["nombre"],
                fila["telefono"],
                int(fila["dni"]),
                fila["email"],
                GestorArchivos.convertir_fecha(fila["fecha_alta"]),
                fecha_baja=GestorArchivos.convertir_fecha(fila["fecha_baja"]),
                id_manual=fila["id"]))