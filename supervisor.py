from empleado import Empleado
from estante import Estante

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

    def sacar_pedido(self, pedido, deposito):
         
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
        for material, cantidad in zip(materiales, cantidades):
            estante_origen = deposito_origen.stock[material]
            estante_destino = deposito_destino.stock.get(material)

        if estante_destino is None:
            estante_destino= Estante()
            deposito_destino.stock[material]= estante_destino
        
        cajas_a_mover = estante_origen.sacar_cajas(cantidad)
    
        for caja in cajas_a_mover:
            estante_destino.agregar_caja(caja.fecha_vencimiento, caja.cantidad)