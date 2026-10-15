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

    def get_id_remesa(self):
        return self._id_remesa
    def get_materiales(self):
        return self._materiales
    def get_proveedor(self):
        return self._proveedor
    def get_solicitud(self):
        return self._solicitud
    def get_cantidades(self):
        return self._cantidades
    def get_fechas_vencimiento(self):
        return self._fechas_vencimiento
    def get_fecha_llegada(self):
        return self._fecha_llegada
    def get_datos(self):
        return self._datos
    
    def set_materiales(self, nuevos_materiales):
        self._materiales = nuevos_materiales
    def set_proveedor(self, nuevo_proveedor):
        self._proveedor = nuevo_proveedor
    def set_solicitud(self, nueva_solicitud):
        self._solicitud = nueva_solicitud
    def set_cantidades(self, nuevas_cantidades):
        self._cantidades = nuevas_cantidades
    def set_fechas_vencimiento(self, nuevas_fechas):
        self._fechas_vencimiento = nuevas_fechas
    def set_fecha_llegada(self, nueva_fecha):
        self._fecha_llegada = nueva_fecha
    def set_datos(self, nuevos_datos):
        self._datos = nuevos_datos

    def evaluar_proveedor(self):
        if self._solicitud and self._proveedor:
            dias_reales = (self._fecha_llegada - self._solicitud.get_fecha()).days
            if dias_reales <= self._proveedor.get_plazo_estimado():
                self._proveedor.modificar_puntaje(0.5)
            else:
                self._proveedor.modificar_puntaje(-0.5)


    def agregar_material(self, material, cantidad, fecha_vencimiento):
        self._materiales.append(material)
        self._cantidades.append(cantidad)
        self._fechas_vencimiento.append(fecha_vencimiento)

    def quitar_material(self, material):
        if material not in self._materiales:
            raise ValueError("El material no se encuentra en la remesa")

        posicion = self._materiales.index(material)
        self._materiales.pop(posicion)
        self._cantidades.pop(posicion)
        self._fechas_vencimiento.pop(posicion)

    def __str__(self):
        return (
            'ID Remesa: ' + str(self.get_id_remesa()) +
            ' Proveedor: ' + self.get_proveedor().get_nombre() +
            ' Materiales: ' + str(self.get_materiales()) +
            ' Cantidades: ' + str(self.get_cantidades()) +
            ' Fecha de llegada: ' + str(self.get_fecha_llegada())
        )

    @classmethod
    def informar(cls):
        return cls.todos

