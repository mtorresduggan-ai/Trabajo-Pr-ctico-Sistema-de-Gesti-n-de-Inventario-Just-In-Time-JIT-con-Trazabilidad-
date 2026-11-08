import csv
from datetime import date

class GestorArchivos:

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
    def leer_csv_dict(ruta):
        try:
            with open(ruta, mode="r", encoding="utf-8-sig", newline="") as archivo:
                return list(csv.DictReader(archivo))
        except FileNotFoundError:
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
