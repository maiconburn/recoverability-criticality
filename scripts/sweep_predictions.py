"""P1 — freeze a-priori rate predictions for the coupling sweep.

The Gauss-Bonnet blackening factor b(z) has branch points where
1 - 4 lambda (1 - z^4) = 0.  In the Pade variable x = 1 - z the frozen
proxy for the reconstruction rate is the Green's function of C \ [0, 1]
at the nearest branch point,

    g(x_s) = ln | w + sqrt(w - 1) sqrt(w + 1) |,   w = 2 x_s - 1,

anchored to the measured critical-channel rate at lambda = 0.08
(alpha_rho = 0.851 +- 0.130 from the validated run).  Frozen predictions:

    alpha_pred(lambda) = alpha_anchor * g(lambda) / g(0.08)
    dN_per_decade(lambda) = ln(10) / (2 alpha_pred)

This file must be run BEFORE any sweep measurement; it timestamps and
writes results/sweep_predictions.json.
"""

import json
import subprocess
from pathlib import Path

import numpy as np

ANCHOR_LAMBDA = 0.08
ANCHOR_ALPHA_RHO = 0.851
ANCHOR_ALPHA_ERR = 0.130
LADDER = [-0.10, -0.05, 0.02, 0.05, 0.08, 0.12, 0.16, 0.20]
OUT = Path(__file__).resolve().parent.parent / "results" / "sweep_predictions.json"


def branch_points(coupling):
    if abs(coupling) < 1e-12:
        return []
    z4 = 1.0 - 1.0 / (4.0 * coupling)
    magnitude = abs(z4) ** 0.25
    base_angle = np.angle(complex(z4)) / 4.0
    return [
        magnitude * np.exp(1j * (base_angle + k * np.pi / 2.0)) for k in range(4)
    ]


def green_interval(x):
    """Green's function of C \\ [0,1] at complex x (log of Joukowski image)."""

    w = 2.0 * complex(x) - 1.0
    phi = w + np.sqrt(w - 1.0) * np.sqrt(w + 1.0)
    value = abs(phi)
    if value < 1.0:
        value = 1.0 / value
    return float(np.log(value))


def nearest_green(coupling):
    greens = [green_interval(1.0 - z) for z in branch_points(coupling)]
    return min(greens) if greens else float("inf")


def main():
    anchor_green = nearest_green(ANCHOR_LAMBDA)
    rows = []
    for coupling in LADDER:
        green = nearest_green(coupling)
        alpha = ANCHOR_ALPHA_RHO * green / anchor_green
        alpha_err = ANCHOR_ALPHA_ERR * green / anchor_green
        rows.append(
            dict(
                coupling=coupling,
                nearest_branch_green=green,
                alpha_rho_pred=alpha,
                alpha_rho_pred_err=alpha_err,
                dn_per_decade_pred=float(np.log(10.0) / (2.0 * alpha)),
                alpha_ep_pred=alpha / 2.0,
            )
        )
    stamp = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                           capture_output=True, text=True).stdout.strip()
    frozen = dict(
        frozen_at=stamp,
        anchor=dict(coupling=ANCHOR_LAMBDA, alpha_rho=ANCHOR_ALPHA_RHO,
                    err=ANCHOR_ALPHA_ERR, green=anchor_green),
        proxy="Green's function of C\\[0,1] at nearest branch point of b; "
              "ratio-normalized to the lambda=0.08 anchor",
        kill_criteria=dict(
            k1="dn/decade fails to track ln10/(2 alpha_pred) in >=5 couplings (R^2<0.9)",
            k2="channel splitting alpha_rho/alpha_sup -> 1 with N (3 sigma)",
            k3="no rate collapse as lambda -> 1/4 (predicted alpha -> larger, "
               "R -> 0 as branch point approaches horizon at lambda -> +inf? "
               "documented: for lambda -> 0.25-, z_s -> 0, x_s -> 1: green -> 0, "
               "alpha_pred -> 0: convergence must DEGRADE)",
        ),
        predictions=rows,
    )
    OUT.write_text(json.dumps(frozen, indent=1))
    for row in rows:
        print(
            f"lambda={row['coupling']:+.3f}  g={row['nearest_branch_green']:.4f}  "
            f"alpha_pred={row['alpha_rho_pred']:.3f}  "
            f"dN/dec_pred={row['dn_per_decade_pred']:.3f}"
        )
    print("frozen ->", OUT)


if __name__ == "__main__":
    main()
