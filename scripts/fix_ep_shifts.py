"""Recompute each family's EP locally around the exact EP.

The global downward march can slip onto the second mirror-pair collision
(near q^2 ~ -17.9) for a family whose split function develops a spurious
positive excursion; here we instead root ρ_N(q^2) starting from the exact
EP, using the family's own ladder pair as seed, which is unambiguous for
every family whose EP shift is small (all N >= 3).
"""

import json
from pathlib import Path

import numpy as np

from recoverability_ep.model import (
    build_constrained_pade,
    exact_gb_metric,
    exact_horizon_coefficients,
)
from recoverability_ep.shooting import (
    ShootingSolver,
    pade_horizon_coefficients,
    pair_invariants,
)

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results" / "validation.json"
COUPLING = 0.08


def main() -> None:
    data = json.loads(RESULTS.read_text())
    q2_ep = data["ep_exact"]["q2"]
    _, _, n_factor = exact_gb_metric(COUPLING)

    for entry in data["levels"]:
        order = entry["N"]
        pade = build_constrained_pade(exact_horizon_coefficients(COUPLING, order))
        coefficients = pade_horizon_coefficients(pade, 24)

        pair = np.array(
            [complex(re, im) for re, im in entry["pairs"][f"{0.0:.6e}"]]
        )

        def rho_at(q2, seed):
            solver = ShootingSolver(
                pade.b, pade.bp, n_factor, q2, horizon_coefficients=coefficients
            )
            new_pair = solver.pair(seed)
            _, rho = pair_invariants(new_pair)
            return float(rho.real), new_pair

        # Walk from the exact EP in the direction that increases rho, then
        # secant on rho.  Seeded by the family's own pair at the exact EP.
        rho_zero, pair = rho_at(q2_ep, pair)
        direction = 1.0 if rho_zero < 0 else -1.0
        step = max(2.0 * abs(rho_zero) / 3.4, 1e-6)
        a, rho_a = q2_ep, rho_zero
        for _ in range(60):
            b_point = a + direction * step
            rho_b, pair = rho_at(b_point, pair)
            if rho_a * rho_b < 0:
                break
            a, rho_a = b_point, rho_b
            step *= 1.6
        else:
            print(f"N={order}: no local bracket, keeping old value")
            continue

        low, rho_low, high, rho_high = a, rho_a, b_point, rho_b
        root = low
        for _ in range(60):
            root = high - rho_high * (low - high) / (rho_low - rho_high)
            rho_root, pair = rho_at(root, pair)
            if abs(rho_root) < 1e-13 or abs(high - low) < 1e-12:
                break
            if rho_root * rho_low > 0:
                low, rho_low = root, rho_root
            else:
                high, rho_high = root, rho_root

        mu, _ = pair_invariants(pair)
        old_shift = entry["ep_q2"] - q2_ep
        entry["ep_q2"] = root
        entry["ep_omega"] = [float(np.real(mu)), float(np.imag(mu))]
        entry["ep_gap"] = float(abs(pair[0] - pair[1]))
        print(
            f"N={order:2d} shift: old={old_shift:+.3e} new={root - q2_ep:+.3e}"
        )

    RESULTS.write_text(json.dumps(data, indent=2))
    print("updated", RESULTS)


if __name__ == "__main__":
    main()
