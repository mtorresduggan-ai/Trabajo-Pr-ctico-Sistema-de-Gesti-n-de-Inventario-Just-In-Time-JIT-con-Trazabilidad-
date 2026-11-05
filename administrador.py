from empleado import Empleado
from datetime import date
from tarea import Tarea


class Administrador(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja=None, id_manual=None):
        super().__init__(nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja, id_manual)
    
    def aceptar_solicitud(self, solicitud):
        if solicitud.get_estado() != "Pendiente": 
            raise ValueError("Solo se pueden aceptar solicitudes en estado Pendiente")
        
        solicitud.set_fecha_envio(date.today())
        solicitud.set_estado("Solicitado")

    def aceptar_pedido_salida(self, pedido, deposito):
        if pedido.get_estado() != "Pendiente":
            raise ValueError("Solo se pueden aceptar pedidos en estado Pendiente")

        faltantes = deposito.materiales_sin_stock(pedido.get_materiales(), pedido.get_cantidades(), date.today())
        if len(faltantes) > 0:
            raise ValueError(f"No hay suficiente stock de {faltantes[0].get_nombre()}")

        pedido.set_fecha_aceptacion(date.today())
        pedido.set_estado('En preparacion')
        
    def crear_transferencia(self, deposito_origen, deposito_destino, materiales, cantidades, tareas_pendientes_supervisor):
        Empleado.validar_materiales(materiales)
        Empleado.validar_cantidades(cantidades)
        self.validar_listas(materiales, cantidades)

        if deposito_destino==deposito_origen:
            raise ValueError('El deposito origen y deposito destino no puede ser el mismo')
        faltantes = deposito_origen.materiales_sin_stock(materiales, cantidades, date.today())
       
        if len(faltantes) > 0:
            raise ValueError(f"Transferencia cancelada: Stock insuficiente de {faltantes[0].get_nombre()} en origen.")
       
        datos = (deposito_origen, deposito_destino, materiales, cantidades)
        tareas_pendientes_supervisor.agregar(Tarea('transferencia', None, datos))

    def ejecutar_siguiente_tarea(self, tareas_pendientes_admin, deposito, tareas_pendientes_supervisor, decision):
        tarea = tareas_pendientes_admin.ver_primera()

        if tarea is None:
            raise ValueError("No hay tareas pendientes")

        acciones = {"solicitud": self.aceptar_solicitud,
        "pedido": lambda objeto: self.aceptar_pedido_salida(objeto, deposito)}

        objeto = tarea.get_objeto()
        tipo = tarea.get_tipo()

        if decision == "rechazar":
            objeto.set_estado("Rechazado")
            tareas_pendientes_admin.sacar()
            return "Tarea rechazada correctamente."

        if decision != "aceptar":
            raise ValueError("Decisión inválida")

        if tipo not in acciones:
            raise ValueError("Tipo de tarea desconocido")

        try:
            acciones[tipo](objeto)
        except ValueError as error:
            objeto.set_estado("Cancelado")
            tareas_pendientes_admin.sacar()
            return f"No se pudo aceptar la tarea: {error}"

        if tipo == "pedido":
            tareas_pendientes_supervisor.agregar(Tarea("pedido", objeto, deposito))

        tareas_pendientes_admin.sacar()
        return "Tarea aceptada correctamente."

    def baja_empleado(self, empleado, empleados):
        if empleado not in empleados:
            raise ValueError("El empleado no está registrado")

        if empleado.get_fecha_baja() is not None:
            raise ValueError("El empleado ya está dado de baja")

        empleado.set_fecha_baja(date.today())
        return f"Empleado {empleado.get_nombre()} dado de baja."

    def modificar_empleado(self, empleado, empleados, nombre=None,telefono=None, email=None, usuario=None, clave=None):
        if empleado not in empleados:
            raise ValueError("El empleado no está registrado")

        if nombre is not None:
            empleado.set_nombre(nombre)
        if telefono is not None:
            empleado.set_telefono(telefono)
        if email is not None:
            empleado.set_email(email)
        if usuario is not None:
            empleado.actualizar_usuario(usuario)
        if clave is not None:
            empleado.set_clave(clave)

    def cargar_precio_proveedor(self, proveedor, material, precio, proveedores):
        if proveedor not in proveedores:
            raise ValueError("Este proveedor no está registrado")
        if proveedor.get_fecha_baja() is not None:
            raise ValueError("El proveedor está dado de baja")
        proveedor.agregar_material(material, precio)
        return f"{proveedor.get_nombre()} ahora vende {material.get_nombre()} a ${precio}"

    def baja_proveedor(self, proveedor, proveedores):
        if proveedor not in proveedores:
            raise ValueError("Este proveedor no está registrado")

        if proveedor.get_fecha_baja() is not None:
            raise ValueError("El proveedor ya está dado de baja")

        proveedor.set_fecha_baja(date.today())
        return f"Proveedor {proveedor.get_nombre()} dado de baja."

    def baja_cliente(self, cliente, clientes):
        if cliente not in clientes:
            raise ValueError("El cliente no está registrado")

        if cliente.get_fecha_baja() is not None:
            raise ValueError("Este cliente ya está dado de baja")

        cliente.set_fecha_baja(date.today())
        return f"Cliente {cliente.get_nombre()} dado de baja."

    def generar_reporte_empleados(self, empleados):
        reporte = "Reporte de empleados:\n"

        for empleado in empleados:
            if empleado.get_fecha_baja() is None:
                estado = "Activo"
            else:
                estado = f"Baja: {empleado.get_fecha_baja()}"

            reporte += (f"Nombre: {empleado.get_nombre()}\n"
                f"DNI: {empleado.get_dni()}\n"
                f"Telefono: {empleado.get_telefono()}\n"
                f"Email: {empleado.get_email()}\n"
                f"Usuario: {empleado.get_usuario()}\n"
                f"Estado: {estado}\n")
        return reporte

    def generar_reporte_proveedores(self, proveedores):
        reporte = "Reporte de proveedores:\n"

        for proveedor in proveedores:
            if proveedor.get_fecha_baja() is None:
                estado = "Activo"
            else:
                estado = f"Baja: {proveedor.get_fecha_baja()}"

            reporte += (f"Nombre: {proveedor.get_nombre()}\n"
                f"DNI: {proveedor.get_dni()}\n"
                f"Telefono: {proveedor.get_telefono()}\n"
                f"Email: {proveedor.get_email()}\n"
                f"Plazo estimado: {proveedor.get_plazo_estimado()} dias\n"
                f"Puntaje: {proveedor.get_puntaje()}\n"
                f"Estado: {estado}\n")
        return reporte

    def generar_reporte_clientes(self, clientes):
        reporte = "Reporte de clientes:\n"

        for cliente in clientes:
            if cliente.get_fecha_baja() is None:
                estado = "Activo"
            else:
                estado = f"Baja: {cliente.get_fecha_baja()}"

            reporte += (f"Nombre: {cliente.get_nombre()}\n"
                f"DNI: {cliente.get_dni()}\n"
                f"Telefono: {cliente.get_telefono()}\n"
                f"Email: {cliente.get_email()}\n"
                f"Estado: {estado}\n")
        return reporte

    @staticmethod
    def validar_listas(materiales, cantidades):
        if not isinstance(materiales, list) or not isinstance(cantidades, list):
            raise TypeError("Materiales y cantidades deben ser listas")
        if len(materiales) != len(cantidades):
            raise ValueError("Debe haber una cantidad por cada material")