"""P14'': multi-crossing gravitational-collider forecast (frozen in
FROZEN_P14_GRAVCOLLIDER.md)."""
import json
import pathlib

import numpy as np
from scipy.integrate import solve_ivp

C0 = np.array([1.0, 1.35, 1.80])
DK = np.array([0.05, 0.12, 0.20])
ETA = np.array([0.05, 0.05, 0.05])
NSAMP, SIG_PHI = 3000, 0.1
OM0, OM_END, PHI0 = 0.8, 2.2, 0.0

# params: [mu, chi, eta1, eta2, eta3, beta, k, Om0, phi0]
P0 = np.array([1.0, 0.5, 0.05, 0.05, 0.05, 0.01, 0.005, OM0, PHI0])
NAMES = ["mu", "chi", "eta1", "eta2", "eta3", "beta", "k", "Om0", "phi0"]

def om_res(mu, chi):
    return mu * C0 * (1 + DK*chi)

def integrate(p):
    mu, chi, e1, e2, e3, beta, k, om0, phi0 = p
    etas = np.array([e1, e2, e3])
    res = om_res(mu, chi)
    def rhs(t, y):
        Om, Phi = y[0], y[1]
        c = y[2:].reshape(3, 2, 2)  # [mode][real/imag? ] -> use complex packing
        # unpack: y[2:] = [cr_k, ci_k for k, both levels]
        dydt = np.zeros_like(y)
        dPb_tot = 0.0
        for kk in range(3):
            base = 2 + kk*4
            c1 = y[base] + 1j*y[base+1]
            c2 = y[base+2] + 1j*y[base+3]
            d = C0[kk]*(1+DK[kk]*chi)*mu  # resonance freq scale unused directly
            delta = 10.0*(Om - res[kk])   # sweep coupling to detuning
            dc1 = -1j*(-delta/2*c1 + etas[kk]*c2)
            dc2 = -1j*(etas[kk]*c1 + delta/2*c2)
            dydt[base] = dc1.real; dydt[base+1] = dc1.imag
            dydt[base+2] = dc2.real; dydt[base+3] = dc2.imag
            dPb_tot += 2*np.real(np.conj(c2)*dc2)
        dOm = k*Om**(11/3) - beta*dPb_tot
        dydt[0] = dOm; dydt[1] = 2*Om
        return dydt
    y0 = np.zeros(2 + 12)
    y0[0] = om0; y0[1] = phi0
    for kk in range(3):
        y0[2+kk*4] = 1.0   # c1 = 1
    def hit(t, y): return y[0] - OM_END
    hit.terminal = True; hit.direction = 1
    sol = solve_ivp(rhs, (0, 800), y0, events=hit, dense_output=True,
                    rtol=1e-10, atol=1e-12)
    t_end = sol.t_events[0][0] if len(sol.t_events[0]) else sol.t[-1]
    ts = np.linspace(0, t_end, NSAMP)
    Y = sol.sol(ts)
    return ts, Y[1], Y[0]   # phase, Omega

def fisher(p, active=None):
    hs = [1e-6, 1e-6, 1e-6, 1e-6, 1e-6, 1e-6, 1e-8, 1e-8, 1e-6]
    idx = active if active is not None else list(range(9))
    D = []
    _, ph0, _ = integrate(p)
    for i in idx:
        pp = p.copy(); pp[i] += hs[i]
        pm = p.copy(); pm[i] -= hs[i]
        _, php, _ = integrate(pp)
        _, phm, _ = integrate(pm)
        D.append((php - phm)/(2*hs[i]))
    X = np.vstack(D).T / SIG_PHI
    F = X.T @ X
    return F, idx

# baseline: full forecast
ts, ph, Om = integrate(P0)
print(f"fiducial: t_end={ts[-1]:.1f}, cycles={ph[-1]/2/np.pi:.1f}", flush=True)
F, idx = fisher(P0)
cond = np.linalg.cond(F)
Fi = np.linalg.pinv(F, rcond=1e-12)
sig = np.sqrt(np.abs(np.diag(Fi)))
sig_mu = sig[0]
print(f"cond(F)={cond:.2e}; JOINT sigma(mu)/mu = {sig_mu*100:.4f}%; sigma(chi)={sig[1]:.4g}", flush=True)

# single-crossing baselines: turn off two clouds (eta=0), keep the strongest
best_single = np.inf
for keep in range(3):
    p = P0.copy()
    for kk in range(3):
        if kk != keep: p[2+kk] = 0.0
    act = [0, 2+keep, 5, 6, 7, 8]   # mu, eta_keep, beta, k, Om0, phi0
    Fs, _ = fisher(p, active=act)
    s = np.sqrt(np.linalg.pinv(Fs)[0,0])
    best_single = min(best_single, s)
    print(f"single crossing {keep}: sigma(mu)/mu = {s*100:.4f}%", flush=True)
gain = best_single/sig_mu
print(f"P14''.1: coherent gain = {gain:.3f} (threshold {np.sqrt(3):.3f}) ->",
      "CONFIRMED" if gain > 0.8*np.sqrt(3) else "KILLED", flush=True)

# chi known vs unknown
F_ck, idx = fisher(P0, active=[0,2,3,4,5,6,7,8])  # drop chi
s_chiknown = np.sqrt(np.linalg.pinv(F_ck, rcond=1e-12)[0,0])
degr = sig_mu/s_chiknown
print(f"P14''.2: chi-unknown/chi-known = {degr:.3f} ->",
      "CONFIRMED" if degr < 2 else ("KILLED" if degr > 5 else "inconclusive"), flush=True)

print(f"P14''.3: sigma(mu)/mu = {sig_mu*100:.4f}% ->",
      "CONFIRMED" if sig_mu < 0.001 else ("KILLED" if sig_mu > 0.01 else "inconclusive"), flush=True)
json.dump({"sig": sig.tolist(), "sig_mu": sig_mu, "gain": gain,
           "degr_chi": degr, "cond": cond},
          open("results/p14_multi.json","w"), indent=1)
print("done", flush=True)
