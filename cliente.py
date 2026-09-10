from individuo import Individuo

class Cliente(Individuo):
    def __init__(self, id, nombre, telefono, dni, email, fecha_alta, fecha_baja):
        super().__init__(id, nombre, telefono, dni, email, fecha_alta, fecha_baja)