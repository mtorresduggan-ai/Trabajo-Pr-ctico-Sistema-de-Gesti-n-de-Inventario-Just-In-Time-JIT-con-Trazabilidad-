from individuo import Individuo
from material import Material

class Empleado(Individuo):
    todos= []

    def __init__(self, nombre, telefono, dni, fecha_alta, email, usuario, clave):
        
        self.validar_usuario(usuario)
        self.validar_clave(clave)
        
        super().__init__(nombre, telefono, dni, email, fecha_alta, fecha_baja=None)

        self.usuario = usuario
        self.clave = clave       

        Empleado.todos.append(self)

    def actualizar_usuario(self,usuario) :
        self.validar_usuario(usuario)
        if usuario == self.usuario:
            raise ValueError("El nuevo usuario debe ser distinto al usuario anterior")
        self.usuario = usuario

    def set_clave(self, nueva_clave):
        self.validar_clave(nueva_clave)
        if nueva_clave == self.clave: 
            raise ValueError("La nueva clave debe ser distinta a la clave anterior")
        self.clave = nueva_clave

    @staticmethod
    def validar_usuario(usuario):
        if not isinstance(usuario,str):
            raise TypeError("El usuario debe ser un str")
        if usuario.strip() == "":
            raise ValueError("El usuario no puede estar vacio")

    @staticmethod
    def validar_clave(clave):
        if not isinstance(clave,str):
            raise TypeError("La clave debe ser un str")
        if len(clave) < 8:
            raise ValueError("La clave debe tener al menos 8 caracteres")
        if not any(caracter.isupper() for caracter in clave):
            raise ValueError("La clave debe contener al menos una mayuscula")
        if not any(caracter.islower() for caracter in clave):
            raise ValueError("La clave debe contener al menos una minuscula")
        if not any(caracter.isdigit() for caracter in clave):
            raise ValueError("La clave debe tener al menos un numero")
        if not any(not caracter.isalnum() for caracter in clave):
            raise ValueError("La clave debe tener al menos un caracter especial")

    @staticmethod 
    def validar_cantidades(cantidades):
        if not isinstance(cantidades, list):
            raise TypeError("Las cantidades deben estar en una lista")
        if not all(isinstance(cantidad, (int, float)) for cantidad in cantidades):
            raise TypeError("Cada cantidad debe ser un numero")
        if any(cantidad <= 0 for cantidad in cantidades):
            raise ValueError("La cantidad debe ser mayor a cero")

    @staticmethod
    def validar_materiales(materiales):
        if not isinstance(materiales, list):
            raise TypeError("Los materiales deben estar en una lista")
        if not all (material in Material.todos for material in materiales):
            raise ValueError("Todos los materiales deben estar registrados")