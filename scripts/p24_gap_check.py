"""P24.1 direct check: is the m = -7, n = 5 root present at B = 3.0, 3.5,
4.0? Seeds from the linear continuation of the deep track
(Re slope -0.03/unit B, Im slope +0.34/unit B from B = 2.679:
0.044666 - 0.894802i) and, at each B, from the previous found root.
kmax 16000 / 32000 / 64000 at 50 digits (resid_max 1e-8), inversions
5 and 6, Muller from the close seed. Output: results/p24_gap_check.json.
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
B0, w0 = mp.mpf("2.67910"), mp.mpc("0.044666222", "-0.89480248")
slope = mp.mpc("-0.030", "0.34")
OUT = {}
prev = None
for B in (3.0, 3.5, 4.0):
    seed = (prev if prev is not None else w0 + slope * (mp.mpf(B) - B0))
    OUT[str(B)] = {"seed": [float(mp.re(seed)), float(mp.im(seed))], "rows": []}
    found = None
    for kmax in (16000, 32000, 64000):
        for ninv in (5, 6):
            t0 = time.time()
            try:
                r = find_qnm(seed, M, B, n=ninv, kmax=kmax, tol=mp.mpf("1e-12"), maxsteps=80, resid_max=mp.mpf("1e-8"))
                close = abs(r - seed) < 0.3 * abs(seed)
                OUT[str(B)]["rows"].append([kmax, ninv, float(mp.re(r)), float(mp.im(r)), bool(close), time.time() - t0])
                print(f"  B={B} kmax={kmax} inv={ninv}: {mp.nstr(r, 9)}  omega*B={mp.nstr(r * B, 6)}  close_to_seed={close}  ({time.time() - t0:.0f}s)", flush=True)
                if close and kmax >= 32000:
                    found = r
            except Exception as e:
                OUT[str(B)]["rows"].append([kmax, ninv, None, None, False, time.time() - t0])
                print(f"  B={B} kmax={kmax} inv={ninv}: FAIL {str(e)[:60]}  ({time.time() - t0:.0f}s)", flush=True)
            pathlib.Path("results/p24_gap_check.json").write_text(json.dumps(OUT, indent=1))
    if found is not None:
        prev = found + slope * mp.mpf("0.5") if B < 4.0 else found
print("done", flush=True)
