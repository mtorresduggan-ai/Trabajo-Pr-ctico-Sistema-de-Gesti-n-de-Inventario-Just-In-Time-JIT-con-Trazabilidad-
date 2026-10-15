from comprador import Comprador
from datetime import date
from material import Material

class MenuComprador:
    def __init__(self, comprador, tareas_pendientes_comprador, tareas_pendientes_admin):
        self.comprador = comprador
        self.tareas_pendientes_comprador = tareas_pendientes_comprador
        self.tareas_pendientes_admin = tareas_pendientes_admin

    def mostrar(self):
        opcion = ""

        while opcion != "7":
            print("\n--- MENÚ COMPRADOR ---")
            print("1. Crear solicitud")
            print("2. Consultar solicitud")
            print("3. Consultar solicitudes todas")
            print("4. Modificar solicitud")
            print("5. Cancelar solicitud")
            print("6.Ejecutar siguiente tarea pendiente")
            print("7. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                fecha=date.today()
                materiales, cantidades= self.input_materiales_cantidades()
                proveedor= input("Ingresa el proveedor")
                tareas_pendientes_admin= tareas_pendientes_admin
                #ojo!
                

                self.Comprador.crear_solicitud(fecha, materiales, cantidades, proveedor, tareas_pendientes_admin)

            elif opcion == "2":
                self.Comprador.consultar_solicitudes_todas()

            elif opcion == "3":
                self.Comprador.consultar_solicitudes_todas()

            elif opcion == "4":
                self.comprador.modificar_solicitud()

            elif opcion == "5":
                self.Comprador.cancelar_solicitud()

            elif opcion == "6":
                self.Comprador.ejecutar_siguiente_tarea()

            elif opcion != "7":
                print("Opción inválida.")

    def input_materiales_cantidades():
        materiales=[]
        cantidades=[]
        
        while continuar == "si":

            material = int(input("Ingrese un material: "))
            cantidad = int(input("Ingrese la cantidad: "))

            materiales.append(material)
            cantidades.append(cantidad)

            continuar = input("¿Desea agregar otro material? (si/no): ").lower()

        return materiales, cantidades