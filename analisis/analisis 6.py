# =============================================================================
# ETAPA 5 - DEMANDA DE CLIENTES: MATERIALES MÁS PEDIDOS POR UNIDAD DE MEDIDA
# Sistema de Gestión de Inventario Just-In-Time (JIT)
#
# Genera un gráfico con un panel por unidad de medida (unidades, kg, litros y
# metros) y, en cada uno, los 5 materiales más pedidos por los clientes.
# Dentro de cada panel las cantidades se pueden comparar (misma unidad).
#
# Medida de demanda: columna "cantidad" de pedidos_items.csv (cantidad SOLICITADA).
# Bibliotecas necesarias: numpy y matplotlib (sin pandas)
# =============================================================================

import os
import csv
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------
# 0. CONFIGURACIÓN
# -----------------------------------------------------------------------------

# Carpeta datos_inventario_jit, que está al lado de este script. Ahí se buscan
# los CSV y se guarda el gráfico, sin importar desde dónde se ejecute.
CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_inventario_jit")

# Se consideran TODOS los pedidos (un pedido cancelado o rechazado también
# expresa una necesidad del cliente). Para analizar solo la demanda vigente:
#     ESTADOS_EXCLUIDOS = ["Cancelado", "Rechazado"]
ESTADOS_EXCLUIDOS = []

TOP_POR_UNIDAD = 5         # materiales que se muestran en cada panel
MOSTRAR_GRAFICOS = True    # False = solo guarda el PNG, sin abrir la ventana

UNIDADES = ["unidad", "kg", "litro", "metro"]
ABREVIATURA = {"unidad": "u.", "kg": "kg", "litro": "L", "metro": "m"}
NOMBRE_UNIDAD = {"unidad": "Unidades", "kg": "Kilogramos (kg)", "litro": "Litros (L)", "metro": "Metros (m)"}
COLOR_UNIDAD = {"unidad": "#3b6ea8", "kg": "#7a5195", "litro": "#2a9d8f", "metro": "#c8553d"}

COLOR_TEXTO = "#0b0b0b"
COLOR_TEXTO_2 = "#52514e"
COLOR_GRILLA = "#e4e3df"

# Estilo general del gráfico
plt.rcParams["font.size"] = 10
plt.rcParams["axes.edgecolor"] = COLOR_TEXTO_2
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["text.color"] = COLOR_TEXTO
plt.rcParams["axes.labelcolor"] = COLOR_TEXTO_2
plt.rcParams["xtick.color"] = COLOR_TEXTO_2
plt.rcParams["ytick.color"] = COLOR_TEXTO
# Al guardar desde la ventana del gráfico (botón del disquete), recortar los bordes
plt.rcParams["savefig.bbox"] = "tight"


# -----------------------------------------------------------------------------
# 1. LECTURA DE LOS ARCHIVOS CSV (lista de diccionarios, una fila cada uno)
# -----------------------------------------------------------------------------
def leer_csv(nombre):
    with open(os.path.join(CARPETA, nombre), "r", encoding="utf-8-sig", newline="") as archivo:
        return list(csv.DictReader(archivo))


materiales = leer_csv("materiales.csv")
pedidos = leer_csv("pedidos.csv")
items = leer_csv("pedidos_items.csv")


# -----------------------------------------------------------------------------
# 2. CANTIDAD SOLICITADA POR MATERIAL
# Diccionario id_material -> suma de las cantidades pedidas
# -----------------------------------------------------------------------------
ids_pedidos_analisis = set(p["id"] for p in pedidos if p["estado"] not in ESTADOS_EXCLUIDOS)

cantidad_por_material = {}
for item in items:
    if item["pedido_id"] in ids_pedidos_analisis:
        cantidad = float(item["cantidad"])
        cantidad_por_material[item["material_id"]] = cantidad_por_material.get(item["material_id"], 0) + cantidad

demanda_material = []
for m in materiales:
    demanda_material.append({
        "id_material": m["id_material"],
        "nombre": m["nombre"],
        "unidad": m["unidad"],
        "cantidad_solicitada": int(cantidad_por_material.get(m["id_material"], 0))})

# Mayor cantidad primero; si empatan, por id de material
demanda_material = sorted(demanda_material, key=lambda f: (-f["cantidad_solicitada"], f["id_material"]))


# -----------------------------------------------------------------------------
# 3. GRÁFICO: MATERIALES MÁS PEDIDOS POR UNIDAD DE MEDIDA
# Un panel por unidad de medida con sus materiales más pedidos.
# -----------------------------------------------------------------------------
fig, ejes = plt.subplots(2, 2, figsize=(13, 8.5))
ejes = ejes.flatten()
u = 0
while u < len(UNIDADES):
    unidad = UNIDADES[u]
    ax = ejes[u]

    # Materiales de esta unidad que tuvieron pedidos, de mayor a menor
    materiales_unidad = [f for f in demanda_material if f["unidad"] == unidad and f["cantidad_solicitada"] > 0]
    total_unidad = sum(f["cantidad_solicitada"] for f in materiales_unidad)
    top_unidad = materiales_unidad[:TOP_POR_UNIDAD]

    nombres_barras = [f["nombre"] for f in top_unidad]
    valores_barras = [f["cantidad_solicitada"] for f in top_unidad]
    posiciones_barras = np.arange(len(top_unidad))[::-1]          # el más pedido queda arriba

    ax.barh(posiciones_barras, valores_barras, height=0.6, color=COLOR_UNIDAD[unidad])
    ax.set_yticks(posiciones_barras)
    ax.set_yticklabels(nombres_barras, fontsize=10)
    ax.set_ylim(-0.6, TOP_POR_UNIDAD - 0.4)

    tope = 1
    if len(valores_barras) > 0:
        tope = max(valores_barras)
    ax.set_xlim(0, tope * 1.25)
    b = 0
    while b < len(valores_barras):
        ax.text(valores_barras[b] + tope * 0.02, posiciones_barras[b],
                str(valores_barras[b]) + " " + ABREVIATURA[unidad],
                va="center", fontsize=10, color=COLOR_TEXTO_2)
        b = b + 1

    ax.set_title(NOMBRE_UNIDAD[unidad] + "  ·  total: " + str(total_unidad) + " " + ABREVIATURA[unidad]
                 + "  ·  " + str(len(materiales_unidad)) + " materiales",
                 loc="left", fontsize=12, fontweight="bold", color=COLOR_UNIDAD[unidad], pad=10)
    ax.set_xlabel("Cantidad solicitada (" + ABREVIATURA[unidad] + ")")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=COLOR_GRILLA, linewidth=0.8)
    ax.set_axisbelow(True)
    u = u + 1

# Título y subtítulo separados de los paneles para que se lean bien
fig.suptitle("Materiales más pedidos por unidad de medida",
             x=0.02, y=0.995, ha="left", va="top", fontsize=18, fontweight="bold")
fig.text(0.02, 0.948, "Los " + str(TOP_POR_UNIDAD) + " materiales más solicitados en cada unidad  ·  "
         "las cantidades se comparan solo dentro de cada panel",
         ha="left", va="top", fontsize=11, color=COLOR_TEXTO_2)
fig.tight_layout(rect=[0, 0, 1, 0.925], h_pad=3, w_pad=3)

ruta_grafico = os.path.join(CARPETA, "grafico_materiales_por_unidad_de_medida.png")
fig.savefig(ruta_grafico, dpi=200, bbox_inches="tight", facecolor="white")
print("Gráfico guardado en: " + ruta_grafico)

if MOSTRAR_GRAFICOS:
    plt.show()
else:
    plt.close("all")