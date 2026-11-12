from datetime import date
from pathlib import Path
import sys

import numpy as np
import matplotlib.pyplot as plt

# Permite importar las clases del proyecto desde la carpeta principal.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from deposito import Deposito


class MaterialPrueba:
    """Material mínimo compatible con la clase Deposito."""
    def __init__(self, nombre, unidad):
        self._nombre = nombre
        self._unidad = unidad

    def get_nombre(self):
        return self._nombre

    def get_unidad_medida(self):
        return self._unidad


def ejecutar_analisis():
    hoy = date.today()
    deposito = Deposito("Depósito aeroespacial de prueba")

    datos_materiales = [
        ("Circuito Cerámico 065", "unidades"),
        ("Soporte MEMS 006", "unidades"),
        ("Fibra Aeroespacial 040", "metros"),
        ("Catalizador reforzado 071", "kg"),
        ("Soporte MEMS 090", "unidades"),
        ("Lámina Aeroespacial 020", "metros"),
        ("Válvula MEMS 046", "unidades"),
        ("Conector Cerámico 025", "unidades"),
        ("Placa Cerámica 013", "unidades"),
        ("Aleación MEMS 014", "kg"),
        ("Sensor Cerámico 057", "unidades"),
        ("Solvente reforzado 099", "litros"),
        ("Resina reforzada 043", "kg"),
        ("Circuito Cerámico 093", "unidades"),
        ("Sensor Cerámico 029", "unidades"),
    ]

    materiales = [
        MaterialPrueba(nombre, unidad)
        for nombre, unidad in datos_materiales
    ]

    cantidades_base = [90, 130, 110, 160, 100, 145, 120, 135]
    dias_base = [75, 420, 160, 610, 30, 300, 230, 500]

    # Guardamos las cantidades iniciales por material y fecha.
    # Esto permite incluir también las cajas que se vacíen por completo.
    cantidades_iniciales = {}

    for indice, material in enumerate(materiales):
        cantidades = [
            cantidad + ((indice * 17 + i * 11) % 45)
            for i, cantidad in enumerate(cantidades_base)
        ]
        dias = [
            dia + ((indice * 13 + i * 7) % 35)
            for i, dia in enumerate(dias_base)
        ]

        cajas = list(zip(dias, cantidades))
        orden_ingreso = cajas[::2] + cajas[1::2][::-1]

        cantidades_iniciales[material] = {}

        for dias_restantes, cantidad in orden_ingreso:
            vencimiento = date.fromordinal(hoy.toordinal() + dias_restantes)
            deposito.ingresar(material, vencimiento, cantidad)
            cantidades_iniciales[material][vencimiento] = cantidad

    # Registramos cuánto se retira de cada caja.
    cantidades_retiradas = {
        material: {fecha: 0 for fecha in cajas}
        for material, cajas in cantidades_iniciales.items()
    }

    pedidos_por_material = [
        [100, 145, 180],
        [120, 160, 190],
        [110, 170, 210],
        [130, 180, 220],
        [95, 155, 185],
        [125, 175, 205],
        [115, 165, 195],
        [105, 150, 200],
        [135, 185, 215],
        [100, 160, 205],
        [120, 170, 220],
        [110, 155, 190],
        [130, 175, 210],
        [95, 145, 185],
        [115, 165, 200],
    ]

    total_pedidos = 0

    for material, pedidos in zip(materiales, pedidos_por_material):
        for cantidad_solicitada in pedidos:
            cajas_sacadas = deposito.retirar(material, cantidad_solicitada)
            total_pedidos += 1

            # Deposito.retirar devuelve las cajas (o partes de cajas)
            # que realmente se utilizaron para completar el pedido.
            for caja in cajas_sacadas:
                fecha = caja.get_fecha_vencimiento()
                cantidad = caja.get_cantidad()
                cantidades_retiradas[material][fecha] += cantidad

    # Armamos los dos ejes con TODAS las cajas originales.
    # Y = porcentaje consumido de cada caja.
    dias_hasta_vencimiento = []
    porcentajes_consumidos = []
    nombres_materiales = []

    for material in materiales:
        for fecha, cantidad_inicial in cantidades_iniciales[material].items():
            cantidad_retirada = cantidades_retiradas[material][fecha]
            porcentaje = 100 * cantidad_retirada / cantidad_inicial

            dias_hasta_vencimiento.append((fecha - hoy).days)
            porcentajes_consumidos.append(porcentaje)
            nombres_materiales.append(material.get_nombre())

    print("=== RESUMEN DEL EXPERIMENTO FEFO ===")
    print(f"Materiales: {len(materiales)}")
    print(f"Cajas iniciales: {sum(len(c) for c in cantidades_iniciales.values())}")
    print(f"Pedidos simulados: {total_pedidos}")

    for material in materiales:
        total_inicial = sum(cantidades_iniciales[material].values())
        total_retirado = sum(cantidades_retiradas[material].values())
        print(
            f"{material.get_nombre():28s} | "
            f"consumido: {total_retirado / total_inicial * 100:5.1f}%"
        )

    # Un punto = una caja. Color = material.
    fig, ax = plt.subplots(figsize=(14, 8))
    colores = plt.get_cmap("turbo", len(materiales))

    for i, material in enumerate(materiales):
        indices = [
            j for j, nombre in enumerate(nombres_materiales)
            if nombre == material.get_nombre()
        ]

        ax.scatter(
            [dias_hasta_vencimiento[j] for j in indices],
            [porcentajes_consumidos[j] for j in indices],
            s=75,
            alpha=0.85,
            color=colores(i),
            edgecolors="black",
            linewidths=0.5,
            label=material.get_nombre()
        )

    ax.set_title(
        "Proximidad del vencimiento y porcentaje consumido por caja",
        fontsize=14,
        pad=15
    )
    ax.set_xlabel("Días restantes hasta el vencimiento")
    ax.set_ylabel("Cantidad consumida (% de la cantidad inicial)")
    ax.set_xlim(left=0)
    ax.set_ylim(-5, 105)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend(
        title="Material",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        fontsize=8
    )

    fig.text(
        0.5, 0.015,
        f"{len(materiales)} materiales · 120 cajas · {total_pedidos} pedidos · "
        f"fecha de referencia: {hoy:%d/%m/%Y}",
        ha="center",
        fontsize=9
    )

    fig.tight_layout(rect=[0, 0.045, 0.82, 1])
    fig.savefig("dispersion_consumo_fefo.png", dpi=180, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    ejecutar_analisis()
