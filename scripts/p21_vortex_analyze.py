"""P21 analysis: read results/p21_vortex_scan.json, print the verdict table
against results/FROZEN_P21_VORTEX.md and draw the trajectories.
"""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = json.loads(pathlib.Path("results/p21_vortex_scan.json").read_text())
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

print("== P21.1 / P21.4 / P21.5: counter-rotating branch")
for key in sorted(k for k in R if k.startswith("counter_m")):
    m = int(key.split("m")[1])
    for nk, rec in sorted(R[key].items()):
        path = rec["path"]
        ax = axes[0]
        ax.plot([p[1] for p in path], [p[2] for p in path], "-", lw=1,
                label=f"m={m} {nk}")
        if "approach_exponent" in rec:
            print(f"  m={m} {nk}: arrival B_last={rec['arrival_B_last']:.5f} "
                  f"omega_last={rec['omega_last']}  exponent={rec['approach_exponent']:.3f} "
                  f"(coarse {rec['approach_exponent_coarse']:.3f})  Bc_fit={rec['Bc_fit']:.5f} "
                  f"Bc_lin={rec['Bc_linear_extrap']}")
            for dB, roots in rec["beyond_principal_sheet_roots"].items():
                print(f"      beyond +{dB}: {len(roots)} principal-sheet roots near arrival: {roots}")
        else:
            print(f"  m={m} {nk}: last B={rec['last_B']:.2f}  large-B exponent of Re: {rec['largeB_exponent_Re']}")
axes[0].axvline(0, color="k", lw=0.5)
axes[0].set_xlabel("Re omega"); axes[0].set_ylabel("Im omega"); axes[0].set_title("counter-rotating (m<0) vs B")
axes[0].legend(fontsize=7)

print("== P21.2: co-rotating adjacent-overtone gaps")
for key in sorted(k for k in R if k.startswith("co_m")):
    m = int(key.split("m")[1])
    for n, path in enumerate(R[key]["paths"]):
        if path:
            axes[1].plot([p[1] for p in path], [p[2] for p in path], "-", lw=1, label=f"m={m} n={n}")
    for pk, g in R[key]["gaps"].items():
        gm = g["min_gap"]
        if gm:
            print(f"  m={m} pair {pk}: min gap {gm[1]:.4f} at B={gm[0]:.3f}  (mu={gm[2]}, rho={gm[3]})")
axes[1].set_xlabel("Re omega"); axes[1].set_ylabel("Im omega"); axes[1].set_title("co-rotating (m>0) vs B")
axes[1].legend(fontsize=7)
plt.tight_layout()
pathlib.Path("results/figures").mkdir(exist_ok=True)
plt.savefig("results/figures/fig_p21_vortex.png", dpi=130)
print("figure: results/figures/fig_p21_vortex.png")
