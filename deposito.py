class Deposito:
    def __init__(self, nombre):
        self._stock = dict()
        self._nombre = nombre

    def get_stock(self):
        return self._stock
    def get_nombre(self): 
        return self._nombre

    def set_stock(self, nuevo_stock):
        self._stock = nuevo_stock
    def set_nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    def __str__(self):
        texto = ""

        for material, estante in self._stock.items():
            actual = estante.get_primera()

            while actual is not None:
                texto += (f"{material.get_nombre()}: {actual.get_cantidad()} "
                        f"{material.get_unidad_medida()}"
                        f" - vence {actual.get_fecha_vencimiento()}\n")
                actual = actual.get_prox()

        return texto

    def stock_total(self, material):
        total = 0
        estante = self._stock.get(material)

        if estante is not None:
            actual = estante.get_primera()

            while actual is not None:
                total += actual.get_cantidad()
                actual = actual.get_prox()
        return total

    @staticmethod
    def seleccionar_deposito(depositos):
        while True:
            nombre = input("Ingresá el nombre de tu depósito: ")

            for deposito in depositos:
                if deposito.get_nombre() == nombre:
                    return deposito

            print("El depósito ingresado no existe. Intentá nuevamente.")