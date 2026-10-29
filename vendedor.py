from empleado import Empleado
from pedido import Pedido_salida
from cliente import Cliente
from tarea import Tarea

class Vendedor(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja=None, id_manual=None):
        super().__init__(nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja, id_manual)

    def crear_pedido_salida(self, fecha, materiales, cantidades, cliente, tareas_pendientes_admin):
        Empleado.validar_fecha(fecha)
        Empleado.validar_cantidades(cantidades)
        Empleado.validar_materiales(materiales)
        self.validar_cliente(cliente)
        self.validar_listas(materiales, cantidades)

        precios_unitarios = []

        for material in materiales:
            precios_unitarios.append(material.get_precio_venta())

        pedido = Pedido_salida(fecha, materiales, cantidades, precios_unitarios, cliente, "Pendiente", self)
        
        tareas_pendientes_admin.agregar(Tarea('pedido', pedido))
        
        return pedido


    def consultar_pedido_todos(self, pedidos):
        return [p for p in pedidos if p.get_vendedor() == self]


    def consultar_pedido(self, id_pedido, pedidos):
        for pedido in pedidos:
            if (pedido.get_vendedor() == self and pedido.get_id_pedido() == id_pedido):
                return pedido
        raise ValueError("No existe ese pedido")


    def cancelar_pedido(self, id_pedido, pedidos):
        pedido = self.consultar_pedido(id_pedido, pedidos)

        if pedido.get_estado() in ("Entregado", "Cancelado"):
            raise ValueError(f"No se puede cancelar un pedido en estado "f"'{pedido.get_estado()}'")

        pedido.set_estado("Cancelado")
        return pedido


    def modificar_pedido(self, id_pedido, pedidos, materiales=None,cantidades=None, fecha=None, cliente=None, estado=None):
        pedido = self.consultar_pedido(id_pedido, pedidos)
        
        if pedido.get_estado() in ("Entregado", "Cancelado"):
            raise ValueError(f"No se puede modificar un pedido en estado '{pedido.get_estado()}'")
        
        campos = {"materiales": (materiales, Empleado.validar_materiales, pedido.set_materiales),
            "cantidades": (cantidades, Empleado.validar_cantidades, pedido.set_cantidades),
            "fecha": (fecha, Empleado.validar_fecha, pedido.set_fecha),
            "cliente": (cliente, self.validar_cliente, pedido.set_cliente),
            "estado": (estado, Pedido_salida.validar_estado, pedido.set_estado),}

        for valor, validar, set_valor in campos.values():
            if valor is not None:
                validar(valor)
                set_valor(valor)

        return pedido

    @staticmethod
    def validar_cliente(cliente, clientes):
        if cliente not in clientes:
            raise ValueError("El cliente no esta registrado")

    @staticmethod
    def validar_listas(materiales, cantidades):
        if len(materiales) != len(cantidades):
            raise ValueError("Debe haber una cantidad por cada material")