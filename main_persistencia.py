from sistema import Sistema
from pendientes import Tareas_pendientes
from menu import Menu


sistema = Sistema()

tareas_admin = Tareas_pendientes()
tareas_supervisor = Tareas_pendientes()
tareas_comprador = Tareas_pendientes()
tareas_vendedor = Tareas_pendientes()


sistema.cargar_estado_total()

deposito = sistema.buscar_deposito("Deposito central")

menu = Menu(tareas_comprador,tareas_vendedor,tareas_supervisor,tareas_admin,deposito)

menu.mostrar_menu()

sistema.guardar_estado_total()