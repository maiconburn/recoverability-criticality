import numpy as np

from recoverability_ep.model import (
    build_constrained_pade,
    exact_gb_metric,
    exact_horizon_coefficients,
    physical_modes_at_zero_momentum,
    qnm_spectrum,
)


def test_exact_metric_boundary_and_horizon():
    b, _, _ = exact_gb_metric(0.08)
    assert np.isclose(b(0.0), 1.0)
    assert np.isclose(b(1.0), 0.0)


def test_constrained_pade_matches_series_and_boundary():
    coefficients = exact_horizon_coefficients(0.08, 7)
    pade = build_constrained_pade(coefficients)
    assert pade.is_admissible()
    assert np.isclose(pade.b(0.0), 1.0)
    assert np.isclose(pade.b(1.0), 0.0)
    # Numerical Taylor recovery at small x checks the leading coefficient.
    x = 1e-6
    assert np.isclose(pade.b(1.0 - x) / x, coefficients[0], rtol=1e-5)


def test_admissibility_rejects_hidden_physical_pole():
    # This order has a denominator zero at x ~= 0.7804.  A coarse sampling
    # grid can miss the narrow sign-changing excursion around that pole.
    pade = build_constrained_pade(exact_horizon_coefficients(0.08, 13))
    assert not pade.is_admissible()


def test_zero_momentum_benchmark():
    b, bp, n_factor = exact_gb_metric(0.08)
    modes = physical_modes_at_zero_momentum(
        qnm_spectrum(b, bp, n_factor, collocation_order=48), count=1
    )
    # Boundary-time normalization.  Multiplying by N_GB gives the alternate
    # horizon-time convention that appeared in the exploratory transcript.
    expected = np.array([3.22527439 - 3.22445417j])
    assert np.allclose(modes, expected, rtol=2e-7, atol=2e-7)
