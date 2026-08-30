"""P14': gravitational-collider forecast on the GW phase observable with
binary-parameter marginalization. Frozen in FROZEN_P14_GRAVCOLLIDER.md."""
import json
import pathlib

import numpy as np
from scipy.integrate import solve_ivp

ETA0, C0, BETA0, OMRES0 = 0.05, 5.0, 0.01, 1.0
OM0, PHI0 = 0.8, 0.0
SIG_PHI, NSAMP = 0.1, 2000

def k_fiducial():
    # local sweep rate near resonance: d(Delta)/dt = c * dOm/dt = c*k*Om^{11/3}
    # want v_eff = c*k*1^{11/3} = 0.02*C0 -> k = 0.02
    return 0.02

K0 = k_fiducial()

def integrate(params, t_max=40.0):
    om_res, eta, beta, k, om0, phi0 = params
    def rhs(t, y):
        Om, Phi, cr1, ci1, cr2, ci2 = y
        c1, c2 = cr1 + 1j*ci1, cr2 + 1j*ci2
        d = C0*(Om - om_res)
        dc1 = -1j*(-d/2*c1 + eta*c2)
        dc2 = -1j*(eta*c1 + d/2*c2)
        dPb = 2*np.real(np.conj(c2)*dc2)
        dOm = k*Om**(11/3) - beta*dPb
        return [dOm, 2*Om, dc1.real, dc1.imag, dc2.real, dc2.imag]
    y0 = [om0, phi0, 1.0, 0.0, 0.0, 0.0]
    # integrate until Om reaches 1.2
    def hit(t, y): return y[0] - 1.2
    hit.terminal = True; hit.direction = 1
    sol = solve_ivp(rhs, (0, 400), y0, events=hit, dense_output=True,
                    rtol=1e-11, atol=1e-13)
    t_end = sol.t_events[0][0] if len(sol.t_events[0]) else sol.t[-1]
    ts = np.linspace(0, t_end, NSAMP)
    Y = sol.sol(ts)
    return ts, Y[1], Y[0], Y[4]**2 + Y[5]**2   # phase, Omega, P_b

P0 = np.array([OMRES0, ETA0, BETA0, K0, OM0, PHI0])
ts, phi0_, Om_, Pb_ = integrate(P0)
print(f"fiducial: t_end={ts[-1]:.1f}, cycles={phi0_[-1]/2/np.pi:.1f}, "
      f"P_b(final)={Pb_[-1]:.4f}", flush=True)

# Fisher via finite differences on the PHASE record
def dphase(i, h):
    p = P0.copy(); p[i] += h
    _, ph_p, _, _ = integrate(p)
    p2 = P0.copy(); p2[i] -= h
    _, ph_m, _, _ = integrate(p2)
    return (ph_p - ph_m)/(2*h)

hs = [1e-6, 1e-6, 1e-6, 1e-8, 1e-8, 1e-6]
D = np.vstack([dphase(i, hs[i]) for i in range(6)])
X = D.T / SIG_PHI
F = X.T @ X
cond = np.linalg.cond(F)
Fi = np.linalg.inv(F)
sig = np.sqrt(np.diag(Fi))
names = ["Om_res", "eta", "beta", "k", "Om0", "phi0"]
print(f"cond(F) = {cond:.2e}", flush=True)
for n, s, v in zip(names, sig, P0):
    print(f"  sigma({n}) = {s:.4g}   rel = {s/abs(v) if v else float('inf'):.4g}", flush=True)
rel_mu = sig[0]/OMRES0
naive = np.sqrt(1.0/ (D[0] @ D[0] / SIG_PHI**2))
print(f"P14'.1: sigma(mu)/mu marginalizado = {rel_mu*100:.3f}%  "
      f"(nao-marginalizado: {naive/OMRES0*100:.4f}%, fator {rel_mu/(naive/OMRES0):.1f})", flush=True)
v141 = "CONFIRMED" if (rel_mu < 0.05 and rel_mu/(naive/OMRES0) > 10 and rel_mu > 0.001) else \
       ("KILLED" if (rel_mu > 0.20 or rel_mu < 0.001) else "inconclusive")
print(f"P14'.1: {v141}", flush=True)

# P14'.2: information localization — Fisher density for Om_res in the window
w = np.abs(Om_ - OMRES0) < 5*ETA0
frac = float((D[0][w] @ D[0][w]) / (D[0] @ D[0]))
print(f"P14'.2: fracao da informacao na janela |Om-Om_res|<5eta: {frac*100:.1f}%", flush=True)
print(f"P14'.2: {'CONFIRMED' if frac >= 0.60 else ('KILLED' if frac < 0.40 else 'inconclusive')}", flush=True)

# P14'.3: correlation with k
r = Fi[0,3]/np.sqrt(Fi[0,0]*Fi[3,3])
print(f"P14'.3: corr(Om_res, k) = {r:+.4f}", flush=True)
print(f"P14'.3: {'CONFIRMED' if abs(r) < 0.9 else ('KILLED' if abs(r) >= 0.95 else 'inconclusive')}", flush=True)
json.dump({"sig": sig.tolist(), "cond": cond, "rel_mu": rel_mu,
           "frac_window": frac, "corr_k": float(r)},
          open("results/p14_prime.json","w"), indent=1)
print("done", flush=True)
