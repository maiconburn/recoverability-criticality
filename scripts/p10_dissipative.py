"""P10.4: dissipative Floquet drive - does the replica resonance now produce
a genuine EP? (frozen before running)"""
import json
import pathlib

import numpy as np
from scipy.linalg import expm

gamma = 1.0
OMEGA_D = 0.8
T = 2*np.pi/OMEGA_D
NSTEP = 400

def U_period(J, A):
    dt = T/NSTEP
    U = np.eye(2, dtype=complex)
    for k in range(NSTEP):
        t = (k + 0.5)*dt
        g_t = gamma*(1.0 + A*np.cos(OMEGA_D*t))
        H = np.array([[0, J], [J, -0.5j*g_t]])
        U = expm(-1j*H*dt) @ U
    return U

def diag_info(J, A):
    U = U_period(J, A)
    w, v = np.linalg.eig(U)
    v0 = v[:, 0]/np.linalg.norm(v[:, 0]); v1 = v[:, 1]/np.linalg.norm(v[:, 1])
    col = abs(np.vdot(v0, v1))
    return abs(w[0]-w[1]), col

best_global = None
for A in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6):
    Js = np.linspace(0.44, 0.50, 121)
    rows = [(J,) + diag_info(J, A) for J in Js]
    jm = min(rows, key=lambda r: r[1])
    print(f"A={A}: min mult-gap {jm[1]:.5f} at J={jm[0]:.4f} col={jm[2]:.4f}", flush=True)
    if best_global is None or jm[1] < best_global[2]:
        best_global = (A,) + jm

# 2D refine around best (J and A both free): coordinate descent
A, J = best_global[0], best_global[1]
for _ in range(24):
    Js = np.linspace(J-0.004, J+0.004, 17)
    J = min(Js, key=lambda x: diag_info(x, A)[0])
    As = np.linspace(max(0.01, A-0.04), min(0.65, A+0.04), 17)
    A = min(As, key=lambda x: diag_info(J, x)[0])
g, col = diag_info(J, A)
print(f"refined: J={J:.6f} A={A:.5f} mult-gap={g:.3e} collinearity={col:.5f}", flush=True)
verdict = "P10.4 CONFIRMED" if (g < 1e-3 and col > 0.99) else "P10.4 KILLED"
print(verdict, flush=True)
json.dump({"J": J, "A": A, "gap": g, "col": col, "verdict": verdict},
          open("results/p10_dissipative.json", "w"), indent=1)
print("done", flush=True)
