"""P23.2: the analytic arrival law as a blind predictor of Kerr NIA
endpoints (frozen in results/FROZEN_P23_TOWER_LAW.md).

For {2,0,10_0}, {2,0,11_0}, {2,-2,14_0}: track upward in spin from
the Schwarzschild limit with the P22 deep discipline (three-inversion
agreement, consecutive caps 1e5..4e6 agreeing to 2e-6; the 48000 gate of
the main P22 run already fails at Re ~ 0.03-0.07 for n >= 10) until Re(omega) < 0.008 or the deep caps
stop converging; fit a cubic Re = c1 d + c2 d^2 + c3 d^3 (d = a0 - a, a0 free)
and a fold Re^2 = s (a0 - a) to the gated points with
0.01 <= Re <= 0.04 ONLY; record both predictions of a0 and the
linear extrapolation of Im to a0 BEFORE computing the deep endpoint
(caps 1e5..4e6). Output: results/p23_kerr_extrap.json.
"""
import json
import math
import pathlib
import time

import numpy as np
from qnm.nearby import NearbyRootFinder
from scipy.optimize import least_squares

CAPS = (100_000, 400_000, 1_000_000, 4_000_000)


def find(a, guess, n_inv, m, A0, Nr_max):
    f = NearbyRootFinder(a=a, s=-2, m=m, A0=A0, l_max=20, omega_guess=guess, tol=1e-13,
                         cf_tol=1e-13, n_inv=n_inv, Nr=300, Nr_min=300, Nr_max=Nr_max)
    return complex(f.do_solve()), complex(f.A)


def gated(a, guess, n, m, A0, near):
    vals = []
    for n_inv in (n - 1, n, n + 1):
        try:
            w, A = find(a, guess, n_inv, m, A0, 16000)
        except Exception:
            continue
        if abs(w - guess) < near and w.real > 0:
            vals.append((w, A))
    if len(vals) < 2:
        return None
    w0, A0_ = vals[0]
    ok = [v for v in vals if abs(v[0] - w0) < 1e-6]
    if len(ok) < 2:
        for i in range(len(vals)):
            for j in range(i + 1, len(vals)):
                if abs(vals[i][0] - vals[j][0]) < 1e-6:
                    w0, A0_ = vals[i]
                    break
        else:
            return None
    try:
        w48, _ = find(a, w0, n, m, A0_, 48000)
        gate = abs(w48 - w0) < 1e-6 * max(abs(w0), 1e-3)
    except Exception:
        gate = False
    return w0, A0_, gate


def deep(a, guess, n, m, A0):
    prev = None
    for cap in CAPS:
        vals = []
        for n_inv in (n - 1, n, n + 1):
            try:
                w, A = find(a, guess, n_inv, m, A0, cap)
            except Exception:
                continue
            if abs(w - guess) < 0.5 * abs(guess) + 0.02 and w.real > 0:
                vals.append((w, A))
        if not vals:
            continue
        w, A = min(vals, key=lambda t: abs(t[0] - guess))
        if prev is not None and abs(w - prev[0]) < 2e-6 * abs(w):
            return w, A, True, cap
        prev = (w, A)
    return (prev[0], prev[1], False, CAPS[-1]) if prev else None


def schwarzschild_seed(n, m, guesses):
    for g in guesses:
        for n_inv in (n, n - 1, n + 1):
            try:
                w, A = find(0.01, g, n_inv, m, 4.0, 16000)
            except Exception:
                continue
            if abs(w - g) < 0.15 and w.real > 0:
                return w, A
    return None


def track(m, n, w0, A0, da, label):
    path = [(0.01, w0, A0, True)]
    a, w, A, step = 0.01, w0, A0, da
    while True:
        an = a + step
        if len(path) >= 2:
            (a1, w1, _, _), (a2, w2, _, _) = path[-2], path[-1]
            seed = w2 + (w2 - w1) * (an - a2) / (a2 - a1)
        else:
            seed = w
        res = deep(an, seed, n, m, A)          # the 48000 gate fails at Re ~ 0.03-0.07 for n >= 10
        if res is None or not res[2] or abs(res[0] - seed) > 0.25 * abs(w) + 0.01:
            step /= 2
            if step < 2e-5:
                break
            continue
        w, A, g = res[0], res[1], res[2]
        a = an
        path.append((a, w, A, g))
        step = min(step * 1.5, da)
        if w.real < 0.008 or not g:
            break
    print(f"  track {label}: {len(path)} pts, last a={a:.5f} omega={w:.6f} gate={g}", flush=True)
    return path


def blind_fits(path):
    sel = [(a, w) for a, w, _, g in path if g and 0.01 <= w.real <= 0.04]
    if len(sel) < 5:
        return None
    A = np.array([a for a, _ in sel]); R = np.array([w.real for _, w in sel]); I = np.array([w.imag for _, w in sel])

    def cubic_res(p):
        a0, c1, c2, c3 = p
        d = a0 - A
        return c1 * d + c2 * d ** 2 + c3 * d ** 3 - R

    def fold_res(p):
        a0, s = p
        return s * (a0 - A) - R ** 2

    a_guess = A[-1] + R[-1] / abs((R[-1] - R[-2]) / (A[-1] - A[-2]))
    cub = least_squares(cubic_res, [a_guess, 1.5, -30, 300], xtol=1e-14, ftol=1e-14)
    fold = least_squares(fold_res, [A[-1] + R[-1] ** 2 / 0.05, 0.05], xtol=1e-14, ftol=1e-14)
    a0c, a0f = cub.x[0], fold.x[0]
    # Im at a0: linear extrapolation in a from the last three selected points
    pI = np.polyfit(A[-3:], I[-3:], 1)
    return {"n_pts": len(sel), "a_range": [float(A[0]), float(A[-1])], "Re_range": [float(R[0]), float(R[-1])],
            "cubic": {"a0": float(a0c), "coef": [float(x) for x in cub.x[1:]], "rms": float(np.sqrt(np.mean(cub.fun ** 2)))},
            "fold": {"a0": float(a0f), "s": float(fold.x[1]), "rms": float(np.sqrt(np.mean(fold.fun ** 2)))},
            "Im_at_a0_cubic": float(np.polyval(pI, a0c))}


t0 = time.time()
OUT = {}
CASES = [
    ("{2,0,10_0}", 0, 10, [0.0600 - 2.5530j, 0.055 - 2.55j, 0.065 - 2.56j], 0.01),
    ("{2,0,11_0}", 0, 11, [0.0568 - 2.8035j, 0.052 - 2.80j, 0.06 - 2.81j], 0.01),
    ("{2,-2,14_0}", -2, 14, [0.0863 - 3.5720j, 0.08 - 3.57j, 0.09 - 3.58j, 0.075 - 3.55j], 0.02),
]
CZ = {"{2,0,10_0}": (0.391144, -2.50000), "{2,0,11_0}": (0.438874, -2.75000), "{2,-2,14_0}": (0.611751, -3.61439)}
for label, m, n, guesses, da in CASES:
    seed = schwarzschild_seed(n, m, guesses)
    print(f"  {label}: Schwarzschild seed {seed[0] if seed else None}", flush=True)
    if not seed:
        OUT[label] = {"error": "no seed"}
        continue
    p = track(m, n, seed[0], seed[1], da, label)
    fits = blind_fits(p)
    print(f"  {label} blind fits: {json.dumps(fits)}", flush=True)
    rec = {"path": [[a, w.real, w.imag, g] for a, w, _, g in p], "blind": fits}
    OUT[label] = rec
    pathlib.Path("results/p23_kerr_extrap.json").write_text(json.dumps(OUT, indent=1))
    # now the deep endpoint (after the blind numbers are on disk)
    if fits:
        a0c = fits["cubic"]["a0"]
        pts = []
        w, A = p[-1][1], p[-1][2]
        a = p[-1][0]
        for frac in (0.5, 0.7, 0.8, 0.88, 0.93):
            an = a + frac * (a0c - a)
            if len(pts) >= 2:
                (a1, w1), (a2, w2) = pts[-2], pts[-1]
                guess = w2 + (w2 - w1) * (an - a2) / (a2 - a1)
            else:
                guess = w
            res = deep(an, guess, n, m, A)
            if res is None or not res[2]:
                print(f"  {label} deep a={an:.5f}: {'none' if res is None else 'unconverged'}", flush=True)
                continue
            w, A = res[0], res[1]
            pts.append((an, w))
            print(f"  {label} deep a={an:.5f}: omega={w:.9f} cap={res[3]}", flush=True)
        if len(pts) >= 2:
            (a1, w1), (a2, w2) = pts[-2], pts[-1]
            a0_deep = a2 - w2.real * (a2 - a1) / (w2.real - w1.real)
            im_deep = w2.imag + (w2.imag - w1.imag) * (a0_deep - a2) / (a2 - a1)
            rec["deep"] = {"points": [[a, w.real, w.imag] for a, w in pts], "a0": a0_deep, "Im_at_a0": im_deep}
            rec["verdict"] = {"cubic_err": a0c - a0_deep, "fold_err": fits["fold"]["a0"] - a0_deep,
                              "Im_err": fits["Im_at_a0_cubic"] - im_deep, "CZ": CZ[label],
                              "cubic_vs_CZ": a0c - CZ[label][0], "deep_vs_CZ": a0_deep - CZ[label][0]}
            print(f"  {label} VERDICT: cubic a0 {a0c:.5f} vs deep {a0_deep:.5f} (err {a0c - a0_deep:+.2e}); fold a0 {fits['fold']['a0']:.5f} (err {fits['fold']['a0'] - a0_deep:+.2e}); Im {fits['Im_at_a0_cubic']:.5f} vs deep {im_deep:.5f}; CZ {CZ[label]}", flush=True)
    pathlib.Path("results/p23_kerr_extrap.json").write_text(json.dumps(OUT, indent=1))
print(f"done ({time.time() - t0:.0f}s)", flush=True)
