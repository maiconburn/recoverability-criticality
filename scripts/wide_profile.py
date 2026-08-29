"""Classify a forest-scan candidate: genuine mirror-EP structure (rho
excursion to O(0.01)+ with real-part splitting outside a collided band) vs
trivial near-parallel imaginary modes (rho ~ 1e-9 everywhere, no Re).

Usage: wide_profile.py LAMBDA Q2C MU_IM [HALF_WINDOW]
"""
import json
import pathlib
import sys

import numpy as np

from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients
from recoverability_ep.shooting import ShootingSolver, pair_invariants

LAM = float(sys.argv[1])
Q2C = float(sys.argv[2])
MU_IM = float(sys.argv[3])
HALF = float(sys.argv[4]) if len(sys.argv) > 4 else 0.8
DQ = 0.005

b, bp, n = exact_gb_metric(LAM)
hc = exact_horizon_coefficients(LAM, 24)

pair = np.array([0.02 + 1j * MU_IM, -0.02 + 1j * MU_IM])
rows = []
for q2 in np.arange(Q2C - HALF, Q2C + HALF + 1e-9, DQ):
    try:
        s = ShootingSolver(b, bp, n, float(q2), horizon_coefficients=hc)
        pair = s.pair(pair)
        sym = abs(pair[0] + np.conj(pair[1]))
        if sym < 1e-3:
            _, rho = pair_invariants(pair)
            rows.append([float(q2), float(rho.real),
                         float(abs(pair[0].real)), float(pair[0].imag)])
    except Exception:
        pair = np.array([0.02 + 1j * MU_IM, -0.02 + 1j * MU_IM])

if rows:
    r = np.array([x[1] for x in rows])
    re = np.array([x[2] for x in rows])
    print(f"lam={LAM} q2c={Q2C}: n={len(rows)} rho_max={r.max():.3e} "
          f"rho_min={r.min():.3e} max|Re omega|={re.max():.3e}", flush=True)
else:
    print(f"lam={LAM} q2c={Q2C}: nothing valid", flush=True)

out = pathlib.Path("results/wide_profile.json")
data = json.loads(out.read_text()) if out.exists() else []
data.append({"lam": LAM, "q2c": Q2C, "mu_im": MU_IM, "rows": rows})
out.write_text(json.dumps(data, indent=1))
