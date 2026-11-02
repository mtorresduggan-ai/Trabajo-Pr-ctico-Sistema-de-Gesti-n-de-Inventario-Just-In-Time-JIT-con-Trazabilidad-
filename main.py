from datetime import date

from material import Material
from proveedor import Proveedor
from cliente import Cliente
from comprador import Comprador
from vendedor import Vendedor
from administrador import Administrador
from deposito import Deposito
from remesa import Remesa
from supervisor import Supervisor
from precios import Precio
from sistema import Sistema
from menu import Menu
from pendientes import Tareas_pendientes


def crear_datos_prueba(sistema, tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor):
    aluminio = Material("Aluminio", "Al", "kg", 100)
    acero = Material("Acero", "Fe", "kg", 50)
    proveedor = Proveedor("Metalúrgica Sur", 5, "1123456789", 30123456,"proveedor@gmail.com", date(2026, 9, 1))
    cliente = Cliente("AeroParts", "1198765432", 30987654,"cliente@gmail.com", date(2026, 9, 1))
    comprador = Comprador("Juan Pérez", "1112345678", 40123456, date(2026, 9, 1),"juan@aerotech.com", "jperez", "Juan123!")
    vendedor = Vendedor("Ana López", "1155555555", 40234567, date(2026, 9, 1),"ana@aerotech.com", "alopez", "Ana1234!")
    administrador = Administrador("Carlos Gómez", "1166666666", 40345678, date(2026, 9, 1),"carlos@aerotech.com", "cgomez", "Carlos123!")
    supervisor = Supervisor("Juana Fernandez", "1177777777", 40456789, date(2026, 9, 1),"jfernandez@gmail.com", "jfernandez", "Juana123!")
    deposito = Deposito('Deposito central')
    precio=Precio()

    sistema.agregar_proveedor(proveedor)
    sistema.agregar_cliente(cliente)
    sistema.agregar_material(aluminio)
    sistema.agregar_material(acero)
    sistema.agregar_empleado(comprador)
    sistema.agregar_empleado(vendedor)
    sistema.agregar_empleado(administrador)
    sistema.agregar_empleado(supervisor)
    sistema.agregar_deposito(deposito)
    sistema.agregar_pedido(pedido)
    sistema.agregar_pedido(pedido)

    proveedores = sistema.get_proveedores()
    clientes = sistema.get_clientes()

    solicitud = comprador.crear_solicitud(date(2026, 9, 29), [aluminio, acero],[150, 80], proveedor, proveedores, tareas_admin, [50,60], precio)
    administrador.ejecutar_siguiente_tarea(tareas_admin, deposito, tareas_supervisor)
    remesa = Remesa([aluminio, acero], proveedor, solicitud, [150, 80],[date(2027, 12, 31), date(2028, 6, 30)], deposito, tareas_supervisor, date(2026, 10, 4))
    supervisor.ejecutar_siguiente_tarea(tareas_supervisor, tareas_comprador)    
    pedido = vendedor.crear_pedido_salida(date(2026, 10, 5), [aluminio, acero],[50, 20], cliente, clientes, tareas_admin)
    administrador.ejecutar_siguiente_tarea(tareas_admin, deposito, tareas_supervisor)
    supervisor.ejecutar_siguiente_tarea(tareas_supervisor, tareas_comprador)
    pedido2 = vendedor.crear_pedido_salida(date(2026, 10, 6), [acero], [1000], cliente, clientes, tareas_admin)

    return deposito
    
def hay_datos(sistema):
    listas = [sistema.get_materiales(),
        sistema.get_proveedores(),
        sistema.get_clientes(),
        sistema.get_empleados(),
        sistema.get_depositos()]

    return any(map(bool, listas))

def main():

    sistema = Sistema()

    tareas_admin = Tareas_pendientes()
    tareas_supervisor = Tareas_pendientes()
    tareas_comprador = Tareas_pendientes()
    tareas_vendedor = Tareas_pendientes()

    sistema.cargar_estado_total(tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor)

    if not hay_datos(sistema):
        print("Primera ejecución: creando datos de prueba...")
        deposito = crear_datos_prueba(
                sistema,
                tareas_admin,
                tareas_supervisor,
                tareas_comprador,
                tareas_vendedor)

    else:
        print("Datos recuperados desde los archivos CSV.")
        depositos = sistema.get_depositos()

        if len(depositos) > 0:
            deposito = depositos[0]
        else:
            deposito = Deposito('Deposito central')
            sistema.agregar_deposito(deposito)

    for tarea in tareas_admin.obtener_tareas():
        print("TIPO:", tarea.get_tipo(), "OBJETO:", tarea.get_objeto())

    sistema.guardar_estado_total(tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor)
    
    menu = Menu(
        tareas_comprador,
        tareas_vendedor,
        tareas_supervisor,
        tareas_admin,
        deposito,
        sistema)

    menu.mostrar_menu()

if __name__ == "__main__":
    main()

