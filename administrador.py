from empleado import Empleado
from datetime import date
from proveedor import Proveedor
from cliente import Cliente
from estante import Estante

class Administrador(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email, usuario, clave):
        super().__init__(nombre, telefono, dni, fecha_alta, email, usuario, clave)

    def aceptar_remesa(self, remesa, deposito):
        Empleado.validar_materiales(remesa.materiales)
        Empleado.validar_cantidades(remesa.cantidades)
        self.validar_fechas_vencimiento(remesa.fechas_vencimiento)
        self.validar_listas(remesa.materiales, remesa.cantidades, remesa.fechas_vencimiento)

        if remesa.fecha_llegada is None:
            raise ValueError("La remesa todavia no llegó")
        Empleado.validar_fecha(remesa.fecha_llegada)

        for material, cantidad, fecha in zip(remesa.materiales, remesa.cantidades, remesa.fechas_vencimiento):

            if material not in deposito.stock:
                deposito.stock[material] = Estante()

            estante = deposito.stock[material]
            estante.agregar_caja(fecha, cantidad)


    def aceptar_pedido_salida(self, pedido, deposito):

        if pedido.estado != "Pendiente":
            raise ValueError("Solo se pueden aceptar pedidos en estado Pendiente")

        for material, cantidad in zip(pedido.materiales, pedido.cantidades):
            if material not in deposito.stock:
                raise ValueError(f"No hay stock de {material.nombre}")


            stock_total = sum(dato.get("cantidad") for dato in datos_material)

            if stock_total < cantidad:
                raise ValueError(f"No hay suficiente stock de {material.nombre}")

        for material, cantidad in zip(pedido.materiales, pedido.cantidades):

            if material not in deposito.stock:
                raise ValueError(f"No hay stock de {material.nombre}")

            estante= deposito.stock[material]

            if estante.stock_total()<cantidad:
                raise ValueError(f"No hay suficiente stock de {material.nombre}")

        for material, cantidad in zip(pedido.materiales, pedido.cantidades):
            estante = deposito.stock[material]
            estante.sacar_cajas(cantidad)

        pedido.estado = "Despachado"


    def transferir_stock(self, deposito_origen, deposito_destino, materiales, cantidades):
        self.validar_listas_2(materiales, cantidades)

        if deposito_destino==deposito_origen:
            raise ValueError('El deposito origen y deposito destino no puede ser el mismo')

        for material, cantidad in zip(materiales, cantidades):
            if material not in deposito_origen.stock:
                raise ValueError(f"No hay stock de {material.nombre} en el depósito de origen")

            stock_disponible = deposito_origen.stock_total(material)
            if stock_disponible < cantidad:
                raise ValueError(f"Transferencia cancelada: Stock insuficiente de {material.nombre} en origen. ")
            
        for material, cantidad in zip(materiales, cantidades):
            estante_origen = deposito_origen.stock[material]
            estante_destino = deposito_destino.stock.get(material)

            if estante_destino is None:
                estante_destino= Estante()
                deposito_destino.stock[material]= estante_destino
            
            cajas_a_mover = estante_origen.sacaar_cajas(cantidad)
        
            for caja in cajas_a_mover:
                estante_destino.agregar_caja(caja.fecha_vencimiento, caja.cantidad)


    def baja_empleado(self, empleado):
        if empleado not in Empleado.todos:
            raise ValueError("El empleado no está registrado")

        if empleado.fecha_baja is not None:
            raise ValueError("El empleado ya está dado de baja")

        empleado.fecha_baja = date.today()

    def modificar_empleado(self, empleado, nombre=None, telefono=None, email=None, usuario=None, clave=None):
        if empleado not in Empleado.todos:
            raise ValueError("El empleado no está registrado")
        if nombre is not None:
            empleado.validar_nombre(nombre)
            empleado.nombre = nombre
        if telefono is not None:
            empleado.validar_telefono(telefono)
            empleado.telefono = telefono
        if email is not None:
            empleado.validar_email(email)
            empleado.email = email
        if usuario is not None:
            empleado.actualizar_usuario(usuario)
        if clave is not None:
            empleado.set_clave(clave) 

    def baja_proveedor(self, proveedor):
        if proveedor not in Proveedor.todos:
            raise ValueError("Este proveedor no está registrado")

        if proveedor.fecha_baja is not None:
            raise ValueError("El proveedor ya está dado de baja")

        proveedor.fecha_baja = date.today()    

    def baja_cliente(self, cliente):
        if cliente not in Cliente.todos:
            raise ValueError("El cliente no está registrado")

        if cliente.fecha_baja is not None:
            raise ValueError("Este cliente ya está dado de baja")

        cliente.fecha_baja = date.today()

    def generar_reporte_empleados(self):
        reporte = "Reporte de empleados:\n"

        for empleado in Empleado.todos:
            if empleado.fecha_baja is None:
                estado = "Activo"
            else:
                estado = f"Baja: {empleado.fecha_baja}"

            reporte += (f"Nombre: {empleado.nombre}\nDNI: {empleado.dni}\nTelefono: {empleado.telefono}\nEmail: {empleado.email}\nUsuario: {empleado.usuario}\nEstado: {estado}\n")

        return reporte


    def generar_reporte_proveedores(self):
        reporte = "Reporte de proveedores:\n"

        for proveedor in Proveedor.todos:
            if proveedor.fecha_baja is None:
                estado = "Activo"
            else:
                estado = f"Baja: {proveedor.fecha_baja}"

            reporte += (
                f"Nombre: {proveedor.nombre}\nDNI: {proveedor.dni}\nTelefono: {proveedor.telefono}\nEmail: {proveedor.email}\nPlazo estimado: {proveedor.plazo_estimado} dias\nPuntaje: {proveedor.puntaje}\nEstado: {estado}\n")

        return reporte


    def generar_reporte_clientes(self):
        reporte = "Reporte de clientes:\n"

        for cliente in Cliente.todos:
            if cliente.fecha_baja is None:
                estado = "Activo"
            else:
                estado = f"Baja: {cliente.fecha_baja}"

            reporte += (f"Nombre: {cliente.nombre}\nDNI: {cliente.dni}\nTelefono: {cliente.telefono}\nEmail: {cliente.email}\nEstado: {estado}\n")

        return reporte


    def generar_reporte_stock(self, deposito):
        reporte = "Reporte de stock:\n"

        for material, datos in deposito.stock.items():
            cantidad_total = sum(dato["cantidad"] for dato in datos)

            if material.necesita_reposicion(cantidad_total):
                reposicion = "Si"
            else:
                reposicion = "No"

            reporte += (
                f"Material: {material.nombre}\nCantidad total: {cantidad_total} {material.unidad_medida}\nPunto de reposicion: {material.punto_reposicion}\nNecesita reposicion: {reposicion}\n")

            for dato in datos:
                reporte += (f"Cantidad: {dato['cantidad']} {material.unidad_medida} - Vence: {dato['fecha_vencimiento']}\n")

            reporte += "\n"

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