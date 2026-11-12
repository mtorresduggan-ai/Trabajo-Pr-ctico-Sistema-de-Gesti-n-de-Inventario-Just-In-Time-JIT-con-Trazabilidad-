# =============================================================================
# ETAPA 4 - DEMANDA Y PEDIDOS DE CLIENTES
# Sistema de Gestión de Inventario Just-In-Time (JIT)
#
# Pregunta que responde el análisis:
#   ¿Qué materiales y categorías concentran la demanda de los clientes
#   y cómo se comportan los pedidos de salida?
#
# Medida de demanda: columna "cantidad" de pedidos_items.csv (cantidad SOLICITADA).
# El precio unitario está en el CSV porque el sistema lo necesita, pero NO se usa
# en ningún cálculo ni gráfico de este script.
#
# Bibliotecas necesarias: pandas, numpy, matplotlib y squarify
#   pip install pandas numpy matplotlib squarify
# =============================================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import squarify


# -----------------------------------------------------------------------------
# 0. CONFIGURACIÓN
# -----------------------------------------------------------------------------

# Carpeta donde está guardado este script. Ahí se buscan los CSV y se guardan
# los resultados, sin importar desde dónde se ejecute
CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_inventario_jit")

# CRITERIO PARA PEDIDOS CANCELADOS Y RECHAZADOS
# Análisis principal: se consideran TODOS los pedidos registrados (lista vacía),
# porque un pedido cancelado o rechazado también expresa una necesidad del cliente.
# Para analizar solo la demanda vigente, reemplazar la línea de abajo por:
#     ESTADOS_EXCLUIDOS = ["Cancelado", "Rechazado"]
# Los archivos generados en ese caso llevan el sufijo "_demanda_vigente".
ESTADOS_EXCLUIDOS = []

TOP_MATERIALES = 15        # cantidad de materiales del gráfico de puntos
MOSTRAR_GRAFICOS = True    # False = solo guarda los PNG, sin abrir ventanas

ESTADOS_VALIDOS = ["Pendiente", "En preparacion", "Despachado", "Entregado", "Cancelado", "Rechazado"]

# Cada categoría tiene siempre el mismo color y el mismo marcador en todos los gráficos
CATEGORIAS = ["Electrónico", "Mecánico", "Químico", "Estructural"]
COLORES = {"Electrónico": "#2a78d6", "Mecánico": "#eb6834", "Químico": "#1baf7a", "Estructural": "#eda100"}
MARCADORES = {"Electrónico": "o", "Mecánico": "s", "Químico": "D", "Estructural": "^"}
UNIDADES = ["unidad", "kg", "litro", "metro"]
ABREVIATURA = {"unidad": "u.", "kg": "kg", "litro": "L", "metro": "m"}

COLOR_TEXTO = "#0b0b0b"
COLOR_TEXTO_2 = "#52514e"
COLOR_GRILLA = "#e4e3df"

SUFIJO = ""
DESCRIPCION_CRITERIO = "Todos los pedidos registrados (incluye cancelados y rechazados)"
if len(ESTADOS_EXCLUIDOS) > 0:
    SUFIJO = "_demanda_vigente"
    DESCRIPCION_CRITERIO = "Demanda vigente: excluye pedidos " + ", ".join(ESTADOS_EXCLUIDOS)

# Estilo general de los gráficos
plt.rcParams["font.size"] = 10
plt.rcParams["axes.edgecolor"] = COLOR_TEXTO_2
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["text.color"] = COLOR_TEXTO
plt.rcParams["axes.labelcolor"] = COLOR_TEXTO_2
plt.rcParams["xtick.color"] = COLOR_TEXTO_2
plt.rcParams["ytick.color"] = COLOR_TEXTO


# -----------------------------------------------------------------------------
# 1. LECTURA DE LOS ARCHIVOS CSV
# -----------------------------------------------------------------------------
materiales = pd.read_csv(os.path.join(CARPETA, "materiales.csv"), encoding="utf-8-sig")
pedidos = pd.read_csv(os.path.join(CARPETA, "pedidos.csv"), encoding="utf-8-sig")
items = pd.read_csv(os.path.join(CARPETA, "pedidos_items.csv"), encoding="utf-8-sig")
clientes = pd.read_csv(os.path.join(CARPETA, "clientes.csv"), encoding="utf-8-sig")
empleados = pd.read_csv(os.path.join(CARPETA, "empleados.csv"), encoding="utf-8-sig")


# -----------------------------------------------------------------------------
# 2. VALIDACIONES DE LOS DATOS
# Cada control guarda una descripción y la cantidad de problemas encontrados.
# Un 0 significa que el control está OK.
# -----------------------------------------------------------------------------
controles = []
problemas = []

# 2.1 Nombres de columnas (deben coincidir exactamente con el sistema)
controles.append("Columnas de materiales.csv")
problemas.append(int(list(materiales.columns) != ["id_material", "nombre", "unidad", "umbral_reabastecimiento", "categoria"]))
controles.append("Columnas de pedidos.csv")
problemas.append(int(list(pedidos.columns) != ["id", "fecha", "cliente_id", "estado", "vendedor_id", "fecha_aceptacion", "fecha_envio"]))
controles.append("Columnas de pedidos_items.csv")
problemas.append(int(list(items.columns) != ["pedido_id", "material_id", "cantidad", "precio_unitario"]))
controles.append("Columnas de clientes.csv")
problemas.append(int(list(clientes.columns) != ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja"]))
controles.append("Columnas de empleados.csv")
problemas.append(int(list(empleados.columns) != ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja", "usuario", "clave", "tipo"]))

# 2.2 Identificadores repetidos
controles.append("IDs de materiales repetidos")
problemas.append(int(materiales["id_material"].duplicated().sum()))
controles.append("IDs de pedidos repetidos")
problemas.append(int(pedidos["id"].duplicated().sum()))
controles.append("IDs de clientes y empleados superpuestos (contador compartido de Individuo)")
problemas.append(int(clientes["id"].isin(empleados["id"]).sum() + clientes["id"].duplicated().sum() + empleados["id"].duplicated().sum()))

# 2.3 Referencias entre archivos
controles.append("Materiales de pedidos_items que no existen en materiales.csv")
problemas.append(int((~items["material_id"].isin(materiales["id_material"])).sum()))
controles.append("Detalles que apuntan a un pedido inexistente")
problemas.append(int((~items["pedido_id"].isin(pedidos["id"])).sum()))
controles.append("Pedidos con cliente inexistente en clientes.csv")
problemas.append(int((~pedidos["cliente_id"].isin(clientes["id"])).sum()))
ids_vendedores = empleados.loc[empleados["tipo"] == "Vendedor", "id"]
controles.append("Pedidos con vendedor inexistente (o que no es de tipo Vendedor)")
problemas.append(int((~pedidos["vendedor_id"].isin(ids_vendedores)).sum()))
controles.append("Pedidos sin ningún detalle en pedidos_items.csv")
problemas.append(int((~pedidos["id"].isin(items["pedido_id"])).sum()))

# 2.4 Cantidades: deben ser numéricas y positivas
cantidad_numerica = pd.to_numeric(items["cantidad"], errors="coerce")
controles.append("Cantidades no numéricas")
problemas.append(int(cantidad_numerica.isna().sum()))
controles.append("Cantidades menores o iguales a cero")
problemas.append(int((cantidad_numerica <= 0).sum()))

# 2.5 Estados válidos
controles.append("Pedidos con estado inválido")
problemas.append(int((~pedidos["estado"].isin(ESTADOS_VALIDOS)).sum()))

# 2.6 Fechas válidas y coherentes (las fechas vacías quedan como NaT y no cuentan como error)
fecha_pedido = pd.to_datetime(pedidos["fecha"], errors="coerce")
fecha_aceptacion = pd.to_datetime(pedidos["fecha_aceptacion"], errors="coerce")
fecha_envio = pd.to_datetime(pedidos["fecha_envio"], errors="coerce")
controles.append("Fechas de pedido vacías o inválidas")
problemas.append(int(fecha_pedido.isna().sum()))
controles.append("Fechas de aceptación/envío escritas pero inválidas")
problemas.append(int((pedidos["fecha_aceptacion"].notna() & fecha_aceptacion.isna()).sum()
                     + (pedidos["fecha_envio"].notna() & fecha_envio.isna()).sum()))
controles.append("Aceptación anterior a la fecha del pedido")
problemas.append(int((fecha_aceptacion < fecha_pedido).sum()))
controles.append("Envío anterior a la fecha del pedido")
problemas.append(int((fecha_envio < fecha_pedido).sum()))
controles.append("Envío anterior a la aceptación")
problemas.append(int((fecha_envio < fecha_aceptacion).sum()))

print("=" * 78)
print("VALIDACIÓN DE LOS DATOS")
print("=" * 78)
i = 0
while i < len(controles):
    if problemas[i] == 0:
        print("  [OK]    " + controles[i])
    else:
        print("  [ERROR] " + controles[i] + " -> " + str(problemas[i]) + " caso(s)")
    i = i + 1
if sum(problemas) > 0:
    print("\n  ATENCIÓN: hay problemas en los datos. Los resultados pueden no ser confiables.")
else:
    print("\n  Todos los controles dieron OK.")


# -----------------------------------------------------------------------------
# 3. FILTRO DE ESTADOS Y UNIÓN DE TABLAS
# detalle = cada línea de pedidos_items + datos del pedido + datos del material
# -----------------------------------------------------------------------------
items["cantidad"] = cantidad_numerica
pedidos_analisis = pedidos[~pedidos["estado"].isin(ESTADOS_EXCLUIDOS)]

detalle = items.merge(pedidos_analisis[["id", "fecha", "cliente_id", "estado"]],
                      left_on="pedido_id", right_on="id", how="inner")
detalle = detalle.drop(columns="id")
detalle = detalle.merge(materiales, left_on="material_id", right_on="id_material", how="left")


# -----------------------------------------------------------------------------
# 4. INDICADORES GENERALES
# -----------------------------------------------------------------------------
total_pedidos = pedidos_analisis["id"].nunique()
clientes_registrados = len(clientes)
clientes_con_pedidos = pedidos_analisis["cliente_id"].nunique()
cantidad_total = detalle["cantidad"].sum()
materiales_distintos = detalle["material_id"].nunique()
lineas_de_pedido = len(detalle)
materiales_por_pedido = np.round(lineas_de_pedido / total_pedidos, 2)
cantidad_media_linea = np.round(np.mean(detalle["cantidad"]), 1)
cantidad_mediana_linea = np.median(detalle["cantidad"])

print("\n" + "=" * 78)
print("INDICADORES GENERALES")
print("Criterio: " + DESCRIPCION_CRITERIO)
print("=" * 78)
print("  Pedidos registrados analizados ........... " + str(total_pedidos))
print("  Clientes que realizaron pedidos .......... " + str(clientes_con_pedidos) + " de " + str(clientes_registrados) + " registrados")
print("  Cantidad total de materiales solicitados . " + str(int(cantidad_total)) + "  (suma de unidades distintas, ver advertencia)")
print("  Materiales diferentes solicitados ........ " + str(materiales_distintos) + " de " + str(len(materiales)))
print("  Líneas de detalle (material dentro de pedido): " + str(lineas_de_pedido))
print("  Materiales distintos por pedido (promedio)  " + str(materiales_por_pedido))
print("  Cantidad por línea: promedio " + str(cantidad_media_linea) + " | mediana " + str(cantidad_mediana_linea))

indicadores = pd.DataFrame({
    "indicador": ["Pedidos registrados analizados", "Clientes registrados", "Clientes que realizaron pedidos",
                  "Cantidad total solicitada (exploratoria)", "Materiales diferentes solicitados",
                  "Líneas de detalle", "Materiales por pedido (promedio)",
                  "Cantidad por línea (promedio)", "Cantidad por línea (mediana)"],
    "valor": [total_pedidos, clientes_registrados, clientes_con_pedidos, cantidad_total, materiales_distintos,
              lineas_de_pedido, materiales_por_pedido, cantidad_media_linea, cantidad_mediana_linea]})


# -----------------------------------------------------------------------------
# 5. DEMANDA POR CATEGORÍA
# -----------------------------------------------------------------------------
demanda_categoria = detalle.groupby("categoria").agg(
    cantidad_solicitada=("cantidad", "sum"),
    pedidos=("pedido_id", "nunique"),
    lineas_de_pedido=("pedido_id", "size"),
    materiales_distintos=("material_id", "nunique")).reset_index()
demanda_categoria["porcentaje"] = np.round(100 * demanda_categoria["cantidad_solicitada"] / demanda_categoria["cantidad_solicitada"].sum(), 1)
demanda_categoria = demanda_categoria.sort_values("cantidad_solicitada", ascending=False).reset_index(drop=True)

print("\n" + "=" * 78)
print("DEMANDA POR CATEGORÍA (suma de cantidades solicitadas)")
print("=" * 78)
print(demanda_categoria.to_string(index=False))


# -----------------------------------------------------------------------------
# 6. DEMANDA POR MATERIAL Y RANKING
# Se parte de los 100 materiales para que los que nadie pidió aparezcan con 0.
# -----------------------------------------------------------------------------
suma_por_material = detalle.groupby("material_id").agg(
    cantidad_solicitada=("cantidad", "sum"),
    pedidos=("pedido_id", "nunique")).reset_index()
demanda_material = materiales[["id_material", "nombre", "categoria", "unidad"]].merge(
    suma_por_material, left_on="id_material", right_on="material_id", how="left").drop(columns="material_id")
demanda_material["cantidad_solicitada"] = demanda_material["cantidad_solicitada"].fillna(0).astype(int)
demanda_material["pedidos"] = demanda_material["pedidos"].fillna(0).astype(int)
demanda_material = demanda_material.sort_values(["cantidad_solicitada", "id_material"], ascending=[False, True]).reset_index(drop=True)
demanda_material.insert(0, "ranking", np.arange(1, len(demanda_material) + 1))

materiales_sin_demanda = int((demanda_material["cantidad_solicitada"] == 0).sum())

print("\n" + "=" * 78)
print("RANKING: LOS " + str(TOP_MATERIALES) + " MATERIALES MÁS SOLICITADOS")
print("=" * 78)
print(demanda_material.head(TOP_MATERIALES).to_string(index=False))
print("\n  Materiales sin ninguna solicitud: " + str(materiales_sin_demanda))
print("  (La cantidad solicitada de cada uno de los 100 materiales se exporta a CSV.)")


# -----------------------------------------------------------------------------
# 7. PEDIDOS POR CLIENTE
# Se parte de clientes.csv para que los clientes sin pedidos aparezcan con 0.
# -----------------------------------------------------------------------------
pedidos_cliente = pedidos_analisis.groupby("cliente_id").agg(cantidad_pedidos=("id", "nunique")).reset_index()
cantidad_cliente = detalle.groupby("cliente_id").agg(cantidad_solicitada=("cantidad", "sum")).reset_index()

pedidos_por_cliente = clientes[["id", "nombre"]].rename(columns={"id": "cliente_id"})
pedidos_por_cliente = pedidos_por_cliente.merge(pedidos_cliente, on="cliente_id", how="left")
pedidos_por_cliente = pedidos_por_cliente.merge(cantidad_cliente, on="cliente_id", how="left")
pedidos_por_cliente["cantidad_pedidos"] = pedidos_por_cliente["cantidad_pedidos"].fillna(0).astype(int)
pedidos_por_cliente["cantidad_solicitada"] = pedidos_por_cliente["cantidad_solicitada"].fillna(0).astype(int)
pedidos_por_cliente["porcentaje_pedidos"] = np.round(100 * pedidos_por_cliente["cantidad_pedidos"] / total_pedidos, 1)
pedidos_por_cliente = pedidos_por_cliente.sort_values(["cantidad_pedidos", "cantidad_solicitada"], ascending=[False, False]).reset_index(drop=True)

# Concentración: qué porcentaje de los pedidos hacen los 5 clientes que más compran
top5_clientes = np.round(pedidos_por_cliente["porcentaje_pedidos"].head(5).sum(), 1)

print("\n" + "=" * 78)
print("PEDIDOS POR CLIENTE")
print("=" * 78)
print(pedidos_por_cliente.to_string(index=False))
print("\n  Los 5 clientes con más pedidos concentran el " + str(top5_clientes) + " % de los pedidos.")
print("  Pedidos por cliente activo: promedio " + str(np.round(total_pedidos / clientes_con_pedidos, 1))
      + " | máximo " + str(pedidos_por_cliente["cantidad_pedidos"].max()))


# -----------------------------------------------------------------------------
# 8. ANÁLISIS COMPLEMENTARIO: DEMANDA POR UNIDAD DE MEDIDA
# Sumar kg con litros o metros no tiene sentido físico. Acá se suma solo dentro
# de cada unidad, así la comparación sí es válida.
# -----------------------------------------------------------------------------
demanda_unidad = detalle.groupby("unidad").agg(
    cantidad_solicitada=("cantidad", "sum"),
    materiales_distintos=("material_id", "nunique"),
    lineas_de_pedido=("pedido_id", "size")).reset_index()
demanda_categoria_unidad = detalle.groupby(["unidad", "categoria"]).agg(
    cantidad_solicitada=("cantidad", "sum"),
    materiales_distintos=("material_id", "nunique")).reset_index()

print("\n" + "=" * 78)
print("DEMANDA POR UNIDAD DE MEDIDA (comparación físicamente válida)")
print("=" * 78)
print(demanda_unidad.to_string(index=False))
print("\nDetalle por unidad y categoría:")
print(demanda_categoria_unidad.to_string(index=False))


# -----------------------------------------------------------------------------
# 9. COMPORTAMIENTO DE LOS PEDIDOS DE SALIDA
# Se usan TODOS los pedidos, para ver cómo se reparten entre estados.
# -----------------------------------------------------------------------------
items_con_estado = items.merge(pedidos[["id", "estado"]], left_on="pedido_id", right_on="id", how="inner")
pedidos_por_estado = pd.DataFrame({"estado": ESTADOS_VALIDOS})
conteo_estado = pedidos.groupby("estado").agg(pedidos=("id", "size")).reset_index()
cantidad_estado = items_con_estado.groupby("estado").agg(cantidad_solicitada=("cantidad", "sum")).reset_index()
pedidos_por_estado = pedidos_por_estado.merge(conteo_estado, on="estado", how="left").merge(cantidad_estado, on="estado", how="left")
pedidos_por_estado = pedidos_por_estado.fillna(0)
pedidos_por_estado["pedidos"] = pedidos_por_estado["pedidos"].astype(int)
pedidos_por_estado["cantidad_solicitada"] = pedidos_por_estado["cantidad_solicitada"].astype(int)
pedidos_por_estado["porcentaje_pedidos"] = np.round(100 * pedidos_por_estado["pedidos"] / len(pedidos), 1)

# Diferencia entre lo solicitado, lo despachado y lo entregado.
# El sistema guarda la cantidad solicitada por línea, no una cantidad despachada
# aparte. Por eso "despachada" y "entregada" se aproximan con la cantidad de los
# pedidos que llegaron a esos estados (suponiendo que se envían completos).
cantidad_solicitada_total = int(items_con_estado["cantidad"].sum())
cantidad_despachada = int(items_con_estado.loc[items_con_estado["estado"].isin(["Despachado", "Entregado"]), "cantidad"].sum())
cantidad_entregada = int(items_con_estado.loc[items_con_estado["estado"] == "Entregado", "cantidad"].sum())

pedidos["mes"] = fecha_pedido.dt.to_period("M").astype(str)
pedidos_por_mes = pedidos.groupby("mes").agg(pedidos=("id", "size")).reset_index()

print("\n" + "=" * 78)
print("COMPORTAMIENTO DE LOS PEDIDOS DE SALIDA (todos los pedidos)")
print("=" * 78)
print(pedidos_por_estado.to_string(index=False))
print("\n  Cantidad SOLICITADA (todos los pedidos) ............ " + str(cantidad_solicitada_total))
print("  En pedidos Despachados o Entregados (aprox. despachada) " + str(cantidad_despachada)
      + "  (" + str(np.round(100 * cantidad_despachada / cantidad_solicitada_total, 1)) + " %)")
print("  En pedidos Entregados (aprox. entregada) ............ " + str(cantidad_entregada)
      + "  (" + str(np.round(100 * cantidad_entregada / cantidad_solicitada_total, 1)) + " %)")
print("  La DEMANDA se mide siempre con la cantidad solicitada.")
print("\nPedidos por mes:")
print(pedidos_por_mes.to_string(index=False))


# -----------------------------------------------------------------------------
# 10. EXPORTACIÓN DE RESÚMENES A CSV
# utf-8-sig para que Excel muestre bien las tildes
# -----------------------------------------------------------------------------
indicadores.to_csv(os.path.join(CARPETA, "resumen_indicadores_generales" + SUFIJO + ".csv"), index=False, encoding="utf-8-sig")
demanda_categoria.to_csv(os.path.join(CARPETA, "resumen_demanda_por_categoria" + SUFIJO + ".csv"), index=False, encoding="utf-8-sig")
demanda_material.to_csv(os.path.join(CARPETA, "resumen_demanda_por_material" + SUFIJO + ".csv"), index=False, encoding="utf-8-sig")
pedidos_por_cliente.to_csv(os.path.join(CARPETA, "resumen_pedidos_por_cliente" + SUFIJO + ".csv"), index=False, encoding="utf-8-sig")
demanda_categoria_unidad.to_csv(os.path.join(CARPETA, "resumen_demanda_por_unidad_y_categoria" + SUFIJO + ".csv"), index=False, encoding="utf-8-sig")
pedidos_por_estado.to_csv(os.path.join(CARPETA, "resumen_pedidos_por_estado.csv"), index=False, encoding="utf-8-sig")
pedidos_por_mes.to_csv(os.path.join(CARPETA, "resumen_pedidos_por_mes.csv"), index=False, encoding="utf-8-sig")
print("\nResúmenes exportados a CSV en: " + CARPETA)


# -----------------------------------------------------------------------------
# 11. GRÁFICO 1: TREEMAP DE DEMANDA POR CATEGORÍA
# El área de cada rectángulo es proporcional a la cantidad solicitada.
# -----------------------------------------------------------------------------
ANCHO = 100
ALTO = 60
valores = demanda_categoria["cantidad_solicitada"].tolist()      # ya ordenados de mayor a menor
rectangulos = squarify.squarify(squarify.normalize_sizes(valores, ANCHO, ALTO), 0, 0, ANCHO, ALTO)

fig1, ax1 = plt.subplots(figsize=(12, 7.2))
i = 0
while i < len(rectangulos):
    r = rectangulos[i]
    fila = demanda_categoria.iloc[i]
    categoria = fila["categoria"]
    # Rectángulo con borde blanco para separar las categorías
    ax1.add_patch(plt.Rectangle((r["x"], r["y"]), r["dx"], r["dy"],
                                facecolor=COLORES[categoria], edgecolor="white", linewidth=4))
    centro_x = r["x"] + r["dx"] / 2
    centro_y = r["y"] + r["dy"] / 2
    ax1.text(centro_x, centro_y + 1.2, categoria, ha="center", va="bottom",
             fontsize=17, fontweight="bold", color=COLOR_TEXTO)
    # Si el rectángulo es angosto, pedidos y materiales van en renglones separados
    separador = "  ·  "
    if r["dx"] < 30:
        separador = "\n"
    detalle_texto = ("Demanda: " + str(int(fila["cantidad_solicitada"])) + "  (" + str(fila["porcentaje"]) + " %)\n"
                     + str(int(fila["pedidos"])) + " pedidos" + separador + str(int(fila["materiales_distintos"])) + " materiales")
    ax1.text(centro_x, centro_y + 0.6, detalle_texto, ha="center", va="top",
             fontsize=11.5, color=COLOR_TEXTO, linespacing=1.5)
    i = i + 1

ax1.set_xlim(0, ANCHO)
ax1.set_ylim(0, ALTO)
ax1.axis("off")
ax1.set_title("Demanda de los clientes por categoría de material", loc="left",
              fontsize=16, fontweight="bold", pad=30)
ax1.text(0, 1.02, "Área proporcional a la cantidad solicitada (suma de pedidos_items.cantidad)  ·  "
         + str(total_pedidos) + " pedidos  ·  " + DESCRIPCION_CRITERIO,
         transform=ax1.transAxes, fontsize=10, color=COLOR_TEXTO_2)
fig1.text(0.125, 0.06, "Advertencia: se suman cantidades expresadas en unidad, kg, litro y metro. El tamaño es un "
          "indicador exploratorio,\nno una comparación de magnitudes físicamente equivalentes "
          "(ver gráfico complementario por unidad de medida).",
          fontsize=9, color=COLOR_TEXTO_2, style="italic")
fig1.savefig(os.path.join(CARPETA, "grafico1_treemap_demanda_por_categoria" + SUFIJO + ".png"),
             dpi=200, bbox_inches="tight", facecolor="white")


# -----------------------------------------------------------------------------
# 12. GRÁFICO 2: GRÁFICO DE PUNTOS DE LOS MATERIALES MÁS SOLICITADOS
# Cada punto es un material. Color y forma indican la categoría.
# -----------------------------------------------------------------------------
top = demanda_material[demanda_material["cantidad_solicitada"] > 0].head(TOP_MATERIALES).reset_index(drop=True)
cantidad_top = len(top)
posiciones = np.arange(cantidad_top)[::-1]          # el puesto 1 queda arriba
maximo = top["cantidad_solicitada"].max()

fig2, ax2 = plt.subplots(figsize=(12, 7.8))
etiquetas_y = []
categorias_presentes = []
i = 0
while i < cantidad_top:
    fila = top.iloc[i]
    categoria = fila["categoria"]
    y = posiciones[i]
    # Línea guía suave desde 0 hasta el punto
    ax2.hlines(y, 0, fila["cantidad_solicitada"], color=COLOR_GRILLA, linewidth=1.5, zorder=1)
    # El punto del material
    ax2.scatter(fila["cantidad_solicitada"], y, s=120, marker=MARCADORES[categoria],
                color=COLORES[categoria], edgecolor="white", linewidth=1.5, zorder=3)
    # Etiqueta con la cantidad y la unidad del material
    ax2.text(fila["cantidad_solicitada"] + maximo * 0.015, y,
             str(int(fila["cantidad_solicitada"])) + " " + ABREVIATURA[fila["unidad"]],
             va="center", fontsize=9.5, color=COLOR_TEXTO_2)
    etiquetas_y.append(str(int(fila["ranking"])) + ".  " + fila["nombre"])
    if categoria not in categorias_presentes:
        categorias_presentes.append(categoria)
    i = i + 1

ax2.set_yticks(posiciones)
ax2.set_yticklabels(etiquetas_y)
ax2.set_xlim(0, maximo * 1.15)
ax2.set_ylim(-0.7, cantidad_top - 0.3)
ax2.spines["left"].set_visible(False)
ax2.tick_params(axis="y", length=0)
ax2.grid(axis="x", color=COLOR_GRILLA, linewidth=0.8)
ax2.set_axisbelow(True)
ax2.set_xlabel("Cantidad solicitada (en la unidad de cada material: u. = unidades, kg, L = litros, m = metros)")
ax2.set_ylabel("Material (puesto en el ranking)")
ax2.set_title("Los " + str(cantidad_top) + " materiales más solicitados por los clientes",
              loc="left", fontsize=16, fontweight="bold", pad=30)
ax2.text(0, 1.02, "Suma de pedidos_items.cantidad por material  ·  " + DESCRIPCION_CRITERIO,
         transform=ax2.transAxes, fontsize=10, color=COLOR_TEXTO_2)

# Leyenda en el orden fijo de las categorías (solo las que aparecen en el top)
manejadores = []
i = 0
while i < len(CATEGORIAS):
    categoria = CATEGORIAS[i]
    if categoria in categorias_presentes:
        manejadores.append(Line2D([0], [0], marker=MARCADORES[categoria], color="white",
                                  markerfacecolor=COLORES[categoria], markersize=10, label=categoria))
    i = i + 1
ax2.legend(handles=manejadores, title="Categoría", loc="lower right", frameon=False)
fig2.text(0.125, 0.0, "Nota: comparar cantidades entre materiales de distinta unidad es solo orientativo.",
          fontsize=9, color=COLOR_TEXTO_2, style="italic")
fig2.savefig(os.path.join(CARPETA, "grafico2_puntos_materiales_mas_solicitados" + SUFIJO + ".png"),
             dpi=200, bbox_inches="tight", facecolor="white")


# -----------------------------------------------------------------------------
# 13. GRÁFICO 3 (COMPLEMENTARIO): DEMANDA POR UNIDAD DE MEDIDA Y CATEGORÍA
# Un panel por unidad: dentro de cada panel las cantidades sí son comparables.
# -----------------------------------------------------------------------------
fig3, ejes = plt.subplots(2, 2, figsize=(12, 7.5))
ejes = ejes.flatten()
u = 0
while u < len(UNIDADES):
    unidad = UNIDADES[u]
    ax = ejes[u]
    datos_unidad = demanda_categoria_unidad[demanda_categoria_unidad["unidad"] == unidad]
    nombres_barras = []
    valores_barras = []
    colores_barras = []
    # Se recorren las categorías en el orden fijo y se toman solo las que usan esta unidad
    c = 0
    while c < len(CATEGORIAS):
        fila_categoria = datos_unidad[datos_unidad["categoria"] == CATEGORIAS[c]]
        if len(fila_categoria) > 0:
            nombres_barras.append(CATEGORIAS[c])
            valores_barras.append(int(fila_categoria["cantidad_solicitada"].iloc[0]))
            colores_barras.append(COLORES[CATEGORIAS[c]])
        c = c + 1
    # Las barras se centran verticalmente (hay paneles con 1, 2 o 3 categorías)
    posiciones_barras = np.arange(len(nombres_barras))[::-1] + (3 - len(nombres_barras)) / 2
    ax.barh(posiciones_barras, valores_barras, height=0.55, color=colores_barras)
    ax.set_yticks(posiciones_barras)
    ax.set_yticklabels(nombres_barras)
    ax.set_ylim(-0.6, 2.6)          # misma escala vertical: todas las barras tienen el mismo grosor
    tope = 1
    if len(valores_barras) > 0:
        tope = max(valores_barras)
    ax.set_xlim(0, tope * 1.25)
    b = 0
    while b < len(valores_barras):
        ax.text(valores_barras[b] + tope * 0.02, posiciones_barras[b], str(valores_barras[b]) + " " + ABREVIATURA[unidad],
                va="center", fontsize=10, color=COLOR_TEXTO_2)
        b = b + 1
    total_unidad = sum(valores_barras)
    ax.set_title("Unidad: " + unidad + "   (total " + str(total_unidad) + " " + ABREVIATURA[unidad] + ")",
                 loc="left", fontsize=12, fontweight="bold")
    ax.set_xlabel("Cantidad solicitada (" + unidad + ")")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=COLOR_GRILLA, linewidth=0.8)
    ax.set_axisbelow(True)
    u = u + 1

fig3.suptitle("Demanda por unidad de medida y categoría (comparación válida dentro de cada panel)",
              x=0.01, ha="left", fontsize=15, fontweight="bold")
fig3.tight_layout()
fig3.savefig(os.path.join(CARPETA, "grafico3_demanda_por_unidad_y_categoria" + SUFIJO + ".png"),
             dpi=200, bbox_inches="tight", facecolor="white")

print("Gráficos guardados como PNG en: " + CARPETA)

if MOSTRAR_GRAFICOS:
    plt.show()
else:
    plt.close("all")
