from menu import Menu
from empleado import Empleado
from deposito import Deposito


class MenuAdministrador(Menu):
    def __init__(self, administrador, tareas_pendientes_admin, tareas_pendientes_supervisor):
        super().__init__(
            tareas_pendientes_comprador=None,
            tareas_pendientes_vendedor=None,
            tareas_pendientes_supervisor=tareas_pendientes_supervisor,
            tareas_pendientes_admin=tareas_pendientes_admin)
        self.administrador = administrador

        def menu_administrador(self):
            opciones = {
                '1': lambda: self.tareas_pendientes_admin.mostrar_cantidades(),
                '2': lambda: self.administrador.ejecutar_siguiente_tarea(
                    self.tareas_pendientes_admin,
                    self.input_deposito("Seleccione el depósito sobre el que impactará la tarea:"),
                    self.tareas_pendientes_supervisor),
                '3': self.input_crear_transferencia,
                '4': lambda: self.administrador.baja_empleado(self.input_empleado()),
                '5': self.input_modificar_empleado,
                '6': lambda: self.administrador.baja_proveedor(self.input_proveedor()),
                '7': lambda: self.administrador.baja_cliente(self.input_cliente()),
                '8': self.administrador.generar_reporte_empleados,
                '9': self.administrador.generar_reporte_proveedores,
                '10': self.administrador.generar_reporte_clientes}

            self.pantalla("MENÚ ADMINISTRADOR", [
                "1. Mostrar tareas pendientes",
                "2. Ejecutar siguiente tarea (Aceptar solicitud/pedido)",
                "3. Crear transferencia de materiales",
                "4. Dar de baja un empleado",
                "5. Modificar datos de un empleado",
                "6. Dar de baja un proveedor",
                "7. Dar de baja un cliente",
                "8. Reporte de empleados",
                "9. Reporte de proveedores",
                "10. Reporte de clientes"], opciones)

    def input_empleado(self):
        print("\nSeleccione un empleado:")
        for i, emp in enumerate(Empleado.todos, start=1):
            print(f"{i}. {emp.get_nombre()} (DNI: {emp.get_dni()})")

        opcion = self.pedir_int("Ingrese el número del empleado (o 'volver'): ")
        return Empleado.todos[opcion - 1]

    def input_deposito(self, mensaje="Seleccione un depósito:"):
        print(f"\n{mensaje}")
        for i, dep in enumerate(Deposito.todos, start=1):
            print(f"{i}. {dep.get_nombre()}")

        opcion = self.pedir_int("Ingrese el número del depósito (o 'volver'): ")
        return Deposito.todos[opcion - 1]

    def input_crear_transferencia(self):
        print("\n--- CREAR TRANSFERENCIA ENTRE DEPÓSITOS ---")
        dep_origen = self.input_deposito("Depósito de origen:")
        dep_destino = self.input_deposito("Depósito de destino:")

        materiales, cantidades = self.input_materiales_cantidades()

        self.administrador.crear_transferencia(dep_origen, dep_destino, materiales, cantidades, self.tareas_pendientes_supervisor)
        return "Transferencia solicitada con éxito."

    def input_modificar_empleado(self):
        empleado = self.input_empleado()
        print("\nDejá en blanco (presioná Enter) en los campos que NO quieras modificar:")

        nombre = self.pedir("Nuevo nombre: ") or None
        telefono = self.pedir("Nuevo teléfono: ") or None
        email = self.pedir("Nuevo email: ") or None
        usuario = self.pedir("Nuevo usuario: ") or None
        clave = self.pedir("Nueva clave: ") or None

        self.administrador.modificar_empleado(empleado=empleado,
            nombre=nombre,
            telefono=telefono,
            email=email,
            usuario=usuario,
            clave=clave)
        
        return f"Empleado {empleado.get_nombre()} modificado con éxito."
