"""Production run for the preregistered exceptional-point validation.

Protocol (frozen in transcript turn 112 before any of this was computed):

  P1  away from the EP:  eps_omega(N, d) ∝ exp(-alpha N) / sqrt(d)
  P2  at the EP:         eps_omega(N, 0) ∝ exp(-alpha N / 2)
  P3  complexity:        N_eps(d) = A + (1 / 2 alpha) ln(1 / d)
  P4  benchmark slope:   about 1.5 extra levels per decade of approach

The exceptional point is the collision of the fundamental scalar mode with
its mirror partner on the negative real q^2 axis.  Distances d below are
measured in q^2; the local map q -> q^2 is linear, so every logarithmic
slope is the same in either variable.

All spectra come from the shooting solver (the collocation eigenproblem is
1e10-conditioned in this momentum region and only supplies seeds); branch
pairs are extracted through the quadratic model of the Wronskian, which
stays well conditioned across the exceptional point.  Results are written
incrementally so an interrupted run resumes where it stopped.
"""

import json
import time
from pathlib import Path

import numpy as np

from recoverability_ep.criticality import SpectralFamily, mirror_seed, track_pair
from recoverability_ep.model import (
    build_constrained_pade,
    exact_gb_metric,
    exact_horizon_coefficients,
)
from recoverability_ep.shooting import (
    ShootingSolver,
    exact_solver,
    pade_horizon_coefficients,
    pair_invariants,
)

import sys as _sys
COUPLING = float(_sys.argv[1]) if len(_sys.argv) > 1 else 0.120
SEED_COLLOCATION_ORDER = 56
CANDIDATE_LEVELS = range(3, 16)
DISTANCES = [10.0 ** (-exponent / 2.0) for exponent in range(2, 9)]  # 1e-1 .. 1e-4
WALK_START = -12.0
OUTPUT = Path(__file__).resolve().parent.parent / "results" / f"validation_deep_{_sys.argv[1] if len(_sys.argv) > 1 else 0.120}.json"


def make_solver(geometry, n_factor, q2):
    b, bp, coefficients = geometry
    return ShootingSolver(b, bp, n_factor, q2, horizon_coefficients=coefficients)


def solver_pair(solver, seed):
    pair = solver.pair(seed)
    if abs(pair[0] - pair[1]) < 1e-9 and abs(seed[0] - seed[1]) > 1e-6:
        pair = solver.quadratic_pair(complex(np.mean(seed)))
    return pair


def falsi(rho_at, low, rho_low, high, rho_high):
    root = high
    for _ in range(60):
        root = high - rho_high * (low - high) / (rho_low - rho_high)
        rho_root = rho_at(root)
        if abs(rho_root) < 1e-13 or abs(high - low) < 1e-12:
            break
        if rho_root * rho_low > 0:
            low, rho_low = root, rho_root
        else:
            high, rho_high = root, rho_root
    return root


def find_ep_global(geometry, n_factor, seed_pair, q2_start=WALK_START, floor=-55.0):
    """Adaptive downward march (steps ~0.1 rho) plus a regula-falsi polish."""

    state = {"pair": np.asarray(seed_pair, dtype=complex)}

    def rho_at(q2):
        solver = make_solver(geometry, n_factor, q2)
        state["pair"] = solver_pair(solver, state["pair"])
        _, rho = pair_invariants(state["pair"])
        return float(rho.real)

    q2 = q2_start
    rho_here = rho_at(q2)
    if rho_here <= 0:
        raise RuntimeError(f"walk start {q2_start} is already overdamped")
    while True:
        step = min(0.25, max(1.5e-3, 0.1 * rho_here))
        q2_next = q2 - step
        rho_next = rho_at(q2_next)
        if rho_next <= 0:
            break
        q2, rho_here = q2_next, rho_next
        if q2 < floor:
            raise RuntimeError(f"no collision found before q2={floor}")

    root = falsi(rho_at, q2_next, rho_next, q2, rho_here)
    solver = make_solver(geometry, n_factor, root)
    pair = solver.quadratic_pair(complex(np.mean(state["pair"])))
    mu, _ = pair_invariants(pair)
    return root, mu, float(abs(pair[0] - pair[1])), pair


def find_ep_local(geometry, n_factor, q2_center, seed_pair):
    """Root rho_N around the exact EP; valid while the family's EP shift is
    small (every admissible N >= 3).  Walking in the direction that raises
    rho gives a bracket in a handful of geometrically growing steps."""

    state = {"pair": np.asarray(seed_pair, dtype=complex)}

    def rho_at(q2):
        solver = make_solver(geometry, n_factor, q2)
        state["pair"] = solver_pair(solver, state["pair"])
        _, rho = pair_invariants(state["pair"])
        return float(rho.real)

    rho_center = rho_at(q2_center)
    direction = 1.0 if rho_center < 0 else -1.0
    step = max(2.0 * abs(rho_center) / 3.4, 1e-7)
    a, rho_a = q2_center, rho_center
    for _ in range(60):
        b_point = a + direction * step
        rho_b = rho_at(b_point)
        if rho_a * rho_b < 0:
            break
        a, rho_a = b_point, rho_b
        step *= 1.6
        if abs(b_point - q2_center) > 1.0:
            raise RuntimeError("local EP search left its trust region")
    else:
        raise RuntimeError("no local bracket")

    root = falsi(rho_at, a, rho_a, b_point, rho_b)
    solver = make_solver(geometry, n_factor, root)
    pair = solver.quadratic_pair(complex(np.mean(state["pair"])))
    mu, _ = pair_invariants(pair)
    return root, mu, float(abs(pair[0] - pair[1])), pair


def ladder(geometry, n_factor, q2_ep, start_pair, per_distance_seeds=None):
    pairs = {}
    running = np.asarray(start_pair, dtype=complex)
    for distance in [0.0] + sorted(DISTANCES):
        seed = (
            per_distance_seeds[distance]
            if per_distance_seeds is not None
            else running
        )
        solver = make_solver(geometry, n_factor, q2_ep + distance)
        running = solver_pair(solver, seed)
        pairs[distance] = running
    return pairs


def complex_pair(value):
    return [float(np.real(value)), float(np.imag(value))]


def decode_pairs(encoded):
    return {
        float(key): np.array([complex(re, im) for re, im in value])
        for key, value in encoded.items()
    }


def pair_error(pair_a, pair_b):
    direct = 0.5 * (abs(pair_a[0] - pair_b[0]) + abs(pair_a[1] - pair_b[1]))
    swapped = 0.5 * (abs(pair_a[0] - pair_b[1]) + abs(pair_a[1] - pair_b[0]))
    return float(min(direct, swapped))


def save(result):
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2))


def main() -> None:
    started = time.time()
    b_exact, bp_exact, n_factor = exact_gb_metric(COUPLING)
    exact_geometry = (b_exact, bp_exact, exact_horizon_coefficients(COUPLING, 24))
    grid = np.linspace(0.0, 1.0, 4001)

    result = None
    if OUTPUT.exists():
        result = json.loads(OUTPUT.read_text())
        print(f"resuming: {len(result['levels'])} levels already done")

    if result is None:
        import json as _json
        if abs(COUPLING - 0.120) < 1e-9:
            _wp = _json.loads((OUTPUT.parent / "wide_profile.json").read_text())
            _rows = [r for r in next(e["rows"] for e in _wp if e["lam"] == 0.12)
                     if r[1] is not None]
            _rmin = min(_rows, key=lambda r: r[1])
            q2_ep = _rmin[0]
            _p0 = np.array([_rmin[2] + 1j * _rmin[3], -_rmin[2] + 1j * _rmin[3]])
        else:
            # lambda=0.117 needle from forest_scan refine
            q2_ep = -32.50
            _p0 = np.array([1e-3 - 10.294j, -1e-3 - 10.294j])
        near_pair = make_solver(exact_geometry, n_factor, q2_ep).pair(_p0)
        from recoverability_ep.shooting import pair_invariants as _pi
        omega_ep, _ = _pi(near_pair)
        ep_gap = float(abs(near_pair[0] - near_pair[1]))
        assert ep_gap < 1e-3
        print(f"exact EP: q2_c={q2_ep:.9f} omega_c={omega_ep:.9f} gap={ep_gap:.1e}")
        exact_pairs = ladder(exact_geometry, n_factor, q2_ep, near_pair)
        result = {
            "coupling": COUPLING,
            "distances": DISTANCES,
            "ep_exact": {
                "q2": q2_ep,
                "omega": complex_pair(omega_ep),
                "gap": ep_gap,
            },
            "exact_pairs": {
                f"{d:.6e}": [complex_pair(p) for p in exact_pairs[d]]
                for d in DISTANCES + [0.0]
            },
            "levels": [],
        }
        save(result)
    else:
        q2_ep = result["ep_exact"]["q2"]
        exact_pairs = decode_pairs(result["exact_pairs"])

    done = {entry["N"] for entry in result["levels"]}
    for order in CANDIDATE_LEVELS:
        if order in done:
            continue
        pade = build_constrained_pade(exact_horizon_coefficients(COUPLING, order))
        if not pade.is_admissible():
            print(f"N={order}: inadmissible Pade, skipped")
            continue
        geometry = (pade.b, pade.bp, pade_horizon_coefficients(pade, 24))
        geometry_error = float(np.max(np.abs(pade.b(grid) - b_exact(grid))))
        pairs_n = ladder(
            geometry, n_factor, q2_ep, None, per_distance_seeds=exact_pairs
        )
        try:
            if order == 2:
                raise RuntimeError("N=2 EP sits far away; use the global walk")
            q2_ep_n, omega_ep_n, gap_n, _ = find_ep_local(
                geometry, n_factor, q2_ep, pairs_n[0.0]
            )
        except RuntimeError:
            family_n = SpectralFamily(
                pade.b, pade.bp, n_factor, collocation_order=SEED_COLLOCATION_ORDER
            )
            for start in (WALK_START, -8.0, -5.0, -3.0):
                walk_n = track_pair(
                    family_n, [0.0, start], seed=mirror_seed(family_n)
                )
                try:
                    q2_ep_n, omega_ep_n, gap_n, _ = find_ep_global(
                        geometry, n_factor, walk_n, q2_start=start
                    )
                    break
                except RuntimeError:
                    continue
            else:
                print(f"N={order}: no EP found, skipped", flush=True)
                continue
        if abs(q2_ep_n - q2_ep) > 0.5:
            print(f"N={order}: relocated EP wandered ({q2_ep_n - q2_ep:+.3f}), skipped", flush=True)
            continue
        errors = {
            f"{d:.6e}": pair_error(pairs_n[d], exact_pairs[d])
            for d in DISTANCES + [0.0]
        }
        result["levels"].append(
            {
                "N": order,
                "geometry_error": geometry_error,
                "ep_q2": q2_ep_n,
                "ep_omega": complex_pair(omega_ep_n),
                "ep_gap": gap_n,
                "pairs": {
                    f"{d:.6e}": [complex_pair(p) for p in pairs_n[d]]
                    for d in DISTANCES + [0.0]
                },
                "errors": errors,
            }
        )
        save(result)
        print(
            f"N={order:2d} geom={geometry_error:.3e} "
            f"ep_shift={q2_ep_n - q2_ep:+.3e} "
            f"eps(1e-1)={errors[f'{1e-1:.6e}']:.3e} "
            f"eps(0)={errors[f'{0.0:.6e}']:.3e} "
            f"[{time.time() - started:.0f}s]"
        )

    if "robustness" not in result:
        omega_ep = complex(*result["ep_exact"]["omega"])
        robust = {}
        for tag, kwargs in (
            ("tight", dict(rtol=1e-12, atol=1e-14)),
            ("offset", dict(horizon_offset=2e-3)),
            ("cut", dict(boundary_cut=5e-4)),
        ):
            solver = exact_solver(
                COUPLING, b_exact, bp_exact, n_factor, q2_ep, **kwargs
            )
            pair = solver.quadratic_pair(omega_ep)
            robust[tag] = [complex_pair(p) for p in pair]
            print(f"robustness {tag}: pair at exact EP = {pair}")
        result["robustness"] = robust
        save(result)

    print(f"wrote {OUTPUT} in {time.time() - started:.0f}s")


if __name__ == "__main__":
    main()
