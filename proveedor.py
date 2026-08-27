class Proveedor:
    todos = []

    def __init__(self, id_proveedor, nombre, plazo_estimado, telefono):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.plazo_estimado = plazo_estimado
        self.telefono = telefono

        Proveedor.todos.append(self)

    def cambiar_plazo_estimado(self, nuevo_plazo):
            self.plazo_estimado = nuevo_plazo

    def proveedor_no_cumple(self, plazo_real):
          return plazo_real > self.plazo_estimado

    def __str__(self):
        return 'Nombre: ' + self.nombre + 'Telefono: ' + self.telefono

    @classmethod
    def informar(cls):
        return cls.todos