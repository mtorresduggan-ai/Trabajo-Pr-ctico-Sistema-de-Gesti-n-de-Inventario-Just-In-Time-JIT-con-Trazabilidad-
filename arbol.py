from nodo_arbol import NodoArbol


class Arbol:
    def __init__(self):
        self.raiz = None
        self.cantidad = 0
        self.pasos_ultima_busqueda = 0

    def get_raiz(self):
        return self.raiz

    def set_raiz(self, nodo):
        self.raiz = nodo

    def get_cantidad(self):
        return self.cantidad

    def get_pasos_ultima_busqueda(self):
        return self.pasos_ultima_busqueda

    def es_vacio(self):
        return self.raiz is None

    def insertar(self, clave, valor, subarbol=None):
        if self.es_vacio():
            self.raiz = NodoArbol(clave, valor)
            self.cantidad += 1
            return

        if subarbol is None:
            subarbol = self.raiz

        if clave < subarbol.get_clave():
            if subarbol.get_sub_izq() is None:
                subarbol.set_sub_izq(NodoArbol(clave, valor))
                self.cantidad += 1
            else:
                self.insertar(clave, valor, subarbol.get_sub_izq())

        elif clave > subarbol.get_clave():
            if subarbol.get_sub_der() is None:
                subarbol.set_sub_der(NodoArbol(clave, valor))
                self.cantidad += 1
            else:
                self.insertar(clave, valor, subarbol.get_sub_der())

        else:
            raise ValueError(f"Ya existe un elemento con la clave '{clave}'")

    def insertar_balanceado(self, pares):
        if len(pares) == 0:
            return

        medio = len(pares) // 2
        clave, valor = pares[medio]
        self.insertar(clave, valor)

        self.insertar_balanceado(pares[:medio])
        self.insertar_balanceado(pares[medio + 1:])

    def buscar(self, clave, subarbol=None, pasos=1):
        if self.es_vacio():
            self.pasos_ultima_busqueda = 0
            raise ValueError(f"No existe un elemento con la clave '{clave}'")

        if subarbol is None:
            subarbol = self.raiz

        if subarbol.get_clave() == clave:
            self.pasos_ultima_busqueda = pasos
            return subarbol.get_valor()

        if clave < subarbol.get_clave():
            siguiente = subarbol.get_sub_izq()
        else:
            siguiente = subarbol.get_sub_der()

        if siguiente is None:
            self.pasos_ultima_busqueda = pasos
            raise ValueError(f"No existe un elemento con la clave '{clave}' (se revisaron {pasos} nodos)")

        return self.buscar(clave, siguiente, pasos + 1)

    def recorrido_inorden(self, subarbol=None, valores=None):
        if valores is None:
            valores = []

        if self.es_vacio():
            return valores

        if subarbol is None:
            subarbol = self.raiz

        if subarbol.get_sub_izq() is not None:
            self.recorrido_inorden(subarbol.get_sub_izq(), valores)

        valores.append(subarbol.get_valor())

        if subarbol.get_sub_der() is not None:
            self.recorrido_inorden(subarbol.get_sub_der(), valores)

        return valores