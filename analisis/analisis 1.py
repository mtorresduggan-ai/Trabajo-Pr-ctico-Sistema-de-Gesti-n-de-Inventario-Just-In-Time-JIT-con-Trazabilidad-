from pathlib import Path
from datetime import date, timedelta
import csv
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------------------
# 1. UBICACIÓN Y LECTURA DE LOS ARCHIVOS
# -----------------------------------------

CARPETA = Path(__file__).resolve().parent / "datos_inventario_jit"

def leer_csv(nombre):
    with open(CARPETA / nombre, "r", encoding="utf-8-sig", newline="") as archivo:
        return list(csv.DictReader(archivo))


materiales = leer_csv("materiales.csv")
movimientos = leer_csv("movimientos.csv")


# -----------------------------------------
# 2. CONFIGURACIÓN DEL PERÍODO
# -----------------------------------------

inicio = date(2025, 1, 1)
fin = date(2025, 12, 31)

fechas = []
fecha_actual = inicio

while fecha_actual <= fin:
    fechas.append(fecha_actual)
    fecha_actual += timedelta(days=1)

cantidad_dias = len(fechas)

meses = [
    "Ene", "Feb", "Mar", "Abr", "May", "Jun",
    "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
]


# -----------------------------------------
# 3. ORGANIZAR LOS MOVIMIENTOS
# -----------------------------------------

movimientos_por_material = {}

for movimiento in movimientos:
    material = movimiento["material"]
    fecha = date.fromisoformat(movimiento["fecha"].split()[0])
    tipo = movimiento["tipo"].upper()
    cantidad = float(movimiento["cantidad"])

    if material not in movimientos_por_material:
        movimientos_por_material[material] = {}

    if fecha not in movimientos_por_material[material]:
        movimientos_por_material[material][fecha] = 0

    if tipo == "INGRESO":
        movimientos_por_material[material][fecha] += cantidad

    elif tipo == "RETIRO":
        movimientos_por_material[material][fecha] -= cantidad


# -----------------------------------------
# 4. CALCULAR LAS MÉTRICAS
# -----------------------------------------

metricas = []
stocks_diarios = {}

for material in materiales:

    id_material = material["id_material"]
    nombre = material["nombre"]
    categoria = material["categoria"]
    umbral = float(material["umbral_reabastecimiento"])

    movimientos_material = movimientos_por_material.get(id_material, {})

    # Encontrar la primera fecha de ingreso
    fechas_ingreso = [
        fecha for fecha in movimientos_material
        if movimientos_material[fecha] > 0
    ]

    if not fechas_ingreso:
        continue

    primera_fecha = min(fechas_ingreso)
    primer_indice = (primera_fecha - inicio).days

    # Calcular el stock acumulado día por día
    movimientos_dia = np.zeros(cantidad_dias)

    for fecha, cantidad in movimientos_material.items():
        indice = (fecha - inicio).days
        movimientos_dia[indice] += cantidad

    stock_diario = np.cumsum(movimientos_dia)

    # Analizar desde el primer ingreso
    stock_analizado = stock_diario[primer_indice:]

    stocks_diarios[id_material] = {
        "nombre": nombre,
        "categoria": categoria,
        "umbral": umbral,
        "primer_indice": primer_indice,
        "stock": stock_diario
    }

    # Consumo total
    consumo = sum(
        -cantidad
        for cantidad in movimientos_material.values()
        if cantidad < 0
    )

    dias_analizados = len(stock_analizado)

    consumo_diario = consumo / dias_analizados

    # Cobertura estimada en días
    if consumo_diario > 0:
        cobertura = stock_diario[-1] / consumo_diario
    else:
        cobertura = np.nan

    stock_actual = stock_diario[-1]

    # Días con stock igual o inferior al umbral
    dias_bajo_umbral = np.sum(stock_analizado <= umbral)

    # Métricas generales
    stock_promedio = np.mean(stock_analizado)
    stock_minimo = np.min(stock_analizado)
    stock_maximo = np.max(stock_analizado)

    relacion_umbral = stock_actual / umbral

    metricas.append({
        "id_material": id_material,
        "nombre": nombre,
        "categoria": categoria,
        "umbral": umbral,
        "stock_actual": stock_actual,
        "stock_promedio": stock_promedio,
        "stock_minimo": stock_minimo,
        "stock_maximo": stock_maximo,
        "consumo_total": consumo,
        "consumo_diario": consumo_diario,
        "cobertura_dias": cobertura,
        "dias_bajo_umbral": int(dias_bajo_umbral),
        "relacion_umbral": relacion_umbral
    })


# -----------------------------------------
# 5. GUARDAR LA TABLA DE MÉTRICAS
# -----------------------------------------

columnas = list(metricas[0].keys())

with open(
    CARPETA / "metricas_salud_inventario.csv",
    "w",
    encoding="utf-8-sig",
    newline=""
) as archivo:

    escritor = csv.DictWriter(archivo, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(metricas)


# -----------------------------------------
# 6. RESUMEN GENERAL
# -----------------------------------------

coberturas = np.array([
    m["cobertura_dias"] for m in metricas
])

dias_bajo = np.array([
    m["dias_bajo_umbral"] for m in metricas
])

stock_actual = np.array([
    m["stock_actual"] for m in metricas
])

print("ANÁLISIS DE SALUD DEL INVENTARIO")
print("--------------------------------")
print("Cantidad de materiales:", len(metricas))
print("Cobertura promedio:", round(np.nanmean(coberturas), 2), "días")
print("Materiales bajo el umbral:", np.sum([
    m["stock_actual"] <= m["umbral"] for m in metricas
]))

print("\nMateriales con más días bajo el umbral:")

criticos = sorted(
    metricas,
    key=lambda m: m["dias_bajo_umbral"],
    reverse=True
)

for m in criticos[:10]:
    print(
        m["nombre"],
        "- Días bajo umbral:", m["dias_bajo_umbral"]
    )


# -----------------------------------------
# 7. CREAR CARPETA DE GRÁFICOS
# -----------------------------------------

CARPETA_GRAFICOS = CARPETA / "graficos_salud_inventario"
CARPETA_GRAFICOS.mkdir(exist_ok=True)


# -----------------------------------------
# GRÁFICO 1: STOCK ACTUAL VS. DÍAS BAJO UMBRAL
# -----------------------------------------

x = np.array([m["relacion_umbral"] for m in metricas])
y = np.array([m["dias_bajo_umbral"] for m in metricas])
colores = np.array([m["cobertura_dias"] for m in metricas])

plt.figure(figsize=(11, 7))

puntos = plt.scatter(
    x, y,
    c=colores,
    cmap="viridis",
    s=65,
    alpha=0.8
)

plt.axvline(
    x=1,
    color="red",
    linestyle="--",
    label="Umbral de reabastecimiento"
)

plt.colorbar(puntos, label="Cobertura (días)")

# Etiquetar los 8 materiales más críticos
for m in criticos[:8]:
    plt.annotate(
        m["id_material"],
        (m["relacion_umbral"], m["dias_bajo_umbral"]),
        fontsize=8
    )

plt.xlabel("Stock actual / Umbral")
plt.ylabel("Días bajo el umbral")
plt.title("Salud del inventario: riesgo por material")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig(
    CARPETA_GRAFICOS / "01_stock_vs_umbral.png",
    dpi=300
)
plt.close()


# -----------------------------------------
# GRÁFICO 2: MAPA DE CALOR DEL STOCK MENSUAL
# -----------------------------------------

# Seleccionar los 15 materiales más críticos
top_15 = criticos[:15]

matriz = np.full((len(top_15), 12), np.nan)

for fila, m in enumerate(top_15):

    datos = stocks_diarios[m["id_material"]]
    stock = datos["stock"]
    primer_indice = datos["primer_indice"]
    umbral = datos["umbral"]

    for mes in range(1, 13):

        indices_mes = [
            i for i, fecha in enumerate(fechas)
            if fecha.month == mes and i >= primer_indice
        ]

        if indices_mes:
            promedio = np.mean(stock[indices_mes])
            matriz[fila, mes - 1] = promedio / umbral

plt.figure(figsize=(15, 9))

mapa = plt.imshow(
    np.ma.masked_invalid(matriz),
    aspect="auto",
    cmap="RdYlGn",
    vmin=0,
    vmax=2
)

plt.colorbar(mapa, label="Stock promedio / Umbral")

plt.xticks(range(12), meses)

# Mostrar los nombres de los materiales
plt.yticks(
    range(len(top_15)),
    [m["nombre"] for m in top_15],
    fontsize=9
)

# Mostrar el valor exacto dentro de cada celda
for fila in range(len(top_15)):
    for columna in range(12):

        valor = matriz[fila, columna]

        if np.isfinite(valor):
            plt.text(
                columna,
                fila,
                f"{valor:.2f}",
                ha="center",
                va="center",
                color="black",
                fontsize=8
            )

plt.xlabel("Mes")
plt.ylabel("Material")
plt.title("Evolución mensual del stock de los 15 materiales críticos")

plt.tight_layout()

plt.savefig(
    CARPETA_GRAFICOS / "02_heatmap_stock_mensual.png",
    dpi=300)
plt.close()


# -----------------------------------------
# GRÁFICO 3: COBERTURA POR CATEGORÍA
# -----------------------------------------

from matplotlib.lines import Line2D

categorias = sorted(set(m["categoria"] for m in metricas))

datos_boxplot = []

for categoria in categorias:
    valores = [
        m["cobertura_dias"]
        for m in metricas
        if m["categoria"] == categoria
        and np.isfinite(m["cobertura_dias"])
    ]

    datos_boxplot.append(valores)

plt.figure(figsize=(13, 7))

grafico = plt.boxplot(
    datos_boxplot,
    tick_labels=[
        f"{cat}\n(n={len(valores)})"
        for cat, valores in zip(categorias, datos_boxplot)
    ],
    patch_artist=True,
    showmeans=True,
    meanprops={
        "marker": "D",
        "markerfacecolor": "white",
        "markeredgecolor": "black",
        "markersize": 7
    }
)

# Colores para diferenciar las categorías
colores = ["#8ECAE6", "#90BE6D", "#F9C74F", "#F4A261"]

for caja, color in zip(grafico["boxes"], colores):
    caja.set_facecolor(color)
    caja.set_alpha(0.8)

# Espacio a la derecha para mostrar los valores
plt.xlim(0.5, len(categorias) + 1.3)

# Mostrar mediana y promedio al costado de cada caja
for i, (mediana, promedio) in enumerate(
    zip(grafico["medians"], grafico["means"])
):
    valor_mediana = mediana.get_ydata()[0]
    valor_promedio = promedio.get_ydata()[0]

    posicion_x = i + 1.12

    # Valor de la mediana
    plt.annotate(
        f"Mediana: {valor_mediana:.1f}",
        xy=(posicion_x, valor_mediana),
        xytext=(5, -9),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
        color="#222222",
        va="top"
    )

    # Valor del promedio
    plt.annotate(
        f"Promedio: {valor_promedio:.1f}",
        xy=(posicion_x, valor_promedio),
        xytext=(5, 9),
        textcoords="offset points",
        fontsize=9,
        color="#444444",
        va="bottom"
    )

# Referencias visuales
leyenda = [
    Line2D(
        [0], [0],
        color="black",
        linewidth=2,
        label="Mediana"
    ),
    Line2D(
        [0], [0],
        marker="D",
        color="white",
        markerfacecolor="white",
        markeredgecolor="black",
        markersize=7,
        linestyle="none",
        label="Promedio"
    ),
    Line2D(
        [0], [0],
        marker="o",
        color="gray",
        linestyle="none",
        label="Valores atípicos"
    )
]

plt.legend(handles=leyenda, loc="upper right")

plt.ylabel("Días de cobertura del stock")
plt.xlabel("Categoría de material")
plt.title("Distribución de los días de cobertura según categoría")

plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()

plt.savefig(
    CARPETA_GRAFICOS / "03_boxplot_cobertura_categoria.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()