"""P25 post-mortem gate (diagnostic, not a frozen prediction): on ONE
SXS simulation far from the crossing (SXS:BBH:1750, a_f = 0.75), keep
the waveform, the window, the noise and seven of the eight Kerr
frequencies, and move omega_6 artificially to omega_5 + delta (same
imaginary part as omega_5) for delta = 0.2 ... 0.005. If the fit
mechanics obey the principle, sigma(D) ~ 1/delta while sigma(M_0) is
flat; the real-data slope of M_0 (-0.75 over six spins) would then be
the spin confounder (the conditioning of the whole overtone block).
Output: results/p25_gate_synthetic_gap.json.
"""
import json
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import qnm
import sxs

sim = sxs.load("SXS:BBH:1750")
df = sxs.load("dataframe", tag="3.0.0")
af = float(df.loc["SXS:BBH:1750", "remnant_dimensionless_spin_mag"])
mf = float(df.loc["SXS:BBH:1750", "remnant_mass"])
w = sim.h
t = np.array(w.t)
hv = np.array(w.data[:, w.index(2, 2)], dtype=complex)
ipk = int(np.argmax(np.abs(hv)))
t0 = t[ipk]
sel = (t >= t0 + 10 * mf) & (t <= t0 + 90 * mf)
ts = (t[sel] - (t0 + 10 * mf)) / mf
hs = hv[sel] / np.max(np.abs(hv))
modes = {n: qnm.modes_cache(s=-2, l=2, m=2, n=n) for n in range(8)}
om_true = np.array([modes[n](a=af)[0] for n in range(8)])
print(f"a_f={af:.4f}, omega_5={om_true[5]:.4f}, omega_6={om_true[6]:.4f}, true gap {abs(om_true[5]-om_true[6]):.4f}", flush=True)
scale = np.max(np.abs(hs))
out = []
for delta in (0.2, 0.1, 0.05, 0.02, 0.01, 0.005):
    om = om_true.copy()
    om[6] = om[5] + delta                     # same damping, real gap = delta
    design = np.stack([np.exp(-1j * om[n] * ts) for n in range(8)], axis=1)
    rng = np.random.default_rng(20260828)
    boot = []
    for _ in range(40):
        noise = 1e-4 * scale * (rng.normal(size=len(ts)) + 1j * rng.normal(size=len(ts)))
        sol, *_ = np.linalg.lstsq(design, hs + noise, rcond=None)
        boot.append(sol)
    boot = np.array(boot)
    A5, A6 = boot[:, 5], boot[:, 6]
    sd = lambda z: float(np.sqrt(np.mean(np.abs(z - z.mean()) ** 2)))
    # also the exact linear-algebra prediction: covariance (X^H X)^-1 sigma^2
    G = np.linalg.inv(design.conj().T @ design)
    s2 = (1e-4 * scale) ** 2 * 2
    v0 = np.zeros(8, complex); v0[5] = v0[6] = 1
    vd = np.zeros(8, complex); vd[5] = 1; vd[6] = -1
    th_M0 = float(np.sqrt(np.real(v0.conj() @ G @ v0) * s2))
    th_D = float(np.sqrt(np.real(vd.conj() @ G @ vd) * s2))
    row = dict(delta=delta, sig_A5=sd(A5), sig_A6=sd(A6), sig_M0=sd(A5 + A6), sig_D=sd(A5 - A6), th_M0=th_M0, th_D=th_D, cond=float(np.linalg.cond(design)))
    out.append(row)
    print(f"delta={delta}: sigA5={row['sig_A5']:.2e} sigM0={row['sig_M0']:.2e} (theory {th_M0:.2e}) sigD={row['sig_D']:.2e} (theory {th_D:.2e}) cond={row['cond']:.1e}", flush=True)
x = np.log([r["delta"] for r in out])
for key in ("sig_A5", "sig_M0", "sig_D", "th_M0", "th_D"):
    s = np.polyfit(x, np.log([r[key] for r in out]), 1)[0]
    print(f"  slope of log {key} vs log delta: {s:+.3f}", flush=True)
json.dump(out, open("results/p25_gate_synthetic_gap.json", "w"), indent=1)
print("done", flush=True)
