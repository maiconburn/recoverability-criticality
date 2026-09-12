"""P32 stage 3: is there a feasible design window at all, and what protocol
works?

Three constraints fight each other:
  (a) oscillatory modes need Q_n = Re c_n/(2|Im c_n|) ~ |m|/(2(2n+1)) > 1,
      so high |m| (Q is an invariant of the tower: no choice of C, D, h
      changes it);
  (b) shallow water at the light ring needs k h = |m| h c_s/(2C) << 1,
      so large C for high |m|;
  (c) the tower damping in physical units is gamma = |Im c| g h / C, which
      SHRINKS with large C, so the viscous bottom-layer damping
      gamma_visc ~ sqrt(nu omega/2)/h takes over.
Scan (h, C) for each |m|, then, inside the feasible region, compute the
required signal-to-noise for a FIXED-FREQUENCY amplitude fit (the only
protocol that works: blind counting recovered 0-1 of 2-12 modes in
p32b) from the least-squares covariance, plus the confluent cluster
alternative. Output: results/p32c_design_window.json
"""
import glob
import json
import pathlib

import numpy as np

G = 981.0          # cm/s^2
NU = 0.01          # cm^2/s kinematic viscosity of water
towers = {}
for f in glob.glob("results/p23_tower_cplx_m*.json"):
    d = json.load(open(f))
    towers[abs(d["m"])] = [complex(*x["root"]) for x in d["members"] if x["root"] and x["root"][0] > 0]
ext = json.load(open("results/p23_tower_ext.json"))
for k, v in ext.items():
    am = abs(int(k))
    rows = [complex(*r["exact"]) for r in v["rows"] if r.get("exact") and r["exact"][0] > 0]
    wkb = [complex(*r["action_wkb"]) for r in v["rows"] if r.get("action_wkb") and r["action_wkb"][0] > 0]
    towers[am] = rows if len(rows) >= len(wkb) else wkb

import sys
R_MAX = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0     # tank radius cap in cm
OUT = {"constraints": {"kh_max": 0.30, "visc_ratio_max": 0.20, "r_LR_max_cm": R_MAX, "f_min_Hz": 0.05}, "windows": {}}
print(f"Feasible (h, C) windows: k h < 0.30 at the light ring, viscous/tower damping < 0.20, r_LR < {R_MAX:.0f} cm, f_0 > 0.05 Hz")
print("| |m| | Q_0 | feasible? | best h (cm) | best C (cm^2/s) | r_LR (cm) | k h | visc ratio | f_0 (Hz) | gamma_0 (1/s) | flow (L/min) at C/D=10 |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for am in sorted(towers):
    c = towers[am]
    Q0 = c[0].real / (2 * abs(c[0].imag))
    best = None
    for h in np.arange(0.3, 4.01, 0.1):
        cs = np.sqrt(G * h)
        for C in np.arange(50, 3001, 25.0):
            r_LR = 2 * C / cs
            kh = am * h * cs / (2 * C)
            f0 = c[0].real * G * h / C / (2 * np.pi)
            g0 = abs(c[0].imag) * G * h / C
            gv = np.sqrt(NU * 2 * np.pi * f0 / 2) / h
            ratio = gv / g0
            ok = kh < 0.30 and ratio < 0.20 and r_LR < R_MAX and f0 > 0.05
            if ok:
                score = -ratio - kh                      # prefer clean water depth and shallowness
                if best is None or score > best["score"]:
                    D = C / 10.0
                    best = dict(score=score, h=h, C=C, r_LR=r_LR, kh=kh, ratio=ratio, f0=f0, g0=g0,
                                flow_Lmin=2 * np.pi * D * h * 60 / 1000.0)
    OUT["windows"][str(am)] = {"Q0": Q0, "feasible": best is not None, "best": best}
    if best:
        print(f"| {am} | {Q0:.2f} | yes | {best['h']:.1f} | {best['C']:.0f} | {best['r_LR']:.1f} | {best['kh']:.3f} | {best['ratio']:.3f} | {best['f0']:.3f} | {best['g0']:.3f} | {best['flow_Lmin']:.1f} |")
    else:
        print(f"| {am} | {Q0:.2f} | NO | | | | | | | | |")

# required SNR for a fixed-frequency amplitude fit, at the best point of each feasible |m|
print("\nFixed-frequency amplitude fit (record = 6 e-foldings of the fundamental, 100 Hz):")
print("| |m| | modes | cond(X) | SNR for 3-sigma on A_0 | on A_1 | on A_2 | cluster {u, t u} cond | SNR for the cluster moment |")
print("|---|---|---|---|---|---|---|---|")
OUT["snr"] = {}
for am in sorted(towers):
    w = OUT["windows"][str(am)]
    if not w["feasible"]:
        continue
    b = w["best"]
    c = towers[am]
    f = np.array([cc.real for cc in c]) * G * b["h"] / b["C"] / (2 * np.pi)
    g = np.abs([cc.imag for cc in c]) * G * b["h"] / b["C"] + np.sqrt(NU * 2 * np.pi * f / 2) / b["h"]
    T = 6 / g[0]
    t = np.arange(0, T, 0.01)
    X = np.stack([np.exp(2j * np.pi * fi * t - gi * t) for fi, gi in zip(f, g)], axis=1)
    Gi = np.linalg.inv(X.conj().T @ X)
    sig_unit = np.sqrt(np.abs(np.diag(Gi)))            # amplitude sigma for unit noise variance
    cond = np.linalg.cond(X)
    # cluster: fundamental column and its confluent partner t*u (the P30 basis)
    u = X[:, 0]
    Xc = np.stack([u, t * u], axis=1)
    Gc = np.linalg.inv(Xc.conj().T @ Xc)
    # amplitude uncertainty = sigma_noise * sqrt(diag(Gi)); 3-sigma detection of a
    # unit-amplitude mode needs 1/sigma_noise (the per-sample SNR) above 3*sqrt(diag Gi)
    req = 3 * sig_unit
    reqc = 3 * np.sqrt(np.abs(Gc[0, 0]))
    OUT["snr"][str(am)] = {"f_Hz": f.tolist(), "gamma_s": g.tolist(), "T_record_s": float(T), "cond": float(cond),
                           "sigma_unit": sig_unit.tolist(), "snr_required": req.tolist(),
                           "cluster_cond": float(np.linalg.cond(Xc)), "snr_cluster": float(reqc)}
    r = [("-" if not np.isfinite(x) else (f"{x:.1f}" if x < 1e3 else f"{x:.0e}")) for x in (list(req) + [np.nan] * 3)[:3]]
    print(f"| {am} | {len(c)} | {cond:.1e} | {r[0]} | {r[1]} | {r[2]} | {np.linalg.cond(Xc):.1e} | {reqc:.1f} |")
pathlib.Path(f"results/p32c_design_window_R{int(R_MAX)}.json").write_text(json.dumps(OUT, indent=1))
print("done")
