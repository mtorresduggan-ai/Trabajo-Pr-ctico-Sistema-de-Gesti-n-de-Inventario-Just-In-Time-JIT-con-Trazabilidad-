class Material:
    todos = []

    def __init__(self,nombre, composicion, unidad_medida, punto_reposicion, fecha_vencimiento):
        self.nombre = nombre
        self.composicion = composicion
        self.unidad_medida = unidad_medida
        self.punto_reposicion = punto_reposicion
        self.fecha_vencimiento = fecha_vencimiento

        Material.todos.append(self)

    def cambiar_punto_reposicion(self, nuevo_punto):
        self.punto_reposicion = nuevo_punto

    def necesita_reposicion(self, stock_actual):
        return stock_actual <= self.punto_reposicion

    def __str__(self):
        return 'Material: ' + self.nombre + 'Composicion: ' + self.composicion + 'Unidad de medida: ' + self.unidad_medida

    @classmethod
    def informar(cls):
        return cls.todos