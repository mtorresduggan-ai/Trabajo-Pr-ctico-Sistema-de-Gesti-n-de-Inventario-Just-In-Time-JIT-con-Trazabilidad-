from datetime import date

class Individuo:
    todos= []

    def __init__(self, nombre, telefono, dni, email, fecha_alta, fecha_baja=None):
        self.nombre = nombre
        self.telefono= telefono
        self.dni = dni
        self.fecha_alta = fecha_alta
        self.fecha_baja = fecha_baja
        self.email = email
        self.id = len(Individuo.todos)+1

        self.validar_nombre(nombre)
        self.validar_telefono(telefono)
        self.validar_dni(dni)
        self.validar_fecha(fecha_baja)
        self.validar_fecha(fecha_alta)
        self.validar_email(email)

    @staticmethod
    def validar_fecha(fecha):
        if fecha is not None:
            if not isinstance(fecha, date):
                raise TypeError(
                    "La fecha de inicio debe ser en formato fecha"
                )

    @staticmethod
    def validar_nombre(nombre):
        if not isinstance(nombre, str):
            raise TypeError("El nombre del empleado debe ser un str")
        if nombre.strip() == "":
            raise ValueError("El nombre del empleado no puede estar vacio")

    @staticmethod
    def validar_telefono(telefono):
        if not isinstance(telefono, str):
            raise TypeError("El telefono debe ser un str")
        telefono_limpio = telefono.replace("+", "").replace("-", "").replace(" ", "")
        if telefono.strip() == "":
            raise ValueError("El telefono no puede estar vacio")
        if not telefono_limpio.isdigit():
            raise ValueError("El telefono debe contener solo numeros, espacios, '+' o '-'")

    @staticmethod
    def validar_dni(dni):
        if not isinstance(dni, int):
            raise TypeError("El DNI del empleado debe ser un entero")
        if dni <= 0:
            raise ValueError("El DNI del empleado debe ser mayor a 0")

    @staticmethod
    def validar_email(email):
        if not isinstance(email, str):
            raise TypeError("El email del empleado debe ser un str")
        if email.strip() == "":
            raise ValueError("El email del empleado no puede estar vacio")


