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

    @staticmethod
    def convertir_fecha(texto_fecha):
        if texto_fecha == "":
            return None

        partes = texto_fecha.split("-")
        anio = int(partes[0])
        mes = int(partes[1])
        dia = int(partes[2])

        return date(anio, mes, dia)


    def guardar_materiales(self):
        filas = []

        for material in self._materiales:
            filas.append(material.a_fila())

        GestorArchivos.escribir_csv(
            "materiales.csv",
            ["id", "nombre", "composicion", "unidad_medida",
            "punto_reposicion", "precio_base", "precio_venta"],
            filas)


    def cargar_materiales(self):
        filas = GestorArchivos.leer_csv_dict("materiales.csv")

        for fila in filas:
            material = Material(
                fila["nombre"],
                fila["composicion"],
                fila["unidad_medida"],
                float(fila["punto_reposicion"]),
                id_manual=fila["id"],
                precio_base=float(fila["precio_base"]),
                precio_venta=float(fila["precio_venta"]))
            self._materiales.append(material)


    def guardar_proveedores(self):
        filas = []

        for proveedor in self._proveedores:
            filas.append(proveedor.a_fila())

        GestorArchivos.escribir_csv("proveedores.csv",
            ["id", "nombre", "telefono", "dni", "email", "fecha_alta",
            "fecha_baja", "plazo_estimado", "puntaje"],
            filas)


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
        filas = []

        for cliente in self._clientes:
            filas.append(cliente.a_fila())

        GestorArchivos.escribir_csv("clientes.csv",
            ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja"],
            filas)


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
            ["id", "nombre", "telefono", "dni", "email", "fecha_alta",
            "fecha_baja", "usuario", "clave", "tipo"],
            filas)


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
                filas_items.append([solicitud.get_id_solicitud(),materiales[i].get_id_material(),
                    cantidades[i],precios_unitarios[i]])

        GestorArchivos.escribir_csv("solicitudes.csv",
            ["id", "fecha", "proveedor_id", "estado", "comprador_id", "fecha_envio"],filas)
        
        GestorArchivos.escribir_csv("solicitudes_items.csv",
            ["solicitud_id", "material_id", "cantidad", "precio_unitario"],filas_items)


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
                            precios_unitarios.append(float(item["precio_unitario"]))

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
                            precios_unitarios.append(float(item["precio_unitario"]))

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
                if solicitud.get_id_solicitud() == int(fila["solicitud_id"]):
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


    def cargar_estado_total(self):
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


    def guardar_estado_total(self):
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