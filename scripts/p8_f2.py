"""P8-F2: does the EP log survive dynamically in the fixed-time spectrum?
Frozen in FROZEN_P8_PREDICTIONS.md before this ran."""
import json
import pathlib
import sys

import numpy as np
from scipy.integrate import solve_ivp

EPS1 = float(sys.argv[1]) if len(sys.argv) > 1 else 0.005
NSTAR = 8.0
M2_0 = 1.25*np.exp(-2*EPS1*NSTAR)   # nu crosses 1 at N*
SHIFT = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0  # detune for F2.2
M2_0 *= np.exp(-2*EPS1*SHIFT*0)     # placeholder
if SHIFT != 0.0:
    # choose m2 so nu at band-center exit is 1+SHIFT and never crosses 1
    M2_0 = (9/4 - (1+SHIFT)**2)*np.exp(-2*EPS1*NSTAR)

N_REF = NSTAR + 6.0

def evolve_to(k, N_ref):
    N0 = np.log(k/50.0)/(1-EPS1)
    def rhs(N, y):
        s, ds = y[:2] + 1j*y[2:], None
        c = y[:2] + 1j*y[2:]
        x = k*np.exp(-(1-EPS1)*N)
        m2H2 = M2_0*np.exp(2*EPS1*N)
        # y = [Re s, Re ds, Im s, Im ds] -- pack properly:
        s_, ds_ = c[0], c[1]
        dds = -(3-EPS1)*ds_ - (x*x + m2H2)*s_
        return np.concatenate([[ds_.real, dds.real],[ds_.imag, dds.imag]])
    a0 = np.exp(N0)
    s0 = 1/(a0*np.sqrt(2*k))
    y0 = np.array([s0, (-s0*(1+1j*50)).real, 0.0, (-s0*(1+1j*50)).imag])
    sol = solve_ivp(rhs, (N0, N_ref), y0, rtol=1e-10, atol=1e-30)
    s_end = sol.y[0,-1] + 1j*sol.y[2,-1]
    return s_end

# band of k: exits spanning N* +- 3 (so the crossing sits inside)
N_exits = np.linspace(NSTAR-3, NSTAR+3, 40)
ks = np.exp((1-EPS1)*N_exits)
kn = ks/ks[len(ks)//2]      # normalize mid-band
ys = []
for k in ks:
    s = evolve_to(k, N_REF)
    ys.append(abs(s)**2 * k**3)
ys = np.array(ys)
ys = ys/ys[0]*(kn[0])       # normalize leading ~ k

lnk = np.log(kn)
def fit(basis):
    X = np.vstack(basis).T
    c, res, *_ = np.linalg.lstsq(X, ys, rcond=None)
    r = ys - X@c
    return c, float(np.sum(r**2))

b_nolog = [kn, kn**3, kn**5, kn**7]
b_log   = [kn, kn**3, kn**3*lnk, kn**5, kn**5*lnk]
c0, rss0 = fit(b_nolog)
c1, rss1 = fit(b_log)
dof = len(ys) - len(b_log)
dchi = (rss0 - rss1)/max(rss1/dof, 1e-300)
clog = c1[2]/c1[1] if abs(c1[1])>0 else np.nan  # log coef relative to k^3 coef
print(f"eps1={EPS1} shift={SHIFT}: rss nolog={rss0:.3e} log={rss1:.3e} "
      f"dchi2/dof_unit={dchi:.1f}", flush=True)
print(f"  c(k)={c1[0]:.4f} c(k3)={c1[1]:.4f} c(k3 lnk)={c1[2]:.4f} "
      f"ratio log/k3 = {clog:.4f}", flush=True)
json.dump({"eps1": EPS1, "shift": SHIFT, "c": [float(x) for x in c1],
           "rss0": rss0, "rss1": rss1, "dchi": dchi},
          open(f"results/p8f2_{EPS1}_{SHIFT}.json","w"), indent=1)
print("done", flush=True)
