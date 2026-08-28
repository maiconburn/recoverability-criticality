"""Exploratory scan: admissible Pade orders and first branch coalescence."""

import time

import numpy as np

from recoverability_ep.criticality import (
    SpectralFamily,
    refine_exceptional_point,
    scan_for_coalescence,
    track_pair,
)
from recoverability_ep.model import (
    build_constrained_pade,
    exact_gb_metric,
    exact_horizon_coefficients,
)

COUPLING = 0.08

def main() -> None:
    b, bp, n_factor = exact_gb_metric(COUPLING)

    admissible = []
    for order in range(2, 17):
        pade = build_constrained_pade(exact_horizon_coefficients(COUPLING, order))
        error = float(
            np.max(np.abs(pade.b(np.linspace(0, 1, 2001)) - b(np.linspace(0, 1, 2001))))
        )
        admissible.append((order, pade.is_admissible(), error))
    print("order admissible sup_error")
    for order, ok, error in admissible:
        print(f"{order:5d} {str(ok):>10s} {error:.3e}")

    family = SpectralFamily(b, bp, n_factor, collocation_order=56)
    print("seed pair at q2=0:", family.seed_pair())

    start = time.time()
    q2_best, pair, records = scan_for_coalescence(
        family,
        real_min=0.0,
        real_max=45.0,
        imag_values=np.arange(-30.0, 0.0 + 1e-9, 1.0),
        step=0.4,
    )
    gaps = sorted(records, key=lambda item: item[1])[:8]
    print(f"scan time {time.time()-start:.1f}s, minima:")
    for q2, gap in gaps:
        print(f"  q2={q2:.2f}  gap={gap:.4f}")

    ep = refine_exceptional_point(family, q2_best, pair)
    print("refined EP (order 56):", ep)

    for order in (72, 88):
        fam = SpectralFamily(b, bp, n_factor, collocation_order=order)
        seed = track_pair(fam, [0.0, 1j * ep.momentum_squared.imag, ep.momentum_squared])
        ep_check = refine_exceptional_point(fam, ep.momentum_squared, seed)
        print(f"refined EP (order {order}):", ep_check)


if __name__ == "__main__":
    main()
