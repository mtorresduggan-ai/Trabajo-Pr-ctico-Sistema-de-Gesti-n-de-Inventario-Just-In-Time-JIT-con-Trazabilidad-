from datetime import date
from menu import Menu


class MenuComprador(Menu):
    def __init__(self, comprador, tareas_pendientes_comprador, tareas_pendientes_admin):
        super().__init__(tareas_pendientes_comprador=tareas_pendientes_comprador,
            tareas_pendientes_vendedor=None,
            tareas_pendientes_supervisor=None,
            tareas_pendientes_admin=tareas_pendientes_admin)
        self.comprador = comprador
        self.tareas_pendientes_comprador = tareas_pendientes_comprador

    def menu_comprador(self):
        opciones= {'1': lambda: self.tareas_pendientes_comprador.mostrar_cantidades(),
                  '2': lambda: self.comprador.ejecutar_siguiente_tarea(self.tareas_pendientes_comprador,date.today(),self.input_proveedor(),self.tareas_pendientes_admin),
                  '3': lambda: self.comprador.crear_solicitud(date.today(),*self.input_materiales_cantidades(),self.input_proveedor(),self.tareas_pendientes_admin),
                  '4': lambda: self.comprador.cancelar_solicitud(int(input("ID de solicitud a cancelar: "))),
                  '5': self.comprador.consultar_solicitudes_todas,
                  '6': lambda: self.comprador.consultar_solicitud(int(input("ID de solicitud: "))),
                  '7': self.input_modificar_solicitud}

        while True:
            print("\n--- MENÚ COMPRADOR ---")
            print("1. Mostrar tareas pendientes")
            print("2. Ejecutar siguiente tarea")
            print("3. Crear solicitud")
            print("4. Cancelar solicitud")
            print("5. Consultar todas las solicitudes")
            print("6. Consultar solicitud por ID")
            print("7. Modificar solicitud")
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

    def input_modificar_solicitud(self):
        id_movimiento = int(input("ID de la solicitud a modificar: "))
        print("\n Dejá en blanco (presioná Enter) en los campos que NO quieras modificar:")
        
        actualizar_mat = input("¿Deseas modificar materiales y cantidades? (si/no): ").strip().lower()
        if actualizar_mat == 'si':
            materiales, cantidades = self.input_materiales_cantidades()
        else:
            materiales, cantidades = None, None

        fecha_str = input("Nueva fecha (YYYY-MM-DD): ").strip()
        fecha = date.fromisoformat(fecha_str) if fecha_str else None

        actualizar_prov = input("¿Deseas modificar el proveedor? (si/no): ").strip().lower()
        proveedor = self.input_proveedor() if actualizar_prov == 'si' else None

        estado_str = input("Nuevo estado: ").strip()
        estado = estado_str if estado_str else None

        return self.comprador.modificar_solicitud(
            id_movimiento=id_movimiento,
            materiales=materiales,
            cantidades=cantidades,
            fecha=fecha,
            proveedor=proveedor,
            estado=estado)