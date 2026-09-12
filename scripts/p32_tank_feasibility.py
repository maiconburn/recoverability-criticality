"""P32: is the tank experiment doable? Excitation and resolvability of the
pure-vortex tower at strong rotation (frozen in
results/FROZEN_P32_TANK_FEASIBILITY.md).

Stage 1: time-domain evolution at B = 10 with generic Gaussian initial
data; amplitudes of the tower modes from a FIXED-FREQUENCY linear least
squares (frequencies c_n/B from the complex-ray towers), on an early
window of 4 e-foldings; excitation factors and residual.
Stage 2: synthetic 60 s record at the design point with viscous damping
and noise; blind matrix pencil; count of recovered counter-rotating modes.
Output: results/p32_tank_feasibility.json
"""
import glob
import json
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, "src")
from recoverability_ep.dbt_td import evolve, prony_modes  # noqa

B = 10.0
MS = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [-2, -3, -4, -5]
SETTINGS = [dict(x0=25.0, width=3.0), dict(x0=40.0, width=6.0), dict(x0=15.0, width=2.0)]
CS2_OVER_C = 1.96          # s^-1 = c_s^2/C at the design point
CS2_OVER_D = CS2_OVER_C * B  # s^-1 = c_s^2/D: THIS is the unit of the horizon-unit omega (P32 lesson)
GAMMA_VISC = 0.1           # s^-1, viscous offset of the note
FS = 100.0                 # Hz sampling
T_REC = 60.0               # s record

towers = {}
for f in glob.glob("results/p23_tower_cplx_m*.json"):
    d = json.load(open(f))
    towers[d["m"]] = [complex(*x["root"]) for x in d["members"] if x["root"] and x["root"][0] > 0]

OUT = {}
for m in MS:
    c = towers[m]
    om_tower = np.array([cc / B for cc in c])          # omega in horizon units
    tfold = B / 0.25                                   # e-folding of the fundamental
    rec = {"tower_c": [[z.real, z.imag] for z in c], "omega_tower": [[w.real, w.imag] for w in om_tower], "settings": []}
    print(f"== m={m}: {len(c)} tower modes, omega = {[f'{w:.4f}' for w in om_tower]}", flush=True)
    for st in SETTINGS:
        t0 = time.time()
        t, s = evolve(m, B, rs_min=-40.0, rs_max=700.0, drs=0.02, cfl=0.4, t_max=400.0, rs_obs=60.0, **st)
        # window: pulse clears the observer at t ~ |rs_obs - x0| + 3 width, then 4 e-foldings
        t_start = abs(60.0 - st["x0"]) + 3 * st["width"] + 10.0
        t_end = min(t_start + 4 * tfold, t[-1])
        sel = (t >= t_start) & (t <= t_end)
        tw, sw = t[sel], s[sel]
        # fixed-frequency linear least squares (symmetric-model recipe)
        X = np.stack([np.exp(-1j * w * (tw - t_start)) for w in om_tower], axis=1)
        A, *_ = np.linalg.lstsq(X, sw, rcond=None)
        resid = np.linalg.norm(X @ A - sw) / np.linalg.norm(sw)
        E = np.abs(A) / abs(A[0])
        rec["settings"].append(dict(x0=st["x0"], width=st["width"], t_window=[float(t_start), float(t_end)],
                                    amplitudes=[[a.real, a.imag] for a in A], E=[float(e) for e in E],
                                    residual=float(resid), seconds=time.time() - t0, n_steps=len(t)))
        print(f"   x0={st['x0']} w={st['width']}: window [{t_start:.0f}, {t_end:.0f}], |A| = {[f'{abs(a):.2e}' for a in A]}, E = {[f'{e:.3f}' for e in E]}, residual {resid:.3f}  ({time.time()-t0:.0f}s, {len(t)} steps)", flush=True)
    # stability of E across settings
    Es = np.array([st["E"] for st in rec["settings"]])
    rec["E_min_over_settings"] = Es.min(axis=0).tolist()
    rec["E_max_over_settings"] = Es.max(axis=0).tolist()
    rec["E_spread_factor"] = (Es.max(axis=0) / np.maximum(Es.min(axis=0), 1e-12)).tolist()
    print(f"   E across settings: min {[f'{x:.3f}' for x in rec['E_min_over_settings']]}, spread factor {[f'{x:.1f}' for x in rec['E_spread_factor']]}", flush=True)

    # ---- stage 2: synthetic physical record and blind counting
    A0 = np.array([complex(*a) for a in rec["settings"][0]["amplitudes"]])
    # omega_tower is in horizon units (c_s^2/D), NOT in c_s^2/C: converting with
    # c_s^2/C understates f and gamma by the factor B (bug found in the first run).
    f_phys = np.array([w.real for w in om_tower]) * CS2_OVER_D / (2 * np.pi)      # Hz
    g_phys = np.abs([w.imag for w in om_tower]) * CS2_OVER_D + GAMMA_VISC         # s^-1
    tt = np.arange(0, T_REC, 1 / FS)
    sig = sum(a * np.exp(2j * np.pi * f * tt - g * tt) for a, f, g in zip(A0, f_phys, g_phys))
    rec["f_phys_Hz"] = f_phys.tolist()
    rec["gamma_phys_s"] = g_phys.tolist()
    rec["blind"] = {}
    rng = np.random.default_rng(20260912)
    for noise in (0.01, 0.05):
        peak = np.max(np.abs(sig))
        best = None
        for order in (6, 8, 10, 12, 14):
            y = sig + noise * peak * (rng.normal(size=len(tt)) + 1j * rng.normal(size=len(tt)))
            try:
                om, Amp = prony_modes(tt, y, order=order, t0=0.0, t1=T_REC)
            except Exception:
                continue
            found = [(w, a) for w, a in zip(om, Amp) if w.real > 0 and w.imag < 0 and 0.005 < w.real / (2 * np.pi) < 1.5]
            found.sort(key=lambda p: -abs(p[1]))
            matched = []
            for f0 in f_phys:
                cand = [(abs(w.real / (2 * np.pi) - f0) / f0, w, a) for w, a in found]
                cand = [x for x in cand if x[0] < 0.10]
                if cand:
                    matched.append(min(cand)[1])
            entry = dict(order=order, n_found=len(found), n_matched=len(matched),
                         matched=[[w.real / (2 * np.pi), -w.imag] for w in matched],
                         all_found=[[w.real / (2 * np.pi), -w.imag, abs(a)] for w, a in found[:8]])
            rec["blind"].setdefault(str(noise), []).append(entry)
            if best is None or entry["n_matched"] > best["n_matched"]:
                best = entry
        print(f"   blind pencil at {int(noise*100)}% noise: best order {best['order']} matched {best['n_matched']}/{len(f_phys)} of the tower; f_true = {[f'{f:.3f}' for f in f_phys]} Hz, gamma_true = {[f'{g:.3f}' for g in g_phys]} 1/s", flush=True)
        print(f"      matched: {[(round(f,4), round(g,3)) for f,g in best['matched']]}", flush=True)
        rec["blind"][str(noise) + "_best"] = best
    OUT[str(m)] = rec
    pathlib.Path("results/p32_tank_feasibility.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
