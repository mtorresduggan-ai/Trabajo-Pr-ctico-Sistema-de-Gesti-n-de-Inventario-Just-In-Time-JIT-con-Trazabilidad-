from empleado import Empleado
from estante import Estante
from tarea import Tarea
from datetime import date

class Supervisor(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email, usuario, clave):
        super().__init__(nombre, telefono, dni, fecha_alta, email, usuario, clave)

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

        stock = deposito.get_stock()

        for material, cantidad, fecha in zip(materiales, cantidades, fechas):
            if material not in stock:
                stock[material] = Estante()

            estante = stock[material]
            estante.agregar_caja(fecha, cantidad)

        remesa.get_solicitud().set_estado("Recibido")

    def sacar_pedido(self, pedido, deposito, tareas_pendientes_comprador):
        materiales = pedido.get_materiales()
        cantidades = pedido.get_cantidades()
        stock = deposito.get_stock()

        for material, cantidad in zip(materiales, cantidades):
            if material not in stock:
                raise ValueError(f"No hay stock de {material.get_nombre()}")

            estante = stock[material]

            if estante.stock_total() < cantidad:
                raise ValueError(f"No hay suficiente stock de {material.get_nombre()}")

        for material, cantidad in zip(materiales, cantidades):
            estante = stock[material]
            estante.sacar_cajas(cantidad)

        pedido.set_estado("Despachado")

        for material in materiales:
            cantidad_stock = deposito.stock_total(material)

            if cantidad_stock <= material.get_punto_reposicion():
                if not tareas_pendientes_comprador.existe_tarea_reposicion(material):
                    tareas_pendientes_comprador.agregar(Tarea("reponer", material))

    def transferir_stock(self, deposito_origen, deposito_destino, materiales, cantidades):
        stock_origen = deposito_origen.get_stock()
        stock_destino = deposito_destino.get_stock()

        for material, cantidad in zip(materiales, cantidades):
            if material not in stock_origen:
                raise ValueError(f"No hay stock de {material.get_nombre()} en el depósito de origen")

            estante_origen = stock_origen[material]
            estante_destino = stock_destino.get(material)

            if estante_destino is None:
                estante_destino = Estante()
                stock_destino[material] = estante_destino

            cajas_a_mover = estante_origen.sacar_cajas(cantidad)

            for caja in cajas_a_mover:
                estante_destino.agregar_caja(caja.get_fecha_vencimiento(), caja.get_cantidad())

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
        hay_vencidas = False

        for estante in deposito.get_stock().values():
            if estante.hay_cajas_vencidas(fecha_actual):
                hay_vencidas = True
                break

        if hay_vencidas:
            tarea = tareas_supervisor.get_frente()
            existe = False

            while tarea is not None:
                if (tarea.get_tipo() == "retirar_vencidos" and tarea.get_objeto() == deposito):
                    existe = True
                    break

                tarea = tarea.get_siguiente()

            if not existe:
                tareas_supervisor.agregar(Tarea("retirar_vencidos", deposito))

    def retirar_vencidos(self, deposito):
        fecha_actual = date.today()

        for estante in deposito.get_stock().values():
            estante.retirar_cajas_vencidas(fecha_actual)

    def generar_reporte_stock(self, deposito):
        reporte = "Reporte de stock:\n"

        for material, estante in deposito.get_stock().items():
            cantidad_total = estante.stock_total()

            if material.necesita_reposicion(cantidad_total):
                reposicion = "Si"
            else:
                reposicion = "No"

            reporte += (
                f"Material: {material.get_nombre()}\nCantidad total: {cantidad_total} {material.get_unidad_medida()}\nPunto de reposicion: {material.get_punto_reposicion()}\nNecesita reposicion: {reposicion}\n")

            caja = estante.get_primera()

            while caja is not None:
                reporte += (f"Cantidad: {caja.get_cantidad()} {material.get_unidad_medida()} - Vence: {caja.get_fecha_vencimiento()}\n")
                caja = caja.get_prox()
            reporte += "\n"

        return reporte

    @staticmethod
    def validar_fechas_vencimiento(fechas):
        if not isinstance(fechas, list):
            raise TypeError("Las fechas de vencimiento deben estar en una lista")

        if not all(isinstance(fecha, date) for fecha in fechas):
            raise TypeError("Cada fecha de vencimiento debe ser una fecha")

    @staticmethod
    def validar_listas(materiales, cantidades, fechas):
        if len(materiales) != len(cantidades) or len(materiales) != len(fechas):
            raise ValueError("Debe haber una cantidad y una fecha de vencimiento por cada material")