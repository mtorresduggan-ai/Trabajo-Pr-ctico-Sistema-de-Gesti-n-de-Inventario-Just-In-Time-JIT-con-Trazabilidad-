from gestor_archivos import GestorArchivos
from tarea import Tarea


class GestorTareas:

    def __init__(self, gestor_materiales, gestor_depositos, gestor_solicitudes, gestor_pedidos, gestor_remesas):
        self._gestor_materiales = gestor_materiales
        self._gestor_depositos = gestor_depositos
        self._gestor_solicitudes = gestor_solicitudes
        self._gestor_pedidos = gestor_pedidos
        self._gestor_remesas = gestor_remesas

    def fila_tarea_solicitud(self, tarea):
        return ["solicitud", tarea.get_objeto().get_id_solicitud(), "", "", "", ""]

    def fila_tarea_pedido(self, tarea):
        deposito = ""

        if tarea.get_datos() is not None:
            deposito = tarea.get_datos().get_nombre()

        return ["pedido", tarea.get_objeto().get_id_pedido(), deposito, "", "", ""]

    def fila_tarea_remesa(self, tarea):
        return ["remesa", tarea.get_objeto().get_id_remesa(), tarea.get_datos().get_nombre(), "", "", ""]

    def fila_tarea_reponer(self, tarea):
        return ["reponer", tarea.get_objeto().get_id_material(), "", "", "", ""]

    def fila_tarea_retirar(self, tarea):
        return ["retirar_vencidos", "", tarea.get_objeto().get_nombre(), "", "", ""]

    def fila_tarea_transferencia(self, tarea):
        origen, destino, materiales, cantidades = tarea.get_datos()

        ids_materiales = list(map(lambda material: str(material.get_id_material()), materiales))

        return ["transferencia", "",
            origen.get_nombre(),
            destino.get_nombre(),
            ";".join(ids_materiales),
            ";".join(map(str, cantidades))]

    def guardar_tareas(self, archivo, cola):
        funciones = {
            "solicitud": self.fila_tarea_solicitud,
            "pedido": self.fila_tarea_pedido,
            "remesa": self.fila_tarea_remesa,
            "reponer": self.fila_tarea_reponer,
            "retirar_vencidos": self.fila_tarea_retirar,
            "transferencia": self.fila_tarea_transferencia
        }

        filas = list(map(lambda tarea: funciones[tarea.get_tipo()](tarea), cola.obtener_tareas()))

        GestorArchivos.escribir_csv(archivo,
            ["tipo", "objeto_id", "deposito", "deposito_destino", "materiales", "cantidades"],
            filas)

    def cargar_tarea_solicitud(self, fila):
        return Tarea("solicitud", self._gestor_solicitudes.buscar_id(fila["objeto_id"]))

    def cargar_tarea_pedido(self, fila):
        datos = None

        if fila["deposito"]:
            datos = self._gestor_depositos.buscar_deposito(fila["deposito"])

        return Tarea("pedido", self._gestor_pedidos.buscar_id(fila["objeto_id"]), datos)

    def cargar_tarea_remesa(self, fila):
        return Tarea("remesa", self._gestor_remesas.buscar_id(fila["objeto_id"]), self._gestor_depositos.buscar_deposito(fila["deposito"]))

    def cargar_tarea_reponer(self, fila):
        return Tarea("reponer", self._gestor_materiales.buscar_id(fila["objeto_id"]))

    def cargar_tarea_retirar(self, fila):
        return Tarea("retirar_vencidos", self._gestor_depositos.buscar_deposito(fila["deposito"]))

    def cargar_tarea_transferencia(self, fila):
        origen = self._gestor_depositos.buscar_deposito(fila["deposito"])
        destino = self._gestor_depositos.buscar_deposito(fila["deposito_destino"])

        materiales = list(map(lambda id_material: self._gestor_materiales.buscar_id(id_material), fila["materiales"].split(";")))
        cantidades = list(map(float, fila["cantidades"].split(";")))

        return Tarea("transferencia", None, (origen, destino, materiales, cantidades))

    def cargar_tareas(self, archivo, cola):
        filas = GestorArchivos.leer_csv_dict(archivo)

        funciones = {
            "solicitud": self.cargar_tarea_solicitud,
            "pedido": self.cargar_tarea_pedido,
            "remesa": self.cargar_tarea_remesa,
            "reponer": self.cargar_tarea_reponer,
            "retirar_vencidos": self.cargar_tarea_retirar,
            "transferencia": self.cargar_tarea_transferencia}

        filas_validas = filter(lambda fila: fila["tipo"] in funciones, filas)
        tareas = map(lambda fila: funciones[fila["tipo"]](fila), filas_validas)

        for tarea in tareas:
            if tarea.get_objeto() is not None or tarea.get_tipo() == "transferencia":
                cola.agregar(tarea)

    def guardar_tareas_todas(self, tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor):
        self.guardar_tareas("tareas_admin.csv", tareas_admin)
        self.guardar_tareas("tareas_supervisor.csv", tareas_supervisor)
        self.guardar_tareas("tareas_comprador.csv", tareas_comprador)
        self.guardar_tareas("tareas_vendedor.csv", tareas_vendedor)

    def cargar_tareas_todas(self, tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor):
        self.cargar_tareas("tareas_admin.csv", tareas_admin)
        self.cargar_tareas("tareas_supervisor.csv", tareas_supervisor)
        self.cargar_tareas("tareas_comprador.csv", tareas_comprador)
        self.cargar_tareas("tareas_vendedor.csv", tareas_vendedor)