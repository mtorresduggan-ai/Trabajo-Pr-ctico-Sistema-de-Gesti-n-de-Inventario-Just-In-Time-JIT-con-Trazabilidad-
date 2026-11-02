from supervisor import Supervisor
from menu import Menu


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
            "4": lambda: self.supervisor.generar_reporte_stock(self.deposito)}
        
        self.pantalla("MENÚ SUPERVISOR", [
            "1. Mostrar tareas pendientes y cantidades",
            "2. Ejecutar siguiente tarea",
            "3. Revisar vencidos",
            "4. Generar reporte"], opciones)


   