from movimiento import Movimiento
from proveedor import Proveedor

class Solicitud_proveedor(Movimiento):
    todos = []

    def __init__(self, id_movimiento, proveedor, fecha, materiales, cantidades, estado, comprador):
        super().__init__(id_movimiento, fecha, materiales, cantidades)
        self.proveedor = proveedor
        self.estado = estado
        self.comprador = comprador

        self.validar_proveedor(proveedor)

        Solicitud_proveedor.todos.append(self)

    def cambiar_proveedor(self, nuevo_proveedor):
        if nuevo_proveedor not in Proveedor.todos:
            raise ValueError("El proveedor no se encuentra en la lista de proveedores registrados en el sistema")        
        self.proveedor = nuevo_proveedor

    def informar(self):
        return 'ID Solicitud: ' + str(self.id_movimiento) + ' Proveedor: ' + self.proveedor.nombre + ' Fecha de emision: ' + str(self.fecha) + ' Cantidad de materiales: ' + str(self.cantidades)

    @classmethod
    def informar_todos(cls):
        return cls.todos

    @staticmethod
    def validar_proveedor(proveedor):
        if proveedor not in Proveedor.todos:
            raise ValueError("El proveedor no esta registrado")

    @staticmethod
    def validar_estado(estado):
        estados_validos = ['Pendiente', 'En preparacion', 'Despachado', 'Entregado', 'Cancelado']

        if estado not in estados_validos:
            raise ValueError(f"Estado no valido. Solo se permiten: {estados_validos}")

    @staticmethod
    def validar_estado(estado):
        estados_validos = ['Pendiente', 'Enviada', 'Aceptada', 'En transito', 'Recibida', 'Cancelada']
        if estado not in estados_validos:
            raise ValueError(f"Estado no valido. Solo se permiten: {estados_validos}")