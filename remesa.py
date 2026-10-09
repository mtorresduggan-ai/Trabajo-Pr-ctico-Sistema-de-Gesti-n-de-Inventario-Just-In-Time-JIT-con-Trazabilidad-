from tarea import Tarea

class Remesa:
    todos = []

    def __init__(self, materiales, proveedor, solicitud, cantidades, fechas_vencimiento, deposito, tareas_pendientes_supervisor, fecha_llegada, **datos):

        self.id_remesa = len(Remesa.todos)+1
        self.materiales = materiales
        self.proveedor = proveedor
        self.solicitud = solicitud
        self.cantidades = cantidades
        self.fechas_vencimiento = fechas_vencimiento
        self.fecha_llegada = fecha_llegada
        self.datos = datos

        self.evaluar_proveedor()

        tareas_pendientes_supervisor.agregar(Tarea("remesa", self, deposito))

        Remesa.todos.append(self)

    def evaluar_proveedor(self):
        if self.solicitud and self.proveedor:
            dias_reales = (self.fecha_llegada - self.solicitud.fecha).days
            if dias_reales <= self.proveedor.plazo_estimado:
                self.proveedor.modificar_puntaje(0.5)
            else:
                self.proveedor.modificar_puntaje(-0.5)


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

