"""P11 v2: analytic transfer-matrix method for the double sech^2 barrier.
v1 was VOID (bidirectional shooting produced unphysical Im omega > 0 roots).
Frozen predictions unchanged (FROZEN_P11_WORMHOLE.md).

Barrier: V(x) = U0 sech^2(x - x0), U0 = V0/2 = 0.15, alpha = 1.
Analytic r(k), t(k) candidates are VALIDATED against direct numerical
integration at real k before any complex-omega use.
"""
import json
import pathlib

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import gamma as cgamma

U0 = 0.15

def s_param():
    # V = U0 sech^2 -> s(s+1) = U0? convention: eigen-problem psi'' + (k^2 - U0 sech^2 x) psi = 0
    return 0.5*(-1 + np.sqrt(complex(1 - 4*U0)))

S = s_param()

def t_amp(k):
    """Transmission amplitude for U0 sech^2 barrier (candidate formula)."""
    ik = -1j*k
    return (cgamma(ik - S)*cgamma(ik + S + 1)) / (cgamma(ik)*cgamma(ik + 1))

def r_amp(k):
    ik = -1j*k
    return (cgamma(1j*k)/cgamma(-1j*k)) * (cgamma(ik - S)*cgamma(ik + S + 1)) / (cgamma(-S)*cgamma(1 + S))

def numeric_rt(k, X=25.0):
    def rhs(x, y):
        sech2 = 1/np.cosh(x)**2
        return [y[1], (U0*sech2 - k*k)*y[0]]
    y0 = [np.exp(1j*k*X), 1j*k*np.exp(1j*k*X)]
    sol = solve_ivp(rhs, (X, -X), y0, rtol=1e-11, atol=1e-13)
    f, d = sol.y[0, -1], sol.y[1, -1]
    # f = A e^{ikx} + B e^{-ikx} at -X  ->  t = 1/A, r = B/A
    e = np.exp(1j*k*(-X))
    A = 0.5*(f + d/(1j*k))/e
    B = 0.5*(f - d/(1j*k))*e
    return 1/A, B/A

print("validating analytic r, t at real k:", flush=True)
ok = True
for k in (0.2, 0.4, 0.7, 1.1):
    tn, rn = numeric_rt(k)
    ta, ra = t_amp(k), r_amp(k)
    et, er = abs(tn - ta), abs(rn - ra)
    print(f"  k={k}: |dt|={et:.2e} |dr|={er:.2e}", flush=True)
    ok = ok and et < 1e-6 and er < 1e-6
print("analytic formulas:", "VALID" if ok else "INVALID", flush=True)
if not ok:
    raise SystemExit("formula validation failed; do not proceed")

# Even/odd quantization for barriers at +-L/2 (center at 0):
# inside region: psi_even = cos(kx), psi_odd = sin(kx).
# Writing the interior wave as incoming+outgoing on the barrier at +L/2 and
# demanding NO incoming wave from +infinity gives, with the barrier's r, t
# referred to its own center:
#   even: 1 + (r/t^*)~ ... use transfer matrix instead (cleaner):
# M maps (a, b) coefficients of a e^{ikx} + b e^{-ikx} from left of barrier
# to right of barrier: for a symmetric barrier,
#   M = [[1/t*, -r*/t*], [-r/t, 1/t]]  (standard, unitary case) -- but at
# complex omega unitarity fails; build M directly from r, t:
#   right coefficients (c, d) with c = (a - r b')/..., safest: derive from
# scattering definition. For incidence from left: (1, r) -> (t, 0):
#   M @ (1, r)^T = (t, 0)^T ; for incidence from right by symmetry:
#   M @ (0, t)^T = (r, 1)^T.  Solve for M columns:
def Mbar(k):
    t, r = t_amp(k), r_amp(k)
    # M [1, r] = [t, 0]; M [0, t] = [r, 1]
    # columns: M[:,0] + r M[:,1] = [t,0]; t M[:,1] = [r,1]
    m1 = np.array([r/t, 1/t])
    m0 = np.array([t, 0]) - r*m1
    return np.array([m0, m1]).T

def quant(k, L, parity):
    # interior wave at barrier center x0=L/2: cos or sin => coefficients in
    # e^{ik(x-x0)}, e^{-ik(x-x0)} basis:
    ph = np.exp(1j*k*L/2)
    if parity == "even":
        a, b = 0.5*ph, 0.5/ph        # cos(kx) = (e^{ikx}+e^{-ikx})/2, shifted
    else:
        a, b = 0.5/1j*ph, -0.5/1j/ph
    out = Mbar(k) @ np.array([a, b])
    return out[1]   # incoming-from-infinity coefficient must vanish

def refine(k0, L, parity, tol=1e-12):
    k, k1 = k0, k0*(1+1e-6) + 1e-6j
    f0, f1 = quant(k, L, parity), quant(k1, L, parity)
    for _ in range(100):
        if f1 == f0: break
        step = -f1*(k1-k)/(f1-f0)
        if abs(step) > 0.05: step *= 0.05/abs(step)
        k, f0 = k1, f1
        k1 = k1 + step
        if abs(step) < tol: break
    return k1

rows = []
for L in (6.0, 8.0, 10.0, 12.0, 14.0, 16.0):
    k0 = np.pi/L
    we = refine(k0 - 0.02j, L, "even")
    wo = refine(k0 - 0.02j, L, "odd")
    dw = abs(we - wo)
    phys = we.imag < 0 and wo.imag < 0
    rows.append([L, we.real, we.imag, wo.real, wo.imag, dw, bool(phys)])
    print(f"L={L:5.1f}: even={we:.6f} odd={wo:.6f} split={dw:.4e} {'ok' if phys else 'UNPHYS'}", flush=True)

rows_a = np.array([r[:6] for r in rows], dtype=float)
sel = np.array([r[6] for r in rows]) & (rows_a[:, 5] > 1e-14)
cf = np.polyfit(rows_a[sel, 0], np.log(rows_a[sel, 5]), 1)
resid = np.log(rows_a[sel, 5]) - np.polyval(cf, rows_a[sel, 0])
r2 = 1 - np.var(resid)/np.var(np.log(rows_a[sel, 5]))
print(f"P11.1: slope={cf[0]:.4f} R^2={r2:.5f}", flush=True)

ts = np.linspace(0.5, 600.0, 1200)
NOISE = 0.01
def crbs(o1, o2):
    E1, E2 = np.exp(-1j*o1*ts), np.exp(-1j*o2*ts)
    d1 = 0.5*(-1j*ts)*E1; d2 = -0.5*(-1j*ts)*E2
    ds, dmu = 0.5*(d1-d2), d1+d2
    sr = lambda v: np.concatenate([v.real, v.imag])
    amps = [sr(E1), sr(1j*E1), sr(E2), sr(1j*E2)]
    freqs = [sr(ds), sr(1j*ds), sr(dmu), sr(1j*dmu)]
    def crb(cols, idx=0):
        X = np.vstack(cols).T
        F = X.T @ X / NOISE**2
        return np.sqrt(np.linalg.pinv(F)[idx, idx])
    return crb(amps), crb(freqs + amps), crb(amps + freqs)

print("L     split      amp|tmpl   split|free  amp|free", flush=True)
hier = []
for (L, re1, im1, re2, im2, dw, phys) in rows:
    if not phys: continue
    t1, t2, t3 = crbs(re1 + 1j*im1, re2 + 1j*im2)
    hier.append([dw, t1, t2, t3])
    print(f"{L:5.1f} {dw:.3e}  {t1:.4g}  {t2:.4g}  {t3:.4g}", flush=True)
hier = np.array(hier)
g = np.log(hier[:, 0])
exps = [np.polyfit(g, np.log(hier[:, k]), 1)[0] for k in (1, 2, 3)]
print(f"exponents: template={exps[0]:.3f} agnostic-split={exps[1]:.3f} amp-free={exps[2]:.3f}", flush=True)
ratio = hier[-1, 2]/hier[-1, 1]
print(f"P11.3 ratio agnostic/template at largest L: {ratio:.2f}", flush=True)
json.dump({"rows": [list(r) for r in rows], "hier": hier.tolist(),
           "slope": cf[0], "R2": r2, "exponents": exps, "ratio": float(ratio)},
          open("results/p11_wormhole_v2.json", "w"), indent=1)
print("done", flush=True)
