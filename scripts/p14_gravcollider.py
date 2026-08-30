"""P14: level-crossing metrology for the gravitational collider (frozen in
FROZEN_P14_GRAVCOLLIDER.md). Landau-Zener two-level cloud, swept by the
binary orbital frequency; CRB for (eta, Omega_res) from a noisy record."""
import json
import pathlib

import numpy as np
from scipy.integrate import solve_ivp

def evolve(eta, om_res, v, t_span=40.0, nt=400):
    """Sweep Delta(t) = v*(t - t_res); record P_b(t) (transferred population)."""
    t_res = 0.0
    ts = np.linspace(-t_span, t_span, nt)
    def rhs(t, y):
        d = v*(t - t_res)
        H = np.array([[-d/2, eta], [eta, d/2]], dtype=complex)
        return (-1j*H @ y.reshape(2)).view(np.float64) if False else None
    # complex ODE via real embedding
    def rhs2(t, y):
        c = y[:2] + 1j*y[2:]
        d = v*(t - t_res)
        H = np.array([[-d/2, eta], [eta, d/2]], dtype=complex)
        dc = -1j*H @ c
        return np.concatenate([dc.real, dc.imag])
    y0 = np.array([1.0, 0.0, 0.0, 0.0])
    sol = solve_ivp(rhs2, (ts[0], ts[-1]), y0, t_eval=ts, rtol=1e-10, atol=1e-12)
    c = sol.y[:2] + 1j*sol.y[2:]
    return ts, np.abs(c[1])**2   # P_b(t)

def crb(eta, v, noise=0.01, dpar=1e-5):
    ts, p0 = evolve(eta, 0.0, v)
    _, p_eta = evolve(eta+dpar, 0.0, v)
    _, p_res = evolve(eta, dpar, v)
    d_eta = (p_eta - p0)/dpar
    d_res = (p_res - p0)/dpar
    X = np.vstack([d_eta, d_res]).T / noise
    F = X.T @ X
    Finv = np.linalg.pinv(F)
    return np.sqrt(Finv[0,0]), np.sqrt(Finv[1,1])

# P14.1: scaling of sigma(eta) with gap = 2*eta at slow sweep
print("== P14.1 (slow sweep v=0.02)", flush=True)
rows = []
for eta in (0.5, 0.35, 0.25, 0.18, 0.12, 0.08):
    se, sr = crb(eta, v=0.02)
    rows.append([2*eta, se, sr])
    print(f"eta={eta}: gap={2*eta:.2f} sigma_eta={se:.4g} sigma_res={sr:.4g}", flush=True)
rows = np.array(rows)
p = np.polyfit(np.log(rows[:,0]), np.log(rows[:,1]), 1)[0]
print(f"P14.1 exponent: {p:.3f}  (window [-2.5,-1.5])", flush=True)
print("P14.1:", "CONFIRMED" if -2.5 <= p <= -1.5 else "KILLED", flush=True)

# P14.2: information vs sweep rate at eta=0.25
print("== P14.2 (eta=0.25)", flush=True)
rows2 = []
for v in (0.005, 0.01, 0.02, 0.0625, 0.125, 0.25, 0.5, 1.0, 2.0):
    se, _ = crb(0.25, v)
    rows2.append([v, 1/se**2])
    print(f"v={v}: info_eta={1/se**2:.4g}", flush=True)
rows2 = np.array(rows2)
imax, iasy = rows2[:,1].max(), rows2[-1,1]
mono = bool(np.all(np.diff(rows2[:,1]) < 0) or np.all(np.diff(rows2[:,1]) > 0))
print(f"P14.2: max/asymptotic = {imax/iasy:.2f}, monotonic={mono}", flush=True)
print("P14.2:", "CONFIRMED" if (not mono and imax/iasy > 3) else "KILLED", flush=True)

# P14.3: boson-mass precision proxy. Omega_res proportional to mu =>
# sigma(mu)/mu = sigma(Omega_res)/Omega_res. Take Omega_res scale ~ 1 in
# sweep units, phase-SNR 100 => noise=0.01 as configured; clean crossing:
se, sr = crb(0.25, v=0.02)
rel = sr/1.0
print(f"P14.3: sigma(mu)/mu ~ sigma_res/Omega_res = {rel*100:.2f}%", flush=True)
print("P14.3:", "CONFIRMED" if rel < 0.05 else ("KILLED" if rel > 0.20 else "inconclusive"), flush=True)
json.dump({"p141": rows.tolist(), "p142": rows2.tolist(), "exp": p, "rel_mu": rel},
          open("results/p14_gravcollider.json","w"), indent=1)
print("done", flush=True)
