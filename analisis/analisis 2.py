
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

    pedido = pedidos_por_id.get(remesa["id_pedido"])

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

    tiempos_reales = [
        e["tiempo_real"] for e in entregas
    ]

    tiempos_previstos = [
        e["tiempo_previsto"] for e in entregas
    ]

    demoras = [
        e["demora"] for e in entregas
    ]

    lead_time = convertir_numero(proveedor["lead_time_dias"])
    confiabilidad = convertir_numero(
        proveedor["indice_confiabilidad"]
    )

    promedio_real = np.mean(tiempos_reales)
    promedio_previsto = np.mean(tiempos_previstos)
    demora_promedio = np.mean(demoras)

    porcentaje_cumplimiento = (
        sum(1 for d in demoras if d <= 0)
        / len(demoras)
    ) * 100

    metricas.append({
        "id_proveedor": id_proveedor,
        "nombre": proveedor["nombre"],
        "cantidad_entregas": len(entregas),
        "lead_time": lead_time,
        "tiempo_real": promedio_real,
        "tiempo_previsto": promedio_previsto,
        "demora": demora_promedio,
        "confiabilidad": confiabilidad,
        "cumplimiento": porcentaje_cumplimiento
    })


# -----------------------------------------
# 5. MOSTRAR RESULTADOS
# -----------------------------------------

metricas.sort(key=lambda m: m["demora"])

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
    print(f"  Demora promedio: {m['demora']:.1f} días")
    print(f"  Cumplimiento de fechas: {m['cumplimiento']:.1f}%")
    print(f"  Confiabilidad: {m['confiabilidad']:.2f}")


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
# 7. GRAFICO 2: CONFIABILIDAD Y DEMORAS
# -----------------------------------------

plt.figure(figsize=(13, 8))
ax = plt.gca()

# Limites de los ejes
ax.set_xlim(-2, 5)
ax.set_ylim(0, 1)

# Fondos de los cuatro cuadrantes
ax.axvspan(-2, 0, ymin=0.5, ymax=1,
           color="#B1E4CC", alpha=0.8)

ax.axvspan(0, 5, ymin=0.5, ymax=1,
           color="#FFE0B2", alpha=0.8)

ax.axvspan(0, 5, ymin=0, ymax=0.5,
           color="#F5C6C6", alpha=0.8)

ax.axvspan(-2, 0, ymin=0, ymax=0.5,
           color="#B7D5EF", alpha=0.8)


# Agregar proveedores
for m in metricas:

    demora = m["demora"]
    confiabilidad = m["confiabilidad"]

    if demora <= 0 and confiabilidad >= 0.5:
        color = "#16866F"
    elif demora > 0 and confiabilidad < 0.5:
        color = "#C74440"
    elif demora > 0 and confiabilidad >= 0.5:
        color = "#D9822B"
    else:
        color = "#3478A8"

    plt.scatter(
        demora,
        confiabilidad,
        color=color,
        s=100,
        edgecolor="black",
        linewidth=0.5,
        zorder=3
    )

    plt.annotate(
        m["nombre"],
        (demora, confiabilidad),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8
    )


# Lineas divisorias
ax.axvline(x=0, color="black", linestyle="--", linewidth=1)
ax.axhline(y=0.5, color="black", linestyle="--", linewidth=1)


# Nombres de los cuadrantes
ax.text(0.02, 0.97, "Confiable y cumple",
        transform=ax.transAxes, ha="left", va="top",
        fontsize=9, fontweight="bold", color="#187C70")

ax.text(0.98, 0.97, "Confiable, pero no cumple",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=9, fontweight="bold", color="#A65D25")

ax.text(0.02, 0.03, "No confiable, pero cumple",
        transform=ax.transAxes, ha="left", va="bottom",
        fontsize=9, fontweight="bold", color="#356B91")

ax.text(0.98, 0.03, "No confiable y no cumple",
        transform=ax.transAxes, ha="right", va="bottom",
        fontsize=9, fontweight="bold", color="#B94343")


# Titulos y formato
plt.xlabel("Demora promedio respecto de la fecha prevista (días)")
plt.ylabel("Índice de confiabilidad")
plt.title("Confiabilidad y cumplimiento de entregas por proveedor")

plt.grid(alpha=0.2)
plt.tight_layout()

# Guardar grafico
plt.savefig(
    CARPETA_GRAFICOS / "02_confiabilidad_demoras.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# -----------------------------------------
# 8. GUARDAR TABLA DE METRICAS
# -----------------------------------------

ruta_metricas = CARPETA_GRAFICOS / "metricas_proveedores.csv"

with open(
    ruta_metricas,
    "w",
    encoding="utf-8-sig",
    newline=""
) as archivo:

    campos = [
        "id_proveedor",
        "nombre",
        "cantidad_entregas",
        "lead_time",
        "tiempo_real",
        "tiempo_previsto",
        "demora",
        "confiabilidad",
        "cumplimiento"
    ]

    escritor = csv.DictWriter(archivo, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(metricas)


print("\nANALISIS TERMINADO.")
print("Se generaron 2 gráficos y la tabla de métricas.")
print(f"Archivos guardados en: {CARPETA_GRAFICOS}")
