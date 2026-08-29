"""Identity-free EP census ("forest scan") at one lambda.

The fundamental-pair identity dissolves in the deep-q^2 forest of
near-degenerate mirror pairs, so lambda_ext keeps receding as resolution
improves.  This scan drops identity tracking entirely: at each q^2 on a
coarse grid, seed the shooting pair solver from a GRID of omega seeds,
collect every distinct mirror-symmetric pair (|omega1 + conj(omega2)| < 1e-4)
and record the global min rho over the census.  The best candidate windows
are then micro-refined (dq = 2e-4) with local tracking.

Verdict per lambda: does ANY mirror pair still produce a rho sign crossing?

Usage: forest_scan.py LAMBDA
"""
import json
import pathlib
import sys

import numpy as np

from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients
from recoverability_ep.shooting import ShootingSolver, pair_invariants

LAM = float(sys.argv[1])
Q2_LO, Q2_HI, DQ = -36.0, -30.0, 0.1
OM_SEEDS = np.arange(-9.75, -5.99, 0.25)

b, bp, n = exact_gb_metric(LAM)
hc = exact_horizon_coefficients(LAM, 24)

def census(q2, seeds_im):
    s = ShootingSolver(b, bp, n, float(q2), horizon_coefficients=hc)
    found = []
    for oi in seeds_im:
        try:
            pair = s.pair(np.array([0.05 + 1j * oi, -0.05 + 1j * oi]))
        except Exception:
            continue
        if abs(pair[0] + np.conj(pair[1])) > 1e-4:
            continue
        mu, rho = pair_invariants(pair)
        key = round(float(np.imag(mu)), 3)
        found.append((key, float(rho.real), pair))
    # dedupe by mu
    best = {}
    for key, r, pair in found:
        if key not in best or r < best[key][0]:
            best[key] = (r, pair)
    return best

rows = []
for q2 in np.arange(Q2_LO, Q2_HI + 1e-9, DQ):
    best = census(q2, OM_SEEDS)
    for key, (r, pair) in best.items():
        rows.append([float(q2), key, r])
    if best:
        rmin = min(v[0] for v in best.values())
        print(f"q2={q2:.1f}: pairs={len(best)} rho_min={rmin:.4f}", flush=True)

# candidates: (q2, mu_im) cells with smallest rho
rows.sort(key=lambda t: t[2])
cands = []
for q2, key, r in rows:
    if all(abs(q2 - c[0]) > 0.3 or abs(key - c[1]) > 0.3 for c in cands):
        cands.append((q2, key, r))
    if len(cands) == 3:
        break
print(f"candidates: {cands}", flush=True)

verdict = []
for q2c, om_im, r0 in cands:
    pair = None
    crossings = 0
    rho_min, q2_min, last_r = np.inf, None, None
    q2 = q2c - 0.06
    seed = np.array([0.02 + 1j * om_im, -0.02 + 1j * om_im])
    while q2 <= q2c + 0.06:
        sv = ShootingSolver(b, bp, n, float(q2), horizon_coefficients=hc)
        try:
            pair = sv.pair(seed if pair is None else pair)
            if abs(pair[0] + np.conj(pair[1])) < 1e-4:
                _, rho = pair_invariants(pair)
                r = float(rho.real)
                if last_r is not None and last_r * r < 0:
                    crossings += 1
                last_r = r
                if r < rho_min:
                    rho_min, q2_min = r, q2
            else:
                last_r = None
        except Exception:
            pair, last_r = None, None
        q2 += 2e-4
    verdict.append({"q2c": q2c, "mu_im": om_im, "rho_min": rho_min if np.isfinite(rho_min) else None,
                    "q2_min": q2_min, "crossings": crossings})
    print(f"refine q2c={q2c:.2f} mu={om_im}: rho_min={rho_min:.3e} crossings={crossings}", flush=True)

out = pathlib.Path("results/forest_scan.json")
data = json.loads(out.read_text()) if out.exists() else []
data.append({"lam": LAM, "census": rows[:200], "verdict": verdict})
out.write_text(json.dumps(data, indent=1))
print("done", flush=True)
