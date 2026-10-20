from material import Material
from proveedor import Proveedor
from cliente import Cliente
from empleado import Empleado
from comprador import Comprador
from vendedor import Vendedor
from administrador import Administrador
from supervisor import Supervisor 

class Menu:
    def __init__(self, tareas_pendientes_comprador, tareas_pendientes_vendedor, tareas_pendientes_supervisor, tareas_pendientes_admin, deposito = None):
        self.tareas_pendientes_comprador = tareas_pendientes_comprador
        self.tareas_pendientes_vendedor = tareas_pendientes_vendedor
        self.tareas_pendientes_supervisor = tareas_pendientes_supervisor
        self.tareas_pendientes_admin = tareas_pendientes_admin
        self.deposito = deposito

    def mostrar_menu(self):
        from menu_comprador import MenuComprador
        from menu_supervisor import MenuSupervisor
        from menu_vendedor import MenuVendedor
        from menu_administrador import MenuAdministrador
        try:
            empleado_logueado = Menu.login()
        except ValueError as error:
            print(f"Error: {error}" )
            return

        mapa_menus = {
            Comprador: lambda: MenuComprador(empleado_logueado, self.tareas_pendientes_comprador, self.tareas_pendientes_admin).menu_comprador(),
            Vendedor: lambda: MenuVendedor(empleado_logueado, self.tareas_pendientes_vendedor, self.tareas_pendientes_admin).menu_vendedor(),
            Administrador: lambda: MenuAdministrador(empleado_logueado, self.tareas_pendientes_admin, self.tareas_pendientes_supervisor).menu_administrador(),
            Supervisor: lambda: MenuSupervisor(empleado_logueado, self.tareas_pendientes_supervisor, self.tareas_pendientes_comprador, self.deposito).menu_supervisor()}

        mapa_menus[type(empleado_logueado)]()

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

    @staticmethod
    def login():
        print("---INICIO DE SESIÓN---")

        usuario_ingresado = input("Usuario: ").strip()
        clave_ingresada = input("Clave: ").strip()

        for empleado in Empleado.todos:
            if (empleado.get_fecha_baja() is None and 
                empleado.get_usuario() == usuario_ingresado and 
                empleado.get_clave() == clave_ingresada):
                
                print(f"\n¡Bienvenido/a {empleado.get_nombre()}!")
                return empleado  

        raise ValueError("Usuario o contraseña incorrectos")