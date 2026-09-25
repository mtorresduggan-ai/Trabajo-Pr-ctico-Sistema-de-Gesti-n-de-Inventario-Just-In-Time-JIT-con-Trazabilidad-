class Deposito:

    def __init__(self):
        self.stock = dict()

    def __str__(self):
        texto = ""

        for material, datos in self.stock.items():
            for dato in datos:
                texto += (
                    f"{material.nombre}: {dato['cantidad']} unidades "
                    f"- vence {dato['fecha_vencimiento']}\n"
                )

        return texto