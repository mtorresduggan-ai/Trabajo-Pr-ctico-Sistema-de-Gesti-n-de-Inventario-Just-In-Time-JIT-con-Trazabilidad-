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
from pendientes import Tareas_pendientes

tareas_admin = Tareas_pendientes()
tareas_supervisor = Tareas_pendientes()
tareas_comprador = Tareas_pendientes()


aluminio = Material("Aluminio", "Al", "kg", 100)
acero = Material("Acero", "Fe", "kg", 50)

proveedor = Proveedor("Metalúrgica Sur", 5, "1123456789", 30123456,"proveedor@gmail.com", date(2026, 9, 1))

cliente = Cliente("AeroParts", "1198765432", 30987654,"cliente@gmail.com", date(2026, 9, 1))

comprador = Comprador("Juan Pérez", "1112345678", 40123456, date(2026, 9, 1),"juan@aerotech.com", "jperez", "Juan123!")

vendedor = Vendedor("Ana López", "1155555555", 40234567, date(2026, 9, 1),"ana@aerotech.com", "alopez", "Ana1234!")

administrador = Administrador("Carlos Gómez", "1166666666", 40345678, date(2026, 9, 1),"carlos@aerotech.com", "cgomez", "Carlos123!")

supervisor = Supervisor("Juana Fernandez", "1177777777", 40456789, date(2026, 9, 1),"jfernandez@gmail.com", "jfernandez", "Juana123!")

deposito = Deposito('Deposito central')
deposito_s = Deposito('Deposito sur')


solicitud = comprador.crear_solicitud(date(2026, 9, 29), [aluminio, acero],[150, 80], proveedor, tareas_admin)
administrador.ejecutar_siguiente_tarea(tareas_admin, deposito, tareas_supervisor)
remesa = Remesa([aluminio, acero], proveedor, solicitud, [150, 80],[date(2027, 12, 31), date(2028, 6, 30)], deposito, tareas_supervisor, date(2026, 10, 4))
supervisor.ejecutar_siguiente_tarea(tareas_supervisor, tareas_comprador)    

print("Depósito tras la remesa:")
print(deposito)


pedido = vendedor.crear_pedido_salida(date(2026, 10, 5), [aluminio, acero],[50, 20], cliente, tareas_admin)
administrador.ejecutar_siguiente_tarea(tareas_admin, deposito, tareas_supervisor)
supervisor.ejecutar_siguiente_tarea(tareas_supervisor, tareas_comprador)

print(pedido)
print("\nDepósito tras el despacho:")
print(deposito)

print("\nTareas pendientes del comprador:")
tareas_comprador.mostrar_cantidades()

pedido2 = vendedor.crear_pedido_salida(date(2026, 10, 6), [acero], [1000], cliente, tareas_admin)

try:
    administrador.ejecutar_siguiente_tarea(tareas_admin, deposito, tareas_supervisor)
except ValueError as e:
    print("Error esperado:", e)

administrador.crear_transferencia(deposito, deposito_s, [aluminio], [10], tareas_supervisor)

supervisor.ejecutar_siguiente_tarea(tareas_supervisor, tareas_comprador)

print("\nDepósito Central tras transferir 10 kg de Aluminio:")
print(deposito)

print("Depósito Sur tras recibir la transferencia:")
print(deposito_s)