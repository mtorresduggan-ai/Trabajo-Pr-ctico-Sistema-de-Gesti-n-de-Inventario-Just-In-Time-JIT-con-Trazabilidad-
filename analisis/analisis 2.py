# -----------------------------------------
# ANALISIS 2: DESEMPEÑO DE PROVEEDORES
# -----------------------------------------

from pathlib import Path
from datetime import datetime
from collections import defaultdict
import csv
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------------------
# 1. CARGA DE ARCHIVOS
# -----------------------------------------

CARPETA = Path(__file__).resolve().parent / "datos_inventario_jit"

CARPETA_GRAFICOS = Path(__file__).resolve().parent / "graficos_analisis_2"
CARPETA_GRAFICOS.mkdir(exist_ok=True)


def leer_csv(nombre):
    ruta = CARPETA / nombre

    with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
        return list(csv.DictReader(archivo))


remesas = leer_csv("remesas.csv")
pedidos = leer_csv("pedidos_jit.csv")
suministradores = leer_csv("suministradores.csv")


# -----------------------------------------
# 2. FUNCIONES AUXILIARES
# -----------------------------------------

def convertir_fecha(fecha):
    if not fecha:
        return None

    fecha = fecha.strip()

    try:
        return datetime.fromisoformat(fecha).date()
    except ValueError:
        return datetime.strptime(fecha, "%d/%m/%Y").date()


def convertir_numero(valor):
    return float(valor.replace(",", "."))


def normalizar(texto):
    return texto.strip().casefold()


# -----------------------------------------
# 3. RELACIONAR PEDIDOS Y REMESAS
# -----------------------------------------

pedidos_por_id = {
    p["id_pedido_ref"].strip(): p
    for p in pedidos
}

proveedores_por_id = {
    s["id_proveedor"].strip(): s
    for s in suministradores
}

entregas_por_proveedor = defaultdict(list)

remesas_sin_pedido = 0
remesas_sin_proveedor = 0

for remesa in remesas:

    pedido = pedidos_por_id.get(remesa["id_pedido"].strip())

    if pedido is None:
        remesas_sin_pedido += 1
        continue

    nombre_proveedor = remesa["proveedor"].strip()

    if not nombre_proveedor:
        nombre_proveedor = pedido["proveedor"].strip()

    id_proveedor = nombre_proveedor

    if "-" in id_proveedor:
        prefijo, numero = id_proveedor.split("-")
        id_proveedor = f"{prefijo}-{numero.zfill(3)}"

    proveedor = proveedores_por_id.get(id_proveedor)

    if proveedor is None:
        remesas_sin_proveedor += 1
        continue

    fecha_emision = convertir_fecha(pedido["fecha_emision"])
    fecha_recepcion = convertir_fecha(remesa["fecha_recepcion"])

    fecha_prevista_texto = (
        remesa["fecha_entrega_prevista"]
        or pedido["fecha_entrega_prevista"]
    )

    fecha_prevista = convertir_fecha(fecha_prevista_texto)

    if fecha_emision is None or fecha_recepcion is None:
        continue

    if fecha_prevista is None:
        continue

    tiempo_real = (fecha_recepcion - fecha_emision).days
    tiempo_previsto = (fecha_prevista - fecha_emision).days

    demora = tiempo_real - tiempo_previsto

    entregas_por_proveedor[proveedor["id_proveedor"]].append({
        "nombre": proveedor["nombre"],
        "tiempo_real": tiempo_real,
        "tiempo_previsto": tiempo_previsto,
        "demora": demora
    })


# -----------------------------------------
# 4. CALCULO DE METRICAS
# -----------------------------------------

metricas = []

for proveedor in suministradores:

    id_proveedor = proveedor["id_proveedor"]
    entregas = entregas_por_proveedor[id_proveedor]

    if not entregas:
        continue

    # Tiempos de entrega
    tiempos_reales = [
        e["tiempo_real"] for e in entregas
    ]

    tiempos_previstos = [
        e["tiempo_previsto"] for e in entregas
    ]

    demoras = [
        e["demora"] for e in entregas
    ]

    # Lead time estimado del proveedor
    lead_time = convertir_numero(
        proveedor["lead_time_dias"]
    )

    # Porcentaje de entregas a tiempo o adelantadas
    porcentaje_cumplimiento = (
        sum(1 for d in demoras if d <= 0)
        / len(demoras)
    ) * 100

    # Demora promedio, considerando solo entregas tardías
    demoras_tardias = [
        d for d in demoras if d > 0
    ]

    demora_tardias = (
        np.mean(demoras_tardias)
        if demoras_tardias else 0
    )

    # Promedios generales
    promedio_real = np.mean(tiempos_reales)
    promedio_previsto = np.mean(tiempos_previstos)
    demora_promedio = np.mean(demoras)

    # Guardar métricas del proveedor
    metricas.append({
        "id_proveedor": id_proveedor,
        "nombre": proveedor["nombre"],
        "cantidad_entregas": len(entregas),
        "lead_time": lead_time,
        "tiempo_real": promedio_real,
        "tiempo_previsto": promedio_previsto,
        "demora": demora_promedio,
        "cumplimiento": porcentaje_cumplimiento,
        "demora_tardias": demora_tardias
    })


# -----------------------------------------
# 5. MOSTRAR RESULTADOS
# -----------------------------------------

metricas.sort(key=lambda m: m["cumplimiento"])

print("\nANALISIS DE DESEMPEÑO DE PROVEEDORES")
print("------------------------------------")

print(f"Cantidad de proveedores analizados: {len(metricas)}")
print(f"Remesas sin pedido relacionado: {remesas_sin_pedido}")
print(f"Remesas sin proveedor identificado: {remesas_sin_proveedor}")

print("\nRESULTADOS POR PROVEEDOR:")

for m in metricas:
    print(f"\nProveedor: {m['nombre']}")
    print(f"  Entregas analizadas: {m['cantidad_entregas']}")
    print(f"  Lead time estimado: {m['lead_time']:.1f} días")
    print(f"  Tiempo real promedio: {m['tiempo_real']:.1f} días")
    print(f"  Tiempo previsto promedio: {m['tiempo_previsto']:.1f} días")
    print(f"  Demora promedio general: {m['demora']:.1f} días")
    print(f"  Porcentaje de cumplimiento: {m['cumplimiento']:.1f}%")
    print(f"  Demora promedio de entregas tardías: {m['demora_tardias']:.1f} días")


# -----------------------------------------
# 6. GRAFICO 1: TIEMPOS DE ENTREGA
# -----------------------------------------

metricas_grafico = sorted(
    metricas,
    key=lambda m: m["tiempo_real"]
)

nombres = [m["nombre"] for m in metricas_grafico]
lead_times = [m["lead_time"] for m in metricas_grafico]
tiempos_reales = [m["tiempo_real"] for m in metricas_grafico]

posiciones = np.arange(len(nombres))

plt.figure(figsize=(13, 8))

for i in range(len(nombres)):
    plt.plot(
        [lead_times[i], tiempos_reales[i]],
        [posiciones[i], posiciones[i]],
        color="gray",
        alpha=0.6,
        linewidth=2
    )

plt.scatter(
    lead_times,
    posiciones,
    color="#457B9D",
    s=65,
    label="Lead time estimado",
    zorder=3
)

plt.scatter(
    tiempos_reales,
    posiciones,
    color="#E76F51",
    s=65,
    label="Tiempo real promedio",
    zorder=3
)

plt.yticks(posiciones, nombres)
plt.xlabel("Días")
plt.ylabel("Proveedor")
plt.title("Comparación entre tiempos estimados y reales de entrega")
plt.legend()
plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()

plt.savefig(
    CARPETA_GRAFICOS / "01_tiempos_entrega.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# -----------------------------------------
# 7. GRAFICO 2: CUMPLIMIENTO Y DEMORAS
# -----------------------------------------

plt.figure(figsize=(13, 8))
ax = plt.gca()

# Limites de los ejes
ax.set_xlim(0, 8)
ax.set_ylim(0, 100)

# Fondos de los cuatro cuadrantes
ax.axvspan(0, 3, ymin=0.6, ymax=1,
           color="#B1E4CC", alpha=0.8)

ax.axvspan(3, 8, ymin=0.6, ymax=1,
           color="#FFE0B2", alpha=0.8)

ax.axvspan(3, 8, ymin=0, ymax=0.6,
           color="#F5C6C6", alpha=0.8)

ax.axvspan(0, 3, ymin=0, ymax=0.6,
           color="#B7D5EF", alpha=0.8)

# Agregar proveedores
for m in metricas:

    demora = m["demora_tardias"]
    cumplimiento = m["cumplimiento"]

    if cumplimiento >= 60 and demora < 3:
        color = "#16866F"
    elif cumplimiento >= 60 and demora >= 3:
        color = "#D9822B"
    elif cumplimiento < 60 and demora >= 3:
        color = "#C74440"
    else:
        color = "#3478A8"

    ax.scatter(
        demora,
        cumplimiento,
        color=color,
        s=100,
        edgecolor="black",
        linewidth=0.5,
        zorder=3
    )

    ax.annotate(
        m["nombre"],
        (demora, cumplimiento),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8
    )

# Lineas divisorias
ax.axvline(x=3, color="black", linestyle="--", linewidth=1)
ax.axhline(y=60, color="black", linestyle="--", linewidth=1)

# Nombres de los cuadrantes
ax.text(0.02, 0.97, "Buen cumplimiento y pocas demoras",
        transform=ax.transAxes, ha="left", va="top",
        fontsize=9, fontweight="bold", color="#187C70")

ax.text(0.98, 0.97, "Buen cumplimiento, pero demoras largas",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=9, fontweight="bold", color="#A65D25")

ax.text(0.02, 0.03, "Bajo cumplimiento y pocas demoras",
        transform=ax.transAxes, ha="left", va="bottom",
        fontsize=9, fontweight="bold", color="#356B91")

ax.text(0.98, 0.03, "Bajo cumplimiento y demoras largas",
        transform=ax.transAxes, ha="right", va="bottom",
        fontsize=9, fontweight="bold", color="#B94343")

# Titulos y formato
plt.xlabel("Demora promedio de las entregas tardías (días)")
plt.ylabel("Porcentaje de cumplimiento (%)")
plt.title("Cumplimiento y demoras por proveedor")

plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig(
    CARPETA_GRAFICOS / "02_cumplimiento_demoras.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("\nANALISIS TERMINADO.")
print("Se generaron 2 gráficos y la tabla de métricas.")
print(f"Archivos guardados en: {CARPETA_GRAFICOS}")