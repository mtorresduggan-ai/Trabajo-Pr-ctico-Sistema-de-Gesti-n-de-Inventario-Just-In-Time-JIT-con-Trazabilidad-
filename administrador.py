from empleado import Empleado
from datetime import date
from proveedor import Proveedor
from cliente import Cliente
from tarea import Tarea


class Administrador(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email, usuario, clave):
        super().__init__(nombre, telefono, dni, fecha_alta, email, usuario, clave)

    def aceptar_solicitud(self, solicitud):
        if solicitud.get_estado != "Pendiente": 
            raise ValueError("Solo se pueden aceptar solicitudes en estado Pendiente")
        
        solicitud.set_fecha_envio = date.today()
        solicitud.set_estado = "Solicitado"


    def aceptar_pedido_salida(self, pedido, deposito):
        if pedido.get_estado != "Pendiente":
            raise ValueError("Solo se pueden aceptar pedidos en estado Pendiente")

        for material, cantidad in zip(pedido.get_materiales, pedido.get_cantidades):
            if material not in deposito.get_stock:
                raise ValueError(f"No hay stock de {material.get_nombre}")

            stock_total = deposito.stock_total(material)

            if stock_total < cantidad:
                raise ValueError(f"No hay suficiente stock de {material.get_nombre}")

        pedido.set_fecha_aceptacion(date.today())
        pedido.set_estado('En preparación')

        
    def crear_transferencia(self, deposito_origen, deposito_destino, materiales, cantidades, tareas_pendientes_supervisor):
        self.validar_listas_2(materiales, cantidades)

        if deposito_destino==deposito_origen:
            raise ValueError('El deposito origen y deposito destino no puede ser el mismo')

        for material, cantidad in zip(materiales, cantidades):
            if material not in deposito_origen.get_stock:
                raise ValueError(f"No hay stock de {material.get_nombre} en el depósito de origen")

            stock_disponible = deposito_origen.stock_total(material)
            if stock_disponible < cantidad:
                raise ValueError(f"Transferencia cancelada: Stock insuficiente de {material.nombre} en origen. ")

        tareas_pendientes_supervisor.agregar(Tarea('transferencia', None, (deposito_origen, deposito_destino, materiales, cantidades)))

    #clase transferencia?

    def ejecutar_siguiente_tarea(self, tareas_pendientes_admin, deposito, tareas_pendientes_supervisor):
        tarea = tareas_pendientes_admin.ver_primera()

        if tarea is None:
            raise ValueError("No hay tareas pendientes")

        if tarea.get_tipo() == "solicitud":
            self.aceptar_solicitud(tarea.get_objeto())

        elif tarea.get_tipo() == "pedido":
            self.aceptar_pedido_salida(tarea.get_objeto(), deposito)

            tareas_pendientes_supervisor.agregar(Tarea("pedido", tarea.get_objeto(), deposito))

        else:
            raise ValueError('Tipo de tarea desconocido')

        tareas_pendientes_admin.sacar()

    def baja_empleado(self, empleado):
        if empleado not in Empleado.todos:
            raise ValueError("El empleado no está registrado")

        if empleado.get_fecha_baja is not None:
            raise ValueError("El empleado ya está dado de baja")

        empleado.set_fecha_baja = date.today()


    def modificar_empleado(self, empleado, nombre=None, telefono=None, email=None, usuario=None, clave=None):
        if empleado not in Empleado.todos:
            raise ValueError("El empleado no está registrado")
        if nombre is not None:
            empleado.validar_nombre(nombre)
            empleado.set_nombre = nombre
        if telefono is not None:
            empleado.validar_telefono(telefono)
            empleado.set_telefono = telefono
        if email is not None:
            empleado.validar_email(email)
            empleado.set_email = email
        if usuario is not None:
            empleado.actualizar_usuario(usuario)
        if clave is not None:
            empleado.set_clave(clave) 


    def baja_proveedor(self, proveedor):
        if proveedor not in Proveedor.todos:
            raise ValueError("Este proveedor no está registrado")

        if proveedor.get_fecha_baja is not None:
            raise ValueError("El proveedor ya está dado de baja")

        proveedor.set_fecha_baja = date.today()    


    def baja_cliente(self, cliente):
        if cliente not in Cliente.todos:
            raise ValueError("El cliente no está registrado")

        if cliente.get_fecha_baja is not None:
            raise ValueError("Este cliente ya está dado de baja")

        cliente.set_fecha_baja = date.today()


    def generar_reporte_empleados(self):
        reporte = "Reporte de empleados:\n"

        for empleado in Empleado.todos:
            if empleado.get_fecha_baja is None:
                estado = "Activo"
            else:
                estado = f"Baja: {empleado.get_fecha_baja}"

            reporte += (f"Nombre: {empleado.get_nombre}\nDNI: {empleado.get_dni}\nTelefono: {empleado.get_telefono}\nEmail: {empleado.get_email}\nUsuario: {empleado.get_usuario}\nEstado: {estado}\n")

        return reporte


    def generar_reporte_proveedores(self):
        reporte = "Reporte de proveedores:\n"

        for proveedor in Proveedor.todos:
            if proveedor.get_fecha_baja is None:
                estado = "Activo"
            else:
                estado = f"Baja: {proveedor.get_fecha_baja}"

            reporte += (
                f"Nombre: {proveedor.get_nombre}\nDNI: {proveedor.get_dni}\nTelefono: {proveedor.get_telefono}\nEmail: {proveedor.get_email}\nPlazo estimado: {proveedor.get_plazo_estimado} dias\nPuntaje: {proveedor.get_puntaje}\nEstado: {estado}\n")

        return reporte


    def generar_reporte_clientes(self):
        reporte = "Reporte de clientes:\n"

        for cliente in Cliente.todos:
            if cliente.get_fecha_baja is None:
                estado = "Activo"
            else:
                estado = f"Baja: {cliente.get_fecha_baja}"

            reporte += (f"Nombre: {cliente.get_nombre}\nDNI: {cliente.get_dni}\nTelefono: {cliente.get_telefono}\nEmail: {cliente.get_email}\nEstado: {estado}\n")

        return reporte

    @staticmethod
    def validar_fechas_vencimiento(fechas):
        if not isinstance(fechas, list):
            raise TypeError("Las fechas de vencimiento deben estar en una lista")

        if not all(isinstance(fecha, date) for fecha in fechas):
            raise TypeError("Todas las fechas de vencimiento deben ser fechas")

    @staticmethod
    def validar_listas(materiales, cantidades, fechas_vencimiento):
        if len(materiales) != len(cantidades) or len(materiales) != len(fechas_vencimiento):
            raise ValueError("Debe haber una cantidad y una fecha de vencimiento por cada material")

    @staticmethod
    def validar_listas_2(materiales, cantidades):
        if not isinstance(materiales, list) or not isinstance(cantidades, list):
            raise TypeError("Materiales y cantidades deben ser listas")
        if len(materiales) != len(cantidades):
            raise ValueError("Debe haber una cantidad por cada material")