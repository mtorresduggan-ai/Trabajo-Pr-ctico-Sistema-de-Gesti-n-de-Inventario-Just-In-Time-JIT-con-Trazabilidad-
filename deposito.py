class Deposito:
    def __init__(self, materiales, cantidades):
        self.materiales = materiales
        self.cantidades = cantidades

        self.validar_cant(cantidades)

    def agregar_materiales(self, materiales, cantidades):
        for material, cantidad in zip(materiales, cantidades):
            if material in self.materiales:
                posicion = self.materiales.index(material)
                self.cantidades[posicion] += cantidad
            else:
                self.materiales.append(material)
                self.cantidades.append(cantidad)

    def sacar_materiales(self, materiales, cantidades):
        for material, cantidad in zip(materiales, cantidades):
            if material not in self.materiales:
                raise ValueError(
                    f"El material '{material.nombre}' no se encuentra en el depósito"
                )

            posicion = self.materiales.index(material)

            if self.cantidades[posicion] < cantidad:
                raise ValueError(
                    f"No hay suficiente stock de '{material.nombre}'"
                )

            self.cantidades[posicion] -= cantidad

    def consultar_stock(self, material=None):
        if material is not None:
            if material not in self.materiales:
                return 0
            else:
                posicion = self.materiales.index(material)
                return self.cantidades[posicion]

        return self.materiales, self.cantidades

    @staticmethod 
    def validar_cant(cant):
        if not isinstance(cant, int):
            raise TypeError("La cantidad debe ser un entero")
        if cant < 0:
            raise ValueError("La cantidad no puede ser negativa")

