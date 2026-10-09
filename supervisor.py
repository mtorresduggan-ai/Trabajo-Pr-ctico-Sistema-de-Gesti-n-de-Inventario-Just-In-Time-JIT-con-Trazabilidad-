from empleado import Empleado
from estante import Estante
from tarea import Tarea
from datetime import date

class Supervisor_deposito(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email, usuario, clave):
        super().__init__(nombre, telefono, dni, fecha_alta, email, usuario, clave)


    def recibir_remesa(self, remesa, deposito):
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

        remesa.solicitud.estado = "Recibida"


    def sacar_pedido(self, pedido, deposito, tareas_pendientes_comprador):
         
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

        for material in pedido.materiales:
            stock = deposito.stock_total(material)

            if stock <= material.punto_reposicion:
                if not tareas_pendientes_comprador.existe_tarea_reposicion(material):
                    tareas_pendientes_comprador.agregar(Tarea("reponer", material))


    def transferir_stock(self, deposito_origen, deposito_destino, materiales, cantidades):
        for material, cantidad in zip(materiales, cantidades):
            estante_origen = deposito_origen.stock[material]
            estante_destino = deposito_destino.stock.get(material)

        if estante_destino is None:
            estante_destino= Estante()
            deposito_destino.stock[material]= estante_destino
        
        cajas_a_mover = estante_origen.sacar_cajas(cantidad)
    
        for caja in cajas_a_mover:
            estante_destino.agregar_caja(caja.fecha_vencimiento, caja.cantidad)


    def ejecutar_siguiente_tarea(self, tareas_pendeintes_supervisor, tareas_pendientes_comprador):
        tarea = tareas_pendeintes_supervisor.ver_primera()

        if tarea is None:
            raise ValueError("No hay tareas pendientes")

        if tarea.tipo == "pedido":
            self.sacar_pedido(tarea.objeto, tarea.datos, tareas_pendientes_comprador)

        elif tarea.tipo == "remesa":
            self.recibir_remesa(tarea.objeto, tarea.datos)

        elif tarea.tipo == "transferencia":
            self.transferir_stock(*tarea.datos)

        elif tarea.tipo == "retirar_vencidos":
            self.retirar_vencidos(tarea.objeto)

        else:
            raise ValueError("Tipo de tarea desconocido")

        tareas_pendeintes_supervisor.sacar()


    def existe_tarea_reposicion(self, material):
        tarea = self.frente

        while tarea is not None:
            if tarea.tipo == "reponer" and tarea.objeto == material:
                return True

            tarea = tarea.siguiente

        return False

    def revisar_vencimientos(self, deposito, tareas_supervisor):
        fecha_actual = date.today()
        hay_vencidas = False

        for estante in deposito.stock.values():
            if estante.hay_cajas_vencidas(fecha_actual):
                hay_vencidas = True
                break

        if hay_vencidas:
            tarea = tareas_supervisor.frente
            existe = False

            while tarea is not None:
                if (tarea.tipo == "retirar_vencidos" and tarea.objeto == deposito):
                    existe = True
                    break

                tarea = tarea.siguiente

            if not existe:
                tareas_supervisor.agregar(Tarea("retirar_vencidos", deposito))

    
    def retirar_vencidos(self, deposito):
        fecha_actual = date.today()

        for estante in deposito.stock.values():
            estante.retirar_cajas_vencidas(fecha_actual)