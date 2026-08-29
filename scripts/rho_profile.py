"""Shooting-based rho(q^2) profile of the primary mirror pair, continued in
lambda.  Purpose: locate the true extinction of the primary-branch EP as the
lambda where min_q2 rho crosses zero (trusted instrument; no collocation in
the deep region).

Method: anchor on the shooting-verified EP at ANCHOR_LAM (pair known), march
the pair up to Q2_HI, then for each lambda in the ladder march down over
[Q2_LO, Q2_HI] with the pair seeded from the previous lambda at Q2_HI.
"""
import json
import pathlib
import sys

import numpy as np

from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients
from recoverability_ep.shooting import ShootingSolver, pair_invariants

ANCHOR_LAM = 0.114
ANCHOR_Q2 = -33.489164251
ANCHOR_OMEGA = 0.000003233 - 7.644615228j
LADDER = [float(a) for a in sys.argv[1:]] or [0.114, 0.116, 0.118, 0.120, 0.122]
Q2_HI, Q2_LO, DQ = -31.0, -37.0, 0.05

def solver_at(lam, q2, hc_cache={}):
    if lam not in hc_cache:
        b, bp, n = exact_gb_metric(lam)
        hc_cache[lam] = (b, bp, n, exact_horizon_coefficients(lam, 24))
    b, bp, n, hc = hc_cache[lam]
    return ShootingSolver(b, bp, n, q2, horizon_coefficients=hc)

# phase A: from the anchor EP, march the pair up to Q2_HI
pair = solver_at(ANCHOR_LAM, ANCHOR_Q2).quadratic_pair(ANCHOR_OMEGA)
q2 = ANCHOR_Q2
while q2 < Q2_HI - 1e-9:
    q2 = min(q2 + 0.1, Q2_HI)
    pair = solver_at(ANCHOR_LAM, q2).pair(pair)
print(f"anchor pair at q2={Q2_HI}: {pair}", flush=True)

# phase B: lambda ladder, each profiles [Q2_LO, Q2_HI]
seed_hi = pair
out = []
for lam in LADDER:
    seed_hi = solver_at(lam, Q2_HI).pair(seed_hi)  # lambda-continuation at Q2_HI
    pair = seed_hi
    profile = []
    q2 = Q2_HI
    while q2 > Q2_LO + 1e-9:
        q2 -= DQ
        try:
            pair = solver_at(lam, q2).pair(pair)
        except Exception as exc:  # keep marching with previous pair as seed
            profile.append([q2, None, None])
            continue
        mu, rho = pair_invariants(pair)
        sym = abs(pair[0] + np.conj(pair[1]))
        profile.append([q2, float(rho.real), float(sym)])
    rhos = [(r, q) for q, r, s in profile if r is not None and s is not None and s < 1e-3]
    rho_min, q2_min = min(rhos) if rhos else (None, None)
    crossing = any(
        a[1] is not None and b[1] is not None and a[1] * b[1] < 0
        for a, b in zip(profile, profile[1:])
    )
    print(f"lam={lam}: rho_min={rho_min} at q2={q2_min} crossing={crossing}", flush=True)
    out.append({"lam": lam, "rho_min": rho_min, "q2_min": q2_min,
                "crossing": crossing, "profile": profile})

p = pathlib.Path("results/rho_profile.json")
prev = json.loads(p.read_text()) if p.exists() else []
p.write_text(json.dumps(prev + out, indent=1))
print("done", flush=True)
