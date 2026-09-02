from material import Material

class Pedido_salida:
    todos = []

    def __init__(self, id_pedido_salida, fecha_emision, materiales, cant_materiales):
        self.id_pedido_salida = id_pedido_salida
        self.fecha_emision = fecha_emision
        self.materiales = materiales
        self.cant_materiales = cant_materiales

        self.validar_id_unico(id_pedido_salida)
        self.validar_materiales(materiales)
        self.validar_fecha(fecha_emision)
        self.validar_cant_materiales(cant_materiales)
        self.validar_id(id_pedido_salida)
        

        Pedido_salida.todos.append(self)

    def set_fecha_emision(self, nueva_fecha):
        self.validar_fecha(nueva_fecha)
        self.fecha_emision = nueva_fecha

    def set_cantidad(self, nueva_cantidad):
        self.validar_cant_materiales(nueva_cantidad)
        self.cant_materiales = nueva_cantidad

    def agregar_material(self, material):
        if material not in Material.todos:
            raise ValueError("El material no esta registrado")
        self.materiales.append(material)

    def quitar_material(self, material):
        if material not in self.materiales:
            raise ValueError("El material no se encuentra en la lista de materiales del pedido")
        self.materiales.remove(material)

    def informar(self):
        return 'ID Pedido: ' + str(self.id_pedido_salida) + ' Fecha de emision: ' + str(self.fecha_emision) + ' Cantidad de materiales: ' + str(self.cant_materiales)

    @classmethod
    def informar_todos(cls):
        return cls.todos

    @classmethod
    def validar_id_unico(cls, id):
        for pedido in cls.todos:
            if pedido.id_pedido_salida == id:
                raise ValueError(f"Ya existe un pedido con id '{id}'")

    @staticmethod
    def validar_materiales(materiales):
        if not isinstance(materiales, list):
            raise TypeError("Los materiales deben estar en una lista")

        for material in materiales:
            if material not in Material.todos:
                raise ValueError("El material no esta registrado")

    @staticmethod
    def validar_fecha(fecha):
        if fecha is not None:
            if not isinstance(fecha, str):
                raise TypeError(
                    "La fecha de emision debe ser un texto o None"
                )

    @staticmethod 
    def validar_cant_materiales(cant_materiales):
        if not isinstance(cant_materiales, int):
            raise TypeError("La cantidad de materiales debe ser un entero")
        if cant_materiales < 0:
            raise ValueError("La cantidad de materiales no puede ser negativa")
    
    @staticmethod
    def validar_id(id_pedido_salida):
        if not isinstance(id_pedido_salida, int):
            raise TypeError("El ID del pedido debe ser un entero")
        if id_pedido_salida <= 0:
            raise ValueError("El ID del pedido debe ser mayor a 0")
    