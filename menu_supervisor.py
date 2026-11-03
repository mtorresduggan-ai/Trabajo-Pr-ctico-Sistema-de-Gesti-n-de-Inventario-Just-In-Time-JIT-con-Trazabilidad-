from supervisor import Supervisor
from menu import Menu
from datetime import date
from remesa import Remesa


class MenuSupervisor(Menu):
    def __init__(self, supervisor, tareas_supervisor, tareas_comprador, deposito, sistema=None):
        super().__init__(
            tareas_comprador=tareas_comprador,
            tareas_vendedor=None,
            tareas_supervisor=tareas_supervisor,
            tareas_admin=None,
            deposito=deposito, 
            sistema=sistema)
        self.supervisor = supervisor

    def menu_supervisor(self):
        opciones = {
            "1": lambda: self.supervisor.mostrar_tareas_pendientes(self.tareas_supervisor),
            "2": lambda: self.supervisor.ejecutar_siguiente_tarea(self.tareas_supervisor, self.tareas_comprador),
            "3": lambda: self.supervisor.revisar_vencimientos(self.deposito, self.tareas_supervisor),
            "4": lambda: self.supervisor.generar_reporte_stock(self.deposito),
            "5": self.input_registrar_remesa}
        
        self.pantalla("MENÚ SUPERVISOR", [
            "1. Mostrar tareas pendientes y cantidades",
            "2. Ejecutar siguiente tarea",
            "3. Revisar vencidos",
            "4. Generar reporte",
            "5. Registrar llegada de remesa"], opciones)

    def tiene_remesa(self, solicitud):
        for remesa in self.sistema.get_remesas():
            if remesa.get_solicitud() == solicitud:
                return True
        return False

    def input_registrar_remesa(self):
        solicitudes = []
        for solicitud in self.sistema.get_solicitudes():
            if solicitud.get_estado() == "Solicitado" and not self.tiene_remesa(solicitud):
                solicitudes.append(solicitud)

        if len(solicitudes) == 0:
            return "No hay solicitudes aceptadas esperando una remesa."

        print("\n--- SOLICITUDES ESPERANDO REMESA ---")
        for i, solicitud in enumerate(solicitudes, start=1):
            print(f"{i}. {solicitud}")

        opcion = self.pedir_int("Ingrese el número de la solicitud (o 'volver'): ")
        if opcion < 1 or opcion > len(solicitudes):
            raise ValueError("Opción fuera de rango")
        solicitud = solicitudes[opcion - 1]

        fecha_llegada = date.today()
        fechas_vencimiento = []

        for material in solicitud.get_materiales():
            texto = self.pedir(f"Vencimiento de {material.get_nombre()} (YYYY-MM-DD, Enter si no vence): ")

            if texto == "":
                fechas_vencimiento.append(None)
            else:
                fecha = self.sistema.convertir_fecha(texto)
                if fecha <= fecha_llegada:
                    raise ValueError("La fecha de vencimiento debe ser posterior a la fecha de llegada")
                fechas_vencimiento.append(fecha)

        remesa = Remesa(list(solicitud.get_materiales()), solicitud.get_proveedor(), solicitud,
            list(solicitud.get_cantidades()), fechas_vencimiento, self.deposito,
            self.tareas_supervisor, fecha_llegada)
        self.sistema.agregar_remesa(remesa)

        return f"Remesa N° {remesa.get_id_remesa()} registrada. Ejecutá la siguiente tarea para ingresarla al depósito."