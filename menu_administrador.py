from menu import Menu
from empleado import Empleado
from deposito import Deposito


class MenuAdministrador(Menu):
    def __init__(self, administrador, tareas_admin,tareas_supervisor, sistema=None):
        super().__init__(
            tareas_comprador=None,
            tareas_vendedor=None,
            tareas_supervisor=tareas_supervisor,
            tareas_admin=tareas_admin,
            sistema=sistema)
        self.administrador = administrador

    def menu_administrador(self):
        opciones = {
            '1': lambda: self.tareas_admin.mostrar_cantidades(), 
            '2': self.input_ejecutar_tarea,
            '3': self.input_crear_transferencia,
            '4': lambda: self.administrador.baja_empleado(self.input_empleado(), self.sistema.get_gestor_empleados().get_empleados()),
            '5': self.input_modificar_empleado,
            '6': lambda: self.administrador.baja_proveedor(self.input_proveedor(), self.sistema.get_gestor_proveedores().get_proveedores()),
            '7': lambda: self.administrador.baja_cliente(self.input_cliente(), self.sistema.get_gestor_clientes().get_clientes()),
            '8': lambda: self.administrador.generar_reporte_empleados(self.sistema.get_gestor_empleados().get_empleados()),
            '9': lambda: self.administrador.generar_reporte_proveedores(self.sistema.get_gestor_proveedores().get_proveedores()),
            '10': lambda: self.administrador.generar_reporte_clientes(self.sistema.get_gestor_clientes().get_clientes()),
            '11': self.input_cargar_precio}

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
            "10. Reporte de clientes",
            "11. Cargar precio de un material a un proveedor"], opciones)

    def input_empleado(self):
        activos = list(filter(lambda e: e.get_fecha_baja() is None, self.sistema.get_gestor_empleados().get_empleados()))
        return self.elegir("SELECCIONAR EMPLEADO", activos,
            lambda e: f"{e.get_nombre()} (DNI: {e.get_dni()})")

    def input_deposito(self, mensaje="SELECCIONAR DEPÓSITO"):
        return self.elegir(mensaje, self.sistema.get_gestor_depositos().get_depositos(), lambda d: d.get_nombre())

    def input_ejecutar_tarea(self):
        tarea = self.tareas_admin.ver_primera()
        if tarea is None:
            raise ValueError("No hay tareas pendientes")

        print(f"\nSiguiente tarea: {tarea.get_objeto()}")
        deposito = self.input_deposito("Seleccione el depósito sobre el que impactará la tarea:")
        decision = self.pedir("¿Aceptar o rechazar? (aceptar/rechazar): ").lower()

        return self.administrador.ejecutar_siguiente_tarea(self.tareas_admin, deposito, self.tareas_supervisor, decision)
    
    def input_crear_transferencia(self):
        print("\n--- CREAR TRANSFERENCIA ENTRE DEPÓSITOS ---")
        dep_origen = self.input_deposito("Depósito de origen:")
        dep_destino = self.input_deposito("Depósito de destino:")

        materiales, cantidades = self.input_materiales_cantidades()

        self.administrador.crear_transferencia(dep_origen, dep_destino, materiales, cantidades, self.tareas_supervisor)
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
            empleados = self.sistema.get_gestor_empleados().get_empleados(),
            nombre=nombre,
            telefono=telefono,
            email=email,
            usuario=usuario,
            clave=clave)
        
        return f"Empleado {empleado.get_nombre()} modificado con éxito."

    def input_cargar_precio(self):
        proveedor = self.input_proveedor()
        material = self.buscar_material(self.pedir("Nombre del material: "))
        try:
            precio = float(self.pedir("Precio unitario: "))
        except ValueError:
            raise ValueError("Ingresá un número válido")
        return self.administrador.cargar_precio_proveedor(proveedor, material, precio, self.sistema.get_gestor_proveedores().get_proveedores())
