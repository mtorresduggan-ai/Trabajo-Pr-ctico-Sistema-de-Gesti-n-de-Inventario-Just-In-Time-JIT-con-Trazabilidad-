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
# Bibliotecas necesarias: numpy y matplotlib (sin pandas)
#   pip install numpy matplotlib
# =============================================================================

import os
import csv
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


# -----------------------------------------------------------------------------
# 0. CONFIGURACIÓN
# -----------------------------------------------------------------------------

# Carpeta datos_inventario_jit, que está al lado de este script. Ahí se buscan
# los CSV y se guardan los resultados, sin importar desde dónde se ejecute.
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
# Al guardar desde la ventana del gráfico (botón del disquete), recortar los bordes
# para que no quede nada afuera, igual que en los PNG que guarda el script
plt.rcParams["savefig.bbox"] = "tight"


# -----------------------------------------------------------------------------
# FUNCIONES AUXILIARES
# -----------------------------------------------------------------------------

def leer_csv(nombre):
    # Devuelve los nombres de las columnas y una lista de diccionarios (una fila cada uno)
    with open(os.path.join(CARPETA, nombre), "r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        filas = list(lector)
        return lector.fieldnames, filas


def guardar_csv(nombre, encabezados, filas):
    # utf-8-sig para que Excel muestre bien las tildes
    with open(os.path.join(CARPETA, nombre), "w", encoding="utf-8-sig", newline="") as archivo:
        escritor = csv.writer(archivo, lineterminator="\n")
        escritor.writerow(encabezados)
        escritor.writerows(filas)


def convertir_numero(texto):
    # "12" -> 12, "12.5" -> 12.5, cualquier otra cosa -> None
    try:
        return int(texto)
    except ValueError:
        try:
            return float(texto)
        except ValueError:
            return None


def convertir_fecha(texto):
    # "2026-03-02" -> date(2026, 3, 2); vacía o inválida -> None
    if texto is None or texto.strip() == "":
        return None
    try:
        return date.fromisoformat(texto.strip())
    except ValueError:
        return None


def contar_repetidos(valores):
    # Cuántos valores sobran porque ya aparecieron antes (igual que duplicated().sum())
    return len(valores) - len(set(valores))


def imprimir_tabla(encabezados, filas):
    # Imprime una tabla con las columnas alineadas a la derecha
    anchos = []
    c = 0
    while c < len(encabezados):
        ancho = len(encabezados[c])
        for fila in filas:
            ancho = max(ancho, len(str(fila[c])))
        anchos.append(ancho)
        c = c + 1
    print("  ".join(str(encabezados[c]).rjust(anchos[c]) for c in range(len(encabezados))))
    for fila in filas:
        print("  ".join(str(fila[c]).rjust(anchos[c]) for c in range(len(encabezados))))


# -----------------------------------------------------------------------------
# 1. LECTURA DE LOS ARCHIVOS CSV
# Cada archivo queda como una lista de diccionarios {columna: valor (texto)}
# -----------------------------------------------------------------------------
columnas_materiales, materiales = leer_csv("materiales.csv")
columnas_pedidos, pedidos = leer_csv("pedidos.csv")
columnas_items, items = leer_csv("pedidos_items.csv")
columnas_clientes, clientes = leer_csv("clientes.csv")
columnas_empleados, empleados = leer_csv("empleados.csv")

# Diccionarios id -> fila, para unir las tablas sin recorrerlas cada vez
materiales_por_id = {m["id_material"]: m for m in materiales}
pedidos_por_id = {p["id"]: p for p in pedidos}


# -----------------------------------------------------------------------------
# 2. VALIDACIONES DE LOS DATOS
# Cada control guarda una descripción y la cantidad de problemas encontrados.
# Un 0 significa que el control está OK.
# -----------------------------------------------------------------------------
controles = []
problemas = []

# 2.1 Nombres de columnas (deben coincidir exactamente con el sistema)
controles.append("Columnas de materiales.csv")
problemas.append(int(columnas_materiales != ["id_material", "nombre", "unidad", "umbral_reabastecimiento", "categoria"]))
controles.append("Columnas de pedidos.csv")
problemas.append(int(columnas_pedidos != ["id", "fecha", "cliente_id", "estado", "vendedor_id", "fecha_aceptacion", "fecha_envio"]))
controles.append("Columnas de pedidos_items.csv")
problemas.append(int(columnas_items != ["pedido_id", "material_id", "cantidad", "precio_unitario"]))
controles.append("Columnas de clientes.csv")
problemas.append(int(columnas_clientes != ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja"]))
controles.append("Columnas de empleados.csv")
problemas.append(int(columnas_empleados != ["id", "nombre", "telefono", "dni", "email", "fecha_alta", "fecha_baja", "usuario", "clave", "tipo"]))

# 2.2 Identificadores repetidos
ids_clientes = [c["id"] for c in clientes]
ids_empleados = [e["id"] for e in empleados]

controles.append("IDs de materiales repetidos")
problemas.append(contar_repetidos([m["id_material"] for m in materiales]))
controles.append("IDs de pedidos repetidos")
problemas.append(contar_repetidos([p["id"] for p in pedidos]))
controles.append("IDs de clientes y empleados superpuestos (contador compartido de Individuo)")
problemas.append(sum(1 for i in ids_clientes if i in set(ids_empleados))
                 + contar_repetidos(ids_clientes) + contar_repetidos(ids_empleados))

# 2.3 Referencias entre archivos
ids_vendedores = set(e["id"] for e in empleados if e["tipo"] == "Vendedor")
pedidos_con_detalle = set(item["pedido_id"] for item in items)

controles.append("Materiales de pedidos_items que no existen en materiales.csv")
problemas.append(sum(1 for item in items if item["material_id"] not in materiales_por_id))
controles.append("Detalles que apuntan a un pedido inexistente")
problemas.append(sum(1 for item in items if item["pedido_id"] not in pedidos_por_id))
controles.append("Pedidos con cliente inexistente en clientes.csv")
problemas.append(sum(1 for p in pedidos if p["cliente_id"] not in set(ids_clientes)))
controles.append("Pedidos con vendedor inexistente (o que no es de tipo Vendedor)")
problemas.append(sum(1 for p in pedidos if p["vendedor_id"] not in ids_vendedores))
controles.append("Pedidos sin ningún detalle en pedidos_items.csv")
problemas.append(sum(1 for p in pedidos if p["id"] not in pedidos_con_detalle))

# 2.4 Cantidades: deben ser numéricas y positivas
for item in items:
    item["cantidad"] = convertir_numero(item["cantidad"])

controles.append("Cantidades no numéricas")
problemas.append(sum(1 for item in items if item["cantidad"] is None))
controles.append("Cantidades menores o iguales a cero")
problemas.append(sum(1 for item in items if item["cantidad"] is not None and item["cantidad"] <= 0))

# 2.5 Estados válidos
controles.append("Pedidos con estado inválido")
problemas.append(sum(1 for p in pedidos if p["estado"] not in ESTADOS_VALIDOS))

# 2.6 Fechas válidas y coherentes (las fechas vacías quedan como None y no cuentan como error)
aceptacion_invalida = 0
envio_invalido = 0
aceptacion_antes_pedido = 0
envio_antes_pedido = 0
envio_antes_aceptacion = 0

for p in pedidos:
    p["fecha_dt"] = convertir_fecha(p["fecha"])
    p["fecha_aceptacion_dt"] = convertir_fecha(p["fecha_aceptacion"])
    p["fecha_envio_dt"] = convertir_fecha(p["fecha_envio"])

    if p["fecha_aceptacion"] != "" and p["fecha_aceptacion_dt"] is None:
        aceptacion_invalida += 1
    if p["fecha_envio"] != "" and p["fecha_envio_dt"] is None:
        envio_invalido += 1
    if p["fecha_dt"] and p["fecha_aceptacion_dt"] and p["fecha_aceptacion_dt"] < p["fecha_dt"]:
        aceptacion_antes_pedido += 1
    if p["fecha_dt"] and p["fecha_envio_dt"] and p["fecha_envio_dt"] < p["fecha_dt"]:
        envio_antes_pedido += 1
    if p["fecha_aceptacion_dt"] and p["fecha_envio_dt"] and p["fecha_envio_dt"] < p["fecha_aceptacion_dt"]:
        envio_antes_aceptacion += 1

controles.append("Fechas de pedido vacías o inválidas")
problemas.append(sum(1 for p in pedidos if p["fecha_dt"] is None))
controles.append("Fechas de aceptación/envío escritas pero inválidas")
problemas.append(aceptacion_invalida + envio_invalido)
controles.append("Aceptación anterior a la fecha del pedido")
problemas.append(aceptacion_antes_pedido)
controles.append("Envío anterior a la fecha del pedido")
problemas.append(envio_antes_pedido)
controles.append("Envío anterior a la aceptación")
problemas.append(envio_antes_aceptacion)

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
pedidos_analisis = [p for p in pedidos if p["estado"] not in ESTADOS_EXCLUIDOS]
ids_pedidos_analisis = set(p["id"] for p in pedidos_analisis)

detalle = []
for item in items:
    if item["pedido_id"] not in ids_pedidos_analisis:
        continue
    pedido = pedidos_por_id[item["pedido_id"]]
    material = materiales_por_id.get(item["material_id"], {})
    detalle.append({
        "pedido_id": item["pedido_id"],
        "material_id": item["material_id"],
        "cantidad": item["cantidad"],
        "fecha": pedido["fecha"],
        "cliente_id": pedido["cliente_id"],
        "estado": pedido["estado"],
        "nombre": material.get("nombre"),
        "unidad": material.get("unidad"),
        "categoria": material.get("categoria")})


# -----------------------------------------------------------------------------
# 4. INDICADORES GENERALES
# -----------------------------------------------------------------------------
total_pedidos = len(ids_pedidos_analisis)
clientes_registrados = len(clientes)
clientes_con_pedidos = len(set(p["cliente_id"] for p in pedidos_analisis))
cantidades_detalle = [d["cantidad"] for d in detalle]
cantidad_total = sum(cantidades_detalle)
materiales_distintos = len(set(d["material_id"] for d in detalle))
lineas_de_pedido = len(detalle)
materiales_por_pedido = float(np.round(lineas_de_pedido / total_pedidos, 2))
cantidad_media_linea = float(np.round(np.mean(cantidades_detalle), 1))
cantidad_mediana_linea = float(np.median(cantidades_detalle))

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

indicadores = [
    ["Pedidos registrados analizados", total_pedidos],
    ["Clientes registrados", clientes_registrados],
    ["Clientes que realizaron pedidos", clientes_con_pedidos],
    ["Cantidad total solicitada (exploratoria)", cantidad_total],
    ["Materiales diferentes solicitados", materiales_distintos],
    ["Líneas de detalle", lineas_de_pedido],
    ["Materiales por pedido (promedio)", materiales_por_pedido],
    ["Cantidad por línea (promedio)", cantidad_media_linea],
    ["Cantidad por línea (mediana)", cantidad_mediana_linea]]


# -----------------------------------------------------------------------------
# 5. DEMANDA POR CATEGORÍA
# Diccionario categoría -> acumuladores. Los conjuntos cuentan pedidos y
# materiales distintos (un mismo pedido o material se cuenta una sola vez).
# -----------------------------------------------------------------------------
acumulado_categoria = {}
for d in detalle:
    categoria = d["categoria"]
    if categoria not in acumulado_categoria:
        acumulado_categoria[categoria] = {"cantidad": 0, "pedidos": set(), "lineas": 0, "materiales": set()}
    acumulado_categoria[categoria]["cantidad"] += d["cantidad"]
    acumulado_categoria[categoria]["pedidos"].add(d["pedido_id"])
    acumulado_categoria[categoria]["lineas"] += 1
    acumulado_categoria[categoria]["materiales"].add(d["material_id"])

suma_categorias = sum(a["cantidad"] for a in acumulado_categoria.values())

demanda_categoria = []
for categoria, a in acumulado_categoria.items():
    demanda_categoria.append({
        "categoria": categoria,
        "cantidad_solicitada": a["cantidad"],
        "pedidos": len(a["pedidos"]),
        "lineas_de_pedido": a["lineas"],
        "materiales_distintos": len(a["materiales"]),
        "porcentaje": float(np.round(100 * a["cantidad"] / suma_categorias, 1))})

demanda_categoria = sorted(demanda_categoria, key=lambda f: f["cantidad_solicitada"], reverse=True)

columnas_categoria = ["categoria", "cantidad_solicitada", "pedidos", "lineas_de_pedido", "materiales_distintos", "porcentaje"]

print("\n" + "=" * 78)
print("DEMANDA POR CATEGORÍA (suma de cantidades solicitadas)")
print("=" * 78)
imprimir_tabla(columnas_categoria, [[f[c] for c in columnas_categoria] for f in demanda_categoria])


# -----------------------------------------------------------------------------
# 6. DEMANDA POR MATERIAL Y RANKING
# Se parte de los 100 materiales para que los que nadie pidió aparezcan con 0.
# -----------------------------------------------------------------------------
cantidad_por_material = {}
pedidos_por_material = {}
for d in detalle:
    cantidad_por_material[d["material_id"]] = cantidad_por_material.get(d["material_id"], 0) + d["cantidad"]
    pedidos_por_material.setdefault(d["material_id"], set()).add(d["pedido_id"])

demanda_material = []
for m in materiales:
    demanda_material.append({
        "id_material": m["id_material"],
        "nombre": m["nombre"],
        "categoria": m["categoria"],
        "unidad": m["unidad"],
        "cantidad_solicitada": int(cantidad_por_material.get(m["id_material"], 0)),
        "pedidos": len(pedidos_por_material.get(m["id_material"], set()))})

# Mayor cantidad primero; si empatan, por id de material
demanda_material = sorted(demanda_material, key=lambda f: (-f["cantidad_solicitada"], f["id_material"]))

ranking = 1
for fila in demanda_material:
    fila["ranking"] = ranking
    ranking = ranking + 1

materiales_sin_demanda = sum(1 for f in demanda_material if f["cantidad_solicitada"] == 0)

columnas_material = ["ranking", "id_material", "nombre", "categoria", "unidad", "cantidad_solicitada", "pedidos"]

print("\n" + "=" * 78)
print("RANKING: LOS " + str(TOP_MATERIALES) + " MATERIALES MÁS SOLICITADOS")
print("=" * 78)
imprimir_tabla(columnas_material, [[f[c] for c in columnas_material] for f in demanda_material[:TOP_MATERIALES]])
print("\n  Materiales sin ninguna solicitud: " + str(materiales_sin_demanda))
print("  (La cantidad solicitada de cada uno de los 100 materiales se exporta a CSV.)")


# -----------------------------------------------------------------------------
# 7. PEDIDOS POR CLIENTE
# Se parte de clientes.csv para que los clientes sin pedidos aparezcan con 0.
# -----------------------------------------------------------------------------
pedidos_de_cliente = {}
for p in pedidos_analisis:
    pedidos_de_cliente.setdefault(p["cliente_id"], set()).add(p["id"])

cantidad_de_cliente = {}
for d in detalle:
    cantidad_de_cliente[d["cliente_id"]] = cantidad_de_cliente.get(d["cliente_id"], 0) + d["cantidad"]

pedidos_por_cliente = []
for c in clientes:
    cantidad_pedidos = len(pedidos_de_cliente.get(c["id"], set()))
    pedidos_por_cliente.append({
        "cliente_id": c["id"],
        "nombre": c["nombre"],
        "cantidad_pedidos": cantidad_pedidos,
        "cantidad_solicitada": int(cantidad_de_cliente.get(c["id"], 0)),
        "porcentaje_pedidos": float(np.round(100 * cantidad_pedidos / total_pedidos, 1))})

# Más pedidos primero; si empatan, más cantidad solicitada
pedidos_por_cliente = sorted(pedidos_por_cliente,
                             key=lambda f: (-f["cantidad_pedidos"], -f["cantidad_solicitada"]))

# Concentración: qué porcentaje de los pedidos hacen los 5 clientes que más compran
top5_clientes = float(np.round(sum(f["porcentaje_pedidos"] for f in pedidos_por_cliente[:5]), 1))

columnas_cliente = ["cliente_id", "nombre", "cantidad_pedidos", "cantidad_solicitada", "porcentaje_pedidos"]

print("\n" + "=" * 78)
print("PEDIDOS POR CLIENTE")
print("=" * 78)
imprimir_tabla(columnas_cliente, [[f[c] for c in columnas_cliente] for f in pedidos_por_cliente])
print("\n  Los 5 clientes con más pedidos concentran el " + str(top5_clientes) + " % de los pedidos.")
print("  Pedidos por cliente activo: promedio " + str(float(np.round(total_pedidos / clientes_con_pedidos, 1)))
      + " | máximo " + str(max(f["cantidad_pedidos"] for f in pedidos_por_cliente)))


# -----------------------------------------------------------------------------
# 8. ANÁLISIS COMPLEMENTARIO: DEMANDA POR UNIDAD DE MEDIDA
# Sumar kg con litros o metros no tiene sentido físico. Acá se suma solo dentro
# de cada unidad, así la comparación sí es válida.
# -----------------------------------------------------------------------------
acumulado_unidad = {}
acumulado_unidad_categoria = {}
for d in detalle:
    if d["unidad"] not in acumulado_unidad:
        acumulado_unidad[d["unidad"]] = {"cantidad": 0, "materiales": set(), "lineas": 0}
    acumulado_unidad[d["unidad"]]["cantidad"] += d["cantidad"]
    acumulado_unidad[d["unidad"]]["materiales"].add(d["material_id"])
    acumulado_unidad[d["unidad"]]["lineas"] += 1

    clave = (d["unidad"], d["categoria"])        # tupla: unidad y categoría juntas
    if clave not in acumulado_unidad_categoria:
        acumulado_unidad_categoria[clave] = {"cantidad": 0, "materiales": set()}
    acumulado_unidad_categoria[clave]["cantidad"] += d["cantidad"]
    acumulado_unidad_categoria[clave]["materiales"].add(d["material_id"])

demanda_unidad = []
for unidad in sorted(acumulado_unidad):
    a = acumulado_unidad[unidad]
    demanda_unidad.append([unidad, a["cantidad"], len(a["materiales"]), a["lineas"]])

demanda_categoria_unidad = []
for unidad, categoria in sorted(acumulado_unidad_categoria):
    a = acumulado_unidad_categoria[(unidad, categoria)]
    demanda_categoria_unidad.append({
        "unidad": unidad,
        "categoria": categoria,
        "cantidad_solicitada": a["cantidad"],
        "materiales_distintos": len(a["materiales"])})

columnas_unidad_categoria = ["unidad", "categoria", "cantidad_solicitada", "materiales_distintos"]

print("\n" + "=" * 78)
print("DEMANDA POR UNIDAD DE MEDIDA (comparación físicamente válida)")
print("=" * 78)
imprimir_tabla(["unidad", "cantidad_solicitada", "materiales_distintos", "lineas_de_pedido"], demanda_unidad)
print("\nDetalle por unidad y categoría:")
imprimir_tabla(columnas_unidad_categoria, [[f[c] for c in columnas_unidad_categoria] for f in demanda_categoria_unidad])


# -----------------------------------------------------------------------------
# 9. COMPORTAMIENTO DE LOS PEDIDOS DE SALIDA
# Se usan TODOS los pedidos, para ver cómo se reparten entre estados.
# -----------------------------------------------------------------------------
# Cada línea de detalle con el estado de su pedido (solo las que tienen pedido)
items_con_estado = []
for item in items:
    if item["pedido_id"] in pedidos_por_id:
        items_con_estado.append({"cantidad": item["cantidad"], "estado": pedidos_por_id[item["pedido_id"]]["estado"]})

pedidos_por_estado = []
for estado in ESTADOS_VALIDOS:
    cantidad_pedidos_estado = sum(1 for p in pedidos if p["estado"] == estado)
    cantidad_estado = sum(i["cantidad"] for i in items_con_estado if i["estado"] == estado)
    pedidos_por_estado.append([estado, cantidad_pedidos_estado, int(cantidad_estado),
                               float(np.round(100 * cantidad_pedidos_estado / len(pedidos), 1))])

# Diferencia entre lo solicitado, lo despachado y lo entregado.
# El sistema guarda la cantidad solicitada por línea, no una cantidad despachada
# aparte. Por eso "despachada" y "entregada" se aproximan con la cantidad de los
# pedidos que llegaron a esos estados (suponiendo que se envían completos).
cantidad_solicitada_total = int(sum(i["cantidad"] for i in items_con_estado))
cantidad_despachada = int(sum(i["cantidad"] for i in items_con_estado if i["estado"] in ["Despachado", "Entregado"]))
cantidad_entregada = int(sum(i["cantidad"] for i in items_con_estado if i["estado"] == "Entregado"))

# Pedidos por mes: el mes es "AAAA-MM", sacado de la fecha del pedido
conteo_mes = {}
for p in pedidos:
    if p["fecha_dt"] is not None:
        mes = str(p["fecha_dt"].year) + "-" + str(p["fecha_dt"].month).zfill(2)
        conteo_mes[mes] = conteo_mes.get(mes, 0) + 1
pedidos_por_mes = [[mes, conteo_mes[mes]] for mes in sorted(conteo_mes)]

print("\n" + "=" * 78)
print("COMPORTAMIENTO DE LOS PEDIDOS DE SALIDA (todos los pedidos)")
print("=" * 78)
imprimir_tabla(["estado", "pedidos", "cantidad_solicitada", "porcentaje_pedidos"], pedidos_por_estado)
print("\n  Cantidad SOLICITADA (todos los pedidos) ............ " + str(cantidad_solicitada_total))
print("  En pedidos Despachados o Entregados (aprox. despachada) " + str(cantidad_despachada)
      + "  (" + str(float(np.round(100 * cantidad_despachada / cantidad_solicitada_total, 1))) + " %)")
print("  En pedidos Entregados (aprox. entregada) ............ " + str(cantidad_entregada)
      + "  (" + str(float(np.round(100 * cantidad_entregada / cantidad_solicitada_total, 1))) + " %)")
print("  La DEMANDA se mide siempre con la cantidad solicitada.")
print("\nPedidos por mes:")
imprimir_tabla(["mes", "pedidos"], pedidos_por_mes)


# -----------------------------------------------------------------------------
# 10. EXPORTACIÓN DE RESÚMENES A CSV
# -----------------------------------------------------------------------------
guardar_csv("resumen_indicadores_generales" + SUFIJO + ".csv", ["indicador", "valor"],
            [[nombre, float(valor)] for nombre, valor in indicadores])
guardar_csv("resumen_demanda_por_categoria" + SUFIJO + ".csv", columnas_categoria,
            [[f[c] for c in columnas_categoria] for f in demanda_categoria])
guardar_csv("resumen_demanda_por_material" + SUFIJO + ".csv", columnas_material,
            [[f[c] for c in columnas_material] for f in demanda_material])
guardar_csv("resumen_pedidos_por_cliente" + SUFIJO + ".csv", columnas_cliente,
            [[f[c] for c in columnas_cliente] for f in pedidos_por_cliente])
guardar_csv("resumen_demanda_por_unidad_y_categoria" + SUFIJO + ".csv", columnas_unidad_categoria,
            [[f[c] for c in columnas_unidad_categoria] for f in demanda_categoria_unidad])
guardar_csv("resumen_pedidos_por_estado.csv", ["estado", "pedidos", "cantidad_solicitada", "porcentaje_pedidos"],
            pedidos_por_estado)
guardar_csv("resumen_pedidos_por_mes.csv", ["mes", "pedidos"], pedidos_por_mes)
print("\nResúmenes exportados a CSV en: " + CARPETA)


# -----------------------------------------------------------------------------
# 11. GRÁFICO 1: TREEMAP DE DEMANDA POR CATEGORÍA
# El área de cada rectángulo es proporcional a la cantidad solicitada.
# Las posiciones se calculan con el algoritmo "squarified" (el mismo del
# análisis 3), que busca rectángulos lo más cuadrados posible.
# -----------------------------------------------------------------------------

def peor_proporcion(fila, lado):
    # La peor relación ancho/alto que tendría la fila si se ubica sobre ese lado
    if not fila or lado <= 0:
        return float("inf")
    suma = sum(fila)
    return max((lado ** 2 * max(fila)) / (suma ** 2), (suma ** 2) / (lado ** 2 * min(fila)))


def distribuir_fila(fila, x, y, ancho, alto):
    # Ubica una fila de áreas sobre el lado más corto y devuelve el espacio que queda
    rectangulos = []
    suma = sum(fila)
    if ancho >= alto:
        ancho_fila = suma / alto
        posicion_y = y
        for area in fila:
            rectangulos.append({"x": x, "y": posicion_y, "dx": ancho_fila, "dy": area / ancho_fila})
            posicion_y += area / ancho_fila
        return rectangulos, x + ancho_fila, y, ancho - ancho_fila, alto
    alto_fila = suma / ancho
    posicion_x = x
    for area in fila:
        rectangulos.append({"x": posicion_x, "y": y, "dx": area / alto_fila, "dy": alto_fila})
        posicion_x += area / alto_fila
    return rectangulos, x, y + alto_fila, ancho, alto - alto_fila


def calcular_treemap(valores, x, y, ancho, alto):
    # valores ordenados de mayor a menor -> un rectángulo por valor, en el mismo orden
    total = sum(valores)
    pendientes = [v * ancho * alto / total for v in valores]     # cada valor pasa a ser un área
    resultado = []
    while pendientes:
        fila = [pendientes.pop(0)]
        while pendientes and peor_proporcion(fila + [pendientes[0]], min(ancho, alto)) <= peor_proporcion(fila, min(ancho, alto)):
            fila.append(pendientes.pop(0))
        rectangulos, x, y, ancho, alto = distribuir_fila(fila, x, y, ancho, alto)
        resultado.extend(rectangulos)
    return resultado


ANCHO = 100
ALTO = 60
valores = [f["cantidad_solicitada"] for f in demanda_categoria]      # ya ordenados de mayor a menor
rectangulos = calcular_treemap(valores, 0, 0, ANCHO, ALTO)

fig1, ax1 = plt.subplots(figsize=(12, 7.2))
i = 0
while i < len(rectangulos):
    r = rectangulos[i]
    fila = demanda_categoria[i]
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
# Márgenes chicos para que el subtítulo y la advertencia entren completos en la ventana
fig1.subplots_adjust(left=0.03, right=0.97, top=0.86, bottom=0.13)
fig1.text(0.03, 0.04, "Advertencia: se suman cantidades expresadas en unidad, kg, litro y metro. El tamaño es un "
          "indicador exploratorio,\nno una comparación de magnitudes físicamente equivalentes "
          "(ver gráfico complementario por unidad de medida).",
          fontsize=9, color=COLOR_TEXTO_2, style="italic")
fig1.savefig(os.path.join(CARPETA, "grafico1_treemap_demanda_por_categoria" + SUFIJO + ".png"),
             dpi=200, bbox_inches="tight", facecolor="white")


# -----------------------------------------------------------------------------
# 12. GRÁFICO 2: GRÁFICO DE PUNTOS DE LOS MATERIALES MÁS SOLICITADOS
# Cada punto es un material. Color y forma indican la categoría.
# -----------------------------------------------------------------------------
top = [f for f in demanda_material if f["cantidad_solicitada"] > 0][:TOP_MATERIALES]
cantidad_top = len(top)
posiciones = np.arange(cantidad_top)[::-1]          # el puesto 1 queda arriba
maximo = max(f["cantidad_solicitada"] for f in top)

fig2, ax2 = plt.subplots(figsize=(12, 7.8))
etiquetas_y = []
categorias_presentes = []
i = 0
while i < cantidad_top:
    fila = top[i]
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
# Acomoda los márgenes para que entren los nombres largos de la izquierda,
# dejando lugar abajo para la nota
fig2.tight_layout(rect=[0, 0.04, 1, 1])
fig2.text(0.01, 0.01, "Nota: comparar cantidades entre materiales de distinta unidad es solo orientativo.",
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
    datos_unidad = [f for f in demanda_categoria_unidad if f["unidad"] == unidad]
    nombres_barras = []
    valores_barras = []
    colores_barras = []
    # Se recorren las categorías en el orden fijo y se toman solo las que usan esta unidad
    c = 0
    while c < len(CATEGORIAS):
        fila_categoria = [f for f in datos_unidad if f["categoria"] == CATEGORIAS[c]]
        if len(fila_categoria) > 0:
            nombres_barras.append(CATEGORIAS[c])
            valores_barras.append(int(fila_categoria[0]["cantidad_solicitada"]))
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