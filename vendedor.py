from empleado import Empleado
from pedido import Pedido_salida
from cliente import Cliente
from tarea import Tarea

class Vendedor(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja=None, id_manual=None):
        super().__init__(nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja, id_manual)

    def crear_pedido_salida(self, fecha, materiales, cantidades, cliente, clientes, tareas_pendientes_admin):
        Empleado.validar_fecha(fecha)
        Empleado.validar_cantidades(cantidades)
        Empleado.validar_materiales(materiales)
        self.validar_cliente(cliente, clientes)
        self.validar_listas(materiales, cantidades)

        precios_unitarios = list(map(lambda material: material.get_precio_venta(), materiales))

        pedido = Pedido_salida(fecha, materiales, cantidades, precios_unitarios, cliente, "Pendiente", self)
        
        tareas_pendientes_admin.agregar(Tarea('pedido', pedido))
        
        return pedido


    def consultar_pedido_todos(self, pedidos):
        return list(filter(lambda pedido: pedido.get_vendedor() == self, pedidos))


    def consultar_pedido(self, id_pedido, pedidos):
        encontrados = list(filter(lambda pedido: pedido.get_id_pedido() == id_pedido,
        self.consultar_pedido_todos(pedidos)))

        if len(encontrados) == 0:
            raise ValueError("No existe ese pedido")

        return encontrados[0]

    def cancelar_pedido(self, id_pedido, pedidos):
        pedido = self.consultar_pedido(id_pedido, pedidos)

        if pedido.get_estado() in ("Despachado", "Entregado", "Cancelado", "Rechazado"):
            raise ValueError(f"No se puede cancelar un pedido en estado "f"'{pedido.get_estado()}'")

        pedido.set_estado("Cancelado")
        return pedido


    def modificar_pedido(self, id_pedido, pedidos, materiales=None,cantidades=None, fecha=None, cliente=None, clientes=None):
        pedido = self.consultar_pedido(id_pedido, pedidos)
        
        if pedido.get_estado() != "Pendiente":
            raise ValueError(f"Solo se pueden modificar pedidos en estado Pendiente (este está '{pedido.get_estado()}')")
        
        precios_nuevos = None
        if materiales is not None:
            precios_nuevos = list(map(lambda material: material.get_precio_venta(), materiales))

        campos = {"materiales": (materiales, Empleado.validar_materiales, pedido.set_materiales),
            "cantidades": (cantidades, Empleado.validar_cantidades, pedido.set_cantidades),
            "fecha": (fecha, Empleado.validar_fecha, pedido.set_fecha),
            "cliente": (cliente, lambda valor: self.validar_cliente(valor, clientes), pedido.set_cliente)}
            
        for valor, validar, set_valor in campos.values():
            if valor is not None:
                validar(valor)
                set_valor(valor)

        if precios_nuevos is not None:
            pedido.set_precios_unitarios(precios_nuevos)

        return pedido

    @staticmethod
    def validar_cliente(cliente, clientes):
        if cliente not in clientes:
            raise ValueError("El cliente no esta registrado")

    @staticmethod
    def validar_listas(materiales, cantidades):
        if len(materiales) != len(cantidades):
            raise ValueError("Debe haber una cantidad por cada material")