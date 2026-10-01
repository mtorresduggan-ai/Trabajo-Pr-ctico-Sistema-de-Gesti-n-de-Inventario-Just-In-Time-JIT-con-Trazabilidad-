from datetime import timedelta

class Remesa:
    todos = []

    def __init__(self, materiales, proveedor, solicitud, saldo_disponible, cantidades, fechas_vencimiento, fecha_llegada, **datos):

        self.validar_saldo_disponible(saldo_disponible)
        self.validar_cant_y_saldo(saldo_disponible, cantidades)

        self.id_remesa = len(Remesa.todos)+1
        self.materiales = materiales
        self.proveedor = proveedor
        self.solicitud = solicitud
        self.saldo_disponible = saldo_disponible
        self.cantidades = cantidades
        self.fechas_vencimiento = fechas_vencimiento
        self.fecha_llegada = fecha_llegada
        self.datos = datos

        self.evaluar_proveedor()

        Remesa.todos.append(self)

    def evaluar_proveedor(self):
        if self.solicitud and self.proveedor:
            dias_reales = (self.fecha_llegada - self.solicitud.fecha).days
            if dias_reales <= self.proveedor.plazo_estimado:
                self.proveedor.modificar_puntaje(0.5)
            else:
                self.proveedor.modificar_puntaje(-0.5)

    def set_saldo(self, nuevo_saldo):
        self.validar_saldo_disponible(nuevo_saldo)
        self.validar_cant_y_saldo(nuevo_saldo, self.cantidades)
        self.saldo_disponible = nuevo_saldo

    def agregar_material(self, material, cantidad, fecha_vencimiento):
        self.materiales.append(material)
        self.cantidades.append(cantidad)
        self.fechas_vencimiento.append(fecha_vencimiento)

    def quitar_material(self, material):
        if material not in self.materiales:
            raise ValueError("El material no se encuentra en la remesa")

        posicion = self.materiales.index(material)
        self.materiales.pop(posicion)
        self.cantidades.pop(posicion)
        self.fechas_vencimiento.pop(posicion)

    def __str__(self):
        return (
            'ID Remesa: ' + str(self.id_remesa) +
            ' Proveedor: ' + self.proveedor.nombre +
            ' Saldo disponible: ' + str(self.saldo_disponible) +
            ' Materiales: ' + str(self.materiales) +
            ' Cantidades: ' + str(self.cantidades) +
            ' Fecha de llegada: ' + str(self.fecha_llegada))

    @classmethod
    def informar(cls):
        return cls.todos

    @staticmethod
    def validar_saldo_disponible(saldo_disponible):
        if not isinstance(saldo_disponible, (int, float)):
            raise TypeError("El saldo debe ser un número")
        if saldo_disponible < 0:
            raise ValueError("El saldo disponible debe ser mayor o igual a cero")

    @staticmethod
    def validar_cant_y_saldo(saldo_disponible, cantidades):
        if saldo_disponible > sum(cantidades):
            raise ValueError("El saldo disponible debe ser menor o igual a la cantidad total recibida")