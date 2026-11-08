from gestor import Gestor
from gestor_archivos import GestorArchivos
from comprador import Comprador
from vendedor import Vendedor
from administrador import Administrador
from supervisor import Supervisor


class GestorEmpleados(Gestor):

    def agregar_empleado(self, empleado):
        self.registrar(empleado.get_id(), empleado, "empleado")

    def get_empleados(self):
        return list(self._elementos.values())

    def autenticar(self, usuario, clave):
        coincidencias = list(filter(lambda empleado: empleado.get_fecha_baja() is None
            and empleado.get_usuario() == usuario
            and empleado.get_clave() == clave, self.get_empleados()))

        if len(coincidencias) == 0:
            raise ValueError("Usuario o contraseña incorrectos")

        return coincidencias[0]

    def guardar_empleados(self):
        filas = list(map(lambda empleado: empleado.a_fila() + [type(empleado).__name__], self.get_empleados()))

        GestorArchivos.escribir_csv("empleados.csv",
            ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja", "usuario", "clave", "tipo"],
            filas)

    def cargar_empleados(self):
        filas = GestorArchivos.leer_csv_dict("empleados.csv")

        clases = {"Comprador": Comprador,
            "Vendedor": Vendedor,
            "Administrador": Administrador,
            "Supervisor": Supervisor}

        for fila in filas:
            if fila["tipo"] not in clases:
                continue

            clase = clases[fila["tipo"]]
            self.agregar_empleado(clase(fila["nombre"], fila["telefono"], int(fila["dni"]),
                GestorArchivos.convertir_fecha(fila["fecha_alta"]), fila["email"], fila["usuario"], fila["clave"],
                fecha_baja=GestorArchivos.convertir_fecha(fila["fecha_baja"]), id_manual=fila["id"]))