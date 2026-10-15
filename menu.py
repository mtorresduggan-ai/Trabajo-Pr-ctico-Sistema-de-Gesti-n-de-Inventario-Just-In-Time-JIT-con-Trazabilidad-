from menu_comprador import MenuComprador

class Menu:
    def __init__(self, comprador, vendedor, administrador, supervisor, tareas_pendientes_comprador, tareas_pendientes_supervisor, tareas_pendientes_admin):

        self.comprador = MenuComprador(comprador, tareas_pendientes_comprador, tareas_pendientes_admin)
        self.vendedor = vendedor
        self.administrador = administrador
        self.supervisor = supervisor
        self.tareas_comprador = tareas_pendientes_comprador
        self.tareas_supervisor = tareas_pendientes_supervisor

    def mostrar_menu(self):
        opcion = ""

        while opcion != "5":
            print("\n--- SISTEMA DE GESTIÓN DE DEPÓSITOS EMPLEADOS ---")
            print("1. Comprador")
            print("2. Vendedor")
            print("3. Administrador")
            print("4. Supervisor de depósito")
            print("5. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.menu_comprador()

            elif opcion == "2":
                self.menu_vendedor()

            elif opcion == "3":
                self.menu_administrador()

            elif opcion == "4":
                self.menu_supervisor()

            elif opcion == "5":
                print("Fin del programa.")

            else:
                print("Opción inválida.")