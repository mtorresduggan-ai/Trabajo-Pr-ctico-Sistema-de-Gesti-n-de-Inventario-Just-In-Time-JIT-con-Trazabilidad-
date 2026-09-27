from individuo import Individuo

class Proveedor(Individuo):
    todos = []

    def __init__(self, nombre, plazo_estimado, telefono, dni, email, fecha_alta, fecha_baja=None):
        
        self.validar_plazo(plazo_estimado)

        super().__init__(nombre, telefono, dni, email, fecha_alta, fecha_baja)
        self.plazo_estimado = plazo_estimado
        self.puntaje = 5

        Proveedor.todos.append(self)

    def set_plazo_estimado(self, nuevo_plazo):
        self.validar_plazo(nuevo_plazo)
        self.plazo_estimado = nuevo_plazo

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
    
    def modificar_puntaje(self, cambio):
        if not isinstance(cambio, (int, float)):
            raise TypeError("El cambio de puntaje debe ser un numero")
        nuevo_puntaje = self.puntaje + cambio

        if nuevo_puntaje < 0:
            self.puntaje = 0
        elif nuevo_puntaje > 10:
            self.puntaje = 10
        else:
            self.puntaje = nuevo_puntaje