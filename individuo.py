from datetime import date

class Individuo:
    todos= []

    def __init__(self, nombre, telefono, dni, email, fecha_alta, fecha_baja=None):
        
        self.validar_nombre(nombre)
        self.validar_telefono(telefono)
        self.validar_dni(dni)
        self.validar_fecha(fecha_baja)
        self.validar_fecha(fecha_alta)
        self.validar_email(email)

        self._nombre = nombre
        self._telefono= telefono
        self._dni = dni
        self._fecha_alta = fecha_alta
        self._fecha_baja = fecha_baja
        self._email = email
        self._id = len(Individuo.todos)+1

        Individuo.todos.append(self)

    def get_nombre(self):
        return self._nombre
    def get_telefono(self):
        return self._telefono
    def get_dni(self):
        return self._dni
    def get_fecha_alta(self):
        return self._fecha_alta
    def get_fecha_baja(self):
        return self._fecha_baja
    def get_email(self):
        return self._email
    def get_id(self):
        return self._id


    def set_nombre(self, nombre):
        self.validar_nombre(nombre)
        self._nombre = nombre

    def set_telefono(self, telefono):
        self.validar_telefono(telefono)
        self._telefono = telefono

    def set_email(self, email):
        self.validar_email(email)
        self._email = email

    def set_fecha_baja(self, fecha_baja):
        self.validar_fecha(fecha_baja)
        self._fecha_baja = fecha_baja

    
    def actualizar_datos(self, nombre=None, telefono=None, email=None, fecha_baja=None):
        if nombre is not None:
            self.set_nombre(nombre)
        if telefono is not None:
            self.set_telefono(telefono)
        if email is not None:
            self.set_email(email)
        if fecha_baja is not None:
            self.set_fecha_baja(fecha_baja)


    @staticmethod
    def validar_fecha(fecha):
        if fecha is not None:
            if not isinstance(fecha, date):
                raise TypeError("La fecha debe ser en formato fecha")

    @staticmethod
    def validar_nombre(nombre):
        if not isinstance(nombre, str):
            raise TypeError("El nombre del individuo debe ser un str")
        if nombre.strip() == "":
            raise ValueError("El nombre del individuo no puede estar vacio")

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
            raise TypeError("El DNI del individuo debe ser un entero")
        if dni <= 0:
            raise ValueError("El DNI del individuo debe ser mayor a 0")

    @staticmethod
    def validar_email(email):
        if not isinstance(email, str):
            raise TypeError("El email del individuo debe ser un str")
        if email.strip() == "":
            raise ValueError("El email del individuo no puede estar vacio")
        if "@" not in email:
            raise ValueError("El email del individuo debe contener un '@'")