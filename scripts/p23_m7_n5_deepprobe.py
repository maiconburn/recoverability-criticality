"""m = -7, n = 5 at B = 2.5, 3.0, 3.5: very deep continued fractions
(kmax 8000 / 16000 / 32000 at 50 digits, residual guard 1e-8,
inversions 4 and 5) seeded from the scaled trend omega B ~ 0.135 - 2.36i
of the deep track (B <= 2.33). The kmax sequence shows whether a root
converges (escape: omega B -> c_5 = 0.0696 - 2.4303i) or whether the
near-axis roots are truncation artifacts (absorption between B = 2.3
and 3). Output: results/p23_m7_n5_deepprobe.json.
"""
import json
import pathlib
import sys
import time

import mpmath as mp

sys.path.insert(0, "src")
from recoverability_ep.dbt import find_qnm  # noqa

mp.mp.dps = 50
M, N = -7, 5
OUT = {}
for B in (2.5, 3.0, 3.5):
    OUT[str(B)] = {}
    base = mp.mpc("0.135", "-2.36") / B
    for kmax in (8000, 16000, 32000):
        rows = []
        for fr in (1.0, 0.6, 1.5):
            seed = mp.mpc(mp.re(base) * fr, mp.im(base))
            for ninv in (4, 5):
                t0 = time.time()
                try:
                    r = find_qnm(seed, M, B, n=ninv, kmax=kmax, tol=mp.mpf("1e-12"), maxsteps=80, resid_max=mp.mpf("1e-8"))
                    rows.append([float(mp.re(r)), float(mp.im(r)), ninv, fr, time.time() - t0])
                    print(f"  B={B} kmax={kmax} inv={ninv} seed_fr={fr}: {mp.nstr(r, 9)}  omega*B={mp.nstr(r * B, 6)}  ({time.time() - t0:.0f}s)", flush=True)
                except Exception as e:
                    print(f"  B={B} kmax={kmax} inv={ninv} seed_fr={fr}: FAIL {str(e)[:70]}  ({time.time() - t0:.0f}s)", flush=True)
        OUT[str(B)][str(kmax)] = rows
        pathlib.Path("results/p23_m7_n5_deepprobe.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
