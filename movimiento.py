class Movimiento:
    todos=[]

    def __init__(self, fecha, materiales, cantidades):
        
        self.id_movimiento = len(Movimiento.todos) + 1
        self.fecha = fecha
        self.materiales = materiales
        self.cantidades = cantidades

        Movimiento.todos.append(self)