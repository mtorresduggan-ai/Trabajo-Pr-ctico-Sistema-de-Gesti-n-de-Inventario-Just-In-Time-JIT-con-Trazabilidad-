from datetime import date

from gestor_archivos import GestorArchivos
from material import Material
from proveedor import Proveedor
from cliente import Cliente
from comprador import Comprador
from vendedor import Vendedor
from administrador import Administrador
from supervisor import Supervisor
from deposito import Deposito
from solicitud_proveedor import Solicitud_proveedor
from pedido import Pedido_salida
from remesa import Remesa
from tarea import Tarea
from arbol import Arbol


class Sistema:

    def __init__(self):
        self._materiales = {}
        self._proveedores = {}
        self._clientes = {}
        self._empleados = {}
        self._depositos = {}
        self._solicitudes = {}
        self._pedidos = {}
        self._remesas = {}
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

    @staticmethod
    def registrar(diccionario, clave, objeto, tipo):
        if clave in diccionario:
            raise ValueError(f"Ya existe un {tipo} con el id {clave}")
        diccionario[clave] = objeto

    @staticmethod
    def buscar_id(diccionario, texto_id):
        if texto_id == "":
            return None
        return diccionario.get(int(texto_id))

    def guardar_csv(self, archivo, encabezados, objetos):
        filas = list(map(lambda objeto: objeto.a_fila(), objetos))
        GestorArchivos.escribir_csv(archivo, encabezados, filas)


    def guardar_materiales(self):
        self.guardar_csv("materiales.csv",
            ["id", "nombre", "composicion", "unidad_medida", "punto_reposicion", "precio_base", "precio_venta"],
            self.get_materiales())

    def cargar_materiales(self):
        filas = GestorArchivos.leer_csv_dict("materiales.csv")

        materiales = list(map(lambda fila: Material(
            fila["nombre"],
            fila["composicion"],
            fila["unidad_medida"],
            float(fila["punto_reposicion"]),
            id_manual=fila["id"],
            precio_base=float(fila["precio_base"]),
            precio_venta=float(fila["precio_venta"])), filas))

        self.agregar_materiales(materiales)

    def agregar_material(self, material):
        self._arbol_materiales.insertar(material.get_nombre().strip().lower(), material)
        self.registrar(self._materiales, material.get_id_material(), material, "material")

    def agregar_materiales(self, materiales):
        pares = list(map(lambda material: (material.get_nombre().strip().lower(), material), materiales))
        pares_ordenados = sorted(pares, key=lambda par: par[0])

        self._arbol_materiales.insertar_balanceado(pares_ordenados)
        self._materiales.update(map(lambda material: (material.get_id_material(), material), materiales))

    def get_materiales(self):
        return list(self._materiales.values())

    def buscar_material_por_id(self, id_material):
        return self.buscar_id(self._materiales, id_material)

    def buscar_material_por_nombre(self, nombre):
        return self._arbol_materiales.buscar(nombre.strip().lower())

    def get_pasos_ultima_busqueda(self):
        return self._arbol_materiales.get_pasos_ultima_busqueda()

    def get_cantidad_materiales(self):
        return self._arbol_materiales.get_cantidad()

    def get_materiales_ordenados(self):
        return self._arbol_materiales.recorrido_inorden()


    def guardar_proveedores(self):
        self.guardar_csv("proveedores.csv",
            ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja", "plazo_estimado", "puntaje"],
            self.get_proveedores())

    def cargar_proveedores(self):
        filas = GestorArchivos.leer_csv_dict("proveedores.csv")

        for fila in filas:
            self.agregar_proveedor(Proveedor(fila["nombre"],
                int(fila["plazo_estimado"]),
                fila["telefono"],
                int(fila["dni"]),
                fila["email"],
                self.convertir_fecha(fila["fecha_alta"]),
                fecha_baja=self.convertir_fecha(fila["fecha_baja"]),
                id_manual=fila["id"],
                puntaje_manual=fila["puntaje"]))

    def agregar_proveedor(self, proveedor):
        self.registrar(self._proveedores, proveedor.get_id(), proveedor, "proveedor")

    def get_proveedores(self):
        return list(self._proveedores.values())

    def guardar_precios_proveedores(self):
        filas = []

        for proveedor in self.get_proveedores():
            precios = proveedor.get_precios_materiales()
            filas += list(map(lambda par: [proveedor.get_id(), par[0], par[1]], precios.items()))

        GestorArchivos.escribir_csv("proveedores_precios.csv",
            ["proveedor_id", "material_id", "precio"], filas)

    def cargar_precios_proveedores(self):
        filas = GestorArchivos.leer_csv_dict("proveedores_precios.csv")

        for fila in filas:
            proveedor = self.buscar_id(self._proveedores, fila["proveedor_id"])
            material = self.buscar_id(self._materiales, fila["material_id"])

            if proveedor is not None and material is not None:
                proveedor.agregar_material(material, float(fila["precio"]))


    def guardar_clientes(self):
        self.guardar_csv("clientes.csv",
            ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja"],
            self.get_clientes())

    def cargar_clientes(self):
        filas = GestorArchivos.leer_csv_dict("clientes.csv")

        for fila in filas:
            self.agregar_cliente(Cliente(fila["nombre"],
                fila["telefono"],
                int(fila["dni"]),
                fila["email"],
                self.convertir_fecha(fila["fecha_alta"]),
                fecha_baja=self.convertir_fecha(fila["fecha_baja"]),
                id_manual=fila["id"]))

    def agregar_cliente(self, cliente):
        self.registrar(self._clientes, cliente.get_id(), cliente, "cliente")

    def get_clientes(self):
        return list(self._clientes.values())


    def guardar_empleados(self):
        filas = list(map(lambda empleado: empleado.a_fila() + [type(empleado).__name__], self.get_empleados()))

        GestorArchivos.escribir_csv("empleados.csv",
            ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja", "usuario", "clave", "tipo"],
            filas)

    def cargar_empleados(self):
        filas = GestorArchivos.leer_csv_dict("empleados.csv")

        clases = {"Comprador": Comprador,
            "Vendedor": Vendedor,
            "Administrador": Administrador,
            "Supervisor": Supervisor}

        for fila in filas:
            if fila["tipo"] not in clases:
                continue

            clase = clases[fila["tipo"]]
            self.agregar_empleado(clase(fila["nombre"], fila["telefono"], int(fila["dni"]),
                self.convertir_fecha(fila["fecha_alta"]), fila["email"], fila["usuario"], fila["clave"],
                fecha_baja=self.convertir_fecha(fila["fecha_baja"]), id_manual=fila["id"]))

    def agregar_empleado(self, empleado):
        self.registrar(self._empleados, empleado.get_id(), empleado, "empleado")

    def get_empleados(self):
        return list(self._empleados.values())

    def autenticar(self, usuario, clave):
        coincidencias = list(filter(lambda empleado: empleado.get_fecha_baja() is None
            and empleado.get_usuario() == usuario
            and empleado.get_clave() == clave, self.get_empleados()))

        if len(coincidencias) == 0:
            raise ValueError("Usuario o contraseña incorrectos")

        return coincidencias[0]


    def buscar_deposito(self, nombre):
        return self._depositos.get(nombre)

    def agregar_deposito(self, deposito):
        self.registrar(self._depositos, deposito.get_nombre(), deposito, "depósito")

    def get_depositos(self):
        return list(self._depositos.values())

    def guardar_depositos(self):
        filas = list(map(lambda deposito: [deposito.get_nombre()], self.get_depositos()))
        GestorArchivos.escribir_csv("depositos.csv", ["nombre"], filas)

    def cargar_depositos(self):
        self._depositos = {}
        filas = GestorArchivos.leer_csv_dict("depositos.csv")

        for fila in filas:
            self.agregar_deposito(Deposito(fila["nombre"]))

    def guardar_stock(self):
        filas = []

        for deposito in self.get_depositos():
            for material in deposito.get_materiales():
                filas += list(map(lambda caja: [deposito.get_nombre(), material.get_id_material(), caja[0], caja[1]],
                    deposito.obtener_cajas(material)))

        GestorArchivos.escribir_csv("stock.csv", ["deposito", "material_id", "fecha_vencimiento", "cantidad"], filas)

    def cargar_stock(self):
        filas = GestorArchivos.leer_csv_dict("stock.csv")

        for fila in filas:
            deposito = self.buscar_deposito(fila["deposito"])
            material = self.buscar_id(self._materiales, fila["material_id"])

            if deposito is None:
                raise ValueError("No se encontró el depósito")

            if material is None:
                raise ValueError("No se encontró el material")

            deposito.ingresar(material,
                self.convertir_fecha(fila["fecha_vencimiento"]),
                float(fila["cantidad"]))


    def agregar_solicitud(self, solicitud):
        self.registrar(self._solicitudes, solicitud.get_id_solicitud(), solicitud, "solicitud")

    def get_solicitudes(self):
        return list(self._solicitudes.values())

    def guardar_solicitudes(self):
        solicitudes = self.get_solicitudes()
        filas = list(map(lambda solicitud: solicitud.a_fila(), solicitudes))
        filas_items = []

        for solicitud in solicitudes:
            materiales = solicitud.get_materiales()
            cantidades = solicitud.get_cantidades()
            precios = solicitud.get_precios_unitarios()

            filas_items += list(map(lambda i: [solicitud.get_id_solicitud(), materiales[i].get_id_material(),
                cantidades[i], precios[i]], range(len(materiales))))

        GestorArchivos.escribir_csv("solicitudes.csv",
            ["id", "fecha", "proveedor_id", "estado", "comprador_id", "fecha_envio"], filas)

        GestorArchivos.escribir_csv("solicitudes_items.csv",
            ["solicitud_id", "material_id", "cantidad", "precio_unitario"], filas_items)

    def cargar_solicitudes(self):
        filas = GestorArchivos.leer_csv_dict("solicitudes.csv")
        filas_items = GestorArchivos.leer_csv_dict("solicitudes_items.csv")

        for fila in filas:
            items = list(filter(lambda item: item["solicitud_id"] == fila["id"]
                and self.buscar_id(self._materiales, item["material_id"]) is not None, filas_items))

            materiales = list(map(lambda item: self.buscar_id(self._materiales, item["material_id"]), items))
            cantidades = list(map(lambda item: float(item["cantidad"]), items))
            precios = list(map(lambda item: float(item["precio_unitario"]), items))

            self.agregar_solicitud(Solicitud_proveedor(
                self.buscar_id(self._proveedores, fila["proveedor_id"]),
                self.convertir_fecha(fila["fecha"]), materiales, cantidades,
                fila["estado"],
                self.buscar_id(self._empleados, fila["comprador_id"]),
                id_manual=fila["id"],
                fecha_envio_manual=self.convertir_fecha(fila["fecha_envio"]),
                precios_unitarios=precios))


    def agregar_pedido(self, pedido):
        self.registrar(self._pedidos, pedido.get_id_pedido(), pedido, "pedido")

    def get_pedidos(self):
        return list(self._pedidos.values())

    def guardar_pedidos(self):
        pedidos = self.get_pedidos()
        filas = list(map(lambda pedido: pedido.a_fila(), pedidos))
        filas_items = []

        for pedido in pedidos:
            materiales = pedido.get_materiales()
            cantidades = pedido.get_cantidades()
            precios = pedido.get_precios_unitarios()

            filas_items += list(map(lambda i: [pedido.get_id_pedido(), materiales[i].get_id_material(),
                cantidades[i], precios[i]], range(len(materiales))))

        GestorArchivos.escribir_csv("pedidos.csv",
            ["id", "fecha", "cliente_id", "estado", "vendedor_id", "fecha_aceptacion", "fecha_envio"], filas)

        GestorArchivos.escribir_csv("pedidos_items.csv",
            ["pedido_id", "material_id", "cantidad", "precio_unitario"], filas_items)

    def cargar_pedidos(self):
        filas = GestorArchivos.leer_csv_dict("pedidos.csv")
        filas_items = GestorArchivos.leer_csv_dict("pedidos_items.csv")

        for fila in filas:
            items = list(filter(lambda item: item["pedido_id"] == fila["id"]
                and self.buscar_id(self._materiales, item["material_id"]) is not None, filas_items))

            materiales = list(map(lambda item: self.buscar_id(self._materiales, item["material_id"]), items))
            cantidades = list(map(lambda item: float(item["cantidad"]), items))
            precios = list(map(lambda item: float(item["precio_unitario"]), items))

            self.agregar_pedido(Pedido_salida(
                self.convertir_fecha(fila["fecha"]), materiales, cantidades, precios,
                self.buscar_id(self._clientes, fila["cliente_id"]),
                fila["estado"],
                self.buscar_id(self._empleados, fila["vendedor_id"]),
                id_manual=fila["id"],
                fecha_aceptacion_manual=self.convertir_fecha(fila["fecha_aceptacion"]),
                fecha_envio_manual=self.convertir_fecha(fila["fecha_envio"])))


    def agregar_remesa(self, remesa):
        self.registrar(self._remesas, remesa.get_id_remesa(), remesa, "remesa")

    def get_remesas(self):
        return list(self._remesas.values())

    def guardar_remesas(self):
        remesas = self.get_remesas()
        filas = list(map(lambda remesa: remesa.a_fila(), remesas))
        filas_items = []

        for remesa in remesas:
            materiales = remesa.get_materiales()
            cantidades = remesa.get_cantidades()
            fechas = remesa.get_fechas_vencimiento()

            filas_items += list(map(lambda i: [remesa.get_id_remesa(), materiales[i].get_id_material(),
                cantidades[i], fechas[i]], range(len(materiales))))

        GestorArchivos.escribir_csv("remesas.csv",
            ["id", "proveedor_id", "solicitud_id", "fecha_llegada"], filas)
        GestorArchivos.escribir_csv("remesas_items.csv",
            ["remesa_id", "material_id", "cantidad", "fecha_vencimiento"], filas_items)

    def cargar_remesas(self):
        filas = GestorArchivos.leer_csv_dict("remesas.csv")
        filas_items = GestorArchivos.leer_csv_dict("remesas_items.csv")

        for fila in filas:
            items = list(filter(lambda item: item["remesa_id"] == fila["id"]
                and self.buscar_id(self._materiales, item["material_id"]) is not None, filas_items))

            materiales = list(map(lambda item: self.buscar_id(self._materiales, item["material_id"]), items))
            cantidades = list(map(lambda item: float(item["cantidad"]), items))
            fechas = list(map(lambda item: self.convertir_fecha(item["fecha_vencimiento"]), items))

            self.agregar_remesa(Remesa(materiales,
                self.buscar_id(self._proveedores, fila["proveedor_id"]),
                self.buscar_id(self._solicitudes, fila["solicitud_id"]),
                cantidades, fechas, None, None,
                self.convertir_fecha(fila["fecha_llegada"]),
                id_manual=fila["id"], cargando=True))


    def fila_tarea_solicitud(self, tarea):
        return ["solicitud", tarea.get_objeto().get_id_solicitud(), "", "", "", ""]

    def fila_tarea_pedido(self, tarea):
        deposito = ""

        if tarea.get_datos() is not None:
            deposito = tarea.get_datos().get_nombre()

        return ["pedido", tarea.get_objeto().get_id_pedido(), deposito, "", "", ""]

    def fila_tarea_remesa(self, tarea):
        return ["remesa", tarea.get_objeto().get_id_remesa(), tarea.get_datos().get_nombre(), "", "", ""]

    def fila_tarea_reponer(self, tarea):
        return ["reponer", tarea.get_objeto().get_id_material(), "", "", "", ""]

    def fila_tarea_retirar(self, tarea):
        return ["retirar_vencidos", "", tarea.get_objeto().get_nombre(), "", "", ""]

    def fila_tarea_transferencia(self, tarea):
        origen, destino, materiales, cantidades = tarea.get_datos()

        ids_materiales = list(map(lambda material: str(material.get_id_material()), materiales))

        return ["transferencia", "",
            origen.get_nombre(),
            destino.get_nombre(),
            ";".join(ids_materiales),
            ";".join(map(str, cantidades))]

    def guardar_tareas(self, archivo, cola):
        funciones = {
            "solicitud": self.fila_tarea_solicitud,
            "pedido": self.fila_tarea_pedido,
            "remesa": self.fila_tarea_remesa,
            "reponer": self.fila_tarea_reponer,
            "retirar_vencidos": self.fila_tarea_retirar,
            "transferencia": self.fila_tarea_transferencia
        }

        filas = list(map(lambda tarea: funciones[tarea.get_tipo()](tarea), cola.obtener_tareas()))

        GestorArchivos.escribir_csv(archivo,
            ["tipo", "objeto_id", "deposito", "deposito_destino", "materiales", "cantidades"],
            filas)

    def cargar_tarea_solicitud(self, fila):
        return Tarea("solicitud", self.buscar_id(self._solicitudes, fila["objeto_id"]))

    def cargar_tarea_pedido(self, fila):
        datos = None

        if fila["deposito"]:
            datos = self.buscar_deposito(fila["deposito"])

        return Tarea("pedido", self.buscar_id(self._pedidos, fila["objeto_id"]), datos)

    def cargar_tarea_remesa(self, fila):
        return Tarea("remesa", self.buscar_id(self._remesas, fila["objeto_id"]), self.buscar_deposito(fila["deposito"]))

    def cargar_tarea_reponer(self, fila):
        return Tarea("reponer", self.buscar_id(self._materiales, fila["objeto_id"]))

    def cargar_tarea_retirar(self, fila):
        return Tarea("retirar_vencidos", self.buscar_deposito(fila["deposito"]))

    def cargar_tarea_transferencia(self, fila):
        origen = self.buscar_deposito(fila["deposito"])
        destino = self.buscar_deposito(fila["deposito_destino"])

        materiales = list(map(lambda id_material: self.buscar_id(self._materiales, id_material), fila["materiales"].split(";")))
        cantidades = list(map(float, fila["cantidades"].split(";")))

        return Tarea("transferencia", None, (origen, destino, materiales, cantidades))

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

        filas_validas = filter(lambda fila: fila["tipo"] in funciones, filas)

        for fila in filas_validas:
            cola.agregar(funciones[fila["tipo"]](fila))

    def guardar_tareas_todas(self, tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor):
        self.guardar_tareas("tareas_admin.csv", tareas_admin)
        self.guardar_tareas("tareas_supervisor.csv", tareas_supervisor)
        self.guardar_tareas("tareas_comprador.csv", tareas_comprador)
        self.guardar_tareas("tareas_vendedor.csv", tareas_vendedor)

    def cargar_tareas_todas(self, tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor):
        self.cargar_tareas("tareas_admin.csv", tareas_admin)
        self.cargar_tareas("tareas_supervisor.csv", tareas_supervisor)
        self.cargar_tareas("tareas_comprador.csv", tareas_comprador)
        self.cargar_tareas("tareas_vendedor.csv", tareas_vendedor)


    def cargar_estado_total(self, tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor):
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
        self.cargar_tareas_todas(tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor)

    def guardar_estado_total(self, tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor):
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
        self.guardar_tareas_todas(tareas_admin, tareas_supervisor, tareas_comprador, tareas_vendedor)