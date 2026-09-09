"""Map all continued-fraction roots near the negative imaginary axis for
m = -3 in the window Re in [-0.02, 0.08], Im in [-1.0, -0.25], at several
rotations, to resolve the m = -3 n = 2 trajectory (tracker gave a
non-monotonic Re near the axis for B in [1.5, 4.7]). Two-inversion
agreement or all-inversion zero required; kmax 1500, 30 digits."""
import json, sys, itertools
import mpmath as mp
sys.path.insert(0, "src")
from recoverability_ep.dbt import find_qnm, leaver_function
mp.mp.dps = 30
M = -3
out = {}
for B in (1.30, 1.45, 1.52, 1.56, 1.65, 1.8, 2.0, 2.4, 3.0, 4.0, 4.68):
    roots = {}
    for re0, im0 in itertools.product([-0.01, 0.005, 0.02, 0.05], [-0.3, -0.45, -0.6, -0.75, -0.9]):
        for n in range(6):
            try:
                r = find_qnm(mp.mpc(re0, im0), M, B, n=n, kmax=1500, tol=mp.mpf("1e-14"), maxsteps=80)
            except Exception:
                continue
            if not (-0.02 <= mp.re(r) <= 0.08 and -1.0 <= mp.im(r) <= -0.25):
                continue
            key = None
            for k in roots:
                if abs(r - roots[k]["w"]) < 1e-6:
                    key = k
                    break
            if key is None:
                key = mp.nstr(r, 8)
                roots[key] = {"w": r, "inv": set()}
            roots[key]["inv"].add(n)
    rows = []
    for k, v in roots.items():
        small = 0
        for kk in range(6):
            try:
                if abs(leaver_function(v["w"], M, B, kk, 1500)) < 1e-3:
                    small += 1
            except ZeroDivisionError:
                pass
        genuine = len(v["inv"]) >= 2 or small >= 5
        rows.append({"omega": [float(mp.re(v["w"])), float(mp.im(v["w"]))], "inversions": sorted(v["inv"]), "small": small, "genuine": genuine})
    out[str(B)] = rows
    print(f"B={B}: " + "; ".join(f"{r['omega'][0]:+.5f}{r['omega'][1]:+.4f}i[{'G' if r['genuine'] else 'a'} inv{r['inversions']} s{r['small']}]" for r in rows), flush=True)
json.dump(out, open("results/p21_m3_axis_map.json", "w"), indent=1)
print("done", flush=True)
