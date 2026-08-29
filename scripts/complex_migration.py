"""Does the EP migrate to complex q^2 above lambda_ext, or die?

Newton continuation of the shooting-solver EP condition rho(q^2) = 0 (complex
rho, complex q^2), seeded at the last real EP (lambda = 0.1145) and continued
upward in lambda.  If the annihilation is two real EPs merging and moving off
the real axis (fold in the complex plane), Im(q2_c) should grow ~ sqrt(lambda
- lambda_ext); if the EP truly terminates, Newton loses the root.

Usage: complex_migration.py  (no args)
Appends rows to results/complex_migration.json.
"""
import json
import pathlib

import numpy as np

from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients
from recoverability_ep.shooting import ShootingSolver, pair_invariants

SEED_LAM = 0.1145
SEED_Q2 = -33.45 + 0.0j
SEED_OMEGA = -7.6e-0j - 7.62j  # placeholder; recomputed below from real anchor
LAMBDAS = [0.1145, 0.115, 0.1155, 0.116, 0.117, 0.118, 0.120, 0.1225, 0.125]

def solver_at(lam, q2, cache={}):
    if lam not in cache:
        b, bp, n = exact_gb_metric(lam)
        cache[lam] = (b, bp, n, exact_horizon_coefficients(lam, 24))
    b, bp, n, hc = cache[lam]
    return ShootingSolver(b, bp, n, complex(q2), horizon_coefficients=hc)

def rho_of(lam, q2, pair_seed):
    s = solver_at(lam, q2)
    pair = s.pair(pair_seed)
    _, rho = pair_invariants(pair)
    return complex(rho), pair

# real anchor: recover the 0.1145 EP pair by marching from the 0.114 EP
pair = solver_at(0.114, -33.489164251).quadratic_pair(0.000003233 - 7.644615228j)
for lam in np.linspace(0.114, SEED_LAM, 3)[1:]:
    pair = solver_at(float(lam), -33.45).pair(pair)

q2 = SEED_Q2
out = []
for lam in LAMBDAS:
    # Newton in complex q2 on rho(q2) = 0
    converged = False
    for it in range(25):
        try:
            rho, pair = rho_of(lam, q2, pair)
            h = 1e-4 * (1 + abs(q2))
            rho_h, _ = rho_of(lam, q2 + h, pair)
            drho = (rho_h - rho) / h
            step = -rho / drho
            if abs(step) > 0.5:
                step *= 0.5 / abs(step)
            q2 = q2 + step
            if abs(rho) < 1e-10 and abs(step) < 1e-8:
                converged = True
                break
        except Exception as exc:
            out.append({"lam": lam, "error": str(exc)})
            break
    row = {"lam": lam, "q2_re": q2.real, "q2_im": q2.imag,
           "abs_rho": abs(rho), "converged": converged,
           "omega": [pair[0].real, pair[0].imag]}
    out.append(row)
    print(json.dumps(row), flush=True)

pathlib.Path("results/complex_migration.json").write_text(json.dumps(out, indent=1))
print("done", flush=True)
