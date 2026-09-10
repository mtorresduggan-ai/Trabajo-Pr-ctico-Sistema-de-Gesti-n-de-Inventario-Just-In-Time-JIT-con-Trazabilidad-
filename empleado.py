from datetime import date

class Empleado:
    todos= []

    def __init__(self, id_empleado, nombre, telefono, dni, fecha_inicio, email):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.telefono = telefono
        self.dni = dni
        self.fecha_inicio = fecha_inicio
        self.email = email

        self.validar_id_unico(id_empleado)
        self.validar_fecha(fecha_inicio)
        self.validar_id(id_empleado)
        self.validar_nombre(nombre)
        self.validar_telefono(telefono)
        self.validar_dni(dni)
        self.validar_email(email)

    @classmethod
    def validar_id_unico(cls, id):
        for solicitud in cls.todos:
            if solicitud.id_solicitud == id:
                raise ValueError(f"Ya existe un empleado con id '{id}'")

    @staticmethod
    def validar_fecha(fecha):
        if fecha is not None:
            if not isinstance(fecha, date):
                raise TypeError(
                    "La fecha de inicio debe ser en formato fecha"
                )

    @staticmethod
    def validar_id(id):
        if not isinstance(id, int):
            raise TypeError("El ID del empleado debe ser un entero")
        if id <= 0:
            raise ValueError("El ID del empleado debe ser mayor a 0")

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

