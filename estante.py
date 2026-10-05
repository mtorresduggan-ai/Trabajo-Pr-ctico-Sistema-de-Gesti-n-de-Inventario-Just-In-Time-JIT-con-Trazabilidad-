from caja import Caja

class Estante:
    def __init__(self, cantidad_inicial, fecha_inicial):
        self.prox_a_vencer=Caja(cantidad_inicial, fecha_inicial)

    