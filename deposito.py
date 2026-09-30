class Deposito:

    def __init__(self):
        self.stock = dict()

    def __str__(self):
        texto = ""

        for material, datos in self.stock.items():
            for dato in datos:
                texto += (f"{material.nombre}: {dato['cantidad']} {material.unidad_medida}"
                    f" - vence {dato['fecha_vencimiento']}\n")
        return texto

    def stock_total(self, material):
        return sum(lote["cantidad"] for lote in self.stock.get(material, []))