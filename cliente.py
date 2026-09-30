from individuo import Individuo

class Cliente(Individuo):

    todos = []

    def __init__(self, nombre, telefono, dni, email, fecha_alta, fecha_baja=None):
        super().__init__(nombre, telefono, dni, email, fecha_alta, fecha_baja)
        Cliente.todos.append(self)

    def __str__(self):
        baja = str(self.fecha_baja) if self.fecha_baja is not None else "Activo"
        return (
            'ID: ' + str(self.id) +
            ' Nombre: ' + self.nombre +
            ' DNI: ' + str(self.dni) +
            ' Telefono: ' + self.telefono +
            ' Email: ' + self.email +
            ' Fecha de alta: ' + str(self.fecha_alta) +
            ' Baja: ' + baja)