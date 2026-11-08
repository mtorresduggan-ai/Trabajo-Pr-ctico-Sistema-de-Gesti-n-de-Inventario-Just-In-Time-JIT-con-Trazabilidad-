from gestor_archivos import GestorArchivos


class Gestor:

    def __init__(self):
        self._elementos = {}

    def registrar(self, clave, objeto, tipo):
        if clave in self._elementos:
            raise ValueError(f"Ya existe un {tipo} con el id {clave}")
        self._elementos[clave] = objeto

    def buscar_id(self, texto_id):
        if texto_id == "":
            return None
        return self._elementos.get(int(texto_id))

    def guardar_csv(self, archivo, encabezados, objetos):
        filas = list(map(lambda objeto: objeto.a_fila(), objetos))
        GestorArchivos.escribir_csv(archivo, encabezados, filas)