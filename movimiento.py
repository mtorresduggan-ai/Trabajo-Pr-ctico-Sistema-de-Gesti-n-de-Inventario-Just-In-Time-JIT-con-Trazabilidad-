class Movimiento:
    todos = []

    def __init__(self, fecha, materiales, cantidades):
        self._id_movimiento = len(Movimiento.todos) + 1
        self._fecha = fecha
        self._materiales = materiales
        self._cantidades = cantidades

        Movimiento.todos.append(self)

 
    def get_id_movimiento(self):
        return self._id_movimiento
    def get_fecha(self):
        return self._fecha
    def get_materiales(self):
        return self._materiales
    def get_cantidades(self):
        return self._cantidades
   
    def set_fecha(self, nueva_fecha):
        self._fecha = nueva_fecha
    def set_materiales(self, nuevos_materiales):
        self._materiales = nuevos_materiales
    def set_cantidades(self, nuevas_cantidades):
        self._cantidades = nuevas_cantidades