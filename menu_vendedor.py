from datetime import date
from menu import Menu


class MenuVendedor(Menu):
    def __init__(self, vendedor, tareas_vendedor, tareas_admin, sistema=None):
        super().__init__(tareas_comprador=None,
        tareas_vendedor=tareas_vendedor,
        tareas_supervisor=None,
        tareas_admin=tareas_admin, 
        sistema=sistema)
        self.vendedor = vendedor

    def menu_vendedor(self):
        opciones = {
            '1': self.input_crear_pedido,
            '2': lambda: self.vendedor.cancelar_pedido(self.pedir_int("ID del pedido a cancelar: "), self.sistema.get_pedidos()),
            '3': self.input_consultar_todos,
            '4': lambda: self.vendedor.consultar_pedido(self.pedir_int("ID del pedido: "), self.sistema.get_pedidos()),
            '5': self.input_modificar_pedido}

        self.pantalla("MENÚ VENDEDOR", [
            "1. Crear pedido de salida",
            "2. Cancelar pedido",
            "3. Consultar todos los pedidos",
            "4. Consultar pedido por ID",
            "5. Modificar pedido"], opciones)

    def input_crear_pedido(self):
        materiales, cantidades = self.input_materiales_cantidades(permitir_nuevo=False)
        cliente = self.input_cliente()

        pedido = self.vendedor.crear_pedido_salida(date.today(), materiales, cantidades, cliente, self.sistema.get_clientes(), self.tareas_admin)
        self.sistema.agregar_pedido(pedido)

        return f"\n ¡Pedido N° {pedido.get_id_pedido()} generado con éxito!"

    def input_consultar_todos(self):
        pedidos = self.vendedor.consultar_pedido_todos(self.sistema.get_pedidos())
        if not pedidos:
            return "\nNo tenés pedidos registrados."

        texto = "\n=== MIS PEDIDOS ===\n"
        for pedido in pedidos:
            texto += str(pedido) + "\n"
        return texto

    def input_modificar_pedido(self):
        id_movimiento = self.pedir_int("ID del pedido a modificar: ")
        print("\nDejá en blanco (presioná Enter) en los campos que NO quieras modificar:")

        actualizar_mat = self.pedir("¿Deseas modificar materiales y cantidades? (si/no): ").lower()
        if actualizar_mat == 'si':
            materiales, cantidades = self.input_materiales_cantidades(permitir_nuevo=False)
        else:
            materiales, cantidades = None, None

        fecha_str = self.pedir("Nueva fecha (YYYY-MM-DD): ")
        fecha = date.fromisoformat(fecha_str) if fecha_str else None

        actualizar_cli = self.pedir("¿Deseas modificar el cliente? (si/no): ").lower()
        cliente = self.input_cliente() if actualizar_cli == 'si' else None

        return self.vendedor.modificar_pedido(
            id_pedido=id_movimiento,
            pedidos=self.sistema.get_pedidos(),
            clientes=self.sistema.get_clientes(),
            materiales=materiales,
            cantidades=cantidades,
            fecha=fecha,
            cliente=cliente)