"""(E) Real SXS ringdowns: sigma(A5,A6) vs distance to the Kerr crossing."""
import warnings; warnings.filterwarnings('ignore')
import json
import numpy as np
import sxs, qnm

ASTAR = 0.8975
TARGETS = [0.8975, 0.893, 0.885, 0.87, 0.83, 0.75, 0.69]
df = sxs.load("dataframe", tag="3.0.0")
a = df["remnant_dimensionless_spin_mag"].astype(float)
picks = []
for tgt in TARGETS:
    idx = (a - tgt).abs().idxmin()
    picks.append((idx, float(a[idx]), float(df.loc[idx, "remnant_mass"])))
    print("pick:", idx, "a_f=", round(float(a[idx]), 5))

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
        om = np.array([modes[n](a=af)[0] for n in range(8)]) / mf * mf  # per-Mf units: t already /mf
        design = np.stack([np.exp(-1j * om[n] * ts) for n in range(8)], axis=1)
        boot = []
        scale = np.max(np.abs(hs))
        for _ in range(40):
            noise = 1e-4 * scale * (rng.normal(size=len(ts)) + 1j * rng.normal(size=len(ts)))
            sol, *_ = np.linalg.lstsq(design, hs + noise, rcond=None)
            boot.append(sol)
        boot = np.array(boot)
        sig_pair = float(np.mean(np.std(boot[:, [5, 6]], axis=0)))
        sig_low = float(np.mean(np.std(boot[:, [0, 1]], axis=0)))
        sol0, res0, *_ = np.linalg.lstsq(design, hs, rcond=None)
        resid = float(np.linalg.norm(design @ sol0 - hs) / np.linalg.norm(hs))
        gap = float(abs(om[5] - om[6]))
        rows.append(dict(sim=str(sim_id), a_f=af, d=abs(af - ASTAR), gap56=gap,
                         sig_pair=sig_pair, sig_low=sig_low, fit_resid=resid))
        print(f"{sim_id}: a_f={af:.5f} d={abs(af-ASTAR):.5f} gap={gap:.4f} "
              f"sig_pair={sig_pair:.3e} sig_low={sig_low:.3e} resid={resid:.3f}", flush=True)
    except Exception as e:
        print(f"{sim_id}: FAILED {type(e).__name__}: {e}", flush=True)
json.dump(rows, open("results/sxs_layer.json", "w"), indent=1)
print("wrote results/sxs_layer.json")
