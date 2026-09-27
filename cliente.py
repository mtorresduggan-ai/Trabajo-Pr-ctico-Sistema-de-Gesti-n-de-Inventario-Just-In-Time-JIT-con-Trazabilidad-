from individuo import Individuo

class Cliente(Individuo):

    todos = []

    def __init__(self, nombre, telefono, dni, email, fecha_alta, fecha_baja=None):
        super().__init__(nombre, telefono, dni, email, fecha_alta, fecha_baja)

        Cliente.todos.append(self)