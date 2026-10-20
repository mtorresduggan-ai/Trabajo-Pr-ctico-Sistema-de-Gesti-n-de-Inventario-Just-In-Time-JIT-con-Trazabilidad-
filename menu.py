from menu_comprador import MenuComprador
from menu_supervisor import MenuSupervisor
from menu_vendedor import MenuVendedor
from menu_administrador import MenuAdministrador
from deposito import Deposito
from material import Material
from proveedor import Proveedor
from cliente import Cliente

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

    def input_materiales_cantidades(self):
        materiales = []
        cantidades = []
        continuar = "si"

        while continuar == "si":
            for i, material in enumerate(Material.todos, start=1):
                print(f"{i}. {material}")

            opcion = int(input("Ingrese el número del material: "))
            materiales.append(Material.todos[opcion - 1])
            cantidades.append(int(input("Ingrese la cantidad: ")))

            continuar = input("¿Desea agregar otro material? (si/no): ").strip().lower()

        return materiales, cantidades

    def input_proveedor(self):
        for i, proveedor in enumerate(Proveedor.todos, start=1):
            print(f"{i}. {proveedor}")

        opcion = int(input("Ingrese el número del proveedor: "))
        return Proveedor.todos[opcion - 1]

    def input_cliente(self):
        for i, cliente in enumerate(Cliente.todos, start=1):
            print(f"{i}. {cliente}")

        opcion = int(input("Ingrese el número del cliente: "))
        return Cliente.todos[opcion - 1]