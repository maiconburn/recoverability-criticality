"""m = -7, n = 5 and n = 6: arrival-or-escape with deep continued
fractions (kmax 3000 / 6000, inversions n-1..n+1, kmax-independence to
1e-4). Seeds: extrapolated from the last reliable tracker points
(n = 5: 0.1684-1.7578i at B = 1.34; n = 6: 0.0697-3.4152i at B = 1.89).
Output: results/p23_m7_arrival.json.
"""
import json
import pathlib
import sys

import mpmath as mp

sys.path.insert(0, "src")
from recoverability_ep.dbt import find_qnm  # noqa

mp.mp.dps = 30
M = -7
OUT = {}


def deep(seed, B, n, kmaxes=(3000, 6000)):
    vals = {}
    for kmax in kmaxes:
        found = []
        for dr, di in ((0, 0), (0.5, 0), (-0.5, 0), (0, 0.05), (0, -0.05)):
            s = mp.mpc(mp.re(seed) * (1 + dr), mp.im(seed) * (1 + di))
            for ninv in (n - 1, n, n + 1):
                try:
                    r = find_qnm(s, M, B, n=ninv, kmax=kmax, tol=mp.mpf("1e-13"), maxsteps=60)
                except Exception:
                    continue
                if mp.re(r) <= 0 or abs(r - seed) > 0.5 * abs(seed) + 0.05:
                    continue
                for it in found:
                    if abs(r - it[0]) < 1e-6:
                        it[1].add(ninv)
                        break
                else:
                    found.append([r, {ninv}])
        vals[kmax] = [(r, sorted(ns)) for r, ns in found if len(ns) >= 2]
    stable = [(r, ns) for r, ns in vals[kmaxes[-1]] if any(abs(r - r2) < 1e-4 * abs(r) for r2, _ in vals[kmaxes[0]])]
    return vals, stable


for n, start, Bs in ((5, (1.3414, mp.mpc("0.16839", "-1.75783")), (1.45, 1.55, 1.65, 1.75, 1.9, 2.2)),
                     (6, (1.8902, mp.mpc("0.06965", "-3.41523")), (1.3, 1.6, 1.9, 2.2, 2.6, 3.0))):
    OUT[str(n)] = {}
    B0, w0 = start
    prev = [(B0, w0)]
    for B in Bs:
        if len(prev) >= 2:
            (b1, w1), (b2, w2) = prev[-2], prev[-1]
            seed = w2 + (w2 - w1) * (B - b2) / (b2 - b1)
        else:
            seed = w0
        vals, stable = deep(seed, B, n)
        OUT[str(n)][str(B)] = {"seed": [float(mp.re(seed)), float(mp.im(seed))],
                               "stable": [[float(mp.re(r)), float(mp.im(r)), ns] for r, ns in stable],
                               "per_kmax": {str(k): [[float(mp.re(r)), float(mp.im(r)), ns] for r, ns in v] for k, v in vals.items()}}
        print(f"  n={n} B={B}: seed {mp.nstr(seed, 5)}; stable {[(mp.nstr(r, 7), ns) for r, ns in stable]}; omega*B {[mp.nstr(r * B, 5) for r, _ in stable]}", flush=True)
        if stable:
            best = min(stable, key=lambda t: abs(t[0] - seed))[0]
            prev.append((B, best))
        pathlib.Path("results/p23_m7_arrival.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
