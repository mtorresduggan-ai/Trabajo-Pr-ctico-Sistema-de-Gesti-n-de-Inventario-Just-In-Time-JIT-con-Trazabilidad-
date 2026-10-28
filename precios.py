class Precio:
    def __init__(self):
        self._precios = {}

    def agregar_precio(self, material, proveedor):
        clave = (material.get_id_material(), proveedor.get_id())

        precio_base = material.get_precio_base()
        precio_proveedor = proveedor.obtener_precio(material)

        precio_venta = precio_base + precio_proveedor

        self._precios[clave] = precio_venta
        material.set_precio_venta(precio_venta)

    def obtener_precio(self, material, proveedor):
        clave = (material.get_id_material(), proveedor.get_id())

        if clave not in self._precios:
            raise ValueError("No existe un precio para esta combinación")

        return self._precios[clave]

    def get_precios(self):
        return self._precios.copy()