from individuo import Individuo

class Proveedor(Individuo):
    todos = []

    def __init__(self, nombre, plazo_estimado, telefono, dni, email, fecha_alta, fecha_baja=None):
        
        self.validar_plazo(plazo_estimado)

        super().__init__(nombre, telefono, dni, email, fecha_alta, fecha_baja)
        self._plazo_estimado = plazo_estimado
        self._puntaje = 5

        Proveedor.todos.append(self)

    def get_plazo_estimado(self):
        return self._plazo_estimado

    def get_puntaje(self):
        return self._puntaje
    
    def set_plazo_estimado(self, nuevo_plazo):
        self.validar_plazo(nuevo_plazo)
        self._plazo_estimado = nuevo_plazo

    def __str__(self):
        return 'Nombre: ' + self.get_nombre + '  Telefono: ' + self.get_telefono

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
        nuevo_puntaje = self._puntaje + cambio

        if nuevo_puntaje < 0:
            self._puntaje = 0
        elif nuevo_puntaje > 10:
            self._puntaje = 10
        else:
            self._puntaje = nuevo_puntaje