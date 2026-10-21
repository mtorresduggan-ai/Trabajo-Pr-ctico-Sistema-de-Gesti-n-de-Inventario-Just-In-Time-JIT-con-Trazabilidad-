import csv

class GestorArchivos:

    @staticmethod
    def leer_csv_dict(ruta):
        try:
            with open(ruta, mode="r", encoding="utf-8", newline="") as archivo:
                return list(csv.DictReader(archivo))
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error al leer {ruta}: {e}")
            return []

    @staticmethod
    def escribir_csv(ruta, encabezados, filas):
        try:
            with open(ruta, mode="w", encoding="utf-8", newline="") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(encabezados)
                escritor.writerows(filas)
            return True
        except PermissionError:
            print(f"El archivo {ruta} está abierto en otro programa.")
            return False
        except Exception as e:
            print(f"Error al guardar {ruta}: {e}")
            return False
