from comprador import Comprador
from datetime import date
from material import Material
from proveedor import Proveedor

class MenuComprador:
    def __init__(self, comprador, tareas_pendientes_comprador, tareas_pendientes_admin):
        self.comprador = comprador
        self.tareas_pendientes_comprador = tareas_pendientes_comprador
        self.tareas_pendientes_admin = tareas_pendientes_admin

    def menu_comprador(self):
        opciones= {'1': self.Comprador.mostrar_tareas,
                  '2': lambda: self.Comprador.ejecutar_siguiente_tarea(),
                  '3': lambda: self.Comprador.crear_solicitud(date.today(),*self.input_materiales_cantidades(),self.input_proveedor(),self.tareas_pendientes_admin),
                  '4': lambda: self.Comprador.cancelar_solicitud(int(input("ID de solicitud a cancelar: "))),
                  '5': self.Comprador.consultar_solicitudes_todas,
                  '6': lambda: self.Comprador.consultar_solicitud(int(input("ID de solicitud: ")))
                  #, "7": MODIFICAR SOLICUTUD (arreglarlo en comprador tmb)
                  }

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
                    print(error)

    
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

            continuar = input("¿Desea agregar otro material? (si/no): ").lower()

        return materiales, cantidades

    def input_proveedor(self):
        for i, proveedor in enumerate(Proveedor.todos, start=1):
            print(f"{i}. {proveedor}")

        opcion = int(input("Ingrese el número del proveedor: "))
        return Proveedor.todos[opcion - 1]
