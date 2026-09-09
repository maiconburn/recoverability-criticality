"""P21h.2 finite-B closure for m = -7: the robust tracker loses n = 5 at
B = 1.34 and n = 6 at B = 2.38 (kmax 600 no longer converges near the
axis). Deep continued-fraction probe (kmax 3000 / 6000 / 12000,
inversions n-1..n+1) at B = 2, 3, 4, 6 near the tower values c_5/B and
c_6/B (complex-ray solver: c_5 = 0.0696-2.4303i; action-WKB
c_6 = -0.6408-2.7109i, i.e. Re < 0, predicted absorbed). A root is
accepted if two kmax values agree to 1e-4 relative and at least two
inversions agree. Output: results/p23_m7_bridge.json.
"""
import json
import pathlib
import sys

import mpmath as mp

sys.path.insert(0, "src")
from recoverability_ep.dbt import find_qnm  # noqa

mp.mp.dps = 40
M = -7
C = {5: mp.mpc("0.0696", "-2.4303"), 6: mp.mpc("-0.6408", "-2.7109")}
OUT = {}


def probe(B, target, n, kmaxes=(3000, 6000, 12000)):
    got = {}
    for kmax in kmaxes:
        found = []
        for fr in (0.6, 1.0, 1.5):
            for fi in (0.9, 1.0, 1.1):
                seed = mp.mpc(abs(mp.re(target)) * fr * (1 if mp.re(target) >= 0 else 1), mp.im(target) * fi)
                for ninv in (n - 1, n, n + 1):
                    try:
                        r = find_qnm(seed, M, B, n=ninv, kmax=kmax, tol=mp.mpf("1e-13"), maxsteps=60, resid_max=mp.mpf("1e-9"))
                    except Exception:
                        continue
                    if mp.re(r) <= 0 or abs(r - target) > 0.6 * abs(target) + 0.05:
                        continue
                    for it in found:
                        if abs(r - it[0]) < 1e-6:
                            it[1].add(ninv)
                            break
                    else:
                        found.append([r, {ninv}])
        got[kmax] = [(r, sorted(ns)) for r, ns in found if len(ns) >= 2]
    stable = []
    ks = list(got)
    for r, ns in got[ks[-1]]:
        if any(abs(r - r2) < 1e-4 * abs(r) for r2, _ in got[ks[-2]]):
            stable.append((r, ns))
    return got, stable


for n in (5, 6):
    OUT[str(n)] = {}
    for B in (2.0, 3.0, 4.0, 6.0):
        target = C[n] / B
        got, stable = probe(B, target, n)
        OUT[str(n)][str(B)] = {"target": [float(mp.re(target)), float(mp.im(target))],
                               "stable": [[float(mp.re(r)), float(mp.im(r)), ns] for r, ns in stable],
                               "per_kmax": {str(k): [[float(mp.re(r)), float(mp.im(r)), ns] for r, ns in v] for k, v in got.items()}}
        print(f"  n={n} B={B}: target {mp.nstr(target, 5)}; stable {[(mp.nstr(r, 7), ns) for r, ns in stable]}; omega*B {[mp.nstr(r * B, 5) for r, _ in stable]}", flush=True)
        pathlib.Path("results/p23_m7_bridge.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
