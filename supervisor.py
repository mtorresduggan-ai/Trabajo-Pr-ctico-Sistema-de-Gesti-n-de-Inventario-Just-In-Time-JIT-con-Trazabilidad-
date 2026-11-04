from empleado import Empleado
from tarea import Tarea
from datetime import date
from remesa import Remesa

class Supervisor(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja=None, id_manual=None):
        super().__init__(nombre, telefono, dni, fecha_alta, email,usuario, clave, fecha_baja, id_manual)
    

    def recibir_remesa(self, remesa, deposito):
        materiales = remesa.get_materiales()
        cantidades = remesa.get_cantidades()
        fechas = remesa.get_fechas_vencimiento()

        Empleado.validar_materiales(materiales)
        Empleado.validar_cantidades(cantidades)
        self.validar_fechas_vencimiento(fechas)
        self.validar_listas(materiales, cantidades, fechas)

        if remesa.get_fecha_llegada() is None:
            raise ValueError("La remesa todavia no llegó")

        Empleado.validar_fecha(remesa.get_fecha_llegada())

        for material, cantidad, fecha in zip(materiales, cantidades, fechas):
            deposito.ingresar(material, fecha, cantidad)

        if remesa.get_solicitud() is not None:
            remesa.get_solicitud().set_estado("Recibido")

    def sacar_pedido(self, pedido, deposito, tareas_pendientes_comprador):

        if pedido.get_estado() == "Cancelado":
            print("Operación omitida: El pedido ya fue cancelado por el vendedor.")
            return

        materiales = pedido.get_materiales()
        cantidades = pedido.get_cantidades()

        faltantes = deposito.materiales_sin_stock(materiales, cantidades, date.today())
        if len(faltantes) > 0:
            raise ValueError(f"No hay suficiente stock de {faltantes[0].get_nombre()} para el pedido")

        for material, cantidad in zip(materiales, cantidades):
            deposito.retirar(material, cantidad)
        pedido.set_estado("Despachado")

        a_reponer = filter(lambda material: deposito.stock_total(material, date.today()) < material.get_punto_reposicion()
            and not tareas_pendientes_comprador.existe_tarea_reposicion(material), materiales)

        for material in a_reponer:
            tareas_pendientes_comprador.agregar(Tarea("reponer", material))

    def solicitudes_esperando_remesa(self, solicitudes, remesas):
        solicitudes_con_remesa = set(map(lambda remesa: remesa.get_solicitud(), remesas))

        return list(filter(lambda solicitud: solicitud.get_estado() == "Solicitado"
            and solicitud not in solicitudes_con_remesa, solicitudes))

    def registrar_remesa(self, solicitud, fechas_vencimiento, fecha_llegada, deposito, tareas_pendientes_supervisor):
        if solicitud.get_estado() != "Solicitado":
            raise ValueError("Solo se pueden registrar remesas de solicitudes aceptadas")

        if len(fechas_vencimiento) != len(solicitud.get_materiales()):
            raise ValueError("Debe haber una fecha de vencimiento por cada material")

        fechas_invalidas = list(filter(lambda fecha: fecha is not None and fecha <= fecha_llegada, fechas_vencimiento))
        if len(fechas_invalidas) > 0:
            raise ValueError("La fecha de vencimiento debe ser posterior a la fecha de llegada")

        return Remesa(list(solicitud.get_materiales()), solicitud.get_proveedor(), solicitud,
            list(solicitud.get_cantidades()), fechas_vencimiento, deposito,
            tareas_pendientes_supervisor, fecha_llegada)

    def transferir_stock(self, deposito_origen, deposito_destino, materiales, cantidades):
        faltantes = deposito_origen.materiales_sin_stock(materiales, cantidades, date.today())
        
        if len(faltantes) > 0:
            raise ValueError(f"No hay suficiente stock de {faltantes[0].get_nombre()} en el depósito origen")
       
        for material, cantidad in zip(materiales, cantidades):
            cajas_a_mover = deposito_origen.retirar(material, cantidad)
            for caja in cajas_a_mover:
                deposito_destino.ingresar(material, caja.get_fecha_vencimiento(), caja.get_cantidad())

    def ejecutar_siguiente_tarea(self, tareas_pendientes_supervisor, tareas_pendientes_comprador):
        tarea = tareas_pendientes_supervisor.ver_primera()

        if tarea is None:
            raise ValueError("No hay tareas pendientes")

        tipo = tarea.get_tipo()
        objeto = tarea.get_objeto()
        datos = tarea.get_datos()

        acciones = {"pedido": lambda: self.sacar_pedido(objeto, datos, tareas_pendientes_comprador),
            "remesa": lambda: self.recibir_remesa(objeto, datos),
            "transferencia": lambda: self.transferir_stock(*datos),
            "retirar_vencidos": lambda: self.retirar_vencidos(objeto)}

        if tipo not in acciones:
            raise ValueError("Tipo de tarea desconocido")
        acciones[tipo]()
        tareas_pendientes_supervisor.sacar()

    def mostrar_tareas_pendientes(self, tareas_pendientes_supervisor):
        cantidades = tareas_pendientes_supervisor.contar_tareas()

        for tipo, cantidad in cantidades.items():
            print(tipo, ":", cantidad)
        
    def revisar_vencimientos(self, deposito, tareas_supervisor):
        fecha_actual = date.today()
        if deposito.hay_vencidos(fecha_actual) and not tareas_supervisor.existe_tarea("retirar_vencidos", deposito):
            tareas_supervisor.agregar(Tarea("retirar_vencidos", deposito))
        
    def retirar_vencidos(self, deposito):
        deposito.retirar_vencidos(date.today())

    def generar_reporte_stock(self, deposito):
        reporte = "Reporte de stock:\n"

        for material in deposito.get_materiales():
            cantidad_total = deposito.stock_total(material)

            if material.necesita_reposicion(deposito.stock_total(material, date.today())):
                reposicion = "Si"
            else:
                reposicion = "No"

            reporte += (f"Material: {material.get_nombre()}\nCantidad total: {cantidad_total} {material.get_unidad_medida()}\nPunto de reposicion: {material.get_punto_reposicion()}\nNecesita reposicion: {reposicion}\n")

            for vencimiento, cantidad in deposito.obtener_cajas(material):
                reporte += f"Cantidad: {cantidad} {material.get_unidad_medida()} - Vence: {vencimiento}\n"
            reporte += "\n"

        return reporte

    @staticmethod
    def validar_fechas_vencimiento(fechas):
        if not isinstance(fechas, list):
            raise TypeError("Las fechas de vencimiento deben estar en una lista")

        if not all(map(lambda fecha: fecha is None or isinstance(fecha, date), fechas)):
            raise TypeError("Cada fecha de vencimiento debe ser una fecha")

    @staticmethod
    def validar_listas(materiales, cantidades, fechas):
        if len(materiales) != len(cantidades) or len(materiales) != len(fechas):
            raise ValueError("Debe haber una cantidad y una fecha de vencimiento por cada material")