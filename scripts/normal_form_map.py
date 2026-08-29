"""Fine shooting map of rho(q^2) near the EP-pair annihilation, one lambda
per invocation.  Extracts: rho_min (fine grid), the q^2 roots of rho (the two
EP positions -> half-width) below threshold, and the local vertex above.

Usage: normal_form_map.py LAMBDA
Appends to results/normal_form_map.json.
"""
import json
import pathlib
import sys

import numpy as np

from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients
from recoverability_ep.shooting import ShootingSolver, pair_invariants

LAM = float(sys.argv[1])
ANCHOR_LAM = 0.114
ANCHOR_Q2 = -33.489164251
ANCHOR_OMEGA = 0.000003233 - 7.644615228j
Q2_HI = -31.0
FINE_LO, FINE_HI, DQ_FINE = -34.4, -32.4, 0.01

def solver_at(lam, q2, cache={}):
    if lam not in cache:
        b, bp, n = exact_gb_metric(lam)
        cache[lam] = (b, bp, n, exact_horizon_coefficients(lam, 24))
    b, bp, n, hc = cache[lam]
    return ShootingSolver(b, bp, n, q2, horizon_coefficients=hc)

# anchor march at 0.114 up to Q2_HI, then lambda-continuation at Q2_HI
pair = solver_at(ANCHOR_LAM, ANCHOR_Q2).quadratic_pair(ANCHOR_OMEGA)
q2 = ANCHOR_Q2
while q2 < Q2_HI - 1e-9:
    q2 = min(q2 + 0.1, Q2_HI)
    pair = solver_at(ANCHOR_LAM, q2).pair(pair)
lam_path = np.linspace(ANCHOR_LAM, LAM, max(2, int(abs(LAM - ANCHOR_LAM) / 0.0005) + 1))
for lam in lam_path[1:]:
    pair = solver_at(float(lam), Q2_HI).pair(pair)

# coarse approach to the fine window, then fine profile
q2 = Q2_HI
while q2 > FINE_HI + 1e-9:
    q2 -= 0.05
    pair = solver_at(LAM, q2).pair(pair)

profile = []
while q2 > FINE_LO + 1e-9:
    q2 -= DQ_FINE
    try:
        pair = solver_at(LAM, q2).pair(pair)
    except Exception:
        profile.append([q2, None, None])
        continue
    mu, rho = pair_invariants(pair)
    sym = abs(pair[0] + np.conj(pair[1]))
    profile.append([q2, float(rho.real), float(sym)])

good = [(q, r) for q, r, s in profile if r is not None and s is not None and s < 1e-3]
qs = np.array([g[0] for g in good])
rs = np.array([g[1] for g in good])
i = int(np.argmin(rs))
rho_min, q2_min = float(rs[i]), float(qs[i])

# roots of rho (linear interpolation on the fine grid)
roots = []
for a, b in zip(good, good[1:]):
    if a[1] * b[1] < 0:
        t = a[1] / (a[1] - b[1])
        roots.append(float(a[0] + t * (b[0] - a[0])))

# local quadratic vertex from the 7 points around the minimum
lo, hi = max(0, i - 3), min(len(qs), i + 4)
c = np.polyfit(qs[lo:hi], rs[lo:hi], 2)
q_v = float(-c[1] / (2 * c[0]))
rho_v = float(np.polyval(c, q_v))

row = {"lam": LAM, "rho_min": rho_min, "q2_min": q2_min, "roots": roots,
       "half_width": abs(roots[0] - roots[-1]) / 2 if len(roots) >= 2 else None,
       "vertex_q2": q_v, "vertex_rho": rho_v, "curv": float(c[0]),
       "n_good": len(good), "n_total": len(profile)}
print(json.dumps(row), flush=True)
out = pathlib.Path("results/normal_form_map.json")
data = json.loads(out.read_text()) if out.exists() else []
data.append(row)
out.write_text(json.dumps(data, indent=1))
