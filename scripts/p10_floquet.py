"""P10: Floquet-layer EPs and the cost law (predictions frozen in
results/FROZEN_P10_FLOQUET.md BEFORE this script ran)."""
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
        H = np.array([[0.5*A*np.cos(OMEGA_D*t), J],
                      [J, -0.5j*gamma - 0.5*A*np.cos(OMEGA_D*t)]])
        U = expm(-1j*H*dt) @ U
    return U

def quasi(J, A):
    U = U_period(J, A)
    w, v = np.linalg.eig(U)
    lam = 1j*np.log(w)/T           # quasi-energies
    # eigenvector collinearity
    v0 = v[:, 0]/np.linalg.norm(v[:, 0])
    v1 = v[:, 1]/np.linalg.norm(v[:, 1])
    col = abs(np.vdot(v0, v1))
    # gap of Floquet multipliers is the invariant thing; also mod-fold the
    # quasi-energy difference into the first zone
    dlam = lam[0] - lam[1]
    re = (dlam.real + OMEGA_D/2) % OMEGA_D - OMEGA_D/2
    gap = abs(re + 1j*dlam.imag)
    return gap, col, lam, w

# --- P10.1: scan (J, A) for layer EPs
print("== P10.1 scan", flush=True)
best = []
for A in (0.1, 0.2, 0.3, 0.4, 0.5):
    Js = np.linspace(0.35, 0.60, 121)
    rows = [(J,) + quasi(J, A)[:2] for J in Js]
    j_min = min(rows, key=lambda r: r[1])
    print(f"A={A}: min quasi-gap {j_min[1]:.5f} at J={j_min[0]:.4f} "
          f"collinearity={j_min[2]:.4f}", flush=True)
    best.append((A,) + j_min)

# refine at the most promising A: golden section on gap
def refine(A, lo, hi):
    invphi = (np.sqrt(5)-1)/2
    c, d = hi - invphi*(hi-lo), lo + invphi*(hi-lo)
    fc, fd = quasi(c, A)[0], quasi(d, A)[0]
    while hi - lo > 1e-6:
        if fc < fd:
            hi, d, fd = d, c, fc
            c = hi - invphi*(hi-lo); fc = quasi(c, A)[0]
        else:
            lo, c, fc = c, d, fd
            d = lo + invphi*(hi-lo); fd = quasi(d, A)[0]
    J = 0.5*(lo+hi)
    return (J,) + quasi(J, A)[:2]

print("== refinements", flush=True)
refined = {}
for A, J0, g0, c0 in best:
    J, g, col = refine(A, J0-0.01, J0+0.01)
    refined[A] = (J, g, col)
    print(f"A={A}: J_EP={J:.6f} quasi-gap={g:.2e} collinearity={col:.5f}", flush=True)

# --- P10.2: cost law at the Floquet EP for A=0.3 (stroboscopic Prony CRB)
print("== P10.2 cost law", flush=True)
A0 = 0.3
J_EP = refined[A0][0]
NS = np.arange(1, 61)
NOISE = 0.01

def crb_split(J, A):
    U = U_period(J, A)
    w, v = np.linalg.eig(U)
    # stroboscopic record: c(n) = [U^n]_{10} = a+ w+^n + a- w-^n
    y = np.array([np.linalg.matrix_power(U, n)[1, 0] for n in NS])
    M = np.vstack([w[0]**NS, w[1]**NS]).T
    coef, *_ = np.linalg.lstsq(M, y, rcond=None)
    ap, am = coef
    E0, E1 = w[0]**NS, w[1]**NS
    d_l0 = ap * NS * w[0]**(NS-1)
    d_l1 = am * NS * w[1]**(NS-1)
    d_s, d_mu = 0.5*(d_l0 - d_l1), d_l0 + d_l1
    def sr(vv): return np.concatenate([vv.real, vv.imag])
    cols = [sr(d_s), sr(1j*d_s), sr(d_mu), sr(1j*d_mu),
            sr(E0), sr(1j*E0), sr(E1), sr(1j*E1)]
    X = np.vstack(cols).T
    F = X.T @ X / NOISE**2
    gap = abs(w[0]-w[1])
    return gap, np.sqrt(np.linalg.pinv(F)[0, 0])

rows_f = []
for dJ in (0.06, 0.04, 0.025, 0.015, 0.009, 0.005, 0.003):
    g, s = crb_split(J_EP + dJ, A0)
    rows_f.append((g, s))
    print(f"Floquet dJ={dJ:.3f}: mult-gap={g:.4f} crb_s={s:.4g}", flush=True)
gl = np.log([r[0] for r in rows_f]); sl = np.log([r[1] for r in rows_f])
exp_f = np.polyfit(gl, sl, 1)[0]

# static counterpart, same machinery: A=0, EP at J=0.25, same window of gaps
rows_s = []
for dJ in (0.06, 0.04, 0.025, 0.015, 0.009, 0.005, 0.003):
    g, s = crb_split(0.25 + dJ, 0.0)
    rows_s.append((g, s))
    print(f"static  dJ={dJ:.3f}: mult-gap={g:.4f} crb_s={s:.4g}", flush=True)
gl = np.log([r[0] for r in rows_s]); sl = np.log([r[1] for r in rows_s])
exp_s = np.polyfit(gl, sl, 1)[0]
print(f"exponent Floquet={exp_f:.3f}  static={exp_s:.3f}  diff={abs(exp_f-exp_s):.3f}", flush=True)

# --- P10.3: drift of the minimum with A -> 0
print("== P10.3 A->0 limit", flush=True)
for A in (0.05, 0.02, 0.01):
    J, g, col = refine(A, 0.44, 0.50)
    print(f"A={A}: J_min={J:.5f} quasi-gap={g:.3e} col={col:.4f}", flush=True)
print(f"static resonance J* = {np.sqrt(0.16+0.0625):.5f}", flush=True)

json.dump({"refined": {str(k): v for k, v in refined.items()},
           "floquet": rows_f, "static": rows_s,
           "exp_f": exp_f, "exp_s": exp_s},
          open("results/p10_floquet.json", "w"), indent=1)
print("done", flush=True)
