from remesa import Remesa


class Deposito:

    def __init__(self):
        self.stock = {}

        for remesa in Remesa.todos:

            for material, cantidad, fecha in zip(
                remesa.materiales,
                remesa.cantidades,
                remesa.fechas_vencimiento
            ):

                if material not in self.stock:
                    self.stock[material] = {}

                if fecha not in self.stock[material]:
                    self.stock[material][fecha] = {}

                proveedor = remesa.proveedor

                if proveedor not in self.stock[material][fecha]:
                    self.stock[material][fecha][proveedor] = 0

                self.stock[material][fecha][proveedor] += cantidad

    def agregar_materiales(self, materiales, cantidades, proveedores, fechas_vencimiento):
        for material, cantidad, proveedor, fecha in zip(
            materiales, cantidades, proveedores, fechas_vencimiento
        ):
            if material in self.materiales:
                posicion = self.materiales.index(material)
                self.cantidades[posicion] += cantidad
            else:
                self.materiales.append(material)
                self.cantidades.append(cantidad)

            if material not in self.stock:
                self.stock[material] = {}

            if fecha not in self.stock[material]:
                self.stock[material][fecha] = {}

            if proveedor not in self.stock[material][fecha]:
                self.stock[material][fecha][proveedor] = 0

            self.stock[material][fecha][proveedor] += cantidad

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

            # Sacar primero lo que vence antes
            cantidad_restante = cantidad

            fechas = sorted(self.stock[material].keys())

            for fecha in fechas:
                proveedores = self.stock[material][fecha]

                for proveedor in list(proveedores.keys()):
                    cantidad_disponible = proveedores[proveedor]

                    cantidad_a_sacar = min(
                        cantidad_restante,
                        cantidad_disponible
                    )

                    proveedores[proveedor] -= cantidad_a_sacar
                    cantidad_restante -= cantidad_a_sacar

                    if proveedores[proveedor] == 0:
                        del proveedores[proveedor]

                    if cantidad_restante == 0:
                        break

                if not proveedores:
                    del self.stock[material][fecha]

                if cantidad_restante == 0:
                    break

    def consultar_stock(self, material=None):
        if material is not None:
            if material not in self.materiales:
                return 0

            posicion = self.materiales.index(material)
            return self.cantidades[posicion]

        return self.materiales, self.cantidades

    @staticmethod
    def validar_cant(cant):
        if not isinstance(cant, int):
            raise TypeError("La cantidad debe ser un entero")

        if cant < 0:
            raise ValueError("La cantidad no puede ser negativa")