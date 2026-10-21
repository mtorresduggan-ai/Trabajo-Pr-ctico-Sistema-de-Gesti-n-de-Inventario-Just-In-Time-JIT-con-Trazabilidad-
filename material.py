class Material:
    todos = []

    def __init__(self, nombre, composicion, unidad_medida, punto_reposicion, id_manual=None):
        self.validar_nombre(nombre)
        self.validar_composicion(composicion)
        self.validar_unidad_medida(unidad_medida)
        self.validar_punto_reposicion(punto_reposicion)

        if id_manual is not None:
            self._id_material = int(id_manual)
        else:
            ids = [material.get_id_material() for material in Material.todos]
            if ids:
                self._id_material = max(ids) + 1
            else:
                self._id_material = 1

        self._nombre = nombre
        self._composicion = composicion
        self._unidad_medida = unidad_medida
        self._punto_reposicion = punto_reposicion

        Material.todos.append(self)

    def a_fila(self):
        return [self._id_material,self._nombre,self._composicion,self._unidad_medida,self._punto_reposicion]

    def get_id_material(self):
        return self._id_material

    def get_nombre(self):
        return self._nombre

    def get_composicion(self):
        return self._composicion

    def get_unidad_medida(self):
        return self._unidad_medida

    def get_punto_reposicion(self):
        return self._punto_reposicion

    def set_nombre(self, nuevo_nombre):
        self.validar_nombre(nuevo_nombre)
        self._nombre = nuevo_nombre

    def set_composicion(self, nueva_composicion):
        self.validar_composicion(nueva_composicion)
        self._composicion = nueva_composicion

    def set_unidad_medida(self, nueva_unidad_medida):
        self.validar_unidad_medida(nueva_unidad_medida)
        self._unidad_medida = nueva_unidad_medida

    def set_punto_reposicion(self, nuevo_punto):
        self.validar_punto_reposicion(nuevo_punto)
        self._punto_reposicion = nuevo_punto

    def necesita_reposicion(self, stock_actual):
        if not isinstance(stock_actual, (int, float)):
            raise TypeError("El stock actual debe ser un número")
        if stock_actual < 0:
            raise ValueError("El stock actual no puede ser negativo")
        return stock_actual <= self._punto_reposicion

    def __str__(self):
        return 'Material: ' + self._nombre + ', Composicion: ' + self._composicion + ', Unidad de medida: ' + self._unidad_medida

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
            raise ValueError("El punto de reposición no puede ser negativo")
