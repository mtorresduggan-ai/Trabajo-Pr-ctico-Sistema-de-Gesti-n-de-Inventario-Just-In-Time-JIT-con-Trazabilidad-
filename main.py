from material import Material
from proveedor import Proveedor
from remesa import Remesa
from pedido import Pedido_salida
from solicitud_proveedor import Solicitud_proveedor

material1 = Material("Aluminio", "Al 7075", "kg", 10, "31/12/2026")
material2 = Material("Titanio", "Ti-6Al-4V", "kg", 50, "31/12/2030")
material3 = Material("Acero inoxidable", "316L", "kg", 80, "31/12/2032")
materiales = Material.todos

proveedor1 = Proveedor(1, "Proveedor A", 5, "123456")

remesa1 = Remesa(1, [material1, material2, material3], proveedor1, 100, 3, "20/08/2026")
remesa2 = Remesa(2, [material2], proveedor1, 75, 1, '30/08/2026')

pedido1 = Pedido_salida(1, "31/08/2026", [material2, material3], 20)

solicitud1 = Solicitud_proveedor(1, proveedor1, "31/08/2026", [material1, material3], 200)


#mostrar las fechas de vencimiento de cada material en una remesa
def consultar_materiales_remesas(remesa=None, material=None):

    if remesa:
        remesas = [remesa]
    else:
        remesas = Remesa.todos

    for r in remesas:
        print("Remesa:", r.id_remesa, '\n')
        for m in r.materiales:
            if material is None or m == material:
                print("Material:", m.nombre)
                print("Vencimiento:", m.fecha_vencimiento, '\n')


#procesar pedido de salida descontando saldo de la remesa
def procesar_pedido(remesa, material, pedido):

    if remesa in Remesa.todos and material in Material.todos and pedido in Pedido_salida.todos:
         if material in remesa.materiales and material in pedido.materiales:
            remesa.cambiar_saldo(remesa.saldo_disponible - pedido.cant_materiales)

            print("Pedido:", pedido.id_pedido_salida)
            print("Material:", material.nombre)
            print("Remesa utilizada:", remesa.id_remesa)
            print("Proveedor:", remesa.proveedor.nombre)
            print("Cantidad retirada:", pedido.cant_materiales)
            print("Nuevo saldo de la remesa:", remesa.saldo_disponible)

    else:
        print('Hubo un error en el sistema.')


#sumar cantidades de un material entre todas las remesas
def consultar_stock_material(material):

    total = 0

    for remesa in Remesa.todos:
        if material in remesa.materiales:
            total += remesa.cant_materiales

    print(f"Cantidad total de {material.nombre}: {total} {material.unidad_medida}")

consultar_materiales_remesas()
procesar_pedido(remesa1, pedido1, proveedor1)
consultar_stock_material(material2)