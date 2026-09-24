from individuo import Individuo

class Cliente(Individuo):

    todos = []

    def __init__(self, id, nombre, telefono, dni, email, fecha_alta, fecha_baja):
        super().__init__(id, nombre, telefono, dni, email, fecha_alta, fecha_baja)

        Cliente.todos.append(self)
