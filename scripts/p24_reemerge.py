"""P24.2: does the m = -7, n = 5 mode re-emerge onto the principal sheet
at B = 6 and 8 near c_5/B = (0.0696 - 2.4303i)/B? Very deep fractions
(kmax 32000 and 64000, 50 digits, resid_max 1e-8), inversions 5 and 6,
seeds with Re = 1.0 and 0.6 of the target. Frozen in
results/FROZEN_P24_VORTEX_MULTIPLET.md. Output: results/p24_reemerge.json.
"""
import json
import pathlib
import sys
import time

import mpmath as mp

sys.path.insert(0, "src")
from recoverability_ep.dbt import find_qnm  # noqa

mp.mp.dps = 50
M = -7
C5 = mp.mpc("0.0696", "-2.4303")
OUT = {}
for B in (6.0, 8.0):
    target = C5 / B
    OUT[str(B)] = {"target": [float(mp.re(target)), float(mp.im(target))], "rows": []}
    for kmax in (32000, 64000):
        for fr in (1.0, 0.6):
            seed = mp.mpc(mp.re(target) * fr, mp.im(target))
            for ninv in (5, 6):
                t0 = time.time()
                try:
                    r = find_qnm(seed, M, B, n=ninv, kmax=kmax, tol=mp.mpf("1e-12"), maxsteps=80, resid_max=mp.mpf("1e-8"))
                    near = abs(r - target) < 0.1 * abs(target) + 0.01
                    OUT[str(B)]["rows"].append([kmax, fr, ninv, float(mp.re(r)), float(mp.im(r)), bool(near), time.time() - t0])
                    print(f"  B={B} kmax={kmax} fr={fr} inv={ninv}: {mp.nstr(r, 9)}  omega*B={mp.nstr(r * B, 6)}  near_target={near}  ({time.time() - t0:.0f}s)", flush=True)
                except Exception as e:
                    OUT[str(B)]["rows"].append([kmax, fr, ninv, None, None, False, time.time() - t0])
                    print(f"  B={B} kmax={kmax} fr={fr} inv={ninv}: FAIL {str(e)[:60]}  ({time.time() - t0:.0f}s)", flush=True)
                pathlib.Path("results/p24_reemerge.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
