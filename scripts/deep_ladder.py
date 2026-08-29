"""Cross-family universality test: the critical-cost law on the DEEP mirror
family (lambda = 0.120, omega_c = -9.73i) — first test of the halving law on
a spectral family other than the fundamental pair.

Reuses the validation machinery: exact ladder in d, constrained-Pade
reconstruction from N horizon coefficients, per-N EP relocation, spectral
errors eps(N, d).  Analysis: slope alpha(d) of log eps vs N; halving =
alpha(d_large) / alpha(d=0) (prediction: 2).
"""
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from run_validation import DISTANCES, falsi, ladder, make_solver, solver_pair  # noqa: E402
from run_validation import find_ep_local  # noqa: E402

from recoverability_ep.model import (
    build_constrained_pade,
    exact_gb_metric,
    exact_horizon_coefficients,
)
from recoverability_ep.shooting import pade_horizon_coefficients, pair_invariants

LAM = 0.120
Q2_GUESS = -32.29
OMEGA_GUESS = -9.73j
LEVELS = range(3, 15)

def pair_error(pair, reference):
    a = sorted(pair, key=lambda w: w.real)
    b = sorted(reference, key=lambda w: w.real)
    return float(max(abs(a[0] - b[0]), abs(a[1] - b[1])))

b_exact, bp_exact, n_factor = exact_gb_metric(LAM)
exact_geometry = (b_exact, bp_exact, exact_horizon_coefficients(LAM, 24))
grid = np.linspace(0.0, 1.0, 4001)

wp = json.loads(pathlib.Path("results/wide_profile.json").read_text())
rows = next(e["rows"] for e in wp if e["lam"] == 0.12)
rows = [r for r in rows if r[1] is not None]
rmin = min(rows, key=lambda r: r[1])
q2_seed = rmin[0]
pair0 = np.array([rmin[2] + 1j * rmin[3], -rmin[2] + 1j * rmin[3]])
print(f"seed row: q2={q2_seed} rho={rmin[1]:.3e} pair~{pair0}", flush=True)
state = {"pair": pair0}

def rho_at(q2):
    solver = make_solver(exact_geometry, n_factor, q2)
    state["pair"] = solver_pair(solver, state["pair"])
    _, rho = pair_invariants(state["pair"])
    return float(rho.real)

q2_ep = q2_seed
solver = make_solver(exact_geometry, n_factor, q2_ep)
near_pair = solver.pair(pair0)
mu, _ = pair_invariants(near_pair)
omega_ep, gap = mu, float(abs(near_pair[0] - near_pair[1]))
print(f"deep EP anchor: q2_c={q2_ep:.9f} omega_c={omega_ep:.9f} gap={gap:.1e}", flush=True)
assert gap < 1e-3, "anchor did not converge"

exact_pairs = ladder(exact_geometry, n_factor, q2_ep, near_pair)
result = {"coupling": LAM, "family": "deep", "ep": {"q2": q2_ep,
          "omega": [omega_ep.real, omega_ep.imag], "gap": gap}, "levels": []}

for order in LEVELS:
    pade = build_constrained_pade(exact_horizon_coefficients(LAM, order))
    if not pade.is_admissible():
        print(f"N={order}: inadmissible", flush=True)
        continue
    geometry = (pade.b, pade.bp, pade_horizon_coefficients(pade, 24))
    geometry_error = float(np.max(np.abs(pade.b(grid) - b_exact(grid))))
    pairs_n = ladder(geometry, n_factor, q2_ep, None, per_distance_seeds=exact_pairs)
    try:
        q2_ep_n, omega_ep_n, gap_n, pair_n = find_ep_local(
            geometry, n_factor, q2_ep, pairs_n[0.0])
        solver_n = make_solver(geometry, n_factor, q2_ep_n)
        pair_at_own_ep = solver_pair(solver_n, pair_n)
        eps_own = pair_error(pair_at_own_ep, exact_pairs[0.0])
        shift = q2_ep_n - q2_ep
    except RuntimeError as exc:
        eps_own, shift, gap_n = None, None, None
        print(f"  N={order}: relocation failed ({exc})", flush=True)
    errors = {f"{d:.6e}": pair_error(pairs_n[d], exact_pairs[d])
              for d in DISTANCES + [0.0]}
    result["levels"].append({"N": order, "geometry_error": geometry_error,
                             "errors": errors, "eps_own_ep": eps_own,
                             "ep_shift": shift, "ep_gap_n": gap_n})
    print(f"N={order:2d} geom={geometry_error:.3e} "
          f"eps(1e-1)={errors[f'{1e-1:.6e}']:.3e} eps(0)={errors[f'{0.0:.6e}']:.3e}",
          flush=True)

pathlib.Path("results/deep_ladder_final.json").write_text(json.dumps(result, indent=1))

# analysis: slopes
lv = result["levels"]
Ns = np.array([e["N"] for e in lv])
print("\nslopes alpha(d) [log eps vs N, N>=5]:", flush=True)
sel = Ns >= 5
alphas = {}
for d in [0.0] + sorted(DISTANCES):
    eps = np.array([e["errors"][f"{d:.6e}"] for e in lv])
    ok = sel & (eps > 0) & np.isfinite(eps)
    if ok.sum() >= 4:
        a = -np.polyfit(Ns[ok], np.log(eps[ok]), 1)[0]
        alphas[d] = a
        print(f"  d={d:.3e}: alpha={a:.4f}", flush=True)
own = np.array([e["eps_own_ep"] if e["eps_own_ep"] else np.nan for e in lv])
oko = sel & np.isfinite(own) & (own > 0)
if oko.sum() >= 4:
    a_ep = -np.polyfit(Ns[oko], np.log(own[oko]), 1)[0]
    print(f"  own-EP: alpha_EP={a_ep:.4f}  (n={oko.sum()})", flush=True)
    if 0.1 in alphas:
        print(f"\nHALVING deep family: alpha(d=1e-1)/alpha_EP(own) = "
              f"{alphas[0.1]/a_ep:.3f}  (prediction 2)", flush=True)
print("done", flush=True)
