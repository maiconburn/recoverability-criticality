"""P23.2 second stage: the tracks of p23_kerr_extrap.py (deep caps,
step 0.01) leave only 2-3 points inside the frozen fitting window
0.01 <= Re(omega M) <= 0.04. This stage densifies the window to a
spacing of 0.0025 in spin with the same deep instrument, performs the
blind cubic and fold fits on window points ONLY, writes them to disk,
and only then computes the deep endpoint. Output: the same JSON,
keys 'window', 'blind', 'deep', 'verdict' per sequence.
"""
import json
import pathlib
import time

import numpy as np
from qnm.nearby import NearbyRootFinder
from scipy.optimize import least_squares

CAPS = (100_000, 400_000, 1_000_000, 4_000_000)
JS = pathlib.Path("results/p23_kerr_extrap.json")


def find(a, guess, n_inv, m, A0, Nr_max):
    f = NearbyRootFinder(a=a, s=-2, m=m, A0=A0, l_max=20, omega_guess=guess, tol=1e-13,
                         cf_tol=1e-13, n_inv=n_inv, Nr=300, Nr_min=300, Nr_max=Nr_max)
    return complex(f.do_solve()), complex(f.A)


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


def fits(win):
    A = np.array([a for a, _ in win]); R = np.array([w.real for _, w in win]); I = np.array([w.imag for _, w in win])

    def cubic_res(p):
        a0, c1, c2, c3 = p
        d = a0 - A
        return c1 * d + c2 * d ** 2 + c3 * d ** 3 - R

    def fold_res(p):
        a0, s = p
        return s * (a0 - A) - R ** 2

    slope = abs((R[-1] - R[-2]) / (A[-1] - A[-2]))
    cub = least_squares(cubic_res, [A[-1] + R[-1] / slope, slope, -30, 300], xtol=1e-15, ftol=1e-15, max_nfev=20000)
    fold = least_squares(fold_res, [A[-1] + R[-1] ** 2 / 0.05, 0.05], xtol=1e-15, ftol=1e-15, max_nfev=20000)
    pI = np.polyfit(A[-3:], I[-3:], 1)
    return {"n_pts": len(win), "a_range": [float(A[0]), float(A[-1])], "Re_range": [float(R[0]), float(R[-1])],
            "cubic": {"a0": float(cub.x[0]), "coef": [float(x) for x in cub.x[1:]], "rms": float(np.sqrt(np.mean(cub.fun ** 2)))},
            "fold": {"a0": float(fold.x[0]), "s": float(fold.x[1]), "rms": float(np.sqrt(np.mean(fold.fun ** 2)))},
            "Im_at_a0_cubic": float(np.polyval(pI, cub.x[0]))}


CZ = {"{2,0,10_0}": (0.391144, -2.50000), "{2,0,11_0}": (0.438874, -2.75000), "{2,-2,14_0}": (0.611751, -3.61439)}
MN = {"{2,0,10_0}": (0, 10), "{2,0,11_0}": (0, 11), "{2,-2,14_0}": (-2, 14)}
t0 = time.time()
OUT = json.loads(JS.read_text())
for label, rec in OUT.items():
    if "path" not in rec:
        continue
    m, n = MN[label]
    path = [(a, complex(r, i)) for a, r, i, g in rec["path"] if g]
    inwin = [(a, w) for a, w in path if 0.01 <= w.real <= 0.04]
    lo = max(a for a, w in path if w.real > 0.04) if any(w.real > 0.04 for _, w in path) else path[0][0]
    hi = min(a for a, w in path if w.real < 0.01) if any(w.real < 0.01 for _, w in path) else path[-1][0]
    grid = np.arange(lo, hi + 1e-9, 0.0025)
    known = {round(a, 6): w for a, w in path}
    win = dict((round(a, 6), w) for a, w in inwin)
    # A0 for the angular problem: recover from a nearby solve
    A = None
    for a in grid:
        ar = round(float(a), 6)
        if ar in known:
            continue
        near = min(known, key=lambda x: abs(x - ar))
        guess = known[near]
        try:
            if A is None:
                _, A = find(near, guess, n, m, 4.0 if m == 0 else 4.0, 100_000)
        except Exception:
            A = 4.0
        res = deep(float(a), guess, n, m, A)
        if res is None or not res[2]:
            print(f"  {label} a={a:.4f}: {'none' if res is None else 'unconverged'}", flush=True)
            continue
        w, A = res[0], res[1]
        known[ar] = w
        if 0.01 <= w.real <= 0.04:
            win[ar] = w
        print(f"  {label} a={a:.4f}: omega={w:.8f} cap={res[3]}", flush=True)
    winl = sorted(win.items())
    rec["window"] = [[a, w.real, w.imag] for a, w in winl]
    bl = fits(winl)
    rec["blind"] = bl
    print(f"  {label} BLIND: {json.dumps(bl)}", flush=True)
    JS.write_text(json.dumps(OUT, indent=1))
    # deep endpoint, after the blind numbers are on disk
    a0c = bl["cubic"]["a0"]
    pts = sorted([(a, w) for a, w in known.items() if w.real < 0.01])
    a_last, w_last = pts[-1] if pts else winl[-1]
    for frac in (0.4, 0.6, 0.75, 0.85, 0.92):
        an = a_last + frac * (a0c - a_last)
        if len(pts) >= 2:
            (a1, w1), (a2, w2) = pts[-2], pts[-1]
            guess = w2 + (w2 - w1) * (an - a2) / (a2 - a1)
        else:
            guess = w_last
        res = deep(an, guess, n, m, A)
        if res is None or not res[2]:
            print(f"  {label} deep a={an:.5f}: {'none' if res is None else 'unconverged'}", flush=True)
            continue
        pts.append((an, res[0]))
        print(f"  {label} deep a={an:.5f}: omega={res[0]:.9f} cap={res[3]}", flush=True)
    (a1, w1), (a2, w2) = pts[-2], pts[-1]
    a0_deep = a2 - w2.real * (a2 - a1) / (w2.real - w1.real)
    im_deep = w2.imag + (w2.imag - w1.imag) * (a0_deep - a2) / (a2 - a1)
    rec["deep"] = {"points": [[a, w.real, w.imag] for a, w in pts], "a0": a0_deep, "Im_at_a0": im_deep}
    rec["verdict"] = {"cubic_err": a0c - a0_deep, "fold_err": bl["fold"]["a0"] - a0_deep, "Im_err": bl["Im_at_a0_cubic"] - im_deep,
                      "CZ": CZ[label], "cubic_vs_CZ": a0c - CZ[label][0], "deep_vs_CZ": a0_deep - CZ[label][0]}
    print(f"  {label} VERDICT: cubic a0 {a0c:.5f} vs deep {a0_deep:.5f} (err {a0c - a0_deep:+.2e}); fold a0 {bl['fold']['a0']:.5f} (err {bl['fold']['a0'] - a0_deep:+.2e}); Im {bl['Im_at_a0_cubic']:.5f} vs deep {im_deep:.5f} (err {bl['Im_at_a0_cubic'] - im_deep:+.1e}); CZ {CZ[label]}", flush=True)
    JS.write_text(json.dumps(OUT, indent=1))
print(f"done ({time.time() - t0:.0f}s)", flush=True)
