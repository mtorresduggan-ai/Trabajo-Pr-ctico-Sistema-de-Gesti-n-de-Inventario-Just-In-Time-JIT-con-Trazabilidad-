from supervisor import Supervisor
from menu import Menu


class MenuSupervisor:
    def __init__(self, supervisor, tareas_pendientes_supervisor, tareas_pendientes_comprador, deposito):
        super().__init__(
            tareas_pendientes_comprador=tareas_pendientes_comprador,
            tareas_pendientes_vendedor=None,
            tareas_pendientes_supervisor=tareas_pendientes_supervisor,
            tareas_pendientes_admin=None,
            deposito=deposito)
        self.supervisor = supervisor

        def menu_supervisor(self):
            opciones = {
                "1": lambda: self.supervisor.mostrar_tareas_pendientes(self.tareas_pendientes_supervisor),
                "2": lambda: self.supervisor.ejecutar_siguiente_tarea(self.tareas_pendientes_supervisor, self.tareas_pendientes_comprador),
                "3": lambda: self.supervisor.revisar_vencimientos(self.deposito, self.tareas_pendientes_supervisor),
                "4": lambda: self.supervisor.generar_reporte_stock(self.deposito)}

            self.pantalla("MENÚ SUPERVISOR", [
                "1. Mostrar tareas pendientes y cantidades",
                "2. Ejecutar siguiente tarea",
                "3. Revisar vencidos",
                "4. Generar reporte"], opciones)


   