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
        depositos = sistema.get_gestor_depositos().get_depositos()

        if len(depositos) > 0:
            deposito = depositos[0]
        else:
            deposito = Deposito('Deposito central')
            sistema.get_gestor_depositos().agregar_deposito(deposito)

    
    sistema.guardar_estado_total(tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor)
    
    print(f"Materiales cargados en el árbol: {sistema.get_gestor_materiales().get_cantidad_materiales()}")
    
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

    aluminio = Material("Aluminio", "Aluminio", "kg", 100, precio_base=5000, precio_venta=7500)
    acero = Material("Acero", "Acero", "kg", 100, precio_base=3000, precio_venta=4500)
    cobre = Material("Cobre", "Cobre", "kg", 30, precio_base=8000, precio_venta=11000)
    disco_corte = Material("Disco de corte 115 mm", "Abrasivo", "unidades", 30, precio_base=900, precio_venta=1400)
    disco_desbaste = Material("Disco de desbaste 115 mm", "Abrasivo", "unidades", 20, precio_base=1200, precio_venta=1800)
    mecha = Material("Mecha de acero rápido 8 mm", "Acero rápido", "unidades", 15, precio_base=1800, precio_venta=2500)
    guantes = Material("Guantes de seguridad", "Poliéster y nitrilo", "pares", 50, precio_base=1500, precio_venta=2200)
    antiparras = Material("Antiparras de seguridad", "Policarbonato", "unidades", 20, precio_base=2500, precio_venta=3500)
    film = Material("Film stretch", "Polietileno", "rollos", 20, precio_base=5000, precio_venta=7000)
    cinta = Material("Cinta de embalaje", "Polipropileno", "rollos", 40, precio_base=800, precio_venta=1200)
    cajas = Material("Caja de cartón reforzado", "Cartón corrugado", "unidades", 100, precio_base=600, precio_venta=950)
    cable = Material("Cable unipolar 2,5 mm", "Cobre y PVC", "metros", 100, precio_base=1200, precio_venta=1800)
    terminal = Material("Terminal eléctrico", "Cobre", "unidades", 100, precio_base=150, precio_venta=250)

    materiales_base = [aluminio, acero, cobre, disco_corte, disco_desbaste, mecha, guantes, antiparras, film, cinta, cajas, cable, terminal]

    tipos = ["Tornillo hexagonal","Tornillo Allen","Tornillo cabeza fresada","Bulón","Perno","Pasador","Espárrago","Varilla roscada"]

    medidas = ["M3", "M4", "M5", "M6", "M8", "M10", "M12", "M16"]
    largos = [6, 10, 16, 20, 25, 30, 40, 50]
    materiales_fijacion = ["acero","acero inoxidable","aluminio","latón"]
    combinaciones = product(tipos, medidas, largos, materiales_fijacion)
    
    catalogo = [Material(f"{c[0]} {c[1]}x{c[2]} {c[3]}", c[3], "unidades", 100, precio_base=int(c[1][1:]) * 10 + c[2] * 5, precio_venta=int(c[1][1:]) * 15 + c[2] * 8) for c in combinaciones]

    tornillo = next(m for m in catalogo if m.get_nombre() == "Tornillo hexagonal M8x30 acero")
    bulon = next(m for m in catalogo if m.get_nombre() == "Bulón M10x50 acero")
    perno = next(m for m in catalogo if m.get_nombre() == "Perno M12x40 acero inoxidable")

    sistema.get_gestor_materiales().agregar_materiales(materiales_base + catalogo)


    proveedor = Proveedor("Metalúrgica Sur", 5, "1123456789", 30123456, "metalurgicasur@gmail.com", date(2026, 9, 1))
    proveedor1 = Proveedor("Ferretería Industrial Norte", 4, "1134567890", 30234567, "ferreterianorte@gmail.com", date(2026, 9, 1))
    proveedor2 = Proveedor("Seguridad Laboral SRL", 3, "1145678901", 30345678, "seguridadlaboral@gmail.com", date(2026, 9, 1))
    proveedor3 = Proveedor("Distribuidora de Embalajes", 6, "1156789012", 30456789, "embalajes@gmail.com", date(2026, 9, 1))
    proveedor4 = Proveedor("Insumos Eléctricos Centro", 4, "1167890123", 30567890, "electricoscentro@gmail.com", date(2026, 9, 1))

    proveedores = [proveedor, proveedor1, proveedor2, proveedor3, proveedor4]

    for p in proveedores:
        sistema.get_gestor_proveedores().agregar_proveedor(p)

    proveedor.agregar_material(aluminio, 5000)
    proveedor.agregar_material(acero, 3000)
    proveedor.agregar_material(cobre, 8000)
    proveedor.agregar_material(tornillo, 350)
    proveedor.agregar_material(bulon, 600)
    proveedor.agregar_material(perno, 750)

    proveedor1.agregar_material(disco_corte, 900)
    proveedor1.agregar_material(disco_desbaste, 1200)
    proveedor1.agregar_material(mecha, 1800)

    proveedor2.agregar_material(guantes, 1500)
    proveedor2.agregar_material(antiparras, 2500)

    proveedor3.agregar_material(film, 5000)
    proveedor3.agregar_material(cinta, 800)
    proveedor3.agregar_material(cajas, 600)

    proveedor4.agregar_material(cable, 1200)
    proveedor4.agregar_material(terminal, 150)

    cliente= Cliente("AeroParts", "1198765432", 30987654, "aeroparts@gmail.com", date(2026, 9, 1))
    cliente1=Cliente("Taller Mecánico Rivadavia", "1156789012", 30456789,"rivadavia@gmail.com", date(2026, 9, 1))
    cliente2=Cliente("Metalúrgica del Oeste", "1167890123", 30567890,"metalurgicaoeste@gmail.com", date(2026, 9, 1))
    cliente3=Cliente("Construcciones Delta", "1178901234", 30678901,"delta@gmail.com", date(2026, 9, 1))
    cliente4=Cliente("Fábrica Industrial Sur", "1189012345", 30789012,"industrial@gmail.com", date(2026, 9, 1))
    cliente5=Cliente("Mantenimiento Integral SRL", "1190123456", 30890123,"mantenimiento@gmail.com", date(2026, 9, 1))

    clientes = [cliente, cliente1, cliente2, cliente3, cliente4, cliente5]

    for c in clientes:
        sistema.get_gestor_clientes().agregar_cliente(c)

    comprador = Comprador("Juan Pérez", "1112345678", 40123456, date(2026, 9, 1), "juan@empresa.com", "jperez", "Juan123!")
    vendedor = Vendedor("María López", "1155555555", 40234567, date(2026, 9, 1), "maria@empresa.com", "mlopez", "Maria123!")
    administrador = Administrador("Carlos Gómez", "1166666666", 40345678,date(2026, 9, 1), "carlos@empresa.com","cgomez", "Carlos123!")
    supervisor = Supervisor("Juana Fernandez", "1177777777", 40456789, date(2026, 9, 1), "juana@empresa.com", "jfernandez", "Juana123!")

    for empleado in [comprador, vendedor, administrador, supervisor]:
        sistema.get_gestor_empleados().agregar_empleado(empleado)

    deposito = Deposito("Depósito central")
    sistema.get_gestor_depositos().agregar_deposito(deposito)

    solicitud1 = comprador.crear_solicitud(date(2026, 11, 3), [aluminio, tornillo], [100, 200], proveedor, proveedores, tareas_admin)
    sistema.get_gestor_solicitudes().agregar_solicitud(solicitud1)
    administrador.ejecutar_siguiente_tarea(tareas_admin, deposito, tareas_supervisor, "aceptar")
    remesa1 = Remesa([aluminio, tornillo], proveedor, solicitud1, [100, 200], [None, None], deposito, tareas_supervisor, date(2026, 11, 6))
    sistema.get_gestor_remesas().agregar_remesa(remesa1)
    supervisor.ejecutar_siguiente_tarea(tareas_supervisor, tareas_comprador)

    solicitud2 = comprador.crear_solicitud(date(2026, 11, 4), [disco_corte, mecha], [50, 20], proveedor1, proveedores, tareas_admin)
    sistema.get_gestor_solicitudes().agregar_solicitud(solicitud2)
    administrador.ejecutar_siguiente_tarea(tareas_admin, deposito, tareas_supervisor, "aceptar")
    remesa2 = Remesa([disco_corte, mecha], proveedor1, solicitud2, [50, 20], [None, None], deposito, tareas_supervisor, date(2026, 11, 9))
    sistema.get_gestor_remesas().agregar_remesa(remesa2)

    solicitud3 = comprador.crear_solicitud(date(2026, 11, 4), [guantes, antiparras], [100, 50], proveedor2, proveedores, tareas_admin)
    sistema.get_gestor_solicitudes().agregar_solicitud(solicitud3)

    pedido1 = vendedor.crear_pedido_salida(date(2026, 11, 4), [aluminio, tornillo], [20, 30], clientes[0], clientes, tareas_admin)
    sistema.get_gestor_pedidos().agregar_pedido(pedido1)

    pedido2 = vendedor.crear_pedido_salida(date(2026, 11, 4), [tornillo, bulon], [180, 50], clientes[1], clientes, tareas_admin)
    sistema.get_gestor_pedidos().agregar_pedido(pedido2)

    return deposito
   


def hay_datos(sistema):
    listas = [sistema.get_gestor_materiales().get_materiales(),
        sistema.get_gestor_proveedores().get_proveedores(),
        sistema.get_gestor_clientes().get_clientes(),
        sistema.get_gestor_empleados().get_empleados(),
        sistema.get_gestor_depositos().get_depositos()]

    return any(map(bool, listas))


if __name__ == "__main__":
    main()

