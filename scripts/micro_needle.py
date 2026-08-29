"""Direct micro-grid evaluation of the rho(q^2) needle — no Newton, no fits.

The complex-migration Newton found near-zero |rho| at REAL q^2 for lambda =
0.1155 and 0.116, where coarser grids report rho_min > 0.  If a needle-thin
dip exists between grid points, lambda_ext moves up again.  Evaluate rho on a
+-0.01 window around the Newton roots with dq = 2e-4, tracking the pair from
the Newton omega.

Usage: micro_needle.py LAMBDA Q2_CENTER OMEGA_IM [HALF_WINDOW]
"""
import json
import pathlib
import sys

import numpy as np

from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients
from recoverability_ep.shooting import ShootingSolver, pair_invariants

LAM = float(sys.argv[1])
Q2C = float(sys.argv[2])
OM_IM = float(sys.argv[3])
HALF = float(sys.argv[4]) if len(sys.argv) > 4 else 0.01
DQ = 2e-4

b, bp, n = exact_gb_metric(LAM)
hc = exact_horizon_coefficients(LAM, 24)

def pair_at(q2, seed):
    s = ShootingSolver(b, bp, n, float(q2), horizon_coefficients=hc)
    return s.pair(seed)

seed = np.array([0.02 + 1j * OM_IM, -0.02 + 1j * OM_IM])
# settle the seed at the left edge, marching in from a bit outside
q2_left = Q2C - HALF
pair = seed
for q2 in np.linspace(Q2C - 3 * HALF, q2_left, 8):
    pair = pair_at(q2, pair)

rows = []
q2 = q2_left
while q2 <= Q2C + HALF + 1e-12:
    try:
        pair = pair_at(q2, pair)
        mu, rho = pair_invariants(pair)
        sym = abs(pair[0] + np.conj(pair[1]))
        rows.append([q2, float(rho.real), float(rho.imag), float(sym),
                     float(pair[0].real), float(pair[0].imag)])
    except Exception:
        rows.append([q2, None, None, None, None, None])
    q2 += DQ

good = [r for r in rows if r[1] is not None and r[3] < 1e-3]
if good:
    gmin = min(good, key=lambda r: r[1])
    crossings = sum(1 for a, b2 in zip(good, good[1:]) if a[1] * b2[1] < 0)
    print(f"lam={LAM}: micro rho_min={gmin[1]:.3e} at q2={gmin[0]:.5f} "
          f"omega=({gmin[4]:.2e},{gmin[5]:.6f}) crossings={crossings} "
          f"n_good={len(good)}/{len(rows)}", flush=True)
else:
    print(f"lam={LAM}: no valid points", flush=True)

out = pathlib.Path("results/micro_needle.json")
data = json.loads(out.read_text()) if out.exists() else []
data.append({"lam": LAM, "q2c": Q2C, "rows": rows})
out.write_text(json.dumps(data, indent=1))
