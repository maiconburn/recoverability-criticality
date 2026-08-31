"""P8 step 1: is the pure-dS QNM tower degeneracy at integer nu a Jordan
block (EP-2) or a diabolic crossing?

Massive scalar in the dS4 static patch (L=1), f = 1 - x^2, l = 0:
    (x^2 f phi')' / x^2 + [omega^2/f - m^2 - eps*dV(x)] phi = 0
Analytic spectrum at eps=0: omega = -i(2n + Delta_pm), Delta_pm = 3/2 +- nu,
nu = sqrt(9/4 - m^2).  At nu = 1 the (n=0, +) and (n=1, -) modes coincide at
omega = -2.5i.  Test: perturb with eps*x^2(1-x^2) and measure the splitting
s(eps).  s ~ sqrt(eps) => EP-2 (Jordan); s ~ eps => diabolic.
Preregistered kill criterion (results/DIRECTION_P8_BIGBANG.md): no mirror-EP
structure => the cosmology bridge is analogy only.
"""
import json
import pathlib

import numpy as np
from scipy.integrate import solve_ivp

NU = 1.0
M2 = 9.0 / 4.0 - NU**2
X0, X1 = 1e-4, 1.0 - 1e-5
SERIES = 10

def rhs_factory(omega, eps):
    def rhs(x, y):
        phi, dphi = y
        f = 1.0 - x * x
        dV = eps * x * x * (1.0 - x * x)
        # (x^2 f phi')' = -x^2 [omega^2/f - M2 - dV] phi
        d2 = (-(2.0 * x * f + x * x * (-2.0 * x)) * dphi
              - x * x * (omega**2 / f - M2 - dV) * phi) / (x * x * f)
        return [dphi, d2]
    return rhs

def wronskian(omega, eps):
    """Ingoing-at-horizon solution integrated to the origin; the coefficient
    of the singular 1/x branch vanishes at a QNM."""
    # Frobenius at x=1: phi = (1-x)^p * sum a_k (1-x)^k, p = -i*omega/2
    p = -1j * omega / 2.0
    u = 1.0 - X1
    a = [1.0 + 0j] * SERIES
    # recursion from the ODE expanded in u = 1-x (numeric Taylor matching)
    # build by collocation: solve for a_k with high-order finite differences is
    # overkill; use two-term seed + tiny offset (series error ~ u^2 handled by
    # small u and DOP853 tolerance)
    phi0 = u**p * (1.0 + 0j)
    dphi0 = -p * u ** (p - 1.0)
    sol = solve_ivp(rhs_factory(omega, eps), (X1, X0), [phi0, dphi0],
                    method="DOP853", rtol=1e-11, atol=1e-13)
    if not sol.success:
        raise RuntimeError("integration failed")
    phi, dphi = sol.y[:, -1]
    return complex(X0**2 * dphi)  # -> -B (singular-branch coefficient)

def refine(omega, eps, tol=1e-11, max_wander=0.35):
    origin = omega
    w0 = wronskian(omega, eps)
    o1 = omega + 1e-5 * (1 + 1j)
    w1 = wronskian(o1, eps)
    for _ in range(60):
        if w1 == w0:
            break
        step = -w1 * (o1 - omega) / (w1 - w0)
        if abs(step) > 0.05:
            step *= 0.05 / abs(step)
        omega, w0 = o1, w1
        o1 = o1 + step
        if abs(o1 - origin) > max_wander:
            raise RuntimeError(f"wandered from {origin} to {o1}")
        w1 = wronskian(o1, eps)
        if abs(step) < tol:
            break
    return o1

# validation: eps=0, nu=0.9 (M2 = 9/4 - 0.81) -> Omega = 2.4, 2.6
out = {"validation": [], "splitting": []}
for nu_test, seeds in [(0.9, (-2.35j, -2.65j))]:
    M2 = 9.0 / 4.0 - nu_test**2
    got = [refine(s, 0.0) for s in seeds]
    out["validation"].append({"nu": nu_test,
                              "expected": [-(3/2 + nu_test + 0), -(2 + 3/2 - nu_test)],
                              "got": [[g.real, g.imag] for g in got]})
    print("validation nu=0.9:", got, flush=True)

M2 = 9.0 / 4.0 - NU**2  # back to nu=1
for eps in (0.32, 0.16, 0.08, 0.04, 0.02, 0.01, 0.005):
    seeds = (-2.5j + 0.12 * np.sqrt(eps) * np.exp(0.5j), -2.5j - 0.12 * np.sqrt(eps) * np.exp(0.5j))
    try:
        r1 = refine(seeds[0], eps)
        r2 = refine(seeds[1], eps)
        s = abs(r1 - r2)
        out["splitting"].append({"eps": eps, "omega1": [r1.real, r1.imag],
                                 "omega2": [r2.real, r2.imag], "split": s})
        print(f"eps={eps}: omega={r1:.6f} / {r2:.6f} split={s:.6e}", flush=True)
    except Exception as exc:
        print(f"eps={eps}: FAIL {exc}", flush=True)

sp = [(d["eps"], d["split"]) for d in out["splitting"] if d["split"] > 1e-9]
if len(sp) >= 3:
    e = np.log([p[0] for p in sp]); s = np.log([p[1] for p in sp])
    slope = np.polyfit(e, s, 1)[0]
    out["exponent"] = float(slope)
    print(f"splitting exponent d(log s)/d(log eps) = {slope:.4f}  (0.5=EP-2, 1.0=diabolic)", flush=True)

pathlib.Path("results/ds_jordan_test.json").write_text(json.dumps(out, indent=1))
print("done", flush=True)
