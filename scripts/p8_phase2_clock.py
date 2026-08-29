"""P8 phase 2: dynamical test of the EP-crossing clock.

Evolve spectator modes through a slow-roll background where m^2/H^2 sweeps
through the critical value 5/4 (nu = 1), and test the adiabatic predictions:
late-time spectral index n(k) = 3 - 2*nu(N_exit) with a localized anomaly
(log feature) around the mode that exits when the EP is crossed.

Background: H = e^{-eps1 N}, a = e^N (units H0 = 1).  Mode equation in
e-folds: sigma'' + (3 - eps1) sigma' + [x^2 + m2/H^2] sigma = 0 with
x = k/(aH), dx/dN = -(1 - eps1) x.  Bunch-Davies WKB init at x0 = 50.
"""
import json
import pathlib

import numpy as np
from scipy.integrate import solve_ivp

EPS1 = 0.005
M2_0 = 1.25 * np.exp(-2 * EPS1 * 8.0)   # crossing at N* = 8
N_EXITS = np.linspace(-6.0, 22.0, 57)   # exit e-folds relative to N=0
X0, X_END = 50.0, 1e-4

def evolve(k):
    N0 = np.log(k / X0)          # a H ~ e^{(1-eps1)N}; solve x(N0)=X0 approx
    # exact: x = k e^{-(1-eps1)N} -> N0 = ln(k/X0)/(1-eps1)
    N0 = np.log(k / X0) / (1 - EPS1)
    N1 = np.log(k / X_END) / (1 - EPS1)
    def rhs(N, y):
        s, ds = y
        x = k * np.exp(-(1 - EPS1) * N)
        m2H2 = M2_0 * np.exp(2 * EPS1 * N)
        return [ds, -(3 - EPS1) * ds - (x * x + m2H2) * s]
    a0 = np.exp(N0)
    s0 = 1.0 / (a0 * np.sqrt(2 * k))
    y0 = [s0, -s0 * (1.0 + 1j * X0)]
    sol = solve_ivp(rhs, (N0, N1), y0, method="DOP853", rtol=1e-10, atol=1e-30)
    if not sol.success:
        return None
    s_end = sol.y[0, -1]
    nu_exit = np.sqrt(max(9/4 - M2_0 * np.exp(2 * EPS1 * (N0 + np.log(X0)/(1-EPS1))), 0))
    return abs(s_end) ** 2 * k ** 3, N0

rows = []
for Ne in N_EXITS:
    k = np.exp((1 - EPS1) * Ne)          # x(Ne) = 1
    r = evolve(k)
    if r is None:
        continue
    P, _ = r
    m2H2_exit = M2_0 * np.exp(2 * EPS1 * Ne)
    nu_exit = np.sqrt(max(9/4 - m2H2_exit, 0.0))
    rows.append([float(Ne), float(np.log(k)), float(np.log(P)), float(nu_exit)])
    print(f"N_exit={Ne:7.2f} nu_exit={nu_exit:.4f} lnP={np.log(P):9.4f}", flush=True)

rows = np.array(rows)
# local spectral slope vs adiabatic prediction 3-2nu... late-time P(k) for a
# decaying spectator ~ k^{3-2nu}? measure n(k) = d lnP / d ln k numerically
n_meas = np.gradient(rows[:, 2], rows[:, 1])
pred = -2 * rows[:, 3] + 0*rows[:,1]  # slope relative shift: d lnP/d ln k = const + (-2 nu)? report both
print("\nN_exit  nu_exit  n_meas   (pred slope ~ c - 2*nu_exit)")
for i in range(0, len(rows), 4):
    print(f"{rows[i,0]:6.1f}  {rows[i,3]:.4f}  {n_meas[i]:8.4f}")
# anomaly detector: residual of n_meas vs smooth fit excluding the crossing window
mask = np.abs(rows[:, 0] - 8.0) > 4.0
cf = np.polyfit(rows[mask, 3], n_meas[mask], 2)
resid = n_meas - np.polyval(cf, rows[:, 3])
print("\ncrossing-window residuals (|N_exit - 8| < 4):")
for i in range(len(rows)):
    if abs(rows[i, 0] - 8.0) < 4.0:
        print(f"  N_exit={rows[i,0]:5.1f}: resid={resid[i]:+.4f}")
pathlib.Path("results/p8_phase2_clock.json").write_text(json.dumps(
    {"eps1": EPS1, "m2_0": M2_0, "rows": rows.tolist(),
     "n_meas": n_meas.tolist(), "resid": resid.tolist()}, indent=1))
print("done", flush=True)
