from gestor_materiales import GestorMateriales
from gestor_proveedores import GestorProveedores
from gestor_clientes import GestorClientes
from gestor_empleados import GestorEmpleados
from gestor_depositos import GestorDepositos
from gestor_solicitudes import GestorSolicitudes
from gestor_pedidos import GestorPedidos
from gestor_remesas import GestorRemesas
from gestor_tareas import GestorTareas


class Sistema:

    def __init__(self):
        self._gestor_materiales = GestorMateriales()
        self._gestor_proveedores = GestorProveedores(self._gestor_materiales)
        self._gestor_clientes = GestorClientes()
        self._gestor_empleados = GestorEmpleados()
        self._gestor_depositos = GestorDepositos(self._gestor_materiales)
        self._gestor_solicitudes = GestorSolicitudes(self._gestor_materiales, self._gestor_proveedores, self._gestor_empleados)
        self._gestor_pedidos = GestorPedidos(self._gestor_materiales, self._gestor_clientes, self._gestor_empleados)
        self._gestor_remesas = GestorRemesas(self._gestor_materiales, self._gestor_proveedores, self._gestor_solicitudes)
        self._gestor_tareas = GestorTareas(self._gestor_materiales, self._gestor_depositos,
            self._gestor_solicitudes, self._gestor_pedidos, self._gestor_remesas)

    def get_gestor_materiales(self):
        return self._gestor_materiales

    def get_gestor_proveedores(self):
        return self._gestor_proveedores

    def get_gestor_clientes(self):
        return self._gestor_clientes

    def get_gestor_empleados(self):
        return self._gestor_empleados

    def get_gestor_depositos(self):
        return self._gestor_depositos

    def get_gestor_solicitudes(self):
        return self._gestor_solicitudes

    def get_gestor_pedidos(self):
        return self._gestor_pedidos

    def get_gestor_remesas(self):
        return self._gestor_remesas

    def cargar_estado_total(self, tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor):
        self._gestor_materiales.cargar_materiales()
        self._gestor_proveedores.cargar_proveedores()
        self._gestor_proveedores.cargar_precios_proveedores()
        self._gestor_clientes.cargar_clientes()
        self._gestor_empleados.cargar_empleados()
        self._gestor_depositos.cargar_depositos()
        self._gestor_solicitudes.cargar_solicitudes()
        self._gestor_pedidos.cargar_pedidos()
        self._gestor_remesas.cargar_remesas()
        self._gestor_depositos.cargar_stock()
        self._gestor_tareas.cargar_tareas_todas(tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor)

    def guardar_estado_total(self, tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor):
        self._gestor_materiales.guardar_materiales()
        self._gestor_proveedores.guardar_proveedores()
        self._gestor_proveedores.guardar_precios_proveedores()
        self._gestor_clientes.guardar_clientes()
        self._gestor_empleados.guardar_empleados()
        self._gestor_depositos.guardar_depositos()
        self._gestor_solicitudes.guardar_solicitudes()
        self._gestor_pedidos.guardar_pedidos()
        self._gestor_remesas.guardar_remesas()
        self._gestor_depositos.guardar_stock()
        self._gestor_tareas.guardar_tareas_todas(tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor)