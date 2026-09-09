"""P24.1: locate the crossing of the m = -7, n = 5 mode between B = 2.68
(root 0.044666 - 0.894802i, present) and B = 3.0 (no root from any
seed with up to 64000 terms). Secant continuation with tiny initial
steps (no Muller hops), fixed kmax 32000 at 50 digits, inversions 5
and 6, steps of 0.02 in B, halving when lost; the kmax-16000 value is
recorded alongside as the convergence indicator. Output:
results/p24_crossing.json.
"""
import json
import pathlib
import sys
import time

import mpmath as mp

sys.path.insert(0, "src")
from recoverability_ep.dbt import leaver_function  # noqa

mp.mp.dps = 50
M = -7


def secant(seed, B, ninv, kmax):
    f = lambda w: leaver_function(w, M, B, ninv, kmax)
    return mp.findroot(f, (mp.mpc(seed), mp.mpc(seed) + mp.mpc("1e-4", "5e-5")), solver="secant", tol=mp.mpf("1e-14"), maxsteps=60)


path = [(mp.mpf("2.67910"), mp.mpc("0.044666222", "-0.89480248"))]
B, w = path[-1]
step = mp.mpf("0.02")
OUT = {"path": [], "lost": []}
while B < mp.mpf("3.05") and step > mp.mpf("0.002"):
    Bn = B + step
    if len(path) >= 2:
        (b1, w1), (b2, w2) = path[-2], path[-1]
        seed = w2 + (w2 - w1) * (Bn - b2) / (b2 - b1)
    else:
        seed = w
    vals = {}
    t0 = time.time()
    for kmax in (16000, 32000):
        for ninv in (5, 6):
            try:
                r = secant(seed, Bn, ninv, kmax)
                if abs(r - seed) < 0.02 + 0.2 * abs(mp.re(seed)):
                    vals[(kmax, ninv)] = r
            except Exception:
                pass
    r32 = [v for (k, n), v in vals.items() if k == 32000]
    if not r32:
        OUT["lost"].append([float(Bn), float(mp.re(seed)), float(mp.im(seed)), {f"{k},{n}": [float(mp.re(v)), float(mp.im(v))] for (k, n), v in vals.items()}])
        print(f"  B={float(Bn):.4f}: no root near seed {mp.nstr(seed, 6)} (found {[(k, mp.nstr(v, 6)) for k, v in vals.items()]}); halving", flush=True)
        step /= 2
        continue
    r = min(r32, key=lambda v: abs(v - seed))
    r16 = vals.get((16000, 5), vals.get((16000, 6)))
    conv = abs(r - r16) / abs(r) if r16 is not None else None
    B, w = Bn, r
    path.append((B, w))
    OUT["path"].append([float(B), float(mp.re(w)), float(mp.im(w)), float(conv) if conv is not None else None])
    print(f"  B={float(B):.4f}: omega = {mp.nstr(w, 9)}  omega*B = {mp.nstr(w * B, 6)}  kmax16k/32k rel diff {conv if conv is None else float(conv):.1e}  ({time.time() - t0:.0f}s)", flush=True)
    pathlib.Path("results/p24_crossing.json").write_text(json.dumps(OUT, indent=1))
    if mp.re(w) < mp.mpf("0.003"):
        break
    step = min(step * mp.mpf("1.5"), mp.mpf("0.02"))
pts = OUT["path"]
if len(pts) >= 2:
    (b1, r1, *_), (b2, r2, *_) = pts[-2], pts[-1]
    Bc = b2 - r2 * (b2 - b1) / (r2 - r1) if r2 != r1 else None
    OUT["Bc_linear"] = Bc
    print(f"  last point B={b2:.4f} Re={r2:.5f}; linear-extrapolated B_c = {Bc}", flush=True)
pathlib.Path("results/p24_crossing.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
