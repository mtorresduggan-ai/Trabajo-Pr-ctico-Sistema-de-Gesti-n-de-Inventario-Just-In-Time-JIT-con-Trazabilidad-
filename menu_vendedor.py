from datetime import date
from menu import Menu


class MenuVendedor(Menu):
    def __init__(self, vendedor, tareas_pendientes_vendedor, tareas_pendientes_admin):
        super().__init__(tareas_pendientes_admin)  # Inicializa el atributo heradedo tareas_pendientes_admin
        self.vendedor = vendedor
        self.tareas_pendientes_vendedor = tareas_pendientes_vendedor

    def menu_vendedor(self):
        opciones = {'1': lambda: self.vendedor.mostrar_tareas(self.tareas_pendientes_vendedor),
            '2': lambda: self.vendedor.ejecutar_siguiente_tarea(self.tareas_pendientes_vendedor),
            '3': lambda: self.vendedor.crear_pedido_salida(date.today(), *self.input_materiales_cantidades(), self.input_cliente(), self.tareas_pendientes_admin),
            '4': lambda: self.vendedor.cancelar_pedido(int(input("ID del pedido a cancelar: "))),
            '5': self.vendedor.consultar_pedido_todos,
            '6': lambda: self.vendedor.consultar_pedido(int(input("ID del pedido: "))),
            '7': self.input_modificar_pedido}

        while True:
            print("\n--- MENÚ VENDEDOR ---")
            print("1. Mostrar tareas pendientes")
            print("2. Ejecutar siguiente tarea")
            print("3. Crear pedido de salida")
            print("4. Cancelar pedido")
            print("5. Consultar todos los pedidos")
            print("6. Consultar pedido por ID")
            print("7. Modificar pedido")
            print("0. Salir")

            opcion = input("Elegí una opción: ")

            if opcion == "0":
                break

            accion = opciones.get(opcion)

            if accion is None:
                print("Opción inválida.")
            else:
                try:
                    resultado = accion()
                    if resultado is not None:
                        print(resultado)
                except (ValueError, TypeError) as error:
                    print(f"Error: {error}")

    def input_modificar_pedido(self):
        id_movimiento = int(input("ID del pedido a modificar: "))
        print("\nDejá en blanco (presioná Enter) en los campos que NO quieras modificar:")

        actualizar_mat = input("¿Deseas modificar materiales y cantidades? (si/no): ").strip().lower()
        if actualizar_mat == 'si':
            materiales, cantidades = self.input_materiales_cantidades()
        else:
            materiales, cantidades = None, None

        fecha_str = input("Nueva fecha (YYYY-MM-DD): ").strip()
        fecha = date.fromisoformat(fecha_str) if fecha_str else None

        actualizar_cli = input("¿Deseas modificar el cliente? (si/no): ").strip().lower()
        cliente = self.input_cliente() if actualizar_cli == 'si' else None

        estado_str = input("Nuevo estado: ").strip()
        estado = estado_str if estado_str else None

        return self.vendedor.modificar_pedido(
            id_movimiento=id_movimiento,
            materiales=materiales,
            cantidades=cantidades,
            fecha=fecha,
            cliente=cliente,
            estado=estado)