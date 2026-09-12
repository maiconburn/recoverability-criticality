"""P32.2 post-mortem (diagnostic, not a frozen prediction): is the 20-60%
residual of the fixed-frequency fit the branch-cut tail?

Refit the same windows with the tower columns PLUS a power-law column
t^-p (p = 1, 2, 3, the DBT tail exponents of a 1/r^2 potential) and
report the residual drop. If the tail explains it, the frozen 10%
threshold was the error, not the tower.
Output: results/p32d_tail_postmortem.json
"""
import glob
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, "src")
from recoverability_ep.dbt_td import evolve  # noqa

B = 10.0
towers = {}
for f in glob.glob("results/p23_tower_cplx_m*.json"):
    d = json.load(open(f))
    towers[d["m"]] = [complex(*x["root"]) for x in d["members"] if x["root"] and x["root"][0] > 0]
OUT = {}
for m in (-2, -3):
    om = np.array([c / B for c in towers[m]])
    t, s = evolve(m, B, rs_min=-40.0, rs_max=700.0, drs=0.02, cfl=0.4, t_max=400.0, rs_obs=60.0, x0=25.0, width=3.0)
    t_start = abs(60.0 - 25.0) + 3 * 3.0 + 10.0
    t_end = min(t_start + 4 * B / 0.25, t[-1])
    sel = (t >= t_start) & (t <= t_end)
    tw, sw = t[sel], s[sel]
    base = np.stack([np.exp(-1j * w * (tw - t_start)) for w in om], axis=1)
    res = {}
    for label, extra in (("tower only", []), ("+ t^-1", [1]), ("+ t^-1,-2", [1, 2]), ("+ t^-1,-2,-3", [1, 2, 3])):
        cols = [base] + [np.stack([(tw / t_start) ** (-p) for p in extra], axis=1)] if extra else [base]
        X = np.concatenate(cols, axis=1) if extra else base
        A, *_ = np.linalg.lstsq(X, sw, rcond=None)
        r = float(np.linalg.norm(X @ A - sw) / np.linalg.norm(sw))
        res[label] = r
        print(f"  m={m} {label}: residual {r:.3f}", flush=True)
    OUT[str(m)] = res
pathlib.Path("results/p32d_tail_postmortem.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
