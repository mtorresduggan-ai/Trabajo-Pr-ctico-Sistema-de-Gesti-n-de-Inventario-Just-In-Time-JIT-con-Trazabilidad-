from datetime import date
from menu import Menu


class MenuComprador(Menu):
    def __init__(self, comprador, tareas_pendientes_comprador, tareas_pendientes_admin):
        super().__init__(tareas_pendientes_comprador=tareas_pendientes_comprador,
            tareas_pendientes_vendedor=None,
            tareas_pendientes_supervisor=None,
            tareas_pendientes_admin=tareas_pendientes_admin)
        self.comprador = comprador
        self.tareas_pendientes_comprador = tareas_pendientes_comprador

        def menu_comprador(self):
            opciones = {
                '1': lambda: self.tareas_pendientes_comprador.mostrar_cantidades(),
                '2': lambda: self.comprador.ejecutar_siguiente_tarea(self.tareas_pendientes_comprador, date.today(), self.input_proveedor(), self.tareas_pendientes_admin),
                '3': lambda: self.comprador.crear_solicitud(date.today(), *self.input_materiales_cantidades(), self.input_proveedor(), self.tareas_pendientes_admin),
                '4': lambda: self.comprador.cancelar_solicitud(self.pedir_int("ID de solicitud a cancelar: ")),
                '5': self.comprador.consultar_solicitudes_todas,
                '6': lambda: self.comprador.consultar_solicitud(self.pedir_int("ID de solicitud: ")),
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