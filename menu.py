from material import Material
from proveedor import Proveedor
from cliente import Cliente
from empleado import Empleado
from comprador import Comprador
from vendedor import Vendedor
from administrador import Administrador
from supervisor import Supervisor 
from excepciones import VolverAtras

class Menu:
    pila = []

    def __init__(self, tareas_pendientes_comprador, tareas_pendientes_vendedor,
            tareas_pendientes_supervisor, tareas_pendientes_admin,deposito=None, sistema=None):
        self.tareas_pendientes_comprador = tareas_pendientes_comprador
        self.tareas_pendientes_vendedor = tareas_pendientes_vendedor
        self.tareas_pendientes_supervisor = tareas_pendientes_supervisor
        self.tareas_pendientes_admin = tareas_pendientes_admin
        self.deposito = deposito
        self.sistema = sistema

    def mostrar_menu(self):
        Menu.pila.append(self.pantalla_general)
        while Menu.pila:
            Menu.pila[-1]()  # ejecuta la pantalla del tope


    def pantalla_general(self):
        print("\n--- MENÚ GENERAL ---")
        print("1. Iniciar sesión")
        print("0. Salir")
        opcion = input("Elegí una opción: ").strip()

        if opcion == "0":
            Menu.volver()
        elif opcion == "1":
            try:
                empleado = self.login()
            except ValueError as error:
                print(f"Error: {error}")
                return
            self.apilar_menu_de(empleado)
        else:
            print("Opción inválida.")

    def apilar_menu_de(self, empleado):
        from menu_comprador import MenuComprador
        from menu_supervisor import MenuSupervisor
        from menu_vendedor import MenuVendedor
        from menu_administrador import MenuAdministrador

        creadores = {
            Comprador: lambda: MenuComprador(empleado, self.tareas_pendientes_comprador, self.tareas_pendientes_admin).menu_comprador,
            Vendedor: lambda: MenuVendedor(empleado, self.tareas_pendientes_vendedor, self.tareas_pendientes_admin).menu_vendedor,
            Administrador: lambda: MenuAdministrador(empleado, self.tareas_pendientes_admin, self.tareas_pendientes_supervisor).menu_administrador,
            Supervisor: lambda: MenuSupervisor(empleado, self.tareas_pendientes_supervisor, self.tareas_pendientes_comprador, self.deposito).menu_supervisor,
        }
        Menu.pila.append(creadores[type(empleado)]())

    def pantalla(self, titulo, textos, opciones):
        print(f"\n--- {titulo} ---")
        for texto in textos:
            print(texto)
        print("0. Volver")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "0":
            Menu.volver()
            return

        accion = opciones.get(opcion)
        if accion is None:
            print("Opción inválida.")
            return

        try:
            resultado = accion()
            if resultado is not None:
                print(resultado)
        except VolverAtras:
            print("Operación cancelada. Volviendo al menú...")
        except (ValueError, TypeError, IndexError) as error:
            print(f"Error: {error}")


    def input_materiales_cantidades(self):
        materiales = []
        cantidades = []
        continuar = "si"

        while continuar == "si":
            for i, material in enumerate(self.sistema._materiales, start=1):
                print(f"{i}. {material}")

            opcion = self.pedir_int("Ingrese el número del material (o 'volver'): ")
            materiales.append(self.sistema._materiales[opcion - 1])
            cantidades.append(self.pedir_int("Ingrese la cantidad: "))

            continuar = self.pedir("¿Desea agregar otro material? (si/no): ").lower()

        return materiales, cantidades

    def input_proveedor(self):
        for i, proveedor in enumerate(self.sistema._proveedores, start=1):
            print(f"{i}. {proveedor}")

        opcion = self.pedir_int("Ingrese el número del proveedor (o 'volver'): ")
        return self.sistema._proveedores[opcion - 1]

    def input_cliente(self):
        for i, cliente in enumerate(self.sistema._clientes, start=1):
            print(f"{i}. {cliente}")

        opcion = self.pedir_int("Ingrese el número del cliente (o 'volver'): ")
        return self.sistema._clientes[opcion - 1]

    def login(self):
        print("---INICIO DE SESIÓN---")

        usuario_ingresado = input("Usuario: ").strip()
        clave_ingresada = input("Clave: ").strip()

        for empleado in self.sistema._empleados:
            if (empleado.get_fecha_baja() is None and
                empleado.get_usuario() == usuario_ingresado and
                empleado.get_clave() == clave_ingresada):

                print(f"\n¡Bienvenido/a {empleado.get_nombre()}!")
                return empleado

        raise ValueError("Usuario o contraseña incorrectos")

    @staticmethod
    def volver():
        if Menu.pila:
            Menu.pila.pop()

    @staticmethod
    def pedir(mensaje):
        valor = input(mensaje).strip()
        if valor.lower() == "volver":
            raise VolverAtras()
        return valor

    @staticmethod
    def pedir_int(mensaje):
        return int(Menu.pedir(mensaje))
