class Deposito:
    todos=[]

    def __init__(self, nombre):
        self.stock = dict()
        self.nombre = nombre
        Deposito.todos.append(self)

    def __str__(self):
        texto = ""

        for material, estante in self.stock.items():
            actual = estante.primero

            while actual is not None:
                texto += (f"{material.nombre}: {actual.cantidad} "
                        f"{material.unidad_medida}"
                        f" - vence {actual.fecha_vencimiento}\n")
                actual = actual.siguiente

        return texto

    def stock_total(self, material):
        total = 0
        estante = self.stock.get(material)

        if estante is not None:
            actual = estante.primero

            while actual is not None:
                total += actual.cantidad
                actual = actual.proximo

        return total