import numpy as np

from recoverability_ep.criticality import (
    SpectralFamily,
    find_mirror_ep,
    match_pair,
    mirror_seed,
    pair_distance,
    track_pair,
)
from recoverability_ep.model import exact_gb_metric


def make_family(order: int = 40) -> SpectralFamily:
    b, bp, n_factor = exact_gb_metric(0.08)
    return SpectralFamily(b, bp, n_factor, collocation_order=order)


def test_match_pair_picks_distinct_nearest():
    spectrum = np.array([1 + 1j, 1.05 + 1j, 4 - 2j, -3 + 0.5j])
    pair = match_pair(spectrum, np.array([1.01 + 1j, 1.04 + 1j]))
    assert set(pair) == {1 + 1j, 1.05 + 1j}


def test_pair_distance_is_permutation_invariant():
    pair_a = np.array([1 + 1j, -1 + 1j])
    pair_b = np.array([-1 + 1.1j, 1 + 0.9j])
    assert np.isclose(pair_distance(pair_a, pair_b), 0.1)


def test_mirror_pair_stays_symmetric_under_tracking():
    family = make_family()
    pair = track_pair(family, [0.0, -4.0], seed=mirror_seed(family))
    assert np.isclose(pair[0].real, -pair[1].real, atol=1e-8)
    assert np.isclose(pair[0].imag, pair[1].imag, atol=1e-8)


def test_mirror_ep_location_and_degeneracy():
    family = make_family(order=48)
    ep = find_mirror_ep(family)
    # Production (shooting) value is q2_c = -16.1472051.  The collocation
    # eigenproblem is ~1e10-conditioned here, which floors the achievable
    # pair gap near 1e-1; the locator must still find the right region.
    assert -16.5 < ep.momentum_squared.real < -15.8
    assert ep.gap < 0.2
    assert abs(ep.frequency.real) < 1e-3
    assert ep.frequency.imag < -4.0
