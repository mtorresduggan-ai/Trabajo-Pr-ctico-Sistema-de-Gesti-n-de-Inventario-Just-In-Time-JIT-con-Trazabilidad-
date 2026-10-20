class Tarea:
    def __init__(self, tipo, objeto, datos=None):
        self._tipo = tipo
        self._objeto = objeto
        self._datos = datos
        self._siguiente = None

    def get_tipo(self):
        return self._tipo

    def get_objeto(self):
        return self._objeto

    def get_siguiente(self):
        return self._siguiente

    def get_datos(self):
        return self._datos

    def set_tipo(self, nuevo_tipo):
        self._tipo = nuevo_tipo

    def set_objeto(self, nuevo_objeto):
        self._objeto = nuevo_objeto

    def set_siguiente(self, nueva_tarea):
        self._siguiente = nueva_tarea