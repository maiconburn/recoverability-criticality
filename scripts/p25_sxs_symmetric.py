"""P25: symmetric (cluster-moment) versus labeled amplitude costs on the
same SXS fits as run_sxs_layer.py (frozen in
results/FROZEN_P25_SXS_SYMMETRIC.md). Identical picks, seed, noise and
design; the bootstrap draws are kept and the combinations
M_0 = A_5 + A_6, M_1 = A_5 w_5 + A_6 w_6, D = A_5 - A_6 and the pair
waveform at t = 0 and t = 20 are evaluated. Output: results/p25_sxs_symmetric.json.
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
    print("pick:", idx, "a_f=", round(float(a[idx]), 5), flush=True)

modes = {n: qnm.modes_cache(s=-2, l=2, m=2, n=n) for n in range(8)}
rng = np.random.default_rng(20260828)
rows = []
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
        design = np.stack([np.exp(-1j * om[n] * ts) for n in range(8)], axis=1)
        boot = []
        scale = np.max(np.abs(hs))
        for _ in range(40):
            noise = 1e-4 * scale * (rng.normal(size=len(ts)) + 1j * rng.normal(size=len(ts)))
            sol, *_ = np.linalg.lstsq(design, hs + noise, rcond=None)
            boot.append(sol)
        boot = np.array(boot)
        A5, A6 = boot[:, 5], boot[:, 6]
        M0 = A5 + A6
        M1 = A5 * om[5] + A6 * om[6]
        D = A5 - A6
        pair0 = M0                                   # pair waveform at t = 0
        pair20 = A5 * np.exp(-1j * om[5] * 20) + A6 * np.exp(-1j * om[6] * 20)
        gap = float(abs(om[5] - om[6]))
        sd = lambda z: float(np.sqrt(np.mean(np.abs(z - z.mean()) ** 2)))
        row = dict(sim=str(sim_id), a_f=af, d=abs(af - ASTAR), gap56=gap,
                   sig_A5=sd(A5), sig_A6=sd(A6), sig_pair=float(np.mean([sd(A5), sd(A6)])),
                   sig_M0=sd(M0), sig_M1=sd(M1), sig_D=sd(D), sig_pair0=sd(pair0), sig_pair20=sd(pair20),
                   sig_low=float(np.mean([sd(boot[:, 0]), sd(boot[:, 1])])),
                   mean_A5=[float(A5.mean().real), float(A5.mean().imag)], mean_A6=[float(A6.mean().real), float(A6.mean().imag)])
        rows.append(row)
        print(f"{sim_id}: a_f={af:.5f} gap={gap:.4f} sigA5={row['sig_A5']:.2e} sigA6={row['sig_A6']:.2e} "
              f"sigM0={row['sig_M0']:.2e} sigM1={row['sig_M1']:.2e} sigD={row['sig_D']:.2e} pair20={row['sig_pair20']:.2e} low={row['sig_low']:.2e}", flush=True)
    except Exception as e:
        print(f"{sim_id}: FAILED {type(e).__name__}: {e}", flush=True)

# slopes vs gap (log-log), excluding the flagged outlier if present
keep = [r for r in rows if r["sim"] != "SXS:BBH:2525"]
x = np.log([r["gap56"] for r in keep])
out = {"rows": rows, "excluded": [r["sim"] for r in rows if r not in keep], "slopes": {}}
for key in ("sig_A5", "sig_A6", "sig_pair", "sig_M0", "sig_M1", "sig_D", "sig_pair0", "sig_pair20", "sig_low"):
    y = np.log([r[key] for r in keep])
    s, b = np.polyfit(x, y, 1)
    c = float(np.corrcoef(x, y)[0, 1])
    out["slopes"][key] = {"slope": float(s), "corr": c}
    print(f"  slope of log {key} vs log gap: {s:+.3f} (corr {c:+.3f})", flush=True)
near = min(keep, key=lambda r: r["d"])
out["contrast_at_crossing"] = {"sim": near["sim"], "sigA5_over_sigM0": near["sig_A5"] / near["sig_M0"], "sigD_over_sigM0": near["sig_D"] / near["sig_M0"]}
print(f"  contrast at the crossing ({near['sim']}): sigma(A5)/sigma(M0) = {near['sig_A5']/near['sig_M0']:.1f}, sigma(D)/sigma(M0) = {near['sig_D']/near['sig_M0']:.1f}", flush=True)
json.dump(out, open("results/p25_sxs_symmetric.json", "w"), indent=1)
print("done", flush=True)
