"""Regenerate the P8-F3 instrument-gate data with a DOCUMENTED grid (the
original gate script was never committed; results/p8f3_gate.json holds
only the shapes), then run the P8-F4' confluence tests frozen in
results/FROZEN_P8F4_CONFLUENCE.md.

Model (CosmoFlow PiSigma, single exchange): H = 1, c_s = 1, quadratic
mixing rho = 0.1 and one cubic vertex kappa2 (dot-pi^2 sigma) = 0.1,
both ramped on with tanh((N - N_i - 1)/0.1) (CosmoFlow's adiabatic
i-epsilon prescription: couplings switch on about one e-fold after the
initial conditions); all other cubics zero. Squeezed configuration
k1 = k2 = k_S = 1 (horizon exit at N = 0), k3 = k_L on a log grid of
15 points over 1.7 decades, k_L in [1e-3, 1e-1] (v2: the first grid reached k_L = 0.5, outside the squeezed regime, and the shapes there were not monotonic). Initial conditions
3 e-folds before the long mode exits; shape read at N_ref = 6.
Shape S = (2 pi)^-4 (k1 k2 k3)^2 <pi pi pi> / (mean Delta^2_pi)^2, the
CosmoFlow tutorial definition. Masses: nu = 1 (m^2 = 5/4) and
nu = 0.85 (m^2 = 9/4 - 0.85^2).
"""
import json
import pathlib
import sys
import time
import types

import numpy as np

try:
    from scipy.misc import derivative  # noqa: F401
except Exception:
    import scipy

    def derivative(func, x0, dx=1e-6, n=1, args=()):
        return (func(x0 + dx, *args) - func(x0 - dx, *args)) / (2 * dx)

    shim = types.ModuleType("scipy.misc")
    shim.derivative = derivative
    sys.modules["scipy.misc"] = shim
    scipy.misc = shim

PISIGMA = pathlib.Path.home() / "fisica/contrib/CosmoFlow/CosmoFlow/PiSigma"
sys.path.insert(0, str(PISIGMA))
from background_inputs import background_inputs  # noqa: E402
from solver import solver  # noqa: E402

KL = np.logspace(-3.0, -1.0, 15)
RHO, KAPPA2 = 0.1, 0.1
N_REF = 6.0
RTOL = [1e-5, 1e-5, 1e-5]
ATOL = [1e-100, 1e-100, 1e-100]


def shape_scan(nu, kl_grid=KL, rtol=RTOL):
    m2 = 9.0 / 4.0 - nu ** 2
    out = []
    for kl in kl_grid:
        Ni = np.log(kl) - 3.0
        N_load = np.linspace(Ni - 2, N_REF + 2, 6000)
        ramp = (np.tanh((N_load - (Ni + 1.0)) / 0.1) + 1) / 2
        ones, zeros = np.ones_like(N_load), np.zeros_like(N_load)
        interp = background_inputs(N_load, ones, ones, np.sqrt(m2) * ones,
                                   RHO * ramp, zeros, zeros, zeros, zeros,
                                   zeros, KAPPA2 * ramp).output()
        Nspan = np.linspace(Ni, N_REF, 4000)
        s = solver(Nspan, 2, interp, rtol, ATOL)
        t0 = time.time()
        f = s.f_solution(k1=1.0, k2=1.0, k3=kl)
        d2 = [f[i][0, 0][-1] * k ** 3 / (2 * np.pi ** 2) for i, k in ((0, 1.0), (1, 1.0), (2, kl))]
        S = (k1k2k3 := (1.0 * 1.0 * kl) ** 2) * f[6][0, 0, 0][-1] / (2 * np.pi) ** 4 / (np.mean(d2)) ** 2
        out.append(float(S))
        print(f"  nu={nu} kL={kl:.4e} S={S:.6e} ({time.time() - t0:.1f}s)", flush=True)
    return np.array(out)


def wls(x, S, basis):
    X = np.vstack(basis).T
    w = 1 / np.abs(S)
    c, *_ = np.linalg.lstsq(X * w[:, None], S * w, rcond=None)
    rel = (S - X @ c) / S
    return c, float(np.sqrt(np.mean(rel ** 2)))


def main():
    res = {"grid_kL": KL.tolist(), "rho": RHO, "kappa2": KAPPA2, "N_ref": N_REF, "rtol": RTOL}
    x = KL / 1.0
    lnx = np.log(x)
    for nu in (1.0, 0.85):
        S = shape_scan(nu)
        res[f"S_nu{nu}"] = S.tolist()
        # leading-slope sanity: S ~ x^{1/2-nu} at small x
        sl = np.polyfit(lnx[:5], np.log(np.abs(S[:5])), 1)[0]
        # F3-style fixed basis (x^{3/2} at both nu)
        c0, r0 = wls(x, S, [x ** (0.5 - nu), x ** 1.5])
        c1, r1 = wls(x, S, [x ** (0.5 - nu), x ** 1.5, x ** 1.5 * lnx])
        # F4'.1 nu-correct basis
        c2, r2 = wls(x, S, [x ** (0.5 - nu), x ** (0.5 + nu)])
        c3, r3 = wls(x, S, [x ** (0.5 - nu), x ** (0.5 + nu), x ** (0.5 + nu) * lnx])
        res[f"nu{nu}"] = {"leading_slope": sl, "expected_leading": 0.5 - nu,
                          "F3_fixed_basis": {"rms_nolog": r0, "rms_log": r1, "R": (r0 / r1) ** 2,
                                             "clog_over_c32": float(c1[2] / c1[1])},
                          "nu_correct_basis": {"rms_nolog": r2, "rms_log": r3, "R": (r2 / r3) ** 2,
                                               "clog_over_csub": float(c3[2] / c3[1])}}
        print(f"nu={nu}: leading slope {sl:.3f} (exp {0.5-nu:.2f}) | F3 fixed basis R={(r0/r1)**2:.2f} "
              f"| nu-correct basis R={(r2/r3)**2:.2f} clog/csub={c3[2]/c3[1]:.3f}", flush=True)
    # F4'.2 mimicry at nu = 1 by a log-free three-power basis with nu' scanned
    S1 = np.array(res["S_nu1.0"])
    _, r_log = wls(x, S1, [x ** -0.5, x ** 1.5, x ** 1.5 * lnx])
    scan = []
    for nup in np.linspace(0.95, 1.05, 41):
        if abs(nup - 1.0) < 1e-9:
            continue
        _, r3p = wls(x, S1, [x ** (0.5 - nup), x ** (0.5 + nup), x ** (2.5 - nup)])
        scan.append([float(nup), r3p])
    best = min(scan, key=lambda t: t[1])
    res["F4p2_mimicry"] = {"rms_log_basis": r_log, "scan": scan, "best_nu_prime": best[0],
                           "best_rms": best[1], "ratio_best_over_log": best[1] / r_log}
    print(f"F4'.2: log-basis rms {r_log:.3e}; best three-power nu'={best[0]:.4f} rms {best[1]:.3e} "
          f"ratio {best[1]/r_log:.2f}", flush=True)
    R1 = res["nu1.0"]["nu_correct_basis"]["R"]
    R85 = res["nu0.85"]["nu_correct_basis"]["R"]
    res["F4p1_localization"] = {"R_nu1": R1, "R_nu085_correct_basis": R85, "ratio": R1 / R85}
    print(f"F4'.1: R(1)={R1:.2f} R(0.85, correct basis)={R85:.2f} ratio {R1/R85:.2f}", flush=True)
    pathlib.Path("results/p8f4_confluence.json").write_text(json.dumps(res, indent=1))
    print("done", flush=True)


if __name__ == "__main__":
    main()
