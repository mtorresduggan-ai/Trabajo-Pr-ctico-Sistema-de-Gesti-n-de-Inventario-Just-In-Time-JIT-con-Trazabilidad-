class Movimiento:
    todos = []

    def __init__(self, fecha, materiales, cantidades, id_manual=None):
        self._fecha = fecha
        self._materiales = materiales
        self._cantidades = cantidades

        if id_manual is not None:
            self._id_movimiento = int(id_manual)
        else:
            ids = []
            for movimiento in Movimiento.todos:
                ids.append(movimiento.get_id_movimiento())
            if len(ids) > 0:
                self._id_movimiento = max(ids) + 1
            else:
                self._id_movimiento = 1

        Movimiento.todos.append(self)

    def a_fila(self):
        return [self.get_id_movimiento(), self.get_fecha()]
 
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