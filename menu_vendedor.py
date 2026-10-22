from datetime import date
from menu import Menu


class MenuVendedor(Menu):
    def __init__(self, vendedor, tareas_pendientes_vendedor, tareas_pendientes_admin):
        super().__init__(tareas_pendientes_comprador=None,
        tareas_pendientes_vendedor=tareas_pendientes_vendedor,
        tareas_pendientes_supervisor=None,
        tareas_pendientes_admin=tareas_pendientes_admin)
        self.vendedor = vendedor

        def menu_vendedor(self):
            opciones = {
                '1': lambda: self.vendedor.crear_pedido_salida(date.today(), *self.input_materiales_cantidades(), self.input_cliente(), self.tareas_pendientes_admin),
                '2': lambda: self.vendedor.cancelar_pedido(self.pedir_int("ID del pedido a cancelar: ")),
                '3': self.vendedor.consultar_pedido_todos,
                '4': lambda: self.vendedor.consultar_pedido(self.pedir_int("ID del pedido: ")),
                '5': self.input_modificar_pedido}

            self.pantalla("MENÚ VENDEDOR", [
                "1. Crear pedido de salida",
                "2. Cancelar pedido",
                "3. Consultar todos los pedidos",
                "4. Consultar pedido por ID",
                "5. Modificar pedido"], opciones)

    def input_modificar_pedido(self):
        id_movimiento = self.pedir_int("ID del pedido a modificar: ")
        print("\nDejá en blanco (presioná Enter) en los campos que NO quieras modificar:")

        actualizar_mat = self.pedir("¿Deseas modificar materiales y cantidades? (si/no): ").lower()
        if actualizar_mat == 'si':
            materiales, cantidades = self.input_materiales_cantidades()
        else:
            materiales, cantidades = None, None

        fecha_str = self.pedir("Nueva fecha (YYYY-MM-DD): ")
        fecha = date.fromisoformat(fecha_str) if fecha_str else None

        actualizar_cli = self.pedir("¿Deseas modificar el cliente? (si/no): ").lower()
        cliente = self.input_cliente() if actualizar_cli == 'si' else None

        estado_str = self.pedir("Nuevo estado: ")
        estado = estado_str if estado_str else None

        return self.vendedor.modificar_pedido(
            id_movimiento=id_movimiento,
            materiales=materiales,
            cantidades=cantidades,
            fecha=fecha,
            cliente=cliente,
            estado=estado)