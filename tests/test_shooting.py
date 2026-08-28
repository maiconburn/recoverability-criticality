import numpy as np

from recoverability_ep.model import (
    build_constrained_pade,
    exact_gb_metric,
    exact_horizon_coefficients,
)
from recoverability_ep.shooting import (
    exact_solver,
    pade_solver,
    pair_invariants,
)

EP_Q2 = -16.147205102
EP_OMEGA = -5.673827755j


def test_fundamental_matches_literature_at_zero_coupling():
    b, bp, n_factor = exact_gb_metric(0.0)
    solver = exact_solver(0.0, b, bp, n_factor, 0.0)
    root = solver.refine_root(3.12 - 2.75j)
    assert abs(root - (3.119452 - 2.746676j)) < 1e-5


def test_fundamental_matches_collocation_at_benchmark_coupling():
    b, bp, n_factor = exact_gb_metric(0.08)
    solver = exact_solver(0.08, b, bp, n_factor, 0.0)
    root = solver.refine_root(3.2253 - 3.2245j)
    assert abs(root - (3.22527439 - 3.22445417j)) < 1e-6


def test_pade_horizon_series_matches_exact_solver():
    pade = build_constrained_pade(exact_horizon_coefficients(0.08, 10))
    _, _, n_factor = exact_gb_metric(0.08)
    solver = pade_solver(pade, n_factor, 0.0)
    root = solver.refine_root(3.2253 - 3.2245j)
    # N=10 geometry reproduces the fundamental to ~1e-4.
    assert abs(root - (3.22527439 - 3.22445417j)) < 1e-3


def test_mirror_pair_is_symmetric_near_exceptional_point():
    b, bp, n_factor = exact_gb_metric(0.08)
    solver = exact_solver(0.08, b, bp, n_factor, EP_Q2 + 1e-2)
    pair = solver.pair(np.array([0.18 - 5.67j, -0.18 - 5.67j]))
    mu, rho = pair_invariants(pair)
    assert abs(pair[0] + np.conj(pair[1])) < 1e-7
    assert abs(mu - EP_OMEGA) < 2e-2
    assert rho.real > 0
    assert abs(rho.imag) < 1e-8
    assert max(abs(solver.wronskian(pair[0])), abs(solver.wronskian(pair[1]))) < 1e-7


def test_pair_degenerates_at_exceptional_point():
    b, bp, n_factor = exact_gb_metric(0.08)
    solver = exact_solver(0.08, b, bp, n_factor, EP_Q2)
    pair = solver.pair(np.array([1e-3 - 5.6738j, -1e-3 - 5.6738j]))
    assert abs(pair[0] - pair[1]) < 1e-4
    assert abs(complex(np.mean(pair)) - EP_OMEGA) < 1e-4
