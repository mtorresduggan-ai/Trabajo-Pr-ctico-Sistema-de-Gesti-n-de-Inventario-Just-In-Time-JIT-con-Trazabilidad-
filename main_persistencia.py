from sistema import Sistema
from pendientes import Tareas_pendientes
from menu import Menu


sistema = Sistema()

tareas_admin = Tareas_pendientes()
tareas_supervisor = Tareas_pendientes()
tareas_comprador = Tareas_pendientes()
tareas_vendedor = Tareas_pendientes()


sistema.cargar_estado_total()
sistema.crear_administrador_inicial()

print("Cantidad de empleados:", len(sistema._empleados))

for empleado in sistema._empleados:
    print("Usuario cargado:", empleado.get_usuario())

deposito = sistema.buscar_deposito("Deposito central")

menu = Menu(tareas_comprador, tareas_vendedor, tareas_supervisor, tareas_admin, deposito, sistema)

menu.mostrar_menu()

sistema.guardar_estado_total()
sistema.cargar_estado_total()
sistema.crear_administrador_inicial()