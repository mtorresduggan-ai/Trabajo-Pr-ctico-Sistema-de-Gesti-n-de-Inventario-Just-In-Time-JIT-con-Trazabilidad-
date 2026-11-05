from datetime import date
from itertools import product

from material import Material
from proveedor import Proveedor
from cliente import Cliente
from comprador import Comprador
from vendedor import Vendedor
from administrador import Administrador
from deposito import Deposito
from remesa import Remesa
from supervisor import Supervisor
from sistema import Sistema
from menu import Menu
from pendientes import Tareas_pendientes

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

    
    sistema.guardar_estado_total(tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor)
    
    print(f"Materiales cargados en el árbol: {sistema.get_cantidad_materiales()}")
    
    menu = Menu(
        tareas_comprador,
        tareas_vendedor,
        tareas_supervisor,
        tareas_admin,
        deposito,
        sistema)

    try:
        menu.mostrar_menu()
    finally:
        sistema.guardar_estado_total(tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor)
        print("¡Datos guardados correctamente!")


def crear_datos_prueba(sistema, tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor):
    aluminio = Material("Aluminio", "Al", "kg", 100, precio_base=5000, precio_venta=7500)
    acero = Material("Acero", "Fe", "kg", 50, precio_base=3000, precio_venta=4500)
    algodon = Material("Tela de algodón", "100% algodón", "metros", 50, precio_base=2500, precio_venta=3500)
    poliester = Material("Tela de poliéster", "100% poliéster", "metros", 40, precio_base=1800, precio_venta=2600)
    hilo_blanco = Material("Hilo blanco", "Algodón", "rollos", 20, precio_base=900, precio_venta=1400)
    hilo_negro = Material("Hilo negro", "Poliéster", "rollos", 15, precio_base=1100, precio_venta=1600)
    botones = Material("Botones medianos", "Plástico", "unidades", 100, precio_base=80, precio_venta=130)
    cierres = Material("Cierres de 20 cm", "Metal", "unidades", 30, precio_base=450, precio_venta=650)
    elastico = Material("Elástico", "Poliéster y látex", "metros", 25, precio_base=700, precio_venta=1000)
    etiquetas = Material("Etiquetas", "Tela", "unidades", 50, precio_base=120, precio_venta=200)

    proveedor = Proveedor("Metalúrgica Sur", 5, "1123456789", 30123456,"proveedor@gmail.com", date(2026, 9, 1))
    proveedor1 = Proveedor("Textil Sur", 5, "1123456789", 30123456, "textilsur@gmail.com", date(2026, 9, 1))
    proveedor2 = Proveedor("Insumos del Centro", 3, "1134567890", 30234567, "insumoscentro@gmail.com", date(2026, 9, 1))
    proveedor3 = Proveedor("Distribuidora Norte", 7, "1145678901", 30345678, "distribuidoranorte@gmail.com", date(2026, 9, 1))
        
    cliente = Cliente("AeroParts", "1198765432", 30987654,"cliente@gmail.com", date(2026, 9, 1))
    cliente1 = Cliente("Confecciones Luna", "1156789012", 30456789, "luna@gmail.com", date(2026, 9, 1))
    cliente2 = Cliente("Moda Urbana", "1167890123", 30567890, "modaurbana@gmail.com", date(2026, 9, 1))
    cliente3 = Cliente("Taller Abril", "1178901234", 30678901, "tallerabril@gmail.com", date(2026, 9, 1))
    cliente4 = Cliente("Diseño Textil", "1189012345", 30789012, "disenotextil@gmail.com", date(2026, 9, 1))
    cliente5 = Cliente("Ropa del Sur", "1190123456", 30890123, "ropadelsur@gmail.com", date(2026, 9, 1))
    
    comprador = Comprador("Juan Pérez", "1112345678", 40123456, date(2026, 9, 1),"juan@aerotech.com", "jperez", "Juan123!")
    vendedor = Vendedor("María López", "1155555555", 40234567, date(2026, 9, 1),"maria@aerotech.com", "mlopez", "Maria123!")
    administrador = Administrador("Carlos Gómez", "1166666666", 40345678, date(2026, 9, 1),"carlos@aerotech.com", "cgomez", "Carlos123!")
    supervisor = Supervisor("Juana Fernandez", "1177777777", 40456789, date(2026, 9, 1),"jfernandez@gmail.com", "jfernandez", "Juana123!")
    deposito = Deposito('Deposito central')
    deposito_norte = Deposito('Deposito norte')

    sistema.agregar_proveedor(proveedor)
    sistema.agregar_proveedor(proveedor1)
    sistema.agregar_proveedor(proveedor2)
    sistema.agregar_proveedor(proveedor3)

    sistema.agregar_cliente(cliente)
    sistema.agregar_cliente(cliente1)
    sistema.agregar_cliente(cliente2)
    sistema.agregar_cliente(cliente3)
    sistema.agregar_cliente(cliente4)
    sistema.agregar_cliente(cliente5)

    materiales = [aluminio, acero, algodon, poliester,hilo_blanco, hilo_negro, botones, cierres, elastico, etiquetas]
    tipos = ["Tornillo", "Tuerca", "Arandela", "Remache", "Perno", "Bulón", "Pasador", "Espárrago"]
    medidas = ["M3", "M4", "M5", "M6", "M8", "M10", "M12", "M16"]
    largos = [6, 10, 16, 20, 25, 30, 40, 50]
    aleaciones = ["acero", "inox", "titanio", "aluminio"]

    catalogo = list(map(lambda combinacion: Material(f"{combinacion[0]} {combinacion[1]}x{combinacion[2]} {combinacion[3]}", combinacion[3], "unidades", 100, precio_base=combinacion[2] * 10, precio_venta=combinacion[2] * 15), product(tipos, medidas, largos, aleaciones)))

    sistema.agregar_materiales(materiales + catalogo)


    sistema.agregar_empleado(comprador)
    sistema.agregar_empleado(vendedor)
    sistema.agregar_empleado(administrador)
    sistema.agregar_empleado(supervisor)

    sistema.agregar_deposito(deposito)
    sistema.agregar_deposito(deposito_norte)

    proveedor.agregar_material(aluminio, 5000)
    proveedor.agregar_material(acero, 3000)
    proveedor1.agregar_material(algodon, 2500)
    proveedor1.agregar_material(poliester, 1800)
    proveedor1.agregar_material(hilo_blanco, 900)
    proveedor2.agregar_material(botones, 80)
    proveedor2.agregar_material(cierres, 450)
    proveedor2.agregar_material(etiquetas, 120)
    proveedor3.agregar_material(hilo_negro, 1100)
    proveedor3.agregar_material(elastico, 700)
    proveedor3.agregar_material(poliester, 1950)

    proveedores = sistema.get_proveedores()
    clientes = sistema.get_clientes()

    solicitud = comprador.crear_solicitud(date(2026, 9, 29), [aluminio, acero],[150, 80], proveedor, proveedores, tareas_admin)
    sistema.agregar_solicitud(solicitud)
    administrador.ejecutar_siguiente_tarea(tareas_admin, deposito, tareas_supervisor, "aceptar")
    remesa = Remesa([aluminio, acero], proveedor, solicitud, [150, 80],[date(2027, 12, 31), date(2028, 6, 30)], deposito, tareas_supervisor, date(2026, 10, 4))
    sistema.agregar_remesa(remesa)
    supervisor.ejecutar_siguiente_tarea(tareas_supervisor, tareas_comprador)    
    
    pedido = vendedor.crear_pedido_salida(date(2026, 10, 5), [aluminio, acero],[50, 20], cliente, clientes, tareas_admin)
    sistema.agregar_pedido(pedido)
    administrador.ejecutar_siguiente_tarea(tareas_admin, deposito, tareas_supervisor, "aceptar")
    supervisor.ejecutar_siguiente_tarea(tareas_supervisor, tareas_comprador)

    #NO QUEDARON CARGADOS!!
    pedido2 = vendedor.crear_pedido_salida(date(2026, 10, 6), [acero], [30], cliente, clientes, tareas_admin)
    sistema.agregar_pedido(pedido2)
    administrador.ejecutar_siguiente_tarea(tareas_admin, deposito, tareas_supervisor, "aceptar")
    supervisor.ejecutar_siguiente_tarea(tareas_supervisor, tareas_comprador)

    solicitud2 = comprador.crear_solicitud(date(2026, 10, 7), [botones, cierres], [200, 60], proveedor2, proveedores, tareas_admin)
    sistema.agregar_solicitud(solicitud2)
    administrador.ejecutar_siguiente_tarea(tareas_admin, deposito, tareas_supervisor, "aceptar")
    remesa2 = Remesa([botones, cierres], proveedor2, solicitud2, [200, 60], [None, None], deposito, tareas_supervisor, date(2026, 10, 12))
    sistema.agregar_remesa(remesa2)

    pedido3 = vendedor.crear_pedido_salida(date(2026, 10, 8), [aluminio], [10], cliente1, clientes, tareas_admin)
    sistema.agregar_pedido(pedido3)
    administrador.ejecutar_siguiente_tarea(tareas_admin, deposito, tareas_supervisor, "aceptar")

    solicitud3 = comprador.crear_solicitud(date(2026, 10, 9), [algodon, poliester], [100, 60], proveedor1, proveedores, tareas_admin)
    sistema.agregar_solicitud(solicitud3)
    pedido4 = vendedor.crear_pedido_salida(date(2026, 10, 10), [hilo_blanco], [5], cliente2, clientes, tareas_admin)
    sistema.agregar_pedido(pedido4)

    return deposito
    
def hay_datos(sistema):
    listas = [sistema.get_materiales(),
        sistema.get_proveedores(),
        sistema.get_clientes(),
        sistema.get_empleados(),
        sistema.get_depositos()]

    return any(map(bool, listas))


if __name__ == "__main__":
    main()

