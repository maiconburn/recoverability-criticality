"""P8 phase 2b: two-tower decomposition of dynamically evolved modes.

For each k, evolve sigma_k(N) and fit the late-time superhorizon evolution
with the two local towers  sigma ~ A e^{-I-(N)} + B e^{-I+(N)},
I∓(N) = int (3/2 ∓ nu(N')) dN'  (adiabatic exponents with the RUNNING nu).
The subleading/leading ratio |B/A|(k) carries the two-tower interference
where the EP log structure lives; prediction: anomaly localized at modes
exiting near the nu=1 crossing (N* = 8).
"""
import json
import pathlib

import numpy as np
from scipy.integrate import quad, solve_ivp

EPS1 = 0.005
M2_0 = 1.25 * np.exp(-2 * EPS1 * 8.0)
X0 = 50.0

def nu_of(N):
    return np.sqrt(np.maximum(9/4 - M2_0 * np.exp(2 * EPS1 * N), 1e-12))

def evolve_traj(k, N_span=14.0, n_out=200):
    N0 = np.log(k / X0) / (1 - EPS1)
    Nexit = np.log(k) / (1 - EPS1)
    N1 = Nexit + N_span
    def rhs(N, y):
        s, ds = y
        x = k * np.exp(-(1 - EPS1) * N)
        return [ds, -(3 - EPS1) * ds - (x * x + M2_0 * np.exp(2 * EPS1 * N)) * s]
    a0 = np.exp(N0)
    s0 = 1.0 / (a0 * np.sqrt(2 * k))
    sol = solve_ivp(rhs, (N0, N1), [s0, -s0 * (1 + 1j * X0)],
                    t_eval=np.linspace(Nexit + 4.0, N1, n_out),
                    method="DOP853", rtol=1e-11, atol=1e-32)
    return sol.t, sol.y[0], Nexit

rows = []
for Ne_target in np.concatenate([np.linspace(-4, 20, 25)]):
    k = np.exp((1 - EPS1) * Ne_target)
    try:
        Ns, sig, Nexit = evolve_traj(k)
    except Exception:
        continue
    # adiabatic integrals from Nexit
    Im = np.array([quad(lambda n: 1.5 - nu_of(n), Nexit, N)[0] for N in Ns])
    Ip = np.array([quad(lambda n: 1.5 + nu_of(n), Nexit, N)[0] for N in Ns])
    E1 = np.exp(-Im); E2 = np.exp(-Ip)
    X = np.vstack([E1, E2]).T
    # complex least squares
    cA, *_ = np.linalg.lstsq(X, sig, rcond=None)
    resid = np.linalg.norm(sig - X @ cA) / np.linalg.norm(sig)
    ratio = abs(cA[1] / cA[0]) if abs(cA[0]) > 0 else np.nan
    rows.append([float(Ne_target), float(nu_of(Nexit)), float(ratio), float(resid)])
    print(f"N_exit={Ne_target:6.2f} nu={nu_of(Nexit):.4f} |B/A|={ratio:.5e} resid={resid:.2e}", flush=True)

pathlib.Path("results/p8_towers.json").write_text(json.dumps(rows, indent=1))
print("done", flush=True)
