from empleado import Empleado

class Administrador(Empleado):
    def __init__(self, nombre, telefono, dni, fecha_alta, email, usuario, clave):
        super().__init__(nombre, telefono, dni, fecha_alta, email, usuario, clave)

    def aceptar_remesa(self, remesa, deposito):
        for material, cantidad, fecha in zip(remesa.materiales, remesa.cantidades, remesa.fechas_vencimiento):

            if material not in deposito.stock:
                deposito.stock[material] = [dict(cantidad=cantidad, fecha_vencimiento=fecha)]

            else:
                datos_material = deposito.stock.get(material)

                coincidencias = list(filter(
                    lambda dato: dato.get("fecha_vencimiento") == fecha,
                    datos_material))

                if coincidencias:
                    dato = coincidencias[0]
                    dato.update(cantidad=dato.get("cantidad") + cantidad)

                else:
                    datos_material.append(
                        dict(cantidad=cantidad, fecha_vencimiento=fecha))

        self.evaluar_plazo_remesa(remesa)


    def evaluar_plazo_remesa(self, remesa):
        dias_reales = remesa.fecha_llegada - remesa.solicitud.fecha_solicitud

        if dias_reales.days <= remesa.proveedor.plazo_estimado:
            remesa.proveedor.modificar_puntaje(0.5)
        else:
            remesa.proveedor.modificar_puntaje(-0.5)

    from empleado import Empleado


    def aceptar_pedido_salida(self, pedido, deposito):

        if pedido.estado != "Pendiente":
            raise ValueError("Solo se pueden aceptar pedidos en estado Pendiente")

        for material, cantidad in zip(pedido.materiales, pedido.cantidades):
            if material not in deposito.stock:
                raise ValueError(f"No hay stock de {material.nombre}")

            datos_material = deposito.stock.get(material)

            stock_total = sum(dato.get("cantidad") for dato in datos_material)

            if stock_total < cantidad:
                raise ValueError(f"No hay suficiente stock de {material.nombre}")

        for material, cantidad in zip(pedido.materiales, pedido.cantidades):
            datos_material = deposito.stock.get(material)
            cantidad_faltante = cantidad

            datos_material.sort(key=lambda dato: dato.get("fecha_vencimiento"))

            for dato in datos_material:
                if cantidad_faltante == 0:
                    break

                cantidad_disponible = dato.get("cantidad")

                if cantidad_disponible <= cantidad_faltante:
                    cantidad_faltante -= cantidad_disponible
                    dato.update(cantidad=0)

                else:
                    dato.update(cantidad=cantidad_disponible - cantidad_faltante)
                    cantidad_faltante = 0

        pedido.estado = "Despachado" 