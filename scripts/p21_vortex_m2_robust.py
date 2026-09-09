"""P21 supplementary: robust tracking of the counter-rotating m = -2 (and
optionally m = -1) overtones with inversion fallback.

Instrument lesson (2026-09-09): the n-th inversion of Leaver's continued
fraction can lose a genuine root through a pole-zero cancellation (the
m = -2, n = 1 mode was lost by the n = 1 inversion at B ~ 1.012 while the
n = 0, 2, 3, 4 inversions all still hold it). A root is accepted only if
at least two inversions agree on it (within 1e-6).

Usage: uv run python scripts/p21_vortex_m2_robust.py [m] [Bmax]
"""
import json
import pathlib
import sys
import time

import mpmath as mp

sys.path.insert(0, "src")
from recoverability_ep.dbt import find_qnm  # noqa

mp.mp.dps = 24
M = int(sys.argv[1]) if len(sys.argv) > 1 else -2
BMAX = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
NLIST = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
OUT = pathlib.Path(f"results/p21_vortex_m{M}_robust" + (("_n" + "-".join(map(str, NLIST))) if NLIST else "") + ".json")

SEEDS = {-1: [(0.406832619667, -0.341236118126), (0.197485919888, -1.23279178598),
              (0.0917790615406, -2.24612961199), (0.03497384613, -3.259712193)],
         -2: [(0.95272809, -0.3507395), (0.78558261, -1.1248441),
              (0.58230954, -2.0623411), (0.45138674, -3.078413)]}


def robust_find(seed, m, B, n_pref, kmax=600):
    """Find the root nearest the seed that at least two inversions agree
    on (within 1e-6). Bug fixed 2026-09-09: the first version returned
    the first agreeing pair, which near B ~ 1.2 for m = -2 was the
    fundamental found by the n = 0 and n = 1 inversions, far from the
    seed, so the tracker stalled."""
    order = [n_pref] + [n for n in range(6) if n != n_pref]
    found = []
    for n in order:
        try:
            r = find_qnm(seed, m, B, n=n, kmax=kmax, tol=mp.mpf("1e-12"), maxsteps=80)
        except Exception:
            continue
        for item in found:
            if abs(r - item[0]) < 1e-6:
                item[1].append(n)
                break
        else:
            found.append([r, [n]])
    agreed = [r for r, ns in found if len(ns) >= 2]
    if not agreed:
        return None
    return min(agreed, key=lambda r: abs(r - seed))


def seeds_at_B0(m, nmax=5):
    """B = 0 seeds for |m| from eikonal guesses omega ~ |m|/2 - i(2n+1)/(2 sqrt 2),
    refined by the continued fraction with two-inversion agreement."""
    out = []
    for n in range(nmax):
        g = mp.mpc(abs(m) / 2 * (1 - 0.12 * n), -(2 * n + 1) / (2 * mp.sqrt(2)) * 0.92)
        w = None
        for dr in (0, -0.15, 0.15, -0.3, 0.3):
            for di in (0, 0.15, -0.15):
                w = robust_find(g + mp.mpc(dr, di), abs(m), 0.0, n)
                if w is not None and all(abs(w - x) > 1e-4 for x in out):
                    break
                w = None
            if w is not None:
                break
        out.append(w)
    print(f"m={m} B=0 seeds: {[mp.nstr(w, 8) if w else None for w in out]}", flush=True)
    return [(float(mp.re(w)), float(mp.im(w))) if w else None for w in out]


def track(m, n, w0, B_end, dB=0.01, max_jump=0.08, min_dB=1e-5):
    path = [(mp.mpf(0), mp.mpc(*w0))]
    B, w = mp.mpf(0), mp.mpc(*w0)
    step = mp.mpf(dB)
    while B < B_end:
        Bn = min(B + step, mp.mpf(B_end))
        if len(path) >= 2:
            (B1, w1), (B2, w2) = path[-2], path[-1]
            seed = w2 + (w2 - w1) * (Bn - B2) / (B2 - B1)
        else:
            seed = w
        wn = robust_find(seed, m, Bn, n)
        if wn is None or abs(wn - w) > max(max_jump * min(1, abs(w) / mp.mpf("0.3")), mp.mpf("0.25") * abs(w)) or mp.re(wn) * mp.re(w) < 0:
            step /= 2
            if step < min_dB:
                break
            continue
        B, w = Bn, wn
        path.append((B, w))
        step = min(step * mp.mpf("1.5"), mp.mpf(dB))
        if mp.re(w) < 1e-7:
            break
    return path


res = {"m": M, "Bmax": BMAX, "started": time.strftime("%Y-%m-%d %H:%M:%S")}
seeds = SEEDS[M] if M in SEEDS else seeds_at_B0(M)
for n, w0 in enumerate(seeds):
    if w0 is None or (NLIST is not None and n not in NLIST) or (NLIST is None and n == 0):
        continue
    t0 = time.time()
    path = track(M, n, w0, BMAX)
    Bs = [float(b) for b, _ in path]
    Re = [float(mp.re(w)) for _, w in path]
    Im = [float(mp.im(w)) for _, w in path]
    slopes = [(Re[i] - Re[i - 1]) / (Bs[i] - Bs[i - 1]) for i in range(max(1, len(Bs) - 6), len(Bs))]
    arrived = Re[-1] < 1e-5 and Bs[-1] < BMAX - 1e-9
    Bc_lin = None
    if arrived and len(Bs) >= 2 and Re[-1] != Re[-2]:
        Bc_lin = Bs[-1] - Re[-1] * (Bs[-1] - Bs[-2]) / (Re[-1] - Re[-2])
    res[f"n{n}"] = {"path": [[b, r, i] for b, r, i in zip(Bs, Re, Im)], "last_B": Bs[-1],
                    "omega_last": [Re[-1], Im[-1]], "arrived_at_axis": arrived, "Bc_linear_extrap": Bc_lin,
                    "last_slopes_dRe_dB": slopes, "seconds": time.time() - t0}
    print(f"m={M} n={n}: {len(path)} pts, last B={Bs[-1]:.5f} omega={Re[-1]:.6f}{Im[-1]:+.6f}i "
          f"arrived={arrived} Bc_lin={Bc_lin} slopes={['%.4f' % s for s in slopes]} ({time.time()-t0:.0f}s)", flush=True)
    OUT.write_text(json.dumps(res, indent=1))
print("done", flush=True)
