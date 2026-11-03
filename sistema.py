from datetime import date

from gestor_archivos import GestorArchivos
from material import Material
from proveedor import Proveedor
from cliente import Cliente
from empleado import Empleado
from comprador import Comprador
from vendedor import Vendedor
from administrador import Administrador
from supervisor import Supervisor
from deposito import Deposito
from estante import Estante
from solicitud_proveedor import Solicitud_proveedor
from pedido import Pedido_salida
from remesa import Remesa
from tarea import Tarea
from arbol import Arbol


class Sistema:

    def __init__(self):
        self._materiales = []
        self._proveedores = []
        self._clientes = []
        self._empleados = []
        self._depositos = []
        self._solicitudes = []
        self._pedidos = []
        self._remesas = []
        self._arbol_materiales = Arbol()

    @staticmethod
    def convertir_fecha(texto_fecha):
        if texto_fecha == "":
            return None

        partes = texto_fecha.split("-")
        anio = int(partes[0])
        mes = int(partes[1])
        dia = int(partes[2])

        return date(anio, mes, dia)

    def guardar_csv(self, archivo, encabezados, objetos):
        filas = []

        for objeto in objetos:
            filas.append(objeto.a_fila())

        GestorArchivos.escribir_csv(archivo, encabezados, filas)

    def guardar_materiales(self):
        self.guardar_csv("materiales.csv", 
            ["id", "nombre", "composicion", "unidad_medida", "punto_reposicion", "precio_base", "precio_venta"],
            self._materiales)


    def cargar_materiales(self):
        filas = GestorArchivos.leer_csv_dict("materiales.csv")
        materiales = []
        for fila in filas:
            material = Material(
                fila["nombre"],
                fila["composicion"],
                fila["unidad_medida"],
                float(fila["punto_reposicion"]),
                id_manual=fila["id"],
                precio_base=float(fila["precio_base"]),
                precio_venta=float(fila["precio_venta"]))
            materiales.append(material)
        self.agregar_materiales(materiales)

    def agregar_pedido(self, pedido):
        self._pedidos.append(pedido)

    def get_pedidos(self):
        return self._pedidos.copy()

    def get_materiales(self):
        return self._materiales.copy()

    def get_empleados(self):
        return self._empleados.copy()

    def guardar_proveedores(self):
        self.guardar_csv("proveedores.csv",
            ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja", "plazo_estimado", "puntaje"],
            self._proveedores)


    def cargar_proveedores(self):
        filas = GestorArchivos.leer_csv_dict("proveedores.csv")

        for fila in filas:
            proveedor = Proveedor(fila["nombre"],
                int(fila["plazo_estimado"]),
                fila["telefono"],
                int(fila["dni"]),
                fila["email"],
                self.convertir_fecha(fila["fecha_alta"]),
                fecha_baja=self.convertir_fecha(fila["fecha_baja"]),
                id_manual=fila["id"],
                puntaje_manual=fila["puntaje"])
            self._proveedores.append(proveedor)


    def guardar_clientes(self):
        self.guardar_csv("clientes.csv",
            ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja"],
            self._clientes)


    def cargar_clientes(self):
        filas = GestorArchivos.leer_csv_dict("clientes.csv")

        for fila in filas:
            cliente = Cliente(fila["nombre"],
                fila["telefono"],
                int(fila["dni"]),
                fila["email"],
                self.convertir_fecha(fila["fecha_alta"]),
                fecha_baja=self.convertir_fecha(fila["fecha_baja"]),
                id_manual=fila["id"])
            self._clientes.append(cliente)


    def guardar_empleados(self):
        filas = []

        for empleado in self._empleados:
            fila = empleado.a_fila()
            fila.append(type(empleado).__name__)
            filas.append(fila)

        GestorArchivos.escribir_csv("empleados.csv",
            ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja", "usuario", "clave", "tipo"],
            filas)


    def crear_administrador_inicial(self):
        if len(self._empleados) == 0:
            administrador = Administrador("Administrador",
                "1111111111",12345678,self.convertir_fecha("2026-01-01"),
                "admin@aerotech.com","admin","Admin1234!")

            self._empleados.append(administrador)


    def cargar_empleados(self):
        filas = GestorArchivos.leer_csv_dict("empleados.csv")

        for fila in filas:
            fecha_alta = self.convertir_fecha(fila["fecha_alta"])
            fecha_baja = self.convertir_fecha(fila["fecha_baja"])

            if fila["tipo"] == "Comprador":
                empleado = Comprador(fila["nombre"], fila["telefono"], int(fila["dni"]),
                    fecha_alta, fila["email"], fila["usuario"], fila["clave"],
                    fecha_baja=fecha_baja, id_manual=fila["id"])

            elif fila["tipo"] == "Vendedor":
                empleado = Vendedor(fila["nombre"], fila["telefono"], int(fila["dni"]),
                    fecha_alta, fila["email"], fila["usuario"], fila["clave"],
                    fecha_baja=fecha_baja, id_manual=fila["id"])

            elif fila["tipo"] == "Administrador":
                empleado = Administrador(fila["nombre"], fila["telefono"], int(fila["dni"]),
                    fecha_alta, fila["email"], fila["usuario"], fila["clave"],
                    fecha_baja=fecha_baja, id_manual=fila["id"])

            elif fila["tipo"] == "Supervisor":
                empleado = Supervisor(fila["nombre"], fila["telefono"], int(fila["dni"]),
                    fecha_alta, fila["email"], fila["usuario"], fila["clave"],
                    fecha_baja=fecha_baja, id_manual=fila["id"])

            else:
                continue

            self._empleados.append(empleado)

    def buscar_deposito(self, nombre):
        for deposito in self._depositos:
            if deposito.get_nombre() == nombre:
                return deposito
        return None

    def guardar_depositos(self):
        filas = []

        for deposito in self._depositos:
            filas.append([deposito.get_nombre()])

        GestorArchivos.escribir_csv("depositos.csv", ["nombre"], filas)

    def cargar_depositos(self):
        self._depositos = []

        filas = GestorArchivos.leer_csv_dict("depositos.csv")

        for fila in filas:
            deposito = Deposito(fila["nombre"])
            self._depositos.append(deposito)


    def guardar_stock(self):
        filas = []

        for deposito in self._depositos:
            for material, estante in deposito.get_stock().items():
                caja = estante.get_primera()

                while caja is not None:
                    filas.append([deposito.get_nombre(),material.get_id_material(),caja.get_fecha_vencimiento(),caja.get_cantidad()])
                    caja = caja.get_prox()

        GestorArchivos.escribir_csv("stock.csv",["deposito", "material_id", "fecha_vencimiento", "cantidad"],filas)


    def cargar_stock(self):
        filas = GestorArchivos.leer_csv_dict("stock.csv")

        for fila in filas:
            deposito_encontrado = None

            for deposito in self._depositos:
                if deposito.get_nombre() == fila["deposito"]:
                    deposito_encontrado = deposito

            material_encontrado = None

            for material in self._materiales:
                if material.get_id_material() == int(fila["material_id"]):
                    material_encontrado = material

            if deposito_encontrado is None:
                raise ValueError("No se encontró el depósito")

            if material_encontrado is None:
                raise ValueError("No se encontró el material")

            stock = deposito_encontrado.get_stock()

            if material_encontrado not in stock:
                stock[material_encontrado] = Estante()

            stock[material_encontrado].agregar_caja(
                self.convertir_fecha(fila["fecha_vencimiento"]),
                float(fila["cantidad"]))


    def guardar_solicitudes(self):
        filas = []
        filas_items = []

        for solicitud in self._solicitudes:
            filas.append(solicitud.a_fila())

            materiales = solicitud.get_materiales()
            cantidades = solicitud.get_cantidades()
            precios_unitarios = solicitud.get_precios_unitarios()

            for i in range(len(materiales)):
                mat = materiales[i]
                mat_id = mat.get_id_material() if hasattr(mat, 'get_id_material') and mat.get_id_material() is not None else 0
                
                filas_items.append([
                    solicitud.get_id_solicitud(),
                    mat_id,
                    cantidades[i],
                    precios_unitarios[i]])

        GestorArchivos.escribir_csv(
            "solicitudes.csv",
            ["id", "fecha", "proveedor_id", "estado", "comprador_id", "fecha_envio"],
            filas)
        
        GestorArchivos.escribir_csv(
            "solicitudes_items.csv",
            ["solicitud_id", "material_id", "cantidad", "precio_unitario"],
            filas_items)


    def cargar_solicitudes(self):
        filas = GestorArchivos.leer_csv_dict("solicitudes.csv")
        filas_items = GestorArchivos.leer_csv_dict("solicitudes_items.csv")

        for fila in filas:
            proveedor_encontrado = None
            comprador_encontrado = None

            for proveedor in self._proveedores:
                if proveedor.get_id() == int(fila["proveedor_id"]):
                    proveedor_encontrado = proveedor

            for empleado in self._empleados:
                if empleado.get_id() == int(fila["comprador_id"]):
                    comprador_encontrado = empleado

            materiales = []
            cantidades = []
            precios_unitarios = []

            for item in filas_items:
                if int(item["solicitud_id"]) == int(fila["id"]):
                    for material in self._materiales:
                        if material.get_id_material() == int(item["material_id"]):
                            materiales.append(material)
                            cantidades.append(float(item["cantidad"]))
                            precio = float(item["precio_unitario"]) if item.get("precio_unitario") else material.get_precio_base()
                            precios_unitarios.append(precio)

            solicitud = Solicitud_proveedor(proveedor_encontrado,
                self.convertir_fecha(fila["fecha"]),materiales,cantidades,
                fila["estado"],comprador_encontrado,
                id_manual=fila["id"],
                fecha_envio_manual=self.convertir_fecha(fila["fecha_envio"]),
                precios_unitarios=precios_unitarios)
            self._solicitudes.append(solicitud)


    def guardar_pedidos(self):
        filas = []
        filas_items = []

        for pedido in self._pedidos:
            filas.append(pedido.a_fila())

            materiales = pedido.get_materiales()
            cantidades = pedido.get_cantidades()
            precios_unitarios = pedido.get_precios_unitarios()

            for i in range(len(materiales)):
                filas_items.append([pedido.get_id_pedido(),
                    materiales[i].get_id_material(),cantidades[i],precios_unitarios[i]])

        GestorArchivos.escribir_csv("pedidos.csv",
            ["id", "fecha", "cliente_id", "estado", "vendedor_id",
            "fecha_aceptacion", "fecha_envio"],filas)
        
        GestorArchivos.escribir_csv("pedidos_items.csv",
            ["pedido_id", "material_id", "cantidad", "precio_unitario"],filas_items)


    def cargar_pedidos(self):
        filas = GestorArchivos.leer_csv_dict("pedidos.csv")
        filas_items = GestorArchivos.leer_csv_dict("pedidos_items.csv")

        for fila in filas:
            cliente_encontrado = None
            vendedor_encontrado = None

            for cliente in self._clientes:
                if cliente.get_id() == int(fila["cliente_id"]):
                    cliente_encontrado = cliente

            for empleado in self._empleados:
                if empleado.get_id() == int(fila["vendedor_id"]):
                    vendedor_encontrado = empleado

            materiales = []
            cantidades = []
            precios_unitarios = []

            for item in filas_items:
                if int(item["pedido_id"]) == int(fila["id"]):
                    for material in self._materiales:
                        if material.get_id_material() == int(item["material_id"]):
                            materiales.append(material)
                            cantidades.append(float(item["cantidad"]))
                            precio = float(item["precio_unitario"]) if item.get("precio_unitario") else material.get_precio_base()
                            precios_unitarios.append(precio)

            pedido = Pedido_salida(
                self.convertir_fecha(fila["fecha"]),materiales,cantidades,
                precios_unitarios,cliente_encontrado, fila["estado"],
                vendedor_encontrado,
                id_manual=fila["id"],
                fecha_aceptacion_manual=self.convertir_fecha(fila["fecha_aceptacion"]),
                fecha_envio_manual=self.convertir_fecha(fila["fecha_envio"]))
            self._pedidos.append(pedido)


    def guardar_remesas(self):
        filas = []
        filas_items = []

        for remesa in self._remesas:
            filas.append(remesa.a_fila())

            materiales = remesa.get_materiales()
            cantidades = remesa.get_cantidades()
            fechas_vencimiento = remesa.get_fechas_vencimiento()

            for i in range(len(materiales)):
                filas_items.append([remesa.get_id_remesa(),
                    materiales[i].get_id_material(),
                    cantidades[i],fechas_vencimiento[i]])

        GestorArchivos.escribir_csv("remesas.csv",
            ["id", "proveedor_id", "solicitud_id", "fecha_llegada"],filas)
        GestorArchivos.escribir_csv("remesas_items.csv",
            ["remesa_id", "material_id", "cantidad", "fecha_vencimiento"],filas_items)


    def cargar_remesas(self):
        filas = GestorArchivos.leer_csv_dict("remesas.csv")
        filas_items = GestorArchivos.leer_csv_dict("remesas_items.csv")

        for fila in filas:
            proveedor_encontrado = None
            solicitud_encontrada = None

            for proveedor in self._proveedores:
                if proveedor.get_id() == int(fila["proveedor_id"]):
                    proveedor_encontrado = proveedor

            for solicitud in self._solicitudes:
                if fila["solicitud_id"] != "" and solicitud.get_id_solicitud() == int(fila["solicitud_id"]):
                    solicitud_encontrada = solicitud

            materiales = []
            cantidades = []
            fechas_vencimiento = []

            for item in filas_items:
                if int(item["remesa_id"]) == int(fila["id"]):
                    for material in self._materiales:
                        if material.get_id_material() == int(item["material_id"]):
                            materiales.append(material)
                            cantidades.append(float(item["cantidad"]))
                            fechas_vencimiento.append(
                                self.convertir_fecha(item["fecha_vencimiento"]))

            remesa = Remesa(materiales,proveedor_encontrado,
                solicitud_encontrada,cantidades,fechas_vencimiento,
                None,None,self.convertir_fecha(fila["fecha_llegada"]),
                id_manual=fila["id"],cargando=True)
            self._remesas.append(remesa)

    def guardar_precios_proveedores(self):
        filas = []

        for proveedor in self._proveedores:
            precios = proveedor.get_precios_materiales()

            for material_id, precio in precios.items():
                filas.append([proveedor.get_id(), material_id, precio])

        GestorArchivos.escribir_csv("proveedores_precios.csv",
            ["proveedor_id", "material_id", "precio"],filas)


    def cargar_precios_proveedores(self):
        filas = GestorArchivos.leer_csv_dict("proveedores_precios.csv")

        for fila in filas:
            proveedor_encontrado = None
            material_encontrado = None

            for proveedor in self._proveedores:
                if proveedor.get_id() == int(fila["proveedor_id"]):
                    proveedor_encontrado = proveedor

            for material in self._materiales:
                if material.get_id_material() == int(fila["material_id"]):
                    material_encontrado = material

            if proveedor_encontrado is not None and material_encontrado is not None:
                proveedor_encontrado.agregar_material(material_encontrado, float(fila["precio"]))

    def agregar_material(self, material):
        self._arbol_materiales.insertar(material.get_nombre().strip().lower(), material)
        self._materiales.append(material)

    def agregar_materiales(self, materiales):
        pares = list(map(lambda material: (material.get_nombre().strip().lower(), material), materiales))
        pares_ordenados = sorted(pares, key=lambda par: par[0])

        self._arbol_materiales.insertar_balanceado(pares_ordenados)
        self._materiales.extend(materiales)

    def buscar_material_por_nombre(self, nombre):
        return self._arbol_materiales.buscar(nombre.strip().lower())

    def get_pasos_ultima_busqueda(self):
        return self._arbol_materiales.get_pasos_ultima_busqueda()

    def get_cantidad_materiales(self):
        return self._arbol_materiales.get_cantidad()

    def get_materiales_ordenados(self):
        return self._arbol_materiales.recorrido_inorden()
    def agregar_solicitud(self, solicitud):
        self._solicitudes.append(solicitud)

    def get_solicitudes(self):
        return self._solicitudes.copy()

    def agregar_remesa(self, remesa):
        self._remesas.append(remesa)

    def get_remesas(self):
        return self._remesas.copy()

    def agregar_proveedor(self, proveedor):
        self._proveedores.append(proveedor)

    def get_proveedores(self):
        return self._proveedores.copy()

    def agregar_cliente(self, cliente):
        self._clientes.append(cliente)

    def get_clientes(self):
        return self._clientes.copy()

    def agregar_deposito(self, deposito):
        self._depositos.append(deposito)
    
    def get_depositos(self):
        return self._depositos.copy()

    def autenticar(self, usuario, clave):
        coincidencias = list(filter(lambda empleado: empleado.get_fecha_baja() is None
            and empleado.get_usuario() == usuario
            and empleado.get_clave() == clave, self._empleados))

        if len(coincidencias) == 0:
            raise ValueError("Usuario o contraseña incorrectos")

        return coincidencias[0]
    
    def agregar_empleado(self, empleado):
        self._empleados.append(empleado)

    def buscar_por_id(self, lista, id_objeto, metodo_id):
        for objeto in lista:
            if getattr(objeto, metodo_id)() == int(id_objeto):
                return objeto
        return None

    def fila_tarea_solicitud(self, tarea):
        return [
            "solicitud", tarea.get_objeto().get_id_solicitud(),
            "", "", "", ""
        ]

    def fila_tarea_pedido(self, tarea):
        deposito = ""

        if tarea.get_datos() is not None:
            deposito = tarea.get_datos().get_nombre()

        return [
            "pedido", tarea.get_objeto().get_id_pedido(),
            deposito, "", "", ""
        ]

    def fila_tarea_remesa(self, tarea):
        return [
            "remesa", tarea.get_objeto().get_id_remesa(),
            tarea.get_datos().get_nombre(), "", "", ""
        ]

    def fila_tarea_reponer(self, tarea):
        return [
            "reponer", tarea.get_objeto().get_id_material(),
            "", "", "", ""
        ]

    def fila_tarea_retirar(self, tarea):
        return [
            "retirar_vencidos", "",
            tarea.get_objeto().get_nombre(), "", "", ""
        ]

    def fila_tarea_transferencia(self, tarea):
        origen, destino, materiales, cantidades = tarea.get_datos()

        ids_materiales = []

        for material in materiales:
            ids_materiales.append(str(material.get_id_material()))

        return [
            "transferencia", "",
            origen.get_nombre(),
            destino.get_nombre(),
            ";".join(ids_materiales),
            ";".join(map(str, cantidades))
        ]

    def guardar_tareas(self, archivo, cola):
        filas = []

        funciones = {
            "solicitud": self.fila_tarea_solicitud,
            "pedido": self.fila_tarea_pedido,
            "remesa": self.fila_tarea_remesa,
            "reponer": self.fila_tarea_reponer,
            "retirar_vencidos": self.fila_tarea_retirar,
            "transferencia": self.fila_tarea_transferencia
        }

        for tarea in cola.obtener_tareas():
            tipo = tarea.get_tipo()
            fila = funciones[tipo](tarea)
            filas.append(fila)

        GestorArchivos.escribir_csv(
            archivo,
            [
                "tipo", "objeto_id", "deposito",
                "deposito_destino", "materiales", "cantidades"
            ],
            filas
        )

    def cargar_tarea_solicitud(self, fila):
        objeto = self.buscar_por_id(
            self._solicitudes,
            fila["objeto_id"],
            "get_id_solicitud"
        )
        return Tarea("solicitud", objeto)

    def cargar_tarea_pedido(self, fila):
        objeto = self.buscar_por_id(
            self._pedidos,
            fila["objeto_id"],
            "get_id_pedido"
        )

        datos = None

        if fila["deposito"]:
            datos = self.buscar_deposito(fila["deposito"])

        return Tarea("pedido", objeto, datos)

    def cargar_tarea_remesa(self, fila):
        objeto = self.buscar_por_id(
            self._remesas,
            fila["objeto_id"],
            "get_id_remesa"
        )
        deposito = self.buscar_deposito(fila["deposito"])

        return Tarea("remesa", objeto, deposito)

    def cargar_tarea_reponer(self, fila):
        objeto = self.buscar_por_id(
            self._materiales,
            fila["objeto_id"],
            "get_id_material"
        )
        return Tarea("reponer", objeto)

    def cargar_tarea_retirar(self, fila):
        deposito = self.buscar_deposito(fila["deposito"])
        return Tarea("retirar_vencidos", deposito)

    def cargar_tarea_transferencia(self, fila):
        origen = self.buscar_deposito(fila["deposito"])
        destino = self.buscar_deposito(fila["deposito_destino"])

        materiales = []
        cantidades = []

        ids_materiales = fila["materiales"].split(";")
        cantidades_texto = fila["cantidades"].split(";")

        for id_material in ids_materiales:
            material = self.buscar_por_id(
                self._materiales,
                id_material,
                "get_id_material"
            )
            materiales.append(material)

        for cantidad in cantidades_texto:
            cantidades.append(float(cantidad))

        datos = (origen, destino, materiales, cantidades)

        return Tarea("transferencia", None, datos)


    def cargar_tareas(self, archivo, cola):
        filas = GestorArchivos.leer_csv_dict(archivo)

        funciones = {
            "solicitud": self.cargar_tarea_solicitud,
            "pedido": self.cargar_tarea_pedido,
            "remesa": self.cargar_tarea_remesa,
            "reponer": self.cargar_tarea_reponer,
            "retirar_vencidos": self.cargar_tarea_retirar,
            "transferencia": self.cargar_tarea_transferencia
        }

        for fila in filas:
            tipo = fila["tipo"]

            if tipo in funciones:
                tarea = funciones[tipo](fila)

                if tarea is not None:
                    cola.agregar(tarea)

    def guardar_tareas_todas(
        self, tareas_admin, tareas_supervisor,
        tareas_comprador, tareas_vendedor):
        self.guardar_tareas("tareas_admin.csv", tareas_admin)
        self.guardar_tareas("tareas_supervisor.csv", tareas_supervisor)
        self.guardar_tareas("tareas_comprador.csv", tareas_comprador)
        self.guardar_tareas("tareas_vendedor.csv", tareas_vendedor)


    def cargar_tareas_todas(
        self, tareas_admin, tareas_supervisor,
        tareas_comprador, tareas_vendedor):
        self.cargar_tareas("tareas_admin.csv", tareas_admin)
        self.cargar_tareas("tareas_supervisor.csv", tareas_supervisor)
        self.cargar_tareas("tareas_comprador.csv", tareas_comprador)
        self.cargar_tareas("tareas_vendedor.csv", tareas_vendedor)

    
    def cargar_estado_total(self, tareas_admin, tareas_supervisor,
        tareas_comprador, tareas_vendedor):
        self.cargar_materiales()
        self.cargar_proveedores()
        self.cargar_precios_proveedores()
        self.cargar_clientes()
        self.cargar_empleados()
        self.cargar_depositos()
        self.cargar_solicitudes()
        self.cargar_pedidos()
        self.cargar_remesas()
        self.cargar_stock()
        self.cargar_tareas_todas(tareas_admin, tareas_supervisor,
        tareas_comprador, tareas_vendedor)


    def guardar_estado_total(self, tareas_admin, tareas_supervisor,
        tareas_comprador, tareas_vendedor):
        self.guardar_materiales()
        self.guardar_proveedores()
        self.guardar_precios_proveedores()
        self.guardar_clientes()
        self.guardar_empleados()
        self.guardar_depositos()
        self.guardar_solicitudes()
        self.guardar_pedidos()
        self.guardar_remesas()
        self.guardar_stock()
        self.guardar_tareas_todas(tareas_admin, tareas_supervisor,
        tareas_comprador, tareas_vendedor)

    