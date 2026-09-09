"""P21g.2: is there a finite-B principal-sheet mode near c_3/B for m = -5
(c_3 = 0.2963 - 1.5861i, the fourth pure-vortex resonance), and does it
have a B = 0 ancestor or is it born from the branch cut?

Steps: at B = 10 and B = 20 search near c_3/B with inversions 0..5 and
kmax 1500 / 3000 (accept if the two agree to 1e-4 relative and at least
two inversions agree); then track the root DOWNWARD in B with the
kmax-1500 continued fraction (multi-inversion agreement, relative jump
guard) until it either reaches the axis (birth point B_b) or reaches a
B = 0 overtone.
"""
import json
import pathlib
import sys

import mpmath as mp

sys.path.insert(0, "src")
from recoverability_ep.dbt import find_qnm  # noqa

mp.mp.dps = 30
M = -5
C3 = mp.mpc("0.2963", "-1.5861")
OUT = {}


def search(B, target, kmax, rel=0.3):
    found = []
    for fr in (0.7, 1.0, 1.3):
        for fi in (0.7, 1.0, 1.3):
            seed = mp.mpc(mp.re(target) * fr, mp.im(target) * fi)
            for n in range(6):
                try:
                    r = find_qnm(seed, M, B, n=n, kmax=kmax, tol=mp.mpf("1e-13"), maxsteps=60)
                except Exception:
                    continue
                if abs(r - target) > rel * abs(target):
                    continue
                for item in found:
                    if abs(r - item[0]) < 1e-6:
                        item[1].add(n)
                        break
                else:
                    found.append([r, {n}])
    return [(r, sorted(ns)) for r, ns in found if len(ns) >= 2]


for B in (10.0, 20.0):
    target = C3 / B
    r1 = search(B, target, 1500)
    r3 = search(B, target, 3000)
    print(f"B={B}: target {mp.nstr(target, 6)}; kmax1500 {[(mp.nstr(r, 8), ns) for r, ns in r1]}; kmax3000 {[(mp.nstr(r, 8), ns) for r, ns in r3]}", flush=True)
    matched = []
    for r, ns in r1:
        for r3_, ns3 in r3:
            if abs(r - r3_) < 1e-4 * abs(r):
                matched.append((r3_, ns, ns3))
    OUT[str(B)] = {"target": [float(mp.re(target)), float(mp.im(target))],
                   "k1500": [[float(mp.re(r)), float(mp.im(r)), ns] for r, ns in r1],
                   "k3000": [[float(mp.re(r)), float(mp.im(r)), ns] for r, ns in r3],
                   "kmax_independent": [[float(mp.re(r)), float(mp.im(r))] for r, _, _ in matched]}
    print(f"   kmax-independent roots: {[mp.nstr(r, 8) for r, _, _ in matched]}", flush=True)

# downward tracking from B = 10 if a root exists there
if OUT["10.0"]["kmax_independent"]:
    w = mp.mpc(*OUT["10.0"]["kmax_independent"][0])
    B = mp.mpf(10)
    path = [(B, w)]
    step = mp.mpf("0.5")
    while B > mp.mpf("0.05"):
        Bn = max(B - step, mp.mpf("0.05"))
        seed = w if len(path) < 2 else path[-1][1] + (path[-1][1] - path[-2][1]) * (Bn - path[-1][0]) / (path[-1][0] - path[-2][0])
        cands = []
        for n in range(6):
            try:
                r = find_qnm(seed, M, Bn, n=n, kmax=1500, tol=mp.mpf("1e-12"), maxsteps=60)
            except Exception:
                continue
            for it in cands:
                if abs(r - it[0]) < 1e-6:
                    it[1] += 1
                    break
            else:
                cands.append([r, 1])
        ok = [r for r, k in cands if k >= 2 and abs(r - w) < mp.mpf("0.3") * abs(w) + mp.mpf("0.01")]
        if not ok or mp.re(min(ok, key=lambda r: abs(r - seed))) < 0:
            step /= 2
            if step < mp.mpf("1e-3"):
                break
            continue
        w = min(ok, key=lambda r: abs(r - seed))
        B = Bn
        path.append((B, w))
        step = min(step * mp.mpf("1.5"), mp.mpf("0.5"))
        if mp.re(w) < mp.mpf("1e-4"):
            break
    OUT["downward"] = [[float(b), float(mp.re(x)), float(mp.im(x))] for b, x in path]
    print(f"downward track: {len(path)} pts, ends at B={mp.nstr(B, 6)} omega={mp.nstr(w, 8)}", flush=True)
    for b, x in path[::max(1, len(path) // 12)] + path[-2:]:
        print(f"   B={mp.nstr(b, 5)} omega={mp.nstr(x, 7)}", flush=True)
pathlib.Path("results/p21g_born_mode.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
