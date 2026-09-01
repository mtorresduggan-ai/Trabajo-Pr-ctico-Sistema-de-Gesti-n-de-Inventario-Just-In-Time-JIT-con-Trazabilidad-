class Material:
    todos = []

    def __init__(self,nombre, composicion, unidad_medida, punto_reposicion, fecha_vencimiento):
        self.nombre = nombre
        self.composicion = composicion
        self.unidad_medida = unidad_medida
        self.punto_reposicion = punto_reposicion
        self.fecha_vencimiento = fecha_vencimiento

        self.validar_nombre(nombre)
        self.validar_composicion(composicion)
        self.validar_unidad_medida(unidad_medida)
        self.validar_punto_reposicion(punto_reposicion)
        self.validar_fecha_vencimiento(fecha_vencimiento)

        Material.todos.append(self)

    def cambiar_punto_reposicion(self, nuevo_punto):
        self.validar_punto_reposicion(nuevo_punto) 
        self.punto_reposicion = nuevo_punto
    

    def necesita_reposicion(self, stock_actual):
        return stock_actual <= self.punto_reposicion
    

    def __str__(self):
        return 'Material: ' + self.nombre + 'Composicion: ' + self.composicion + 'Unidad de medida: ' + self.unidad_medida

    @classmethod
    def informar(cls):
        return cls.todos

    @staticmethod
    def validar_nombre(nombre):
        if not isinstance(nombre, str):
            raise TypeError("El nombre del material debe ser un str")
        if nombre.strip() == "":
            raise ValueError("El nombre del material no puede estar vacio")

    @staticmethod
    def validar_composicion(composicion):
        if not isinstance(composicion, str):
            raise TypeError("La composicion debe ser un str")
        if composicion.strip() == "":
            raise ValueError("La composicion no puede estar vacia")

    @staticmethod
    def validar_unidad_medida(unidad_medida):
        if not isinstance(unidad_medida, str):
            raise TypeError("La unidad de medida debe ser un str")
        if unidad_medida.strip() == "":
            raise ValueError("La unidad de medida no puede estar vacia")

    @staticmethod
    def validar_punto_reposicion(punto_reposicion):
        if not isinstance(punto_reposicion, (int, float)):
            raise TypeError("El punto de reposición debe ser un número")

        if punto_reposicion < 0:
            raise ValueError(
                "El punto de reposición no puede ser negativo"
            )
#### ACA HAY QUE VALIDAR BIEN
    @staticmethod
    def validar_fecha_vencimiento(fecha_vencimiento):
        if fecha_vencimiento is not None:
            if not isinstance(fecha_vencimiento, str):
                raise TypeError(
                    "La fecha de vencimiento debe ser un texto o None"
                )