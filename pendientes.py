from tarea import Tarea

class Tareas_pendientes:
    def __init__(self):
        self._frente = None
        self._final = None
        self._registradas = set()

    def get_frente(self):
        return self._frente
    
    def get_final(self):
        return self._final

    def set_frente(self, nueva_frente):
        self._frente = nueva_frente

    def set_final(self, nuevo_final):
        self._final = nuevo_final

    def es_vacia(self):
        return self._frente is None

    def agregar(self, tarea):
        if not isinstance(tarea, Tarea):
            raise TypeError("Debe agregarse una tarea")

        nuevo = tarea
        nuevo.set_siguiente(None)

        if self.es_vacia():
            self._frente = nuevo
        else:
            self._final.set_siguiente(nuevo)

        self._final = nuevo

        if tarea.get_objeto() is not None:
            self._registradas.add((tarea.get_tipo(), tarea.get_objeto()))

    def sacar(self):
        if self.es_vacia():
            raise ValueError("No hay tareas pendientes")

        tarea = self._frente
        self._frente = self._frente.get_siguiente()
        tarea.set_siguiente(None)

        if self._frente is None:
            self._final = None

        self._registradas.discard((tarea.get_tipo(), tarea.get_objeto()))

        return tarea

    def ver_primera(self):
        return self._frente

    def contar_tareas(self):
        cantidades = {}
        actual = self.get_frente()

        while actual is not None:
            tipo = actual.get_tipo()

            if tipo in cantidades:
                cantidades[tipo] += 1
            else:
                cantidades[tipo] = 1

            actual = actual.get_siguiente()

        return cantidades

    def mostrar_cantidades(self):
        print(self.contar_tareas())

    def existe_tarea(self, tipo, objeto):
        return (tipo, objeto) in self._registradas

    def existe_tarea_reposicion(self, material):
        return self.existe_tarea("reponer", material)
   
    def obtener_tareas(self):
        tareas = []
        actual = self._frente

        while actual is not None:
            tareas.append(actual)
            actual = actual.get_siguiente()

        return tareas