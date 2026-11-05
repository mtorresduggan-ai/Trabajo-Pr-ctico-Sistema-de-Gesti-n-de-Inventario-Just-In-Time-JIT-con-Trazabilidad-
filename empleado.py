from individuo import Individuo

class Empleado(Individuo):

    def __init__(self, nombre, telefono, dni, fecha_alta, email, usuario, clave, fecha_baja=None, id_manual=None):
        self.validar_usuario(usuario)
        self.validar_clave(clave)

        super().__init__(nombre, telefono, dni, email, fecha_alta, fecha_baja, id_manual)
        self._usuario = usuario
        self._clave = clave

    def a_fila(self):
        return super().a_fila() + [self.get_usuario(), self.get_clave()]

    def get_usuario(self):
        return self._usuario

    def get_clave(self):
        return self._clave

    def set_usuario(self, nuevo_usuario):
        self.validar_usuario(nuevo_usuario)

        if nuevo_usuario == self._usuario:
            raise ValueError("El nuevo usuario debe ser distinto al usuario anterior")

        self._usuario = nuevo_usuario

    def set_clave(self, nueva_clave):
        self.validar_clave(nueva_clave)
        if nueva_clave == self._clave:
            raise ValueError("La nueva clave debe ser distinta a la clave anterior")
        self._clave = nueva_clave

    @staticmethod
    def validar_usuario(usuario):
        if not isinstance(usuario, str):
            raise TypeError("El usuario debe ser un str")
        if usuario.strip() == "":
            raise ValueError("El usuario no puede estar vacio")

    @staticmethod
    def validar_clave(clave):
        if not isinstance(clave, str):
            raise TypeError("La clave debe ser un str")
        if len(clave) < 8:
            raise ValueError("La clave debe tener al menos 8 caracteres")
        if not any(map(lambda caracter: caracter.isupper(), clave)):
            raise ValueError("La clave debe contener al menos una mayuscula")
        if not any(map(lambda caracter: caracter.islower(), clave)):
            raise ValueError("La clave debe contener al menos una minuscula")
        if not any(map(lambda caracter: caracter.isdigit(), clave)):
            raise ValueError("La clave debe tener al menos un numero")
        if not any(map(lambda caracter: not caracter.isalnum(), clave)):
            raise ValueError("La clave debe tener al menos un caracter especial")

    @staticmethod
    def validar_cantidades(cantidades):
        if not isinstance(cantidades, list):
            raise TypeError("Las cantidades deben estar en una lista")
        if not all(map(lambda cantidad: isinstance(cantidad, (int, float)), cantidades)):
            raise TypeError("Cada cantidad debe ser un numero")
        if any(map(lambda cantidad: cantidad <= 0, cantidades)):
            raise ValueError("La cantidad debe ser mayor a cero")

    @staticmethod
    def validar_materiales(materiales):
        if not isinstance(materiales, list):
            raise TypeError("Los materiales deben estar en una lista")