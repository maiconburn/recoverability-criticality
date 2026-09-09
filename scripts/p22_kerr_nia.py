"""P22: Kerr overtone sequences arriving at the negative imaginary axis
(frozen in results/FROZEN_P22_KERR_NIA.md before this run).

Uses the qnm package's NearbyRootFinder with the P21 discipline:
three-inversion agreement and a truncation-cap gate (Nr_max 4000 vs
16000). Tracks {2,0,9_0} and {2,-2,13_0} upward in spin to their arrival,
measures the approach law, and searches the {2,0,9} gap and
re-emergence.
"""
import json
import math
import pathlib
import sys
import time

import numpy as np
from qnm.nearby import NearbyRootFinder

OUT = {}


def find(a, guess, n_inv, m, A0, Nr_max=4000):
    f = NearbyRootFinder(a=a, s=-2, m=m, A0=A0, l_max=20, omega_guess=guess, tol=1e-12,
                         cf_tol=1e-12, n_inv=n_inv, Nr=300, Nr_min=300, Nr_max=Nr_max)
    w = f.do_solve()
    return complex(w), complex(f.A)


def gated(a, guess, n, m, A0, near=None):
    """Three-inversion agreement at Nr_max = 16000 (at 4000 the inversions
    differ by ~1e-5, at 16000 by ~1e-9) + a deeper gate at 48000.
    Returns (omega, A, ok_gate)."""
    vals = []
    for n_inv in (n - 1, n, n + 1):
        try:
            w, A = find(a, guess, n_inv, m, A0, Nr_max=16000)
        except Exception:
            continue
        if near is not None and abs(w - guess) > near:
            continue
        vals.append((w, A, n_inv))
    if len(vals) < 2:
        return None
    w0, A0_, _ = vals[0]
    if any(abs(w - w0) > 1e-6 for w, _, _ in vals):   # inversions differ by ~1e-7 at Nr_max = 4000
        # pick the pair that agrees, if any
        for i in range(len(vals)):
            for j in range(i + 1, len(vals)):
                if abs(vals[i][0] - vals[j][0]) < 1e-6:
                    w0, A0_ = vals[i][0], vals[i][1]
                    break
        else:
            return None
    try:
        w48, _ = find(a, w0, n, m, A0_, Nr_max=48000)
        gate = abs(w48 - w0) < 1e-6 * max(abs(w0), 1e-3)
    except Exception:
        gate = False
    return w0, A0_, gate


def track(m, n, a0, w0, A0, a_end=0.99, da=0.01, label=""):
    path = [(a0, w0, A0, True)]
    a, w, A = a0, w0, A0
    gate = True
    step = da
    while a < a_end:
        an = min(a + step, a_end)
        if len(path) >= 2:
            (a1, w1, _, _), (a2, w2, _, _) = path[-2], path[-1]
            seed = w2 + (w2 - w1) * (an - a2) / (a2 - a1)
        else:
            seed = w
        res = gated(an, seed, n, m, A, near=0.25 * abs(w) + 0.01)
        if res is None or res[0].real <= 0:
            step /= 2
            if step < 2e-5:
                break
            continue
        w, A, gate = res
        a = an
        path.append((a, w, A, gate))
        step = min(step * 1.5, da)
        if w.real < 1e-6:
            break
    print(f"  track {label}: {len(path)} pts, last a={a:.6f} omega={w:.7f} gate={gate}", flush=True)
    return path


def approach(path):
    pts = [(a, w) for a, w, _, g in path if g and w.real > 0]
    if len(pts) < 4:
        return None
    (a1, w1), (a2, w2) = pts[-2], pts[-1]
    a0 = a2 - w2.real * (a2 - a1) / (w2.real - w1.real) if w2.real != w1.real else None
    slopes = [(pts[i][1].real - pts[i - 1][1].real) / (pts[i][0] - pts[i - 1][0]) for i in range(max(1, len(pts) - 6), len(pts))]
    expo = None
    if a0:
        sel = [(a, w) for a, w in pts if 1e-4 < (a0 - a) < 0.05]
        if len(sel) >= 3:
            xs = [math.log(a0 - a) for a, _ in sel]
            ys = [math.log(w.real) for _, w in sel]
            mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
            expo = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return {"a0_linear": a0, "Im_at_last": pts[-1][1].imag, "last_slopes": slopes, "exponent": expo,
            "last_pts": [[a, w.real, w.imag] for a, w in pts[-8:]]}


t0 = time.time()
# ---- P22.1: {2,0,9_0}
w, A = find(0.05, 0.0627 - 2.3016j, 9, 0, 4.0)
p = track(0, 9, 0.05, w, A, label="{2,0,9_0}")
OUT["P22.1"] = {"path": [[a, w.real, w.imag, g] for a, w, _, g in p], "approach": approach(p)}
print(f"  P22.1 approach: {OUT['P22.1']['approach']}", flush=True)
pathlib.Path("results/p22_kerr_nia.json").write_text(json.dumps(OUT, indent=1))

# ---- P22.3: gap and re-emergence for {2,0,9}
gap = {}
for a in (0.32, 0.34, 0.36, 0.38, 0.395, 0.405, 0.41, 0.42, 0.44):
    found = []
    for gr in (0.002, 0.01, 0.03):
        for gi in (-2.20, -2.25, -2.30, -2.35, -2.39, -2.43):
            res = gated(a, complex(gr, gi), 9, 0, 4.0, near=0.12)
            if res and res[2] and 0 < res[0].real < 0.05 and -2.45 < res[0].imag < -2.15:
                if all(abs(res[0] - f) > 1e-6 for f in found):
                    found.append(res[0])
    gap[str(a)] = [[f.real, f.imag] for f in found]
    print(f"  gap search a={a}: {[f'{f:.6f}' for f in found]}", flush=True)
OUT["P22.3"] = gap
pathlib.Path("results/p22_kerr_nia.json").write_text(json.dumps(OUT, indent=1))

# ---- P22.2: {2,-2,13_0}: locate the Schwarzschild n=13 first
seed = None
for g in (0.04 - 3.30j, 0.06 - 3.35j, 0.03 - 3.25j, 0.08 - 3.40j, 0.02 - 3.20j):
    for n_inv in (13, 12, 14):
        try:
            w, A = find(0.01, g, n_inv, -2, 4.0)
        except Exception:
            continue
        if -3.5 < w.imag < -3.1 and w.real > 0:
            seed = (w, A)
            break
    if seed:
        break
print(f"  n=13 seed at a=0.01: {seed}", flush=True)
if seed:
    p2 = track(-2, 13, 0.01, seed[0], seed[1], label="{2,-2,13_0}", da=0.02)
    OUT["P22.2"] = {"path": [[a, w.real, w.imag, g] for a, w, _, g in p2], "approach": approach(p2)}
    print(f"  P22.2 approach: {OUT['P22.2']['approach']}", flush=True)
pathlib.Path("results/p22_kerr_nia.json").write_text(json.dumps(OUT, indent=1))
print(f"done ({time.time()-t0:.0f}s)", flush=True)
