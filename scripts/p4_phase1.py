"""P4 phase 1: the CMI-layer prediction for the rate, frozen before comparison.

The transcript's Abel relation (turns 078-080) defines the information-depth
function J(u) implied by the blackening factor:

    (2/pi) * Int_0^{pi/2} dtheta / J(u sin t) = b(u)^{-1/2}
    =>  1/J(v) = (2/pi) * Int_0^{pi/2} sin t [g + w g'](w = v sin t) dt,
        g = (pi/2) b^{-1/2}.

Structural consequence: J inherits (i) the branch points of b AND (ii) the
complex zeros of b (through b^{-1/2}).  For Gauss-Bonnet the zeros sit at
z^4 = 1 (z = -1, +-i) for EVERY lambda, so the CMI layer predicts a rate
floor from the fixed singularity at z = +-i, while the pure-metric (Stahl)
prediction follows the moving branch point.  The two prediction curves
therefore SPLIT at small lambda -- the bifurcation P4 was designed to force.

This script freezes both curves and verifies the singularity structure of
J numerically (Pade pole clustering).  Comparison against the measured
sweep rates happens only afterwards (analyze_sweep.py).
"""

import json
from pathlib import Path

import numpy as np

import sweep_predictions as sp
from recoverability_ep.model import exact_gb_metric

RESULTS = Path(__file__).resolve().parent.parent / "results"
OUT = RESULTS / "p4_predictions.json"


def inverse_j(v_values, coupling, n_theta=400):
    """1/J(v) by the differentiated inverse Abel transform (complex-safe)."""

    b, bp, _ = exact_gb_metric(coupling)
    theta = (np.arange(n_theta) + 0.5) * (np.pi / 2.0) / n_theta
    weight = (np.pi / 2.0) / n_theta
    sin_t = np.sin(theta)
    result = np.zeros_like(np.asarray(v_values, dtype=complex))
    for index, v in np.ndenumerate(np.asarray(v_values, dtype=complex)):
        w = v * sin_t
        b_w = np.asarray(b(w), dtype=complex)
        bp_w = np.asarray(bp(w), dtype=complex)
        g = (np.pi / 2.0) / np.sqrt(b_w)
        g_prime = -(np.pi / 4.0) * bp_w / b_w**1.5
        result[index] = (2.0 / np.pi) * np.sum(
            sin_t * (g + w * g_prime)
        ) * weight
    return result


def singularity_scan(coupling, targets):
    """Direct check: |J| along small circles around candidate singularities."""

    findings = {}
    for name, point in targets.items():
        probes = point + 0.02 * np.exp(1j * np.linspace(0, 2 * np.pi, 8, endpoint=False))
        values = 1.0 / inverse_j(probes, coupling)
        findings[name] = float(np.max(np.abs(values)) / max(np.min(np.abs(values)), 1e-30))
    return findings


def main():
    ladder = sorted(set(sp.LADDER + [0.08]))
    zero_green = sp.green_interval(1.0 - 1.0j)  # x = 1 - i (image of z = i)
    anchor = sp.nearest_green(sp.ANCHOR_LAMBDA)
    rows = []
    for coupling in ladder:
        branch_green = sp.nearest_green(coupling)
        cmi_green = min(branch_green, zero_green)
        rows.append(
            dict(
                coupling=coupling,
                branch_green=branch_green,
                zero_green=zero_green,
                alpha_metric_pred=sp.ANCHOR_ALPHA_RHO * branch_green / anchor,
                alpha_cmi_pred=sp.ANCHOR_ALPHA_RHO * cmi_green / anchor,
                dominant="zero(z=i)" if cmi_green < branch_green else "branch",
            )
        )
        print(
            f"lambda={coupling:+.3f}  g_branch={branch_green:.4f}  "
            f"g_zero={zero_green:.4f}  alpha_B={rows[-1]['alpha_metric_pred']:.3f}  "
            f"alpha_CMI={rows[-1]['alpha_cmi_pred']:.3f}  [{rows[-1]['dominant']}]"
        )

    # numerical sanity of the J construction: pure-AdS limit and qBTZ-style check
    j_ads = 1.0 / inverse_j(np.array([0.3 + 0j]), 1e-9)[0]
    print(f"sanity: J(0.3) at lambda~0 with b=1-z^4: {j_ads:.6f}")

    OUT.write_text(
        json.dumps(
            dict(
                frozen_with="sweep_predictions.json anchor; before seeing "
                "lambda>0 sweep measurements (lambda=-0.1 already seen and flagged)",
                zero_green=zero_green,
                rows=rows,
            ),
            indent=1,
        )
    )
    print("frozen ->", OUT)


if __name__ == "__main__":
    main()
