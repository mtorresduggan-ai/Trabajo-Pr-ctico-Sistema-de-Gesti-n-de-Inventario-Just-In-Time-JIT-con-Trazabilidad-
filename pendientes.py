from tarea import Tarea

class Tareas_pendientes():
    def _init_(self):
        self._frente = None
        self._final = None

    
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
        
        nuevo = Tarea(tarea)

        if self._frente is None:
            self._frente = nuevo
            self._final = nuevo
        else:
            self._final.set_siguiente = nuevo
            self._final = nuevo

    def sacar(self):
        if self.es_vacia():
            raise ValueError("No hay tareas pendientes")

        tarea = self.frente
        self._frente = self._frente.get_siguiente
        tarea.set_siguiente(None)

        if self._frente is None:
            self._final = None

        return tarea

    def ver_primera(self):
        return self._frente