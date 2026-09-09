"""m = -7, n = 6: deep re-track (kmax 2000, gate 4000, inversions 5..7,
relative jump guard) upward from the last reliable kmax-600 point
B = 0.525 (0.5478 - 3.8847i) until Re(omega) -> 0 (arrival at the cut)
or B = 3. Output: results/p23_m7_n6_track.json.
"""
import json
import pathlib
import sys

import mpmath as mp

sys.path.insert(0, "src")
from recoverability_ep.dbt import find_qnm  # noqa

mp.mp.dps = 40
M, N = -7, 6


def deep(seed, B, kmax):
    found = []
    for ninv in (N - 1, N, N + 1):
        try:
            r = find_qnm(seed, M, B, n=ninv, kmax=kmax, tol=mp.mpf("1e-11"), maxsteps=80, resid_max=mp.mpf("1e-9"))
        except Exception:
            continue
        if mp.re(r) <= 0 or abs(r - seed) > 0.25 * abs(seed) + 0.02:
            continue
        for it in found:
            if abs(r - it[0]) < 1e-7:
                it[1].add(ninv)
                break
        else:
            found.append([r, {ninv}])
    ok = [(r, sorted(ns)) for r, ns in found if len(ns) >= 2]
    return min(ok, key=lambda t: abs(t[0] - seed)) if ok else None


path = [(mp.mpf("0.525"), mp.mpc("0.5478", "-3.8847"))]
B, w = path[-1]
step = mp.mpf("0.05")
while B < 3 and step > mp.mpf("1e-4"):
    Bn = B + step
    if len(path) >= 2:
        (b1, w1), (b2, w2) = path[-2], path[-1]
        seed = w2 + (w2 - w1) * (Bn - b2) / (b2 - b1)
    else:
        seed = w
    r3 = deep(seed, Bn, 2000)
    if r3 is None:
        step /= 2
        continue
    r6 = deep(r3[0], Bn, 4000)
    gate = r6 is not None and abs(r6[0] - r3[0]) < 2e-3 * abs(r3[0])   # near the axis the fraction converges slowly in kmax; 2e-3 between 2000 and 4000 terms
    if not gate:
        print(f"  B={float(Bn):.5f}: kmax gate failed ({r3[0]} vs {r6[0] if r6 else None}); halving", flush=True)
        step /= 2
        continue
    B, w = Bn, r6[0]
    path.append((B, w))
    print(f"  B={float(B):.5f}: omega = {mp.nstr(w, 8)}  inversions {r6[1]}", flush=True)
    step = min(step * mp.mpf("1.5"), mp.mpf("0.05"))
    if mp.re(w) < mp.mpf("1e-2"):
        break
pts = [(float(b), float(mp.re(x)), float(mp.im(x))) for b, x in path]
if len(pts) >= 3:
    (b1, r1, _), (b2, r2, _) = pts[-2], pts[-1]
    Bc = b2 - r2 * (b2 - b1) / (r2 - r1)
    slopes = [(pts[i][1] - pts[i - 1][1]) / (pts[i][0] - pts[i - 1][0]) for i in range(max(1, len(pts) - 6), len(pts))]
    print(f"  arrival: B_c (linear extrapolation) = {Bc:.4f}; last slopes {[round(s, 3) for s in slopes]}; Im at last point {pts[-1][2]:.4f}", flush=True)
else:
    Bc, slopes = None, []
pathlib.Path("results/p23_m7_n6_track.json").write_text(json.dumps({"path": pts, "Bc_linear": Bc, "last_slopes": slopes}, indent=1))
print("done", flush=True)
