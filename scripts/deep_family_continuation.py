"""Continue the deep-family mirror EP (found at lambda = 0.120, omega_c =
-9.73i, q^2 in [-32.300, -32.285]) upward in lambda: does it survive at and
beyond the eikonal threshold 1/8?

Per lambda: profile rho(q^2) over a window around the previous EP position
(dq = 0.004), pair tracked by continuation from the previous lambda.  Report
rho_min, the rho<0 interval, and omega at the minimum.
"""
import json
import pathlib

import numpy as np

from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients
from recoverability_ep.shooting import ShootingSolver, pair_invariants

LADDER = [0.120, 0.1215, 0.123, 0.1245, 0.125, 0.1255, 0.127, 0.129, 0.132]
Q2_START = -32.29
MU_START = -9.73
HALF, DQ = 0.7, 0.004

def solver_at(lam, q2, cache={}):
    if lam not in cache:
        b, bp, n = exact_gb_metric(lam)
        cache[lam] = (b, bp, n, exact_horizon_coefficients(lam, 24))
    b, bp, n, hc = cache[lam]
    return ShootingSolver(b, bp, n, float(q2), horizon_coefficients=hc)

center = Q2_START
seed = np.array([0.02 + 1j * MU_START, -0.02 + 1j * MU_START])
out = []
for lam in LADDER:
    pair = seed
    rows = []
    q2 = center + HALF
    while q2 >= center - HALF:
        try:
            pair = solver_at(lam, q2).pair(pair)
            if abs(pair[0] + np.conj(pair[1])) < 1e-3:
                _, rho = pair_invariants(pair)
                rows.append([q2, float(rho.real), float(pair[0].imag)])
        except Exception:
            pass
        q2 -= DQ
    if not rows:
        print(f"lam={lam}: tracking lost", flush=True)
        out.append({"lam": lam, "lost": True})
        continue
    rmin = min(rows, key=lambda r: r[1])
    neg = [r for r in rows if r[1] < 0]
    row = {"lam": lam, "rho_min": rmin[1], "q2_min": rmin[0], "mu_im": rmin[2],
           "neg_interval": [neg[0][0], neg[-1][0]] if neg else None,
           "rho_max": max(r[1] for r in rows), "n": len(rows)}
    out.append(row)
    print(f"lam={lam}: rho_min={rmin[1]:.3e} at q2={rmin[0]:.3f} mu={rmin[2]:.3f} "
          f"neg={row['neg_interval']} rho_max={row['rho_max']:.2f}", flush=True)
    # recenter on the minimum; reseed from its pair neighborhood
    center = rmin[0]
    seed = np.array([0.02 + 1j * rmin[2], -0.02 + 1j * rmin[2]])

pathlib.Path("results/deep_family.json").write_text(json.dumps(out, indent=1))
print("done", flush=True)
