"""Instrument validation: CosmoFlow vs the exact massive-scalar spectrum
in pure de Sitter, before any P8 phase-2 use (house rule: unit-test gates
before physics).

Exact target (H = 1, mode k, e-fold N, exit at N = 0 for k = 1):
  Delta^2_sigma(N) = k^3/(2 pi^2) |u_k|^2
                   = (1/(8 pi)) e^{-3N} |H^(1)_nu(k e^{-N})|^2,
  nu = sqrt(9/4 - m^2).
Gate: relative deviation < 1% for N in [1, 5] after exit, at
  m^2 = 5/4 (nu = 1, our critical point),
  m^2 = 2   (nu = 1/2),
  m^2 = 9/4 (nu = 0, the AHM logarithmic point; this is the money check
             that the tool captures the Jordan/log physics).

Requires the CosmoFlow clone at ~/fisica/contrib/CosmoFlow (PiSigma
model, rho = 0, all cubic couplings zero). scipy >= 1.12 lacks
scipy.misc.derivative; a central-difference shim is installed first.
"""
import json
import pathlib
import sys
import types

import numpy as np

# scipy.misc.derivative shim for scipy >= 1.12
try:
    from scipy.misc import derivative  # noqa: F401
except Exception:
    import scipy

    def derivative(func, x0, dx=1e-6, n=1, args=()):
        if n != 1:
            raise NotImplementedError
        return (func(x0 + dx, *args) - func(x0 - dx, *args)) / (2 * dx)

    shim = types.ModuleType("scipy.misc")
    shim.derivative = derivative
    sys.modules["scipy.misc"] = shim
    scipy.misc = shim

PISIGMA = pathlib.Path.home() / "fisica/contrib/CosmoFlow/CosmoFlow/CosmoFlow/PiSigma"
if not PISIGMA.is_dir():
    PISIGMA = pathlib.Path.home() / "fisica/contrib/CosmoFlow/CosmoFlow/PiSigma"
sys.path.insert(0, str(PISIGMA))
from background_inputs import background_inputs  # noqa: E402
from solver import solver  # noqa: E402

from mpmath import mp, hankel1  # noqa: E402

mp.dps = 30

N_load = np.linspace(-8.0, 12.0, 2001)
ones = np.ones_like(N_load)
zeros = np.zeros_like(N_load)
NSPAN = np.linspace(-4.0, 6.0, 1200)
K = 1.0
RTOL = [1e-6, 1e-6, 1e-5]
ATOL = [1e-12, 1e-12, 1e-10]

CASES = [("nu1_critical", 1.25), ("nu_half", 2.0), ("nu0_AHM", 2.25)]
out = {}
for label, m2 in CASES:
    m = np.sqrt(m2)
    interpolated = background_inputs(
        N_load, ones, ones, m * ones, zeros, zeros, zeros, zeros, zeros,
        zeros, zeros).output()
    s = solver(NSPAN, 2, interpolated, RTOL, ATOL)
    Sigma = s.SigmaAB_solution(K, "Re")
    delta2_num = K ** 3 / (2 * np.pi ** 2) * Sigma[1, 1]

    nu = complex(np.sqrt(complex(9.0 / 4.0 - m2)))
    exact = []
    for N in NSPAN:
        x = mp.mpf(K) * mp.e ** (-mp.mpf(N))
        h = hankel1(mp.mpc(nu.real, nu.imag), x)
        exact.append(float(mp.e ** (-3 * mp.mpf(N)) * abs(h) ** 2 / (8 * mp.pi)))
    exact = np.array(exact)

    sel = (NSPAN >= 1.0) & (NSPAN <= 5.0)
    rel = np.abs(delta2_num[sel] / exact[sel] - 1.0)
    out[label] = {"m2": m2, "max_rel_dev_N1_5": float(rel.max()),
                  "mean_rel_dev": float(rel.mean()),
                  "delta2_at_N4_num": float(np.interp(4.0, NSPAN, delta2_num)),
                  "delta2_at_N4_exact": float(np.interp(4.0, NSPAN, exact))}
    print(f"{label}: m2={m2} max_rel_dev(N in [1,5]) = {rel.max():.3e} "
          f"mean = {rel.mean():.3e}", flush=True)

gate = all(v["max_rel_dev_N1_5"] < 0.01 for v in out.values())
out["gate_1pct"] = gate
print(f"GATE (<1% all three masses): {'PASS' if gate else 'FAIL'}", flush=True)
pathlib.Path("results/p18_cosmoflow_validation.json").write_text(
    json.dumps(out, indent=1))
print("done", flush=True)
