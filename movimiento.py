class Movimiento:
    todos=[]

    def __init__(self, id_movimiento, fecha, materiales, cantidades):
        
        self.id_movimiento = id_movimiento
        self.fecha = fecha
        self.materiales = materiales
        self.cantidades = cantidades

        Movimiento.todos.append(self)