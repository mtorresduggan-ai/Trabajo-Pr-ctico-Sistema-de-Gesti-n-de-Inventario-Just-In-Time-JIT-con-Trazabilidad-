from datetime import date
from menu import Menu


class MenuComprador(Menu):
    def __init__(self, comprador, tareas_comprador, tareas_admin, sistema=None):
        super().__init__(tareas_comprador=tareas_comprador,
            tareas_vendedor=None,
            tareas_supervisor=None,
            tareas_admin=tareas_admin,
            sistema=sistema)
        self.comprador = comprador
        self.tareas_comprador = tareas_comprador
        self.tareas_admin=tareas_admin

    def menu_comprador(self):
        opciones = {
            '1': lambda: self.tareas_comprador.mostrar_cantidades(),
            '2': self.input_ejecutar_tarea,
            '3': self.input_crear_solicitud,
            '4': lambda: self.comprador.cancelar_solicitud(self.pedir_int("ID de solicitud a cancelar: "), self.sistema._solicitudes),
            '5': self.input_consultar_todas,
            '6': self.input_consultar_por_id,
            '7': self.input_modificar_solicitud}

        self.pantalla("MENÚ COMPRADOR", [
            "1. Mostrar tareas pendientes",
            "2. Ejecutar siguiente tarea",
            "3. Crear solicitud",
            "4. Cancelar solicitud",
            "5. Consultar todas las solicitudes",
            "6. Consultar solicitud por ID",
            "7. Modificar solicitud"], opciones)

    def input_ejecutar_tarea(self):
        proveedor = self.input_proveedor()
        solicitud = self.comprador.ejecutar_siguiente_tarea(self.tareas_comprador, date.today(), proveedor, self.sistema.get_proveedores(), self.tareas_admin, None)
        self.sistema.agregar_solicitud(solicitud)
        return solicitud

    def input_modificar_solicitud(self):
        id_movimiento = self.pedir_int("ID de la solicitud a modificar: ")
        print("\n Dejá en blanco (presioná Enter) en los campos que NO quieras modificar:")
        
        actualizar_mat = self.pedir("¿Deseas modificar materiales y cantidades? (si/no): ").lower()
        if actualizar_mat == 'si':
            materiales, cantidades = self.input_materiales_cantidades()
        else:
            materiales, cantidades = None, None

        fecha_str = self.pedir("Nueva fecha (YYYY-MM-DD): ")
        fecha = date.fromisoformat(fecha_str) if fecha_str else None

        actualizar_prov = self.pedir("¿Deseas modificar el proveedor? (si/no): ").lower()
        proveedor = self.input_proveedor() if actualizar_prov == 'si' else None

        estado_str = self.pedir("Nuevo estado: ")
        estado = estado_str if estado_str else None

        return self.comprador.modificar_solicitud(
            id_solicitud=id_movimiento,
            solicitudes=self.sistema._solicitudes,
            proveedores=self.sistema.get_proveedores(),
            materiales=materiales,
            cantidades=cantidades,
            fecha=fecha,
            proveedor=proveedor,
            estado=estado)

    def input_crear_solicitud(self):
        materiales, cantidades = self.input_materiales_cantidades()
        proveedor = self.input_proveedor()
        
        precios_unitarios = []
        for material in materiales:
            try:
                precio = proveedor.obtener_precio(material)
            except ValueError:
                precio = float(self.pedir(f"Precio unitario de {material.get_nombre()} para este proveedor: "))
            precios_unitarios.append(precio)

        solicitud= self.comprador.crear_solicitud(
            date.today(),
            materiales,
            cantidades,
            proveedor,
            self.sistema.get_proveedores(),
            self.tareas_admin,
            precios_unitarios,
            None)

        self.sistema._solicitudes.append(solicitud)
        
        return f"\n ¡Solicitud N° {solicitud.get_id_solicitud()} generada con éxito!"

    def input_consultar_todas(self):
        solicitudes = self.comprador.consultar_solicitudes_todas(self.sistema._solicitudes)
        if not solicitudes:
            return "\nNo tenés solicitudes registradas."
        
        lineas = ["\n=== MIS SOLICITUDES ==="]
        for s in solicitudes:
            lineas.append(f"• ID: {s.get_id_solicitud()} | Proveedor: {s.get_proveedor().get_nombre()} | Estado: {s.get_estado()}")
        return "\n".join(lineas)

    def input_consultar_por_id(self):
        id_sol = self.pedir_int("ID de solicitud: ")
        solicitud = self.comprador.consultar_solicitud(id_sol, self.sistema._solicitudes)
        
        lineas = [
            f"\n=== DETALLE DE SOLICITUD N° {solicitud.get_id_solicitud()} ===",
            f"Fecha: {solicitud.get_fecha()}",
            f"Estado: {solicitud.get_estado()}",
            f"Proveedor: {solicitud.get_proveedor().get_nombre()}",
            "\nItems:"
        ]
        
        for i in range(len(solicitud.get_materiales())):
            material = solicitud.get_materiales()[i]
            cantidad = solicitud.get_cantidades()[i]
            precio = solicitud.get_precios_unitarios()[i]
            lineas.append(f"  - {material.get_nombre()}: {cantidad} {material.get_unidad_medida()} x ${precio} = ${solicitud.calcular_subtotal(i)}")

        lineas.append(f"\nTotal: ${solicitud.calcular_total()}")

        return "\n".join(lineas)
        