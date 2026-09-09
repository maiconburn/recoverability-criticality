"""P30 (method note, not a frozen prediction): confluent cluster fitting
of the (2,2,5)/(2,2,6) pair on the six SXS waveforms of P25/P29.
Three models on identical data, noise and window:
  L: eight labeled columns e_n (n = 0..7)                     -> A_5, A_6
  S: seven columns, pair replaced by u = (e_5 + e_6)/2         -> S
  C: eight columns, pair replaced by the confluent basis
     {u, v} with v = t u (the Jordan-block partner)            -> C_0, C_1
Checks: (i) sigma(M_0)/sigma(S) of the L fit equals the variance
inflation factor sqrt(1/(1 - rho^2)) with rho the partial correlation
of u and (e_5 - e_6)/2 after projecting out the other six columns
(exact identity of least squares); (ii) the C fit's coefficients have
finite, gap-independent cost and reproduce the pair's waveform as well
as L. Output: results/p30_cluster_fit.json.
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
sd = lambda z: float(np.sqrt(np.mean(np.abs(z - z.mean()) ** 2)))
rows = []
for sim_id, af, mf in picks:
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
    e = [np.exp(-1j * om[n] * ts) for n in range(8)]
    u = (e[5] + e[6]) / 2
    vdiff = (e[5] - e[6]) / 2
    XL = np.stack(e, axis=1)
    XS = np.stack(e[:5] + [u] + [e[7]], axis=1)
    XC = np.stack(e[:5] + [u, ts * u] + [e[7]], axis=1)
    scale = np.max(np.abs(hs))
    bL, bS, bC = [], [], []
    for _ in range(40):
        noise = 1e-4 * scale * (rng.normal(size=len(ts)) + 1j * rng.normal(size=len(ts)))
        y = hs + noise
        bL.append(np.linalg.lstsq(XL, y, rcond=None)[0]); bS.append(np.linalg.lstsq(XS, y, rcond=None)[0]); bC.append(np.linalg.lstsq(XC, y, rcond=None)[0])
    bL, bS, bC = map(np.array, (bL, bS, bC))
    # VIF identity: project u and vdiff on the orthogonal complement of the other six columns
    O = np.stack(e[:5] + [e[7]], axis=1)
    P = np.eye(len(ts)) - O @ np.linalg.pinv(O)
    ur, vr = P @ u, P @ vdiff
    rho = abs(np.vdot(ur, vr)) / (np.linalg.norm(ur) * np.linalg.norm(vr))
    vif = 1 / np.sqrt(1 - rho ** 2)
    # pair-waveform reconstruction error at t = 0..20 M from each model (relative to the noiseless L fit)
    sol0 = np.linalg.lstsq(XL, hs, rcond=None)[0]
    pair_true = sol0[5] * e[5] + sol0[6] * e[6]
    win = ts <= 20
    errL = [np.linalg.norm((b[5] * e[5] + b[6] * e[6] - pair_true)[win]) for b in bL]
    errC = [np.linalg.norm((b[5] * u + b[6] * ts * u - pair_true)[win]) for b in bC]
    errS = [np.linalg.norm((b[5] * u - pair_true)[win]) for b in bS]
    gap = float(abs(om[5] - om[6]))
    row = dict(sim=str(sim_id), a_f=af, gap56=gap, sig_A5=sd(bL[:, 5]), sig_M0=sd(bL[:, 5] + bL[:, 6]), sig_S=sd(bS[:, 5]),
               sig_C0=sd(bC[:, 5]), sig_C1=sd(bC[:, 6]), rho_partial=float(rho), vif=float(vif), ratio_M0_S=sd(bL[:, 5] + bL[:, 6]) / sd(bS[:, 5]),
               pair_err_L=float(np.mean(errL)), pair_err_C=float(np.mean(errC)), pair_err_S=float(np.mean(errS)))
    rows.append(row)
    print(f"{sim_id}: gap={gap:.4f} sigA5={row['sig_A5']:.2e} M0/S={row['ratio_M0_S']:.2f} VIF={vif:.2f} (rho={rho:.4f}) | cluster fit: sigC0={row['sig_C0']:.2e} sigC1={row['sig_C1']:.2e} | pair-waveform err L/C/S = {row['pair_err_L']:.2e}/{row['pair_err_C']:.2e}/{row['pair_err_S']:.2e}", flush=True)
keep = [r for r in rows if r["sim"] != "SXS:BBH:2525"]
x = np.log([r["gap56"] for r in keep])
out = {"rows": rows, "slopes": {}}
for key in ("sig_A5", "sig_C0", "sig_C1", "sig_S", "pair_err_L", "pair_err_C"):
    y = np.log([r[key] for r in keep]); s = float(np.polyfit(x, y, 1)[0])
    out["slopes"][key] = s
    print(f"  slope of log {key} vs log gap: {s:+.3f}", flush=True)
json.dump(out, open("results/p30_cluster_fit.json", "w"), indent=1)
print("done", flush=True)
