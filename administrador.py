from empleado import Empleado

class Administrador(Empleado):
    def __init__(self, id_empleado, nombre, telefono, dni):
        super().__init__(id_empleado, nombre, telefono, dni)