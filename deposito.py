class Deposito:
    todos=[]

    def __init__(self, nombre):
        self.stock = dict()
        self.nombre = nombre
        Deposito.todos.append(self)

    def __str__(self):
        texto = ""

        for material, estante in self.stock.items():
            for caja in estante:
                texto += (f"{material.nombre}: {caja['cantidad']} {material.unidad_medida}"
                    f" - vence {caja['fecha_vencimiento']}\n")
        return texto

    def stock_total(self, material):
        return sum(caja["cantidad"] for caja in self.stock.get(material, []))
