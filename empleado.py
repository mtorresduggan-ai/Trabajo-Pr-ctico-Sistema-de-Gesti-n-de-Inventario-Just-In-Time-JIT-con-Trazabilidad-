from datetime import date

class Empleado:
    todos= []

    def _init_(self, id_empleado, nombre, telefono, dni, fecha_inicio, email, usuario, clave, fecha_contratacion, estado):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.telefono = telefono
        self.dni = dni
        self.fecha_inicio = fecha_inicio
        self.email = email
        self.usuario = usuario
        self.clave = clave
        self.fecha_contratacion = fecha_contratacion
        self.estado = estado

        self.validar_usuario(usuario)
        self.validar_clave(clave)
        self.validar_fecha_contratacion(fecha_contratacion)
        self.validar_estado(estado)

    def actualizar_datos(self, nombre=None, telefono=None, dni=None, fecha_inicio=None, usuario=None, fecha_contratacion = None, estado = None):
        if  nombre is not None:
            self.validar_nombre(nombre)
            self.nombre = nombre
        if  telefono is not None:
            self.validar_telefono(telefono)
            self.telefono = telefono
        if  dni is not None:
            self.validar_dni(dni)
            self.dni = dni
        if  fecha_inicio is not None:
            self.validar_fecha_inicio(fecha_inicio)
            self.fecha_inicio = fecha_inicio
        if  usuario is not None:
            self.validar_usuario(usuario)
            self.usuario = usuario
        if fecha_contratacion is not None:
            self.validar_fecha_contratacion(fecha_contratacion)
            self.fecha_contratacion = fecha_contratacion
        if estado is not None:
            self.validar_estado(estado)
            self.estado = estado


    def cambiar_clave(self, nueva_clave):
        self.validar_clave(nueva_clave)
        if nueva_clave == self.clave: 
            raise ValueError("La nueva clave debe ser distinta a la clave anterior")
        self.clave = nueva_clave


    @staticmethod
    def validar_usuario(usuario):
        if not isinstance(usuario,str):
            raise TypeError("El usuario debe ser un sstr")
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
            raise ValueError("La clave debe contener la menos una minuscula")
        if not any(caracter.isdigit() for caracter in clave):
            raise ValueError("La clave debe tener al menos un numero")
        if not any(caracter.isalum() for caracter in clave):
            raise ValueError("La clave debe tener al menos un caracter especial")

    @staticmethod
    def validar_fecha_contratacion(fecha_contratacion):
        if not isinstance(fecha_contratacion, date):
            raise TypeError("La fecha de contratacion debe ser una fecha")

    @staticmethod
    def validar_estado(estado):
        if not isinstance(estado, str):
            raise ValueError("El estado debe ser un str")