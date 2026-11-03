class NodoArbol:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.sub_izq = None
        self.sub_der = None

    def __str__(self):
        return f"{self.clave}: {self.valor}"

    def get_clave(self):
        return self.clave

    def get_valor(self):
        return self.valor

    def get_sub_izq(self):
        return self.sub_izq

    def get_sub_der(self):
        return self.sub_der

    def set_sub_izq(self, nodo):
        self.sub_izq = nodo

    def set_sub_der(self, nodo):
        self.sub_der = nodo