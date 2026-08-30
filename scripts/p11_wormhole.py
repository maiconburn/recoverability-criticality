"""P11: wormhole doublet resolution cost (frozen in FROZEN_P11_WORMHOLE.md
before this ran). Double Poschl-Teller cavity, outgoing QNMs via complex-
omega shooting, then CRB hierarchy on the finite-duration ringdown."""
import json
import pathlib

import numpy as np
from scipy.integrate import solve_ivp

V0, XMAX = 0.3, 60.0

def V(x, L):
    return 0.5*V0*(1/np.cosh(x - L/2)**2 + 1/np.cosh(x + L/2)**2)

def wronskian(omega, L):
    """Integrate from both ends with outgoing waves; W at x=0."""
    def rhs(x, y):
        return [y[1], (V(x, L) - omega**2)*y[0]]
    # right solution: psi ~ e^{+i omega x} at +XMAX, integrate to 0
    yR0 = [np.exp(1j*omega*XMAX), 1j*omega*np.exp(1j*omega*XMAX)]
    sR = solve_ivp(rhs, (XMAX, 0.0), yR0, rtol=1e-10, atol=1e-12)
    # left solution: psi ~ e^{-i omega x} at -XMAX
    yL0 = [np.exp(1j*omega*XMAX), -1j*omega*np.exp(1j*omega*XMAX)]
    sL = solve_ivp(rhs, (-XMAX, 0.0), yL0, rtol=1e-10, atol=1e-12)
    fR, dR = sR.y[0, -1], sR.y[1, -1]
    fL, dL = sL.y[0, -1], sL.y[1, -1]
    return fL*dR - fR*dL

def refine(omega, L, tol=1e-12):
    o0, o1 = omega, omega*(1 + 1e-5) + 1e-5j
    w0, w1 = wronskian(o0, L), wronskian(o1, L)
    for _ in range(80):
        if w1 == w0:
            break
        step = -w1*(o1 - o0)/(w1 - w0)
        if abs(step) > 0.05:
            step *= 0.05/abs(step)
        o0, w0 = o1, w1
        o1 = o1 + step
        if abs(step) < tol:
            break
    return o1

# cavity-mode seeds: quasi-bound levels omega ~ n*pi/L - i*small
rows = []
for L in (6.0, 8.0, 10.0, 12.0, 14.0, 16.0):
    seed = np.pi/L
    # symmetric/antisymmetric doublet around the n=1 cavity mode:
    # seed two nearby starting points and deflate
    o1 = refine(seed*(1+0.02) - 0.02j, L)
    o2 = refine(seed*(1-0.02) - 0.02j, L)
    if abs(o1 - o2) < 1e-8:  # fell to same root; nudge harder
        o2 = refine(seed*(1-0.06) - 0.05j, L)
    dw = abs(o1 - o2)
    rows.append([L, o1.real, o1.imag, o2.real, o2.imag, dw])
    print(f"L={L:5.1f}: w1={o1:.6f} w2={o2:.6f} split={dw:.3e}", flush=True)

rows = np.array(rows)
ok = np.isfinite(rows[:, 5]) & (rows[:, 5] > 1e-12)
cf = np.polyfit(rows[ok, 0], np.log(rows[ok, 5]), 1)
resid = np.log(rows[ok, 5]) - np.polyval(cf, rows[ok, 0])
ss = 1 - np.var(resid)/np.var(np.log(rows[ok, 5]))
print(f"P11.1: ln(split) vs L slope={cf[0]:.4f}  R^2={ss:.5f}", flush=True)

# CRB hierarchy on finite ringdown, per L
ts = np.linspace(0.5, 400.0, 800)
NOISE = 0.01
def crbs(o1, o2):
    E1, E2 = np.exp(-1j*o1*ts), np.exp(-1j*o2*ts)
    a1, a2 = 0.5, -0.5
    d1 = a1*(-1j*ts)*E1; d2 = a2*(-1j*ts)*E2
    ds, dmu = 0.5*(d1-d2), d1+d2
    sr = lambda v: np.concatenate([v.real, v.imag])
    amps = [sr(E1), sr(1j*E1), sr(E2), sr(1j*E2)]
    freqs = [sr(ds), sr(1j*ds), sr(dmu), sr(1j*dmu)]
    def crb(cols, idx=0):
        X = np.vstack(cols).T
        F = X.T @ X / NOISE**2
        return np.sqrt(np.linalg.pinv(F)[idx, idx])
    return (crb(amps),                 # amplitudes, freqs fixed (template)
            crb(freqs + amps),         # splitting, all free (agnostic)
            crb(amps + freqs))         # amplitude, freqs free

print("L     split      amp|tmpl   split|free  amp|free", flush=True)
hier = []
for L, r1, i1, r2, i2, dw in rows:
    t1, t2, t3 = crbs(r1 + 1j*i1, r2 + 1j*i2)
    hier.append([dw, t1, t2, t3])
    print(f"{L:5.1f} {dw:.3e}  {t1:.4g}  {t2:.4g}  {t3:.4g}", flush=True)
hier = np.array(hier)
sel = hier[:, 0] > 1e-10
g = np.log(hier[sel, 0])
exps = [np.polyfit(g, np.log(hier[sel, k]), 1)[0] for k in (1, 2, 3)]
print(f"exponents: template={exps[0]:.3f} agnostic-split={exps[1]:.3f} amp-free={exps[2]:.3f}", flush=True)
ratio = hier[sel][-1, 2]/hier[sel][-1, 1]
print(f"P11.3 ratio agnostic/template at largest L: {ratio:.1f}", flush=True)
json.dump({"doublets": rows.tolist(), "hier": hier.tolist(),
           "slope_L": cf[0], "R2": ss, "exponents": exps, "ratio": ratio},
          open("results/p11_wormhole.json", "w"), indent=1)
print("done", flush=True)
