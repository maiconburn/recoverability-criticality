"""P21b: time-domain continuity through the branch cut (frozen in
results/FROZEN_P21B_VORTEX_TIMEDOMAIN.md).

Usage: uv run python scripts/p21b_vortex_timedomain.py <B_c> [omega_c_im]
Runs the DBT evolution for m = -1 at B_c +- delta, measures the relative
L2 distance between the signals (P21b.1), the matrix-pencil component
nearest -i y_c on both sides (P21b.2), and the n = 1 frequency at
B_c - 0.04 against the continued-fraction value (P21b.3, supplied as an
optional third argument as re,im).
"""
import json
import math
import pathlib
import sys

import numpy as np

sys.path.insert(0, "src")
from recoverability_ep.dbt_td import evolve, prony_modes  # noqa

M = -1
Bc = float(sys.argv[1])
yc = float(sys.argv[2]) if len(sys.argv) > 2 else None
cf_ref = complex(*[float(x) for x in sys.argv[3].split(",")]) if len(sys.argv) > 3 else None

RS_OBS, X0, WIDTH, OM0 = 20.0, 12.0, 1.0, 0.3
T_ARR = RS_OBS - X0 + 2 * X0   # direct pulse passes at ~8, scattered return ~ x0 + rs_obs
WIN = (T_ARR + 5, T_ARR + 40)


def run(B, drs=0.05):
    t, s = evolve(M, B, rs_min=-60, rs_max=300, drs=drs, t_max=WIN[1] + 20,
                  rs_obs=RS_OBS, x0=X0, width=WIDTH, omega0=OM0, order=4)
    return t, s


def window(t, s):
    sel = (t >= WIN[0]) & (t <= WIN[1])
    return t[sel], s[sel]


res = {"Bc": Bc, "window": WIN}
# convergence gate at B_c - 0.04
t1, s1 = run(Bc - 0.04)
t2, s2 = run(Bc - 0.04, drs=0.025)
om1, A1 = prony_modes(*window(t1, s1), order=6)
om2, A2 = prony_modes(*window(t2, s2), order=6)
res["gate_dr_halving"] = {"drs0.05": [[o.real, o.imag, abs(a)] for o, a in zip(om1[:4], A1[:4])],
                          "drs0.025": [[o.real, o.imag, abs(a)] for o, a in zip(om2[:4], A2[:4])]}
print("gate dr halving:", res["gate_dr_halving"], flush=True)
if cf_ref is not None:
    d = min(abs(o - cf_ref) for o in om1[:6])
    res["P21b3_distance_to_CF"] = d
    print(f"P21b.3: nearest pencil component to CF n=1 {cf_ref}: distance {d:.4f}", flush=True)

# continuity
t0, s0 = run(Bc)
_, w0 = window(t0, s0)
norm0 = np.linalg.norm(w0)
cont = {}
for delta in (0.005, 0.01, 0.02, 0.04):
    _, sp = run(Bc + delta)
    _, sm = run(Bc - delta)
    _, wp = window(t0, sp)
    _, wm = window(t0, sm)
    cont[str(delta)] = float(np.linalg.norm(wp - wm) / norm0)
    print(f"delta={delta}: relative L2 distance {cont[str(delta)]:.4e}", flush=True)
ds = sorted(float(k) for k in cont)
xs = [math.log(d) for d in ds]
ys = [math.log(cont[str(d)]) for d in ds]
mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
res["P21b1_continuity"] = {"distances": cont, "exponent": slope}
print(f"P21b.1 exponent: {slope:.3f}", flush=True)

# ghost
ghost = {}
for delta in (-0.01, 0.01):
    _, sg = run(Bc + delta)
    om, A = prony_modes(*window(t0, sg), order=6)
    target = complex(0, -yc) if yc is not None else None
    if target is not None:
        j = int(np.argmin(np.abs(om - target)))
        ghost[str(delta)] = {"omega": [om[j].real, om[j].imag], "amp": float(abs(A[j])),
                             "dist": float(abs(om[j] - target))}
    ghost.setdefault(str(delta), {})["all"] = [[o.real, o.imag, abs(a)] for o, a in zip(om[:5], A[:5])]
    print(f"ghost B_c{delta:+.2f}: {ghost[str(delta)]}", flush=True)
if yc is not None and all("amp" in ghost[k] for k in ghost):
    res["P21b2_ghost"] = {"ratio_amp_plus_over_minus": ghost["0.01"]["amp"] / ghost["-0.01"]["amp"], **ghost}
    print(f"P21b.2 amplitude ratio (+/-): {res['P21b2_ghost']['ratio_amp_plus_over_minus']:.3f}", flush=True)
else:
    res["P21b2_ghost"] = ghost
pathlib.Path("results/p21b_vortex_timedomain.json").write_text(json.dumps(res, indent=1))
print("done", flush=True)
