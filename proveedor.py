class Proveedor:
    todos = []

    def __init__(self, id, nombre, plazo_estimado, telefono, dni, email, fecha_alta, fecha_baja):
        super().__init__(id, nombre, telefono, dni, email, fecha_alta, fecha_baja)
        self.plazo_estimado = plazo_estimado

        self.validar_plazo(plazo_estimado)

        Proveedor.todos.append(self)

    def cambiar_plazo_estimado(self, nuevo_plazo):
        self.validar_plazo(nuevo_plazo)
        self.plazo_estimado = nuevo_plazo

    def proveedor_no_cumple(self, plazo_real):
        self.validar_plazo(plazo_real)
        return plazo_real > self.plazo_estimado

    def __str__(self):
        return 'Nombre: ' + self.nombre + '  Telefono: ' + self.telefono

    @classmethod
    def informar(cls):
        return cls.todos

    @staticmethod
    def validar_plazo(plazo):
        if not isinstance(plazo, int):
            raise TypeError("El plazo de entrega debe ser un int")
        if plazo <= 0:
            raise ValueError("El plazo de entrega debe ser mayor a 0 días")
