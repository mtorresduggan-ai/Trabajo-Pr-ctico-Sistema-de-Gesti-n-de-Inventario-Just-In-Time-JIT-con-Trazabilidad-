from tarea import Tarea

class Tareas_pendientes():
    def _init_(self):
        self.frente = None
        self.final = None

    def es_vacia(self):
        return self.frente is None

    def agregar(self, tarea):
        if not isinstance(tarea, Tarea): 
            raise TypeError("Debe agregarse una tarea")
        
        nuevo = Tarea(tarea)

        if self.frente is None:
            self.frente = nuevo
            self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo

    def sacar(self):
        if self.es_vacia():
            raise ValueError("No hay tareas pendientes")

        tarea = self.frente
        self.frente = self.frente.siguiente
        tarea.siguiente = None

        if self.frente is None:
            self.final = None

        return tarea

    def ver_primera(self):
        return self.frente