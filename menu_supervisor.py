from supervisor import Supervisor
from menu import Menu
from datetime import date


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
            "5": self.input_registrar_remesa,
            "6": self.input_buscar_material,
            "7": self.input_listar_materiales}
        
        self.pantalla("MENÚ SUPERVISOR", [
            "1. Mostrar tareas pendientes y cantidades",
            "2. Ejecutar siguiente tarea",
            "3. Revisar vencidos",
            "4. Generar reporte",
            "5. Registrar llegada de remesa",
            "6. Buscar material por nombre",
            "7. Listar materiales en orden alfabético"]
            , opciones)

    def input_registrar_remesa(self):
        solicitudes = self.supervisor.solicitudes_esperando_remesa(self.sistema.get_solicitudes(), self.sistema.get_remesas())

        if len(solicitudes) == 0:
            return "No hay solicitudes aceptadas esperando una remesa."

        print("\n--- SOLICITUDES ESPERANDO REMESA ---")
        for i, solicitud in enumerate(solicitudes, start=1):
            print(f"{i}. {solicitud}")

        opcion = self.pedir_int("Ingrese el número de la solicitud (o 'volver'): ")
        if opcion < 1 or opcion > len(solicitudes):
            raise ValueError("Opción fuera de rango")
        solicitud = solicitudes[opcion - 1]

        fechas_vencimiento = []
        for material in solicitud.get_materiales():
            texto = self.pedir(f"Vencimiento de {material.get_nombre()} (YYYY-MM-DD, Enter si no vence): ")
            if texto == "":
                fechas_vencimiento.append(None)
            else:
                fechas_vencimiento.append(self.sistema.convertir_fecha(texto))

        remesa = self.supervisor.registrar_remesa(solicitud, fechas_vencimiento, date.today(), self.deposito, self.tareas_supervisor)
        self.sistema.agregar_remesa(remesa)

        return f"Remesa N° {remesa.get_id_remesa()} registrada. Ejecutá la siguiente tarea para ingresarla al depósito."

    def texto_material(self, material):
        unidad = material.get_unidad_medida()
        return (f"{material.get_nombre()} (ID {material.get_id_material()})"
            f" - Stock total: {self.deposito.stock_total(material)} {unidad}"
            f" - Disponible: {self.deposito.stock_total(material, date.today())} {unidad}"
            f" - Punto de reposición: {material.get_punto_reposicion()} {unidad}")

    def input_buscar_material(self):
        nombre = self.pedir("Nombre del material: ")
        material = self.buscar_material(nombre)
        return self.texto_material(material)

    def input_listar_materiales(self):
        materiales = self.sistema.get_materiales_ordenados()
        texto = "\n--- MATERIALES (A-Z) ---\n"
        for material in materiales:
            texto += self.texto_material(material) + "\n"
        texto += f"Total: {len(materiales)} materiales\n"
        return texto
