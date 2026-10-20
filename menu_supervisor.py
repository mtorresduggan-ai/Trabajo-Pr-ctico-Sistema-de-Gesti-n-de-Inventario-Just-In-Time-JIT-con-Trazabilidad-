from supervisor import Supervisor

class MenuSupervisor:
    def __init__(self, supervisor, tareas_pendientes_supervisor, tareas_pendientes_comprador, deposito):
        self.Supervisor = supervisor
        self.tareas_pendientes_supervisor = tareas_pendientes_supervisor
        self.tareas_pendientes_comprador = tareas_pendientes_comprador
        self.deposito = deposito

    def menu_supervisor(self):
        opciones = {"1": self.Supervisor.mostrar_tareas,
            "2": lambda: self.Supervisor.ejecutar_siguiente_tarea(self.tareas_pendientes_supervisor, self.tareas_pendientes_comprador),
            "3": lambda: self.Supervisor.retirar_vencidos(self.deposito),
            "4": lambda: self.Supervisor.generar_reporte(self.deposito)}

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
                accion()


   