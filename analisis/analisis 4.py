import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

fig, ax = plt.subplots(figsize=(13, 7.5))
ax.set_xlim(0, 13)
ax.set_ylim(0, 8)
ax.axis("off")

roles = {
    "COMPRADOR": (1.5, "#DCEBFF", "#3478C8"),
    "ADMINISTRADOR": (4.8, "#E5F4E8", "#32965A"),
    "SUPERVISOR": (8.1, "#FFF0D9", "#D68A20"),
    "VENDEDOR": (11.4, "#F0E5FA", "#8B5BC2"),
}
for name, (x, fill, edge) in roles.items():
    ax.add_patch(FancyBboxPatch(
        (x-1.35, 0.5), 2.7, 6.9,
        boxstyle="round,pad=0.03,rounding_size=0.18",
        fc=fill, ec=edge, lw=2, alpha=.72
    ))
    ax.text(x, 7.05, name, ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=edge)

def node(x, y, label, edge, w=2.05):
    ax.add_patch(FancyBboxPatch(
        (x-w/2, y-.31), w, .62,
        boxstyle="round,pad=0.06,rounding_size=0.13",
        fc="white", ec=edge, lw=1.6
    ))
    ax.text(x, y, label, ha="center", va="center",
            fontsize=9, color="#263238")

def arrow(start, end, label, color, curve=0, label_xy=None):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=14,
        lw=2.5, color=color,
        connectionstyle=f"arc3,rad={curve}",
        shrinkA=4, shrinkB=4
    ))
    if label_xy:
        ax.text(*label_xy, label, ha="center", va="center",
                fontsize=8, fontweight="bold", color=color,
                bbox=dict(boxstyle="round,pad=.2", fc="white",
                          ec="none", alpha=.95))

x = {"c": 1.5, "a": 4.8, "s": 8.1, "v": 11.4}

# Solicitud de compra: Comprador -> Administrador
node(x["c"], 6.0, "Crea solicitud", "#3478C8")
node(x["a"], 6.0, "Recibe solicitud", "#32965A")
arrow((2.55, 6.0), (3.75, 6.0), "SOLICITUD", "#3478C8", label_xy=(3.15, 6.32))

# Pedido de venta: Vendedor -> Administrador
node(x["v"], 5.0, "Crea pedido", "#8B5BC2")
node(x["a"], 5.0, "Recibe pedido", "#32965A")
arrow((10.35, 5.0), (5.85, 5.0), "PEDIDO", "#8B5BC2", label_xy=(8.1, 5.32))

# Transferencia: Administrador -> Supervisor
node(x["a"], 3.85, "Crea transferencia", "#32965A")
node(x["s"], 3.85, "Recibe transferencia", "#D68A20")
arrow((5.85, 3.85), (7.05, 3.85), "TRANSFERENCIA", "#D68A20",
      label_xy=(6.45, 4.17))

# Remesa: registro -> Supervisor (evento propio)
node(x["a"], 2.55, "Registra remesa", "#32965A")
node(x["s"], 2.55, "Recibe remesa", "#D68A20")
arrow((5.85, 2.55), (7.05, 2.55), "REMESA", "#D68A20",
      label_xy=(6.45, 2.87))

# Despacho -> reposición si stock bajo
node(x["v"], 1.2, "Despacha pedido", "#8B5BC2")
node(x["c"], 1.2, "Recibe reposición", "#3478C8")
arrow((10.35, 1.2), (2.55, 1.2), "REPONER · si stock bajo", "#3478C8",
      curve=-.12, label_xy=(6.45, .88))

ax.text(6.5, 7.72, "CIRCULACIÓN DE TAREAS · SISTEMA JIT",
        ha="center", va="center", fontsize=16,
        fontweight="bold", color="#263238")
ax.text(6.5, .18,
        "Colores = roles  |  Flechas = tareas derivadas entre colas",
        ha="center", va="center", fontsize=9, color="#555555")

plt.tight_layout()
salida = Path(__file__).resolve().parent / "diagrama_tareas_color.png"
plt.savefig(salida, dpi=220, bbox_inches="tight")
print(f"Gráfico guardado en: {salida}")
plt.show()
