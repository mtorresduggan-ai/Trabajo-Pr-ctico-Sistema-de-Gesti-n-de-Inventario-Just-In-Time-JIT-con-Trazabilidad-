from tarea import Tarea

class Pendientes():
    def _init_(self):
        self.inicio = None
        self.final = None

    def esVacia(self):
        return self.inicio is None

    def agregar(self, tarea):
        nuevo = Tarea(tarea)

        if self.frente is None:
            self.frente = nuevo
            self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo

    def sacar(self):
        if self.frente is None:
            raise ValueError("No hay tareas pendientes")

        tarea = self.frente.tarea
        self.frente = self.frente.siguiente

        if self.frente is None:
            self.final = None

        return tarea