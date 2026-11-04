from datetime import date
from estante import Estante


class Deposito:
    def __init__(self, nombre):
        self._stock = dict()
        self._nombre = nombre

    def get_stock(self):
        return dict(self._stock)
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

    def stock_total(self, material, fecha=None):
        total = 0
        estante = self._stock.get(material)

        if estante is not None:
            actual = estante.get_primera()

            while actual is not None:
                vencimiento = actual.get_fecha_vencimiento()
                if fecha is None or vencimiento is None or vencimiento >= fecha:
                    total += actual.get_cantidad()
                actual = actual.get_prox()
        return total
    
    def get_materiales(self):
        return list(self._stock.keys())

    def obtener_cajas(self, material):
        if material not in self._stock:
            return []
        return self._stock[material].obtener_cajas()

    def ingresar(self, material, fecha_vencimiento, cantidad):
        if material not in self._stock:
            self._stock[material] = Estante()
        self._stock[material].agregar_caja(fecha_vencimiento, cantidad)

    def retirar(self, material, cantidad):
        if self.stock_total(material, date.today()) < cantidad:
            raise ValueError(f"No hay suficiente stock de {material.get_nombre()}")
        return self._stock[material].sacar_cajas(cantidad)

    def hay_vencidos(self, fecha):
        return any(map(lambda estante: estante.hay_cajas_vencidas(fecha), self._stock.values()))

    def retirar_vencidos(self, fecha):
        for estante in self._stock.values():
            estante.retirar_cajas_vencidas(fecha)

    @staticmethod
    def seleccionar_deposito(depositos):
        while True:
            nombre = input("Ingresá el nombre de tu depósito: ")

            for deposito in depositos:
                if deposito.get_nombre() == nombre:
                    return deposito

            print("El depósito ingresado no existe. Intentá nuevamente.")