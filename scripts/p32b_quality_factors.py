"""P32 stage 2, corrected and extended: quality factors of the pure-vortex
tower and blind resolvability at the physical design point.

The quality factor Q_n = Re c_n / (2 |Im c_n|) is a property of the TOWER
alone: it is invariant under every choice of C, D and depth, because both
frequency and damping scale with c_s^2/C. So whether the tank experiment
can see oscillations at all is decided here, with no PDE run and no
freedom left to the experimenter. Blind matrix-pencil counting is then
tested on synthetic records at the design point with the CORRECT unit
conversion (horizon-unit omega carries c_s^2/D, not c_s^2/C).
Output: results/p32b_quality_factors.json
"""
import glob
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, "src")
from recoverability_ep.dbt_td import prony_modes  # noqa

CS2_OVER_C = 1.96      # s^-1 at the design point of EXPERIMENT_DESIGN_VORTEX_TANK.md
GAMMA_VISC = 0.1       # s^-1 viscous offset
FS, T_REC = 100.0, 60.0

towers = {}
for f in glob.glob("results/p23_tower_cplx_m*.json"):
    d = json.load(open(f))
    towers[abs(d["m"])] = [complex(*x["root"]) for x in d["members"] if x["root"] and x["root"][0] > 0]
ext = json.load(open("results/p23_tower_ext.json"))
for k, v in ext.items():
    am = abs(int(k))
    rows = [complex(*r["exact"]) for r in v["rows"] if r.get("exact") and r["exact"][0] > 0]
    wkb = [complex(*r["action_wkb"]) for r in v["rows"] if r.get("action_wkb") and r["action_wkb"][0] > 0]
    towers[am] = rows if len(rows) >= len(wkb) else wkb          # |m| = 12, 15: action-WKB where exact is missing

OUT = {"design_point": {"cs2_over_C": CS2_OVER_C, "gamma_visc": GAMMA_VISC, "fs": FS, "T_rec": T_REC}, "towers": {}}
print("Quality factors Q_n = Re c / (2|Im c|) of the tower (invariant: no choice of C, D, h changes them)")
print("| |m| | N | Q_0 | Q_1 | Q_2 | Q_3 | modes with Q > 1 | f_0 (Hz) | gamma_0 (1/s) | cycles before 1/e |")
print("|---|---|---|---|---|---|---|---|---|---|")
for am in sorted(towers):
    c = towers[am]
    Q = [cc.real / (2 * abs(cc.imag)) for cc in c]
    nQ1 = sum(1 for q in Q if q > 1)
    f0 = c[0].real * CS2_OVER_C / (2 * np.pi)
    g0 = abs(c[0].imag) * CS2_OVER_C + GAMMA_VISC
    cycles = f0 / g0
    OUT["towers"][str(am)] = {"c": [[z.real, z.imag] for z in c], "Q": Q, "n_Q_above_1": nQ1,
                             "f0_Hz": f0, "gamma0_s": g0, "cycles_per_efold": cycles}
    qs = [f"{q:.2f}" if q is not None else "-" for q in (Q + [None] * 4)[:4]]
    print(f"| {am} | {len(c)} | {qs[0]} | {qs[1]} | {qs[2]} | {qs[3]} | {nQ1} | {f0:.3f} | {g0:.3f} | {cycles:.2f} |")

# blind resolvability at the design point, correct units, for a few |m|
print("\nBlind matrix pencil on a 60 s / 100 Hz synthetic record (equal unit amplitudes, random phases):")
rng = np.random.default_rng(20260912)
tt = np.arange(0, T_REC, 1 / FS)
OUT["blind"] = {}
for am in (2, 5, 10, 15):
    if am not in towers:
        continue
    c = towers[am]
    f = np.array([cc.real for cc in c]) * CS2_OVER_C / (2 * np.pi)
    g = np.abs([cc.imag for cc in c]) * CS2_OVER_C + GAMMA_VISC
    A = np.exp(2j * np.pi * rng.random(len(c)))
    sig = sum(a * np.exp(2j * np.pi * fi * tt - gi * tt) for a, fi, gi in zip(A, f, g))
    peak = np.max(np.abs(sig))
    rows = []
    for noise in (0.001, 0.01):
        best = {"n_matched": -1}
        for order in (4, 6, 8, 10, 12):
            y = sig + noise * peak * (rng.normal(size=len(tt)) + 1j * rng.normal(size=len(tt)))
            try:
                om, Amp = prony_modes(tt, y, order=order, t0=0.0, t1=T_REC)
            except Exception:
                continue
            found = [(w.real / (2 * np.pi), -w.imag) for w in om if w.real > 0 and w.imag < 0]
            matched = []
            for fi in f:
                cand = [x for x in found if abs(x[0] - fi) / fi < 0.10]
                if cand:
                    matched.append(min(cand, key=lambda x: abs(x[0] - fi)))
            if len(matched) > best["n_matched"]:
                best = {"order": order, "n_matched": len(matched), "matched": matched, "n_found": len(found)}
        rows.append({"noise": noise, **best})
        print(f"  |m|={am} ({len(c)} modes, f = {[f'{x:.3f}' for x in f]} Hz, gamma = {[f'{x:.2f}' for x in g]} 1/s): "
              f"{int(noise*1000)/10}% noise -> best order {best.get('order')} matched {best['n_matched']}/{len(c)}")
    OUT["blind"][str(am)] = {"f_Hz": f.tolist(), "gamma_s": g.tolist(), "rows": rows}
pathlib.Path("results/p32b_quality_factors.json").write_text(json.dumps(OUT, indent=1))
print("done")
