"""P23.1 towers with the complex-ray scaled solver (dbt_scaled.wronskian_cplx,
find_c_cplx): inner solution integrated along rho = r e^{-i theta}, where
the physical branch is dominant, so the deep members are no longer
cutoff-sensitive (the real-axis solver of P21f-h was contaminated by
admixture for members with |Im c| > ~2; e.g. m = -7, n = 5 moved from
0.1425-2.4185i to 0.0696-2.4303i, which the action-WKB predicts at
0.0681-2.4245i). Seeds: the action-WKB tower (results/p23_action_wkb.json)
and, for |m| <= 7, the old exact values. Each root is verified at
theta = 0.5 and 0.8 and at rho_m = 1.0 and 0.7 (agreement to 1e-4).
Usage: p23_tower_cplx.py m1,m2,...  -> results/p23_tower_cplx_m{M}.json
"""
import json
import pathlib
import sys
import time

sys.path.insert(0, "src")
from recoverability_ep.dbt_scaled import find_c_cplx  # noqa

MS = [int(x) for x in sys.argv[1].split(",")]
aw = json.loads(pathlib.Path("results/p23_action_wkb.json").read_text())


def robust(seed, m):
    vals = []
    for kw in ({"theta": 0.5, "rho_m": 1.0}, {"theta": 0.8, "rho_m": 1.0}, {"theta": 0.5, "rho_m": 0.7}):
        try:
            c, res = find_c_cplx(seed, m, rtol=1e-12, **kw)
            if res < 1e-7:
                vals.append(c)
        except Exception:
            pass
    if len(vals) < 2:
        return None
    spread = max(abs(a - b) for a in vals for b in vals)
    return vals[0], spread


for m in MS:
    t0 = time.time()
    rows = aw[str(m)]["rows"]
    members = []
    for r in rows:
        n = r["n"]
        seeds = []
        if r.get("exact"):
            seeds.append(complex(*r["exact"]))
        if r.get("action_wkb"):
            seeds.append(complex(*r["action_wkb"]))
        found = None
        for s in seeds:
            res = robust(s, m)
            if res is not None and res[1] < 1e-3 and abs(res[0] - s) < 0.3:
                found = res
                break
        if found is None:
            print(f"  m={m} n={n}: no verified root from seeds {[f'{s:.3f}' for s in seeds]}", flush=True)
            members.append({"n": n, "root": None, "seeds": [[s.real, s.imag] for s in seeds]})
            continue
        c, spread = found
        w = complex(*r["action_wkb"]) if r.get("action_wkb") else None
        print(f"  m={m} n={n}: c = {c.real:.5f}{c.imag:+.5f}i (spread {spread:.0e}); action-WKB dev {abs(c - w) if w else float('nan'):.4f}; old {r.get('exact')}", flush=True)
        members.append({"n": n, "root": [c.real, c.imag], "spread": spread, "action_wkb": r.get("action_wkb"), "old_exact": r.get("exact")})
        if c.real < -0.5:
            break
    N = sum(1 for x in members if x["root"] and x["root"][0] > 0)
    print(f"  m={m}: N = {N}  ({time.time() - t0:.0f}s)", flush=True)
    pathlib.Path(f"results/p23_tower_cplx_m{m}.json").write_text(json.dumps({"m": m, "N": N, "members": members}, indent=1))
print("done", flush=True)
