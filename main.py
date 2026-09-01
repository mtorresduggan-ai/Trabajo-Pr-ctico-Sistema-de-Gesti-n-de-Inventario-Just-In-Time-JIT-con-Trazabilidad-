from material import Material
from proveedor import Proveedor
from remesa import Remesa
from pedido import Pedido_salida
from solicitud_proveedor import Solicitud_proveedor

material1 = Material("Aluminio", "Al 7075", "kg", 10, "31/12/2026")
material2 = Material("Titanio", "Ti-6Al-4V", "kg", 50, "31/12/2030")
material3 = Material("Acero inoxidable", "316L", "kg", 80, "31/12/2032")
proveedor1 = Proveedor(1, "Proveedor A", 5, "123456")
remesa1 = Remesa(1, [material1, material2, material3], proveedor1, 100, 1, "20/08/2026")
pedido1 = Pedido_salida(1, "31/08/2026", [], 20)
solicitud1 = Solicitud_proveedor(1, proveedor1, "31/08/2026", [material1, material3], 200)

