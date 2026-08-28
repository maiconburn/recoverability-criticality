"""Einstein--Gauss--Bonnet reconstruction and scalar QNM utilities.

The background is the five-dimensional planar Einstein--Gauss--Bonnet black
brane with horizon at z=1 and AdS boundary at z=0.  Frequencies and momenta
are dimensionless in horizon-radius units.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Iterable

import numpy as np
import sympy as sp
from scipy.linalg import eig

Array = np.ndarray
MetricFunction = Callable[[Array | float], Array | float]


def gb_normalization(coupling: float) -> tuple[float, float]:
    """Return (N_GB^2, N_GB), choosing unit boundary speed of light."""

    if coupling >= 0.25:
        raise ValueError("The Einstein branch requires lambda_GB < 1/4.")
    n_squared = (1.0 + np.sqrt(1.0 - 4.0 * coupling)) / 2.0
    return float(n_squared), float(np.sqrt(n_squared))


def exact_gb_metric(
    coupling: float,
) -> tuple[MetricFunction, MetricFunction, float]:
    """Return b(z), db/dz and N_GB for the exact black-brane geometry."""

    n_squared, n_factor = gb_normalization(coupling)

    if abs(coupling) < 1e-14:
        def b(z: Array | float) -> Array | float:
            z_array = np.asarray(z)
            return 1.0 - z_array**4

        def bp(z: Array | float) -> Array | float:
            z_array = np.asarray(z)
            return -4.0 * z_array**3

        return b, bp, n_factor

    def b(z: Array | float) -> Array | float:
        z_array = np.asarray(z)
        radicand = 1.0 - 4.0 * coupling * (1.0 - z_array**4)
        return n_squared / (2.0 * coupling) * (1.0 - np.sqrt(radicand))

    def bp(z: Array | float) -> Array | float:
        z_array = np.asarray(z)
        radicand = 1.0 - 4.0 * coupling * (1.0 - z_array**4)
        return -4.0 * n_squared * z_array**3 / np.sqrt(radicand)

    return b, bp, n_factor


@lru_cache(maxsize=None)
def exact_horizon_coefficients(coupling: float, order: int) -> tuple[float, ...]:
    """Taylor coefficients a_n of b(z)=sum a_n(1-z)^n at the horizon."""

    if order < 1:
        return ()
    x = sp.symbols("x")
    lam = sp.Float(coupling, 60)
    z = 1 - x
    if abs(coupling) < 1e-14:
        expression = 1 - z**4
    else:
        n_squared = (1 + sp.sqrt(1 - 4 * lam)) / 2
        expression = n_squared / (2 * lam) * (
            1 - sp.sqrt(1 - 4 * lam * (1 - z**4))
        )
    series = sp.series(expression, x, 0, order + 1).removeO().expand()
    return tuple(float(sp.N(series.coeff(x, n), 40)) for n in range(1, order + 1))


@dataclass(frozen=True)
class ConstrainedPade:
    """Boundary-normalized Padé continuation of a horizon Taylor series."""

    numerator: Array
    denominator: Array
    matched_order: int

    def b(self, z: Array | float) -> Array | float:
        x = 1.0 - np.asarray(z)
        p = np.polynomial.polynomial.polyval(x, self.numerator)
        q = np.polynomial.polynomial.polyval(x, self.denominator)
        return x * p / q

    def bp(self, z: Array | float) -> Array | float:
        x = 1.0 - np.asarray(z)
        p = np.polynomial.polynomial.polyval(x, self.numerator)
        q = np.polynomial.polynomial.polyval(x, self.denominator)
        dp_coeff = np.arange(1, len(self.numerator)) * self.numerator[1:]
        dq_coeff = np.arange(1, len(self.denominator)) * self.denominator[1:]
        dp = (
            np.polynomial.polynomial.polyval(x, dp_coeff)
            if len(dp_coeff)
            else 0.0
        )
        dq = (
            np.polynomial.polynomial.polyval(x, dq_coeff)
            if len(dq_coeff)
            else 0.0
        )
        derivative_x = ((p + x * dp) * q - x * p * dq) / q**2
        return -derivative_x

    def minimum_denominator(self, samples: int = 2001) -> float:
        x = np.linspace(0.0, 1.0, samples)
        values = np.polynomial.polynomial.polyval(x, self.denominator)
        return float(np.min(np.abs(values)))

    def is_admissible(self, samples: int = 2001, tolerance: float = 1e-8) -> bool:
        # A grid-only check can miss a very narrow real pole.  Order 13 of the
        # present benchmark is an explicit example, so reject denominator
        # roots on the physical continuation interval before sampling b(z).
        roots = np.roots(self.denominator[::-1])
        has_physical_pole = np.any(
            (np.abs(roots.imag) < 1e-9)
            & (roots.real >= -1e-10)
            & (roots.real <= 1.0 + 1e-10)
        )
        z = np.linspace(0.0, 1.0, samples)
        values = np.asarray(self.b(z))
        return bool(
            not has_physical_pole
            and self.minimum_denominator(samples) > 1e-7
            and np.all(np.isfinite(values))
            and values.min() >= -tolerance
            and values.max() <= 5.0
        )


def build_constrained_pade(
    coefficients: Iterable[float], denominator_degree: int | None = None
) -> ConstrainedPade:
    """Match N horizon coefficients and impose b(0)=1.

    The ansatz is b(x)=x P_{L-1}(x)/Q_M(x), x=1-z, Q_M(0)=1,
    with L+M=N+1.  The default is the nearly diagonal split used in the
    preregistered reconstruction protocol.
    """

    rec = np.asarray(tuple(coefficients), dtype=float)
    order = len(rec)
    if order < 1:
        raise ValueError("At least one horizon coefficient is required.")
    m_degree = (order + 1) // 2 if denominator_degree is None else denominator_degree
    l_count = order + 1 - m_degree
    if m_degree < 0 or l_count < 1:
        raise ValueError("Invalid Padé degree split.")

    # Unknowns are p_0,...,p_{L-1},q_1,...,q_M.
    matrix = np.zeros((order + 1, l_count + m_degree), dtype=float)
    rhs = np.zeros(order + 1, dtype=float)
    a = np.r_[0.0, rec]
    for row, power in enumerate(range(1, order + 1)):
        if power - 1 < l_count:
            matrix[row, power - 1] = -1.0
        for j in range(1, m_degree + 1):
            if power - j >= 1:
                matrix[row, l_count + j - 1] += a[power - j]
        rhs[row] = -a[power]

    # P(1)=Q(1) enforces b(z=0)=1.
    matrix[order, :l_count] = 1.0
    matrix[order, l_count:] = -1.0
    rhs[order] = 1.0
    solution = np.linalg.solve(matrix, rhs)
    numerator = solution[:l_count]
    denominator = np.r_[1.0, solution[l_count:]]
    return ConstrainedPade(numerator, denominator, order)


def chebyshev_matrix(intervals: int) -> tuple[Array, Array]:
    """Chebyshev differentiation matrix and nodes on [-1,1]."""

    if intervals < 1:
        return np.array([[0.0]]), np.array([1.0])
    nodes = np.cos(np.pi * np.arange(intervals + 1) / intervals)
    weights = np.ones(intervals + 1)
    weights[[0, -1]] = 2.0
    weights *= (-1.0) ** np.arange(intervals + 1)
    tiled = np.tile(nodes, (intervals + 1, 1)).T
    differences = tiled - tiled.T
    derivative = np.outer(weights, 1.0 / weights) / (
        differences + np.eye(intervals + 1)
    )
    derivative -= np.diag(np.sum(derivative, axis=1))
    return derivative, nodes


def qnm_spectrum(
    b: MetricFunction,
    bp: MetricFunction,
    n_factor: float,
    momentum_squared: complex = 0.0,
    collocation_order: int = 60,
    max_abs_frequency: float = 100.0,
) -> Array:
    r"""Compute massless-scalar QNMs using ingoing EF collocation.

    After writing the normalizable field as Phi=z^4 psi, the radial equation is

      z b psi'' + (5b+z b') psi' + 4b' psi
      + i N omega (2z psi' + 5psi) - N^2 q^2 z psi = 0.

    The returned array contains all finite modes below ``max_abs_frequency``;
    callers perform branch tracking rather than relying on a global sort.
    """

    derivative_x, x_nodes = chebyshev_matrix(collocation_order)
    z = (1.0 - x_nodes) / 2.0
    derivative_z = -2.0 * derivative_x
    derivative_zz = derivative_z @ derivative_z
    b_values = np.asarray(b(z), dtype=complex)
    bp_values = np.asarray(bp(z), dtype=complex)

    operator = (
        np.diag(z * b_values) @ derivative_zz
        + np.diag(5.0 * b_values + z * bp_values) @ derivative_z
        + np.diag(4.0 * bp_values)
        - (n_factor**2) * momentum_squared * np.diag(z)
    )
    frequency_operator = 2.0 * np.diag(z) @ derivative_z + 5.0 * np.eye(
        collocation_order + 1
    )
    eigenvalues = eig(operator, frequency_operator, right=False)
    frequencies = 1j * eigenvalues / n_factor
    mask = np.isfinite(frequencies) & (np.abs(frequencies) < max_abs_frequency)
    return frequencies[mask]


def physical_modes_at_zero_momentum(
    frequencies: Array, count: int = 6
) -> Array:
    """Select the positive-real, damped scalar branch at real q=0."""

    selected = frequencies[
        (frequencies.real > 1e-7) & (frequencies.imag < -1e-7)
    ]
    selected = selected[np.argsort(np.abs(selected.imag))]
    return selected[:count]
