from menu_comprador import MenuComprador
from menu_supervisor import MenuSupervisor
from deposito import Deposito

class Menu:
    def __init__(self, comprador, vendedor, administrador, supervisor, tareas_pendientes_comprador, tareas_pendientes_supervisor, tareas_pendientes_admin):

        self.Comprador = comprador
        self.Vendedor = vendedor
        self.Administrador = administrador
        self.Supervisor = supervisor
        self.tareas_pendientes_comprador = tareas_pendientes_comprador
        self.tareas_pendientes_supervisor = tareas_pendientes_supervisor
        self.tareas_pendientes_admin = tareas_pendientes_admin

    def mostrar_menu(self):
        opciones = {"1": lambda: MenuComprador(self.Comprador,Deposito.seleccionar_deposito(), self.tareas_pendientes_comprador).menu_comprador(),
            "2": lambda: MenuVendedor(self.Vendedor, Deposito.seleccionar_deposito()).menu_vendedor(),
            "3": lambda: MenuAdministrador(self.Administrador, self.tareas_pendientes_admin).menu_administrador(),
            "4": lambda: MenuSupervisor(self.Supervisor, Deposito.seleccionar_deposito(),self.tareas_pendientes_supervisor,self.tareas_pendientes_comprador).menu_supervisor()}

        while True:
            print("\n--- MENÚ ---")
            print("1. Comprador")
            print("2. Vendedor")
            print("3. Administrador")
            print("4. Supervisor")
            print("0. Salir")

            opcion = input("Elegí una opción: ")

            accion = opciones.get(opcion)

            if accion is not None:
                accion()
            else:
                print("Opción inválida.")