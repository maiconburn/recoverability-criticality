"""Track the fundamental mode and its mirror partner along negative real q^2."""

import numpy as np

from recoverability_ep.criticality import SpectralFamily, match_pair
from recoverability_ep.model import exact_gb_metric

COUPLING = 0.08


def main() -> None:
    b, bp, n_factor = exact_gb_metric(COUPLING)
    family = SpectralFamily(b, bp, n_factor, collocation_order=72)
    omega0 = family.seed_pair()[0]
    pair = np.array([omega0, -np.conj(omega0)])
    print("mirror seed:", pair)
    for q2 in np.arange(0.0, -15.0 - 1e-9, -0.25):
        pair = match_pair(family.spectrum(q2), pair)
        split_sq = (pair[0] - pair[1]) ** 2
        print(
            f"q2={q2:7.2f}  pair=({pair[0]:.4f})({pair[1]:.4f})  "
            f"gap={abs(pair[0]-pair[1]):8.4f}  s={split_sq:.4f}"
        )


if __name__ == "__main__":
    main()
