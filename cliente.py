from individuo import Individuo

class Cliente(Individuo):

    todos = []

    def __init__(self, nombre, telefono, dni, email, fecha_alta, fecha_baja=None):
        super().__init__(nombre, telefono, dni, email, fecha_alta, fecha_baja)
        Cliente.todos.append(self)

    def __str__(self):
        baja = str(self.get_fecha_baja()) if self.get_fecha_baja() is not None else "Activo"
        return (
            'ID: ' + str(self.get_id()) +
            ' Nombre: ' + self.get_nombre() +
            ' DNI: ' + str(self.get_dni()) +
            ' Telefono: ' + self.get_telefono() +
            ' Email: ' + self.get_email() +
            ' Fecha de alta: ' + str(self.get_fecha_alta()) +
            ' Baja: ' + baja)