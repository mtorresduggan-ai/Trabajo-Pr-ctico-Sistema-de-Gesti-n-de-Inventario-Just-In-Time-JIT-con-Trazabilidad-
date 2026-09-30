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
    # Alta de datos
    aluminio = Material("Aluminio", "Al", "kg", 100)
    acero = Material("Acero", "Fe", "kg", 50)
    proveedor = Proveedor("Metalúrgica Sur", 5, "1123456789", 30123456,"proveedor@gmail.com", date(2026, 9, 1))
    cliente = Cliente("AeroParts", "1198765432", 30987654,"cliente@gmail.com", date(2026, 9, 1))
    comprador = Comprador("Juan Pérez", "1112345678", 40123456, date(2026, 9, 1),"juan@aerotech.com", "jperez", "Juan123!")
    vendedor = Vendedor("Ana López", "1155555555", 40234567, date(2026, 9, 1),"ana@aerotech.com", "alopez", "Ana1234!")
    administrador = Administrador("Carlos Gómez", "1166666666", 40345678, date(2026, 9, 1),"carlos@aerotech.com", "cgomez", "Carlos123!")
    deposito = Deposito()

    # Compra: solicitud -> remesa -> depósito
    solicitud = comprador.crear_solicitud(date(2026, 9, 29), [aluminio, acero],[150, 80], proveedor)
    remesa = Remesa(1, [aluminio, acero], proveedor, solicitud, 230, [150, 80],[date(2027, 12, 31), date(2028, 6, 30)], date(2026, 10, 4))
    
    administrador.aceptar_remesa(remesa, deposito)
    print("Depósito tras la remesa:")
    print(deposito)

    # Venta: pedido -> despacho
    pedido = vendedor.crear_pedido_salida(date(2026, 10, 5), [aluminio, acero],[50, 20], cliente)
    
    a_reponer = administrador.aceptar_pedido_salida(pedido, deposito)
    print(pedido)
    print("\nDepósito tras el despacho:")
    print(deposito)
    for material in a_reponer:
        print(f"ALERTA: {material.nombre} en {deposito.stock_total(material)} "
              f"{material.unidad_medida} (punto de reposición: "
              f"{material.punto_reposicion}), reponer\n")

    # Un caso de error controlado
    pedido2 = vendedor.crear_pedido_salida(date(2026, 10, 6), [acero], [1000], cliente)
    try:
        administrador.aceptar_pedido_salida(pedido2, deposito)
    except ValueError as e:
        print("Error esperado:", e)


if __name__ == "__main__":
    main()