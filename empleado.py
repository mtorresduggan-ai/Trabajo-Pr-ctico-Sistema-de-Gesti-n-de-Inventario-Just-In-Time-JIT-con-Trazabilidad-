from individuo import Individuo
from material import Material
from datetime import date

class Empleado(Individuo):
    todos= []

    def __init__(self, nombre, telefono, dni, fecha_alta, email, usuario, clave):
        
        self.validar_usuario(usuario)
        self.validar_clave(clave)
        
        super().__init__(nombre, telefono, dni, email, fecha_alta, fecha_baja=None)

        self.usuario = usuario
        self.clave = clave       

        Empleado.todos.append(self)

    def actualizar_usuario(self,usuario=None) :
        if  usuario is not None:
            self.validar_usuario(usuario)
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
    def validar_fecha(fecha):
        if fecha is not None:
            if not isinstance(fecha, date):
                raise TypeError(
                    "La fecha de inicio debe ser en formato fecha"
                )

    @staticmethod 
    def validar_cantidades(cant):
        if not isinstance(cant, float):
            raise TypeError("La cantidad debe ser un numero real")
        if cant < 0:
            raise ValueError("La cantidad no puede ser negativa")

    @staticmethod
    def validar_materiales(materiales):
        if not isinstance(materiales, list):
            raise TypeError("Los materiales deben estar en una lista")

        for material in materiales:
            if material not in Material.todos:
                raise ValueError("El material no esta registrado")
