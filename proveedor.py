class Proveedor:
    todos = []

    def __init__(self, id_proveedor, nombre, plazo_estimado, telefono):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.plazo_estimado = plazo_estimado
        self.telefono = telefono

        self.validar_id_unico(id_proveedor)
        self.validar_nombre(nombre)
        self.validar_plazo(plazo_estimado)
        self.validar_telefono(telefono)

        Proveedor.todos.append(self)

    def cambiar_plazo_estimado(self, nuevo_plazo):
            self.plazo_estimado = nuevo_plazo

    def proveedor_no_cumple(self, plazo_real):
          return plazo_real > self.plazo_estimado

    def __str__(self):
        return 'Nombre: ' + self.nombre + 'Telefono: ' + self.telefono

    @classmethod
    def informar(cls):
        return cls.todos

    @classmethod
    def validar_id_unico(cls, id_proveedor):
        for proveedor in cls.todos:
            if proveedor.id_proveedor == id_proveedor:
                raise ValueError(f"Ya existe un proveedor con id '{id_proveedor}'")

    @staticmethod
    def validar_nombre(nombre):
        if not isinstance(nombre, str):
            raise TypeError("El nombre del material debe ser un str")
        if nombre.strip() == "":
            raise ValueError("El nombre del material no puede estar vacio")

    @staticmethod
    def validar_plazo(plazo):
        if not isinstance(plazo, int):
            raise TypeError("El plazo de entrega debe ser un int")
        if plazo <= 0:
            raise ValueError("El plazo de entrega debe ser mayor a 0 días")

    @staticmethod
    def validar_telefono(telefono):
        if not isinstance(telefono, str):
            raise TypeError("El telefono debe ser un str")
        telefono_limpio = telefono.replace("+", "").replace("-", "").replace(" ", "")
        if not telefono_limpio.isdigit():
            raise ValueError("El telefono debe contener solo numeros, espacios, '+' o '-'")