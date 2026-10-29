from individuo import Individuo

from individuo import Individuo

class Proveedor(Individuo):

    def __init__(self, nombre, plazo_estimado, telefono, dni, email, fecha_alta, fecha_baja=None, id_manual=None, puntaje_manual=None):
        self.validar_plazo(plazo_estimado)

        super().__init__(nombre, telefono, dni, email, fecha_alta, fecha_baja, id_manual)
        self._plazo_estimado = plazo_estimado

        if puntaje_manual is not None:
            self._puntaje = float(puntaje_manual)
        else:
            self._puntaje = 5

        self._precios_materiales = {}

    def a_fila(self):
        return super().a_fila() + [self.get_plazo_estimado(),self.get_puntaje()]

    def get_plazo_estimado(self):
        return self._plazo_estimado

    def get_puntaje(self):
        return self._puntaje

    def get_precios_materiales(self):
        return self._precios_materiales.copy()
    
    def set_plazo_estimado(self, nuevo_plazo):
        self.validar_plazo(nuevo_plazo)
        self._plazo_estimado = nuevo_plazo

    def __str__(self):
        return 'Nombre: ' + self.get_nombre() + '  Telefono: ' + self.get_telefono()


    @staticmethod
    def validar_plazo(plazo):
        if not isinstance(plazo, int):
            raise TypeError("El plazo de entrega debe ser un int")
        if plazo <= 0:
            raise ValueError("El plazo de entrega debe ser mayor a 0 días")
    
    def modificar_puntaje(self, cambio):
        if not isinstance(cambio, (int, float)):
            raise TypeError("El cambio de puntaje debe ser un numero")
        nuevo_puntaje = self._puntaje + cambio

        if nuevo_puntaje < 0:
            self._puntaje = 0
        elif nuevo_puntaje > 10:
            self._puntaje = 10
        else:
            self._puntaje = nuevo_puntaje
    
    def agregar_material(self, material, precio_unitario):
        self.validar_precio(precio_unitario)
        codigo = material.get_id_material()

        if codigo not in self._precios_materiales:
            self._precios_materiales[codigo] = precio_unitario

        elif self._precios_materiales[codigo] != precio_unitario:
            self._precios_materiales[codigo] = precio_unitario
    
    def obtener_precio(self, material):
        codigo = material.get_id_material()
        return self._precios_materiales[codigo]
    
    @staticmethod
    def validar_precio(precio):
        if not isinstance(precio, (int, float)):
            raise TypeError("El precio debe ser un número")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")