"""P29: controlled symmetric-versus-labeled comparison on the SXS fits
(frozen in results/FROZEN_P29_SXS_CONTROLLED.md). Same pipeline as
p25_sxs_symmetric.py plus a seven-column reference fit whose pair
columns are replaced by their mean; ratios of the eight-column
uncertainties to sigma(S) remove the spin-dependent block conditioning.
Output: results/p29_sxs_controlled.json.
"""
import json
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import qnm
import sxs

ASTAR = 0.8975
TARGETS = [0.8975, 0.893, 0.885, 0.87, 0.83, 0.75, 0.69]
df = sxs.load("dataframe", tag="3.0.0")
a = df["remnant_dimensionless_spin_mag"].astype(float)
picks = []
for tgt in TARGETS:
    idx = (a - tgt).abs().idxmin()
    picks.append((idx, float(a[idx]), float(df.loc[idx, "remnant_mass"])))
modes = {n: qnm.modes_cache(s=-2, l=2, m=2, n=n) for n in range(8)}
rng = np.random.default_rng(20260828)
rows = []
sd = lambda z: float(np.sqrt(np.mean(np.abs(z - z.mean()) ** 2)))
for sim_id, af, mf in picks:
    try:
        sim = sxs.load(str(sim_id))
        w = sim.h
        t = np.array(w.t)
        hv = np.array(w.data[:, w.index(2, 2)], dtype=complex)
        ipk = int(np.argmax(np.abs(hv)))
        t0 = t[ipk]
        sel = (t >= t0 + 10 * mf) & (t <= t0 + 90 * mf)
        ts = (t[sel] - (t0 + 10 * mf)) / mf
        hs = hv[sel] / np.max(np.abs(hv))
        om = np.array([modes[n](a=af)[0] for n in range(8)])
        cols = [np.exp(-1j * om[n] * ts) for n in range(8)]
        design8 = np.stack(cols, axis=1)
        design7 = np.stack(cols[:5] + [(cols[5] + cols[6]) / 2] + [cols[7]], axis=1)
        scale = np.max(np.abs(hs))
        b8, b7 = [], []
        for _ in range(40):
            noise = 1e-4 * scale * (rng.normal(size=len(ts)) + 1j * rng.normal(size=len(ts)))
            s8, *_ = np.linalg.lstsq(design8, hs + noise, rcond=None)
            s7, *_ = np.linalg.lstsq(design7, hs + noise, rcond=None)
            b8.append(s8); b7.append(s7)
        b8, b7 = np.array(b8), np.array(b7)
        A5, A6, S = b8[:, 5], b8[:, 6], b7[:, 5]
        gap = float(abs(om[5] - om[6]))
        row = dict(sim=str(sim_id), a_f=af, gap56=gap, sig_A5=sd(A5), sig_A6=sd(A6), sig_M0=sd(A5 + A6), sig_D=sd(A5 - A6), sig_S=sd(S),
                   r_M0=sd(A5 + A6) / sd(S), r_D=sd(A5 - A6) / sd(S), r_A5=sd(A5) / sd(S))
        rows.append(row)
        print(f"{sim_id}: a_f={af:.5f} gap={gap:.4f} sigS={row['sig_S']:.2e} sigM0={row['sig_M0']:.2e} sigD={row['sig_D']:.2e} sigA5={row['sig_A5']:.2e}  ratios M0/S={row['r_M0']:.2f} D/S={row['r_D']:.2f} A5/S={row['r_A5']:.2f}", flush=True)
    except Exception as e:
        print(f"{sim_id}: FAILED {type(e).__name__}: {e}", flush=True)
keep = [r for r in rows if r["sim"] != "SXS:BBH:2525"]
x = np.log([r["gap56"] for r in keep])
out = {"rows": rows, "slopes": {}}
for key in ("r_M0", "r_D", "r_A5", "sig_S", "sig_M0", "sig_D"):
    y = np.log([r[key] for r in keep])
    s = float(np.polyfit(x, y, 1)[0]); c = float(np.corrcoef(x, y)[0, 1])
    out["slopes"][key] = {"slope": s, "corr": c}
    print(f"  slope of log {key} vs log gap: {s:+.3f} (corr {c:+.3f})", flush=True)
near = min(keep, key=lambda r: abs(r["a_f"] - ASTAR))
out["at_crossing"] = {"sim": near["sim"], "r_M0": near["r_M0"], "r_D": near["r_D"], "r_A5": near["r_A5"]}
out["r_M0_range"] = [min(r["r_M0"] for r in keep), max(r["r_M0"] for r in keep)]
print(f"  at the crossing ({near['sim']}): M0/S = {near['r_M0']:.2f}, D/S = {near['r_D']:.2f}, A5/S = {near['r_A5']:.2f}; M0/S range over six sims {out['r_M0_range']}", flush=True)
json.dump(out, open("results/p29_sxs_controlled.json", "w"), indent=1)
print("done", flush=True)
