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
            '2': lambda: self.comprador.ejecutar_siguiente_tarea(self.tareas_comprador, date.today(), self.input_proveedor(), self.tareas_admin),
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
            id_movimiento=id_movimiento,
            materiales=materiales,
            cantidades=cantidades,
            fecha=fecha,
            proveedor=proveedor,
            estado=estado)

    def input_crear_solicitud(self):
        materiales, cantidades = self.input_materiales_cantidades()
        proveedor = self.input_proveedor()
        
        precios_unitarios = [material.get_precio_base() for material in materiales]

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
        
        for material, cant in zip(solicitud.get_materiales(), solicitud.get_cantidades()):
            lineas.append(f"  - {material.get_nombre()}: {cant} {material.get_unidad_medida()}")
            
        return "\n".join(lineas)
        