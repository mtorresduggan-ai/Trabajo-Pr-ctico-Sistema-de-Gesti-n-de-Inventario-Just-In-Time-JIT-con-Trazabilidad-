from sistema import Sistema
from pendientes import Tareas_pendientes
from deposito import Deposito
from menu import Menu


sistema = Sistema()

tareas_admin = Tareas_pendientes()
tareas_supervisor = Tareas_pendientes()
tareas_comprador = Tareas_pendientes()
tareas_vendedor = Tareas_pendientes()


sistema.cargar_estado_total()


deposito = None

for deposito_cargado in Deposito.todos:
    if deposito_cargado.get_nombre() == "Deposito central":
        deposito = deposito_cargado


menu = Menu(tareas_comprador, tareas_vendedor, tareas_supervisor, tareas_admin, deposito)

menu.mostrar_menu()


sistema.guardar_estado_total()