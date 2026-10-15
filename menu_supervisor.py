
from deposito import Deposito

class MenuSupervisor:
    def __init__(self, supervisor, tareas_pendientes_supervisor, tareas_pendientes_comprador, deposito):
        self.supervisor = supervisor
        self.tareas_supervisor = tareas_pendientes_supervisor
        self.tareas_comprador = tareas_pendientes_comprador
        self.depositos = deposito

    def mostrar(self):
        opcion = ""

        while opcion != "4":
            print("\n--- MENÚ SUPERVISOR DE DEPÓSITO ---")
            print("1. Ejecutar siguiente tarea pendiente")
            print("2. Revisar vencimientos")
            print("3. Consultar stock")
            print("4. Volver")

            opcion = input("Seleccione una opción: ")

            try:
                if opcion == "1":
                    self.ejecutar_tarea()

                elif opcion == "2":
                    self.revisar_vencimientos()

                elif opcion == "3":
                    self.consultar_stock()

                elif opcion != "4":
                    print("Opción inválida.")

            except (ValueError, TypeError) as error:
                print("Error:", error)
