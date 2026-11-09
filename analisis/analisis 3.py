
from pathlib import Path
from datetime import datetime, date, timedelta
from collections import defaultdict
import csv
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# -----------------------------------------
# 1. CONFIGURACIÓN
# -----------------------------------------

CARPETA = Path(__file__).resolve().parent / "datos_inventario_jit"

CARPETA_GRAFICOS = Path(__file__).resolve().parent / "graficos_analisis_3"
CARPETA_GRAFICOS.mkdir(exist_ok=True)

FECHA_CORTE = date(2025, 12, 31)
DIAS_ANTICIPACION = 30
CANTIDAD_MATERIALES = 10


# -----------------------------------------
# 2. FUNCIONES AUXILIARES
# -----------------------------------------

def leer_csv(nombre):
    ruta = CARPETA / nombre

    with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
        return list(csv.DictReader(archivo))


def convertir_fecha(fecha):
    if not fecha or not fecha.strip():
        return None

    formatos = ["%Y-%m-%d", "%d/%m/%Y"]

    for formato in formatos:
        try:
            return datetime.strptime(fecha.strip(), formato).date()
        except ValueError:
            pass

    return None


def convertir_numero(valor):
    if not valor or not valor.strip():
        return 0.0

    return float(valor.replace(",", "."))


# -----------------------------------------
# 3. CARGA DE DATOS
# -----------------------------------------

remesas = leer_csv("remesas.csv")
materiales = leer_csv("materiales.csv")

materiales_por_id = {
    material["id_material"].strip(): material
    for material in materiales
}


# -----------------------------------------
# 4. CLASIFICACIÓN DE CADUCIDADES
# -----------------------------------------

cantidades_por_estado = defaultdict(float)
cantidades_por_material_estado = defaultdict(float)

for remesa in remesas:

    cantidad = convertir_numero(remesa["cantidad_actual"])

    if cantidad <= 0:
        continue

    id_material = remesa["id_material"].strip()
    material = materiales_por_id.get(id_material)

    if material is None:
        continue

    fecha_caducidad = convertir_fecha(remesa["fecha_caducidad"])

    if fecha_caducidad is None:
        estado = "Sin fecha de caducidad"

    elif fecha_caducidad <= FECHA_CORTE:
        estado = "Vencido"

    elif fecha_caducidad <= FECHA_CORTE + timedelta(days=DIAS_ANTICIPACION):
        estado = "Próximo a vencer"

    else:
        estado = "Vigente"

    cantidades_por_estado[estado] += cantidad
    cantidades_por_material_estado[(id_material, estado)] += cantidad


# -----------------------------------------
# 5. RESULTADOS GENERALES
# -----------------------------------------

print("\nANÁLISIS DE CADUCIDADES")
print("-----------------------------------------")
print(f"Fecha de corte: {FECHA_CORTE.strftime('%d/%m/%Y')}")
print(f"Período de anticipación: {DIAS_ANTICIPACION} días")

print("\nCantidad disponible por estado:")

estados = [
    "Vencido",
    "Próximo a vencer",
    "Vigente",
    "Sin fecha de caducidad"
]

for estado in estados:
    cantidad = cantidades_por_estado[estado]
    print(f"{estado}: {cantidad:.2f}")


# -----------------------------------------
# 6. CANTIDADES EN RIESGO POR MATERIAL
# -----------------------------------------

cantidades_por_material_riesgo = defaultdict(lambda: defaultdict(float))

for (id_material, estado), cantidad in cantidades_por_material_estado.items():

    if estado in ["Vencido", "Próximo a vencer"]:
        cantidades_por_material_riesgo[id_material][estado] += cantidad


print("\nTOP 10 - MATERIALES CON MAYOR CANTIDAD EN RIESGO")
print("-----------------------------------------")

materiales_criticos = []

for id_material, cantidades in cantidades_por_material_riesgo.items():

    vencido = cantidades["Vencido"]
    proximo = cantidades["Próximo a vencer"]
    total = vencido + proximo

    materiales_criticos.append({
        "id": id_material,
        "nombre": materiales_por_id[id_material]["nombre"],
        "vencido": vencido,
        "proximo": proximo,
        "total": total
    })

materiales_criticos.sort(
    key=lambda material: material["total"],
    reverse=True
)

for material in materiales_criticos[:CANTIDAD_MATERIALES]:

    print(
        f'{material["nombre"]}: '
        f'{material["total"]:.2f} en riesgo '
        f'(vencido: {material["vencido"]:.2f}, '
        f'próximo a vencer: {material["proximo"]:.2f})'
    )


# -----------------------------------------
# 7. PREPARACIÓN DEL TREEMAP
# -----------------------------------------

datos_treemap = []

for material in materiales_criticos[:CANTIDAD_MATERIALES]:

    datos_treemap.append({
        "nombre": material["nombre"],
        "cantidad": material["total"],
        "vencido": material["vencido"],
        "proximo": material["proximo"]
    })


# -----------------------------------------
# 8. ALGORITMO SQUARIFIED TREEMAP
# -----------------------------------------

def peor_proporcion(fila, lado):

    if not fila or lado <= 0:
        return float("inf")

    suma = sum(d["area"] for d in fila)
    mayor = max(d["area"] for d in fila)
    menor = min(d["area"] for d in fila)

    return max(
        (lado ** 2 * mayor) / (suma ** 2),
        (suma ** 2) / (lado ** 2 * menor)
    )



def distribuir_fila(fila, x, y, ancho, alto):

    rectangulos = []
    suma = sum(d["area"] for d in fila)

    if ancho >= alto:

        ancho_fila = suma / alto
        posicion_y = y

        for dato in fila:

            alto_actual = dato["area"] / ancho_fila

            rectangulos.append((
                x,
                posicion_y,
                ancho_fila,
                alto_actual,
                dato
            ))

            posicion_y += alto_actual

        nuevo_x = x + ancho_fila
        nuevo_y = y
        nuevo_ancho = ancho - ancho_fila
        nuevo_alto = alto

    else:

        alto_fila = suma / ancho
        posicion_x = x

        for dato in fila:

            ancho_actual = dato["area"] / alto_fila

            rectangulos.append((
                posicion_x,
                y,
                ancho_actual,
                alto_fila,
                dato
            ))

            posicion_x += ancho_actual

        nuevo_x = x
        nuevo_y = y + alto_fila
        nuevo_ancho = ancho
        nuevo_alto = alto - alto_fila

    return rectangulos, nuevo_x, nuevo_y, nuevo_ancho, nuevo_alto



def crear_treemap(datos, x, y, ancho, alto):

    if not datos:
        return []

    total = sum(d["cantidad"] for d in datos)

    if total <= 0:
        return []

    datos_normalizados = []

    for dato in sorted(datos, key=lambda d: d["cantidad"], reverse=True):

        datos_normalizados.append({
            **dato,
            "area": (dato["cantidad"] / total) * ancho * alto
        })

    pendientes = datos_normalizados[:]
    rectangulos_finales = []

    while pendientes:

        fila = [pendientes.pop(0)]

        while pendientes:

            lado = min(ancho, alto)

            if peor_proporcion(
                fila + [pendientes[0]], lado
            ) <= peor_proporcion(fila, lado):
                fila.append(pendientes.pop(0))
            else:
                break

        rectangulos, x, y, ancho, alto = distribuir_fila(
            fila, x, y, ancho, alto
        )

        rectangulos_finales.extend(rectangulos)

    return rectangulos_finales


# -----------------------------------------
# 9. CREACIÓN DEL GRÁFICO
# -----------------------------------------

fig, ax = plt.subplots(figsize=(15, 9))

if not datos_treemap:

    ax.text(
        0.5, 0.5,
        "No se registran materiales en riesgo de caducidad",
        ha="center",
        va="center",
        fontsize=14
    )

else:

    rectangulos = crear_treemap(
        datos_treemap,
        0,
        0,
        100,
        100
    )

    # Cada material tiene un color diferente.
    mapa_colores = plt.get_cmap("tab10")

    for indice, (x, y, ancho, alto, dato) in enumerate(rectangulos):

        color = mapa_colores(indice % 10)

        rect = patches.Rectangle(
            (x, y),
            ancho,
            alto,
            facecolor=color,
            edgecolor="white",
            linewidth=2
        )

        ax.add_patch(rect)

        # Etiquetas en los rectángulos con espacio suficiente.
        if ancho > 12 and alto > 12:

            nombre = textwrap.fill(dato["nombre"], width=18)

            ax.text(
                x + ancho / 2,
                y + alto / 2,
                f'{nombre}\n{dato["cantidad"]:.2f}',
                ha="center",
                va="center",
                fontsize=8,
                wrap=True
            )

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")

ax.set_title(
    "Top 10 de materiales con mayor cantidad en riesgo de caducidad",
    fontsize=15,
    fontweight="bold",
    pad=20
)

plt.tight_layout()


# -----------------------------------------
# 10. GUARDAR GRÁFICO
# -----------------------------------------

ruta_grafico = CARPETA_GRAFICOS / "01_treemap_caducidad.png"

plt.savefig(
    ruta_grafico,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nGráfico guardado en:")
print(ruta_grafico)

