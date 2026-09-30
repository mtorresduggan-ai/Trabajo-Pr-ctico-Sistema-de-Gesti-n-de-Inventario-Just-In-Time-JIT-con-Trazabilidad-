from datetime import date

from material import Material
from proveedor import Proveedor
from cliente import Cliente
from comprador import Comprador
from vendedor import Vendedor
from administrador import Administrador
from deposito import Deposito
from remesa import Remesa

def main():

    print("=== SISTEMA DE INVENTARIO AEROTECH ===")

    # Materiales
    aluminio = Material("Aluminio","Al","kg",100)
    acero = Material("Acero","Fe","kg",50)

    # Proveedor
    proveedor = Proveedor("Metalúrgica Sur",5,"1123456789", 30123456, "proveedor@gmail.com",date(2026, 9, 1))

    # Cliente
    cliente = Cliente( "AeroParts","1198765432",30987654,"cliente@gmail.com",date(2026, 9, 1))

    # Empleados
    comprador = Comprador("Juan Pérez","1112345678",40123456,date(2026, 9, 1),"juan@aerotech.com", "jperez","Juan123!")
    vendedor = Vendedor("Ana López","1155555555",40234567,date(2026, 9, 1),"ana@aerotech.com", "alopez","Ana1234!")
    administrador = Administrador("Carlos Gómez","1166666666",40345678,date(2026, 9, 1),"carlos@aerotech.com","cgomez","Carlos123!")

    # Depósito
    deposito = Deposito()

    solicitud = comprador.crear_solicitud(date(2026, 9, 29),[aluminio, acero],[150, 80],proveedor)

    remesa = Remesa(1,[aluminio, acero],proveedor,solicitud,230,[150, 80],[date(2027, 12, 31), date(2028, 6, 30)],date(2026, 10, 4))

    administrador.aceptar_remesa(remesa, deposito)

    pedido = vendedor.crear_pedido_salida(date(2026, 10, 5),[aluminio, acero], [50, 20],cliente)

    administrador.aceptar_pedido_salida(pedido, deposito)

    print(deposito)
    print(pedido)

if __name__ == "__main__":
    main()