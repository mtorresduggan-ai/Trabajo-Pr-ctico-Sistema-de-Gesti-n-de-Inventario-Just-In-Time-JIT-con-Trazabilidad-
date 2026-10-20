from supervisor import Supervisor

class MenuSupervisor:
    def __init__(self, supervisor, tareas_pendientes_supervisor, tareas_pendientes_comprador, deposito):
        self.supervisor = supervisor
        self.tareas_pendientes_supervisor = tareas_pendientes_supervisor
        self.tareas_pendientes_comprador = tareas_pendientes_comprador
        self.deposito = deposito

    def menu_supervisor(self):
        opciones = {"1": lambda: self.supervisor.mostrar_tareas_pendientes(self.tareas_pendientes_supervisor),
            "2": lambda: self.supervisor.ejecutar_siguiente_tarea(self.tareas_pendientes_supervisor, self.tareas_pendientes_comprador),
            "3": lambda: self.supervisor.revisar_vencimientos(self.deposito, self.tareas_pendientes_supervisor),
            "4": lambda: self.supervisor.generar_reporte_stock(self.deposito)}

        while True:
            print("\n--- MENÚ SUPERVISOR ---")
            print("1. Mostrar tareas pendientes y cantidades")
            print("2. Ejecutar siguiente tarea")
            print("3. Revisar vencidos")
            print("4. Generar reporte")
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


   