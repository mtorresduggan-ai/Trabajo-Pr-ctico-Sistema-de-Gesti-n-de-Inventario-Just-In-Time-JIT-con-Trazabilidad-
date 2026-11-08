from gestor import Gestor
from gestor_archivos import GestorArchivos
from pedido import Pedido_salida


class GestorPedidos(Gestor):

    def __init__(self, gestor_materiales, gestor_clientes, gestor_empleados):
        super().__init__()
        self._gestor_materiales = gestor_materiales
        self._gestor_clientes = gestor_clientes
        self._gestor_empleados = gestor_empleados

    def agregar_pedido(self, pedido):
        self.registrar(pedido.get_id_pedido(), pedido, "pedido")

    def get_pedidos(self):
        return list(self._elementos.values())

    def guardar_pedidos(self):
        pedidos = self.get_pedidos()
        filas = list(map(lambda pedido: pedido.a_fila(), pedidos))
        filas_items = []

        for pedido in pedidos:
            materiales = pedido.get_materiales()
            cantidades = pedido.get_cantidades()
            precios = pedido.get_precios_unitarios()

            filas_items += list(map(lambda i: [pedido.get_id_pedido(), materiales[i].get_id_material(),
                cantidades[i], precios[i]], range(len(materiales))))

        GestorArchivos.escribir_csv("pedidos.csv",
            ["id", "fecha", "cliente_id", "estado", "vendedor_id", "fecha_aceptacion", "fecha_envio"], filas)

        GestorArchivos.escribir_csv("pedidos_items.csv",
            ["pedido_id", "material_id", "cantidad", "precio_unitario"], filas_items)

    def cargar_pedidos(self):
        filas = GestorArchivos.leer_csv_dict("pedidos.csv")
        filas_items = GestorArchivos.leer_csv_dict("pedidos_items.csv")

        for fila in filas:
            items = list(filter(lambda item: item["pedido_id"] == fila["id"]
                and self._gestor_materiales.buscar_id(item["material_id"]) is not None, filas_items))

            materiales = list(map(lambda item: self._gestor_materiales.buscar_id(item["material_id"]), items))
            cantidades = list(map(lambda item: float(item["cantidad"]), items))
            precios = list(map(lambda item: float(item["precio_unitario"]), items))

            self.agregar_pedido(Pedido_salida(
                GestorArchivos.convertir_fecha(fila["fecha"]), materiales, cantidades, precios,
                self._gestor_clientes.buscar_id(fila["cliente_id"]),
                fila["estado"],
                self._gestor_empleados.buscar_id(fila["vendedor_id"]),
                id_manual=fila["id"],
                fecha_aceptacion_manual=GestorArchivos.convertir_fecha(fila["fecha_aceptacion"]),
                fecha_envio_manual=GestorArchivos.convertir_fecha(fila["fecha_envio"])))