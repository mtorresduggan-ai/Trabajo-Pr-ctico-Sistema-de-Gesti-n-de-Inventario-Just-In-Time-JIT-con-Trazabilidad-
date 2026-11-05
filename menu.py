from material import Material
from proveedor import Proveedor
from cliente import Cliente
from empleado import Empleado
from comprador import Comprador
from vendedor import Vendedor
from administrador import Administrador
from supervisor import Supervisor 
from excepciones import VolverAtras
import math 

class Menu:
    pila = []

    def __init__(self, tareas_comprador, tareas_vendedor,
            tareas_supervisor, tareas_admin,deposito=None, sistema=None):
        self.tareas_comprador = tareas_comprador
        self.tareas_vendedor = tareas_vendedor
        self.tareas_supervisor = tareas_supervisor
        self.tareas_admin = tareas_admin
        self.deposito = deposito
        self.sistema = sistema

    def mostrar_menu(self):
        Menu.pila.append(self.pantalla_general)
        while Menu.pila:
            Menu.pila[-1]() 

    def login(self):
        usuario = self.pedir("Usuario: ")
        clave = self.pedir("Contraseña: ")

        return self.sistema.autenticar(usuario, clave)


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
            Comprador: lambda: MenuComprador(empleado, self.tareas_comprador, self.tareas_admin, self.sistema).menu_comprador,
            Vendedor: lambda: MenuVendedor(empleado, self.tareas_vendedor, self.tareas_admin, self.sistema).menu_vendedor,
            Administrador: lambda: MenuAdministrador(empleado, self.tareas_admin, self.tareas_supervisor, self.sistema).menu_administrador,
            Supervisor: lambda: MenuSupervisor(empleado, self.tareas_supervisor, self.tareas_comprador, self.deposito, self.sistema).menu_supervisor,
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
        except Exception as error:
            print(f"Error inesperado ({type(error).__name__}): {error}")

    def buscar_material(self, nombre):
        material = self.sistema.buscar_material_por_nombre(nombre)

        pasos = self.sistema.get_pasos_ultima_busqueda()
        n = self.sistema.get_cantidad_materiales()
        print(f"[Árbol] '{material.get_nombre()}' encontrado en {pasos} saltos | n = {n} materiales | "
            f"log2(n) = {round(math.log2(n), 2)} | una búsqueda lineal revisaría hasta {n}")

        return material

    def input_materiales_cantidades(self, permitir_nuevo=True):
        print("\n--- SELECCIÓN DE MATERIALES ---")
        materiales_seleccionados, cantidades = [], []

        while True:
            print("\n--- BÚSQUEDA Y FILTRADO ---")
            print("Presioná ENTER sin escribir para omitir un filtro.")
            filtro_nombre = self.pedir("Filtrar por nombre (ej: 'tornillo'): ")
            filtro_comp = self.pedir("Filtrar por composición (ej: 'acero'): ")

            resultados = self.sistema.filtrar_materiales(nombre=filtro_nombre, composicion=filtro_comp)

            if not resultados:
                print("No se encontraron materiales con esos criterios.")
                if self.pedir("¿Intentar otra búsqueda? (si/no): ").lower() != "si":
                    break
                continue

            pagina_actual = 0
            por_pagina = 20
            material_elegido = None

            while material_elegido is None:
                total = len(resultados)
                total_paginas = ((total - 1) // por_pagina) + 1
                inicio = pagina_actual * por_pagina
                sub_lista = resultados[inicio:inicio + por_pagina]

                print(f"\n--- RESULTADOS ({total} encontrados) - Página {pagina_actual + 1} de {total_paginas} ---")
                for idx, mat in enumerate(sub_lista, start=1):
                    print(f"{idx}. {mat.get_nombre()} | Comp: {mat.get_composicion()} | Unidad: {mat.get_unidad_medida()}")

                controles = []
                if pagina_actual < total_paginas - 1:
                    controles.append("S: Siguiente")
                if pagina_actual > 0:
                    controles.append("A: Anterior")
                controles.append("F: Cambiar Filtros")
                if permitir_nuevo:
                    controles.append("0: Nuevo Material (temporal)")

                prompt = f"\nSeleccionar [1-{len(sub_lista)}] | " + " | ".join(controles) + ": "
                opcion = self.pedir(prompt).strip().lower()

                if opcion == "s" and pagina_actual < total_paginas - 1:
                    pagina_actual += 1
                elif opcion == "a" and pagina_actual > 0:
                    pagina_actual -= 1
                elif opcion == "f":
                    break 
                elif opcion == "0" and permitir_nuevo:
                    nombre_temp = self.pedir("Nombre: ")
                    comp_temp = self.pedir("Composición: ")
                    unidad_temp = self.pedir("Unidad de medida: ")
                    material_elegido = Material(nombre_temp, comp_temp, unidad_temp, punto_reposicion=0)
                    self.sistema.agregar_material(material_elegido)
                elif opcion.isdigit() and 1 <= int(opcion) <= len(sub_lista):
                    material_elegido = sub_lista[int(opcion) - 1]
                else:
                    print("Opción inválida.")

            if material_elegido is None:
                continue

            cant = self.pedir_int(f"Cantidad para '{material_elegido.get_nombre()}': ")
            if cant <= 0:
                print("La cantidad debe ser mayor a 0.")
                continue

            materiales_seleccionados.append(material_elegido)
            cantidades.append(cant)

            if self.pedir("¿Agregar otro material al pedido/solicitud? (si/no): ").lower() != "si":
                break

        return materiales_seleccionados, cantidades
    
    def elegir(self, titulo, items, formatear=str):
        if not items:
            raise ValueError("No hay opciones disponibles")
        print(f"\n--- {titulo} ---")
        for i, item in enumerate(items, start=1):
            print(f"{i}. {formatear(item)}")
        opcion = self.pedir_int("Ingrese el número (o 'volver'): ")
        if not 1 <= opcion <= len(items):
            raise ValueError("Opción fuera de rango")
        return items[opcion - 1]


    def input_proveedor(self):
        activos = list(filter(lambda p: p.get_fecha_baja() is None, self.sistema.get_proveedores()))
        return self.elegir("SELECCIONAR PROVEEDOR", activos)

    def input_cliente(self):
        activos = list(filter(lambda c: c.get_fecha_baja() is None, self.sistema.get_clientes()))
        return self.elegir("SELECCIONAR CLIENTE", activos)

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
        try:
            return int(Menu.pedir(mensaje))
        except ValueError:
            raise ValueError("Ingresá un número entero válido")
