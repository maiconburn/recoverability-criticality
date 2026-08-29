"""P8 step 1, v2: bisection version (no secant wandering).

For pure-imaginary omega = -i*Omega the dS radial ODE is real, so the
Wronskian-like shooting function W(Omega) is real: QNMs on the axis are its
sign changes, found by scan + bisection.  At nu = 1, eps = 0 the towers give a
double root at Omega = 2.5.  Under eps*x^2(1-x^2):

  - two real sign changes near 2.5      -> real splitting s(eps)
  - no sign change but |W| dips         -> pair moved off-axis (complex);
    then s(eps) = 2*|Im omega| via complex secant seeded at the |W| minimum.

s ~ sqrt(eps) => EP-2 (Jordan).  s ~ eps => diabolic.
"""
import json
import pathlib

import numpy as np
from scipy.integrate import solve_ivp

NU = 1.0
M2 = 9.0 / 4.0 - NU**2
X0, X1 = 1e-4, 1.0 - 1e-5

def wronskian(omega, eps, m2):
    p = -1j * omega / 2.0
    u = 1.0 - X1

    def rhs(x, y):
        phi, dphi = y
        f = 1.0 - x * x
        dV = eps * x * x * f
        d2 = (-(2.0 * x * f - 2.0 * x**3) * dphi
              - x * x * (omega**2 / f - m2 - dV) * phi) / (x * x * f)
        return [dphi, d2]

    phi0 = u**p
    dphi0 = -p * u ** (p - 1.0)
    sol = solve_ivp(rhs, (X1, X0), [phi0, dphi0], method="DOP853",
                    rtol=1e-11, atol=1e-13)
    if not sol.success:
        raise RuntimeError("integration failed")
    phi, dphi = sol.y[:, -1]
    return complex(X0**2 * dphi)

def w_real(Omega, eps, m2):
    return wronskian(-1j * Omega, eps, m2).real

def axis_roots(eps, m2, lo=2.05, hi=2.95, n=181):
    om = np.linspace(lo, hi, n)
    w = np.array([w_real(o, eps, m2) for o in om])
    roots = []
    for i in range(n - 1):
        if w[i] * w[i + 1] < 0:
            a, b = om[i], om[i + 1]
            fa = w[i]
            for _ in range(60):
                m = 0.5 * (a + b)
                fm = w_real(m, eps, m2)
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
            roots.append(0.5 * (a + b))
    i_min = int(np.argmin(np.abs(w)))
    return roots, float(om[i_min]), w

def complex_root(omega, eps, m2, tol=1e-11):
    o0, o1 = omega, omega + 1e-5 * (1 + 1j)
    w0, w1 = wronskian(o0, eps, m2), wronskian(o1, eps, m2)
    for _ in range(80):
        if w1 == w0:
            break
        step = -w1 * (o1 - o0) / (w1 - w0)
        if abs(step) > 0.03:
            step *= 0.03 / abs(step)
        o0, w0 = o1, w1
        o1 = o1 + step
        if abs(step) < tol:
            break
    return o1

# validation at eps=0, nu=0.9: expect 2.4 and 2.6
m2_val = 9.0 / 4.0 - 0.81
r, _, _ = axis_roots(0.0, m2_val)
print(f"validation nu=0.9 eps=0: axis roots = {np.round(r, 6)} (expect 2.4, 2.6)", flush=True)

out = {"validation": r, "rows": []}
for eps in (0.32, 0.16, 0.08, 0.04, 0.02, 0.01, 0.005):
    roots, om_min, _ = axis_roots(eps, M2)
    if len(roots) >= 2:
        s = abs(roots[-1] - roots[0])
        kind = "real"
        pair = [[0.0, -roots[0]], [0.0, -roots[-1]]]
    else:
        c = complex_root(-1j * om_min + 0.02j + 0.02, eps, M2)
        s = 2.0 * abs(c.real)  # mirror partner at -conj(c)
        kind = "complex"
        pair = [[c.real, c.imag], [-c.real, c.imag]]
    out["rows"].append({"eps": eps, "kind": kind, "split": s, "pair": pair,
                        "n_axis_roots": len(roots)})
    print(f"eps={eps}: kind={kind} split={s:.6e} axis_roots={np.round(roots,5)}", flush=True)

sp = [(d["eps"], d["split"]) for d in out["rows"] if d["split"] > 1e-8]
if len(sp) >= 3:
    slope = float(np.polyfit(np.log([p[0] for p in sp]), np.log([p[1] for p in sp]), 1)[0])
    out["exponent"] = slope
    print(f"splitting exponent = {slope:.4f}  (0.5=EP-2 Jordan, 1.0=diabolic)", flush=True)

pathlib.Path("results/ds_jordan_test.json").write_text(json.dumps(out, indent=1))
print("done", flush=True)
