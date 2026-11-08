from gestor import Gestor
from gestor_archivos import GestorArchivos
from material import Material
from arbol import Arbol


class GestorMateriales(Gestor):

    def __init__(self):
        super().__init__()
        self._arbol = Arbol()

    def agregar_material(self, material):
        self._arbol.insertar(material.get_nombre().strip().lower(), material)
        self.registrar(material.get_id_material(), material, "material")

    def agregar_materiales(self, materiales):
        pares = list(map(lambda material: (material.get_nombre().strip().lower(), material), materiales))
        pares_ordenados = sorted(pares, key=lambda par: par[0])

        self._arbol.insertar_balanceado(pares_ordenados)
        self._elementos.update(map(lambda material: (material.get_id_material(), material), materiales))

    def get_materiales(self):
        return list(self._elementos.values())

    def buscar_material_por_id(self, id_material):
        return self.buscar_id(id_material)

    def buscar_material_por_nombre(self, nombre):
        try:
            return self._arbol.buscar(nombre.strip().lower())
        except ValueError:
            pasos = self._arbol.get_pasos_ultima_busqueda()
            raise ValueError(f"No se encontró el material '{nombre}' (se revisaron {pasos} nodos)")

    def get_pasos_ultima_busqueda(self):
        return self._arbol.get_pasos_ultima_busqueda()

    def get_cantidad_materiales(self):
        return self._arbol.get_cantidad()

    def get_materiales_ordenados(self):
        return self._arbol.recorrido_inorden()

    def filtrar_materiales(self, nombre=None, composicion=None):
        nombre = nombre.casefold().strip() if nombre else ""
        composicion = composicion.casefold().strip() if composicion else ""

        return list(filter(
            lambda m: nombre in m.get_nombre().casefold() and composicion in m.get_composicion().casefold(),
            self._elementos.values()))

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