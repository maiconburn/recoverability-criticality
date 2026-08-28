"""Two-panel summary figure of the P6 dry run."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
data = json.loads((HERE / "results_p6.json").read_text())

INK, MUTED, GRID = "#1f2430", "#6b7280", "#e5e7eb"
COLORS = {"S-A(controle-acidental)": "#8b91a0", "S-B": "#4f46e5", "S-C": "#0891b2"}
WARM = "#d97706"

plt.rcParams.update({
    "figure.dpi": 150, "font.size": 10.5, "axes.edgecolor": MUTED,
    "axes.labelcolor": INK, "axes.titlecolor": INK, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "savefig.bbox": "tight", "savefig.facecolor": "white",
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

for cfg in data["configs"]:
    tag = cfg["tag"]
    color = COLORS[tag]
    label = tag.replace("(controle-acidental)", " (acidente ctrl)")
    ds, ratios = [], []
    for d_key, entry in cfg["per_distance"].items():
        d = float(d_key)
        if d > 0:
            ds.append(d)
            ratios.append(entry["ratio"])
    order = np.argsort(ds)
    ax1.semilogx(np.array(ds)[order], np.array(ratios)[order], "o-", color=color,
                 lw=1.5, ms=5, label=label)
ax1.axhline(1.0, color=WARM, ls="--", lw=1.6, label="ontologia: razão = 1")
ax1.set_xlabel("d = (g − g_EP)/g_EP")
ax1.set_ylabel("α_Petz / α_spec")
ax1.set_title("K1: razão das taxas — depende do botão,\nsó ≈1 no acidente numérico")
ax1.legend(fontsize=8, loc="center left")
ax1.set_ylim(0, 1.5)

tags, spec_h, petz_h = [], [], []
for cfg in data["configs"]:
    off_spec = np.mean([cfg["per_distance"][k]["alpha_spec"] for k in ("0.3", "0.1", "0.03")])
    off_petz = np.mean([cfg["per_distance"][k]["alpha_petz"] for k in ("0.01", "0.003")])
    ep = cfg["per_distance"]["0"]
    tags.append(cfg["tag"].replace("(controle-acidental)", ""))
    spec_h.append(ep["alpha_spec"] / off_spec)
    petz_h.append(ep["alpha_petz"] / off_petz)
x = np.arange(len(tags))
width = 0.36
bars1 = ax2.bar(x - width / 2, spec_h, width, color="#4f46e5", label="espectral")
bars2 = ax2.bar(x + width / 2, petz_h, width, color="#0891b2", label="Petz")
for bars in (bars1, bars2):
    for b in bars:
        ax2.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.02,
                 f"{b.get_height():.2f}", ha="center", fontsize=8.5, color=INK)
ax2.axhline(0.5, color=WARM, ls="--", lw=1.4)
ax2.text(2.35, 0.51, "halving (0.5)", color=WARM, fontsize=8.5)
ax2.axhline(1.0, color=MUTED, ls=":", lw=1.2)
ax2.text(2.35, 1.01, "sem halving (1)", color=MUTED, fontsize=8.5)
ax2.set_xticks(x, tags)
ax2.set_ylabel("α(EP) / α(fora do EP)")
ax2.set_title("K2: no EP a taxa espectral halva,\na taxa de Petz não")
ax2.legend(fontsize=9)
ax2.set_ylim(0, 1.35)

fig.savefig(HERE / "fig_p6_dryrun.png")
print("wrote fig_p6_dryrun.png")
