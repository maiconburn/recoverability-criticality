"""High-accuracy scalar QNM shooting solver.

The Chebyshev collocation operator becomes strongly non-normal at the large
spacelike momenta where the mirror-pair exceptional point lives (eigenvalue
condition numbers of order 1e10), which floors double-precision eigenvalues
near 1e-3.  This module instead integrates the radial equation

    z b psi'' + (5b + z b') psi' + 4 b' psi
    + i N omega (2 z psi' + 5 psi) - N^2 q^2 z psi = 0

from the horizon (regular ingoing solution, seeded with a high-order
Frobenius series) toward the boundary and roots the source coefficient
W(omega) = z^5 psi'(z)|_{z=eps}.  W is analytic in omega and evaluated to
~1e-10, so isolated roots are recovered to that accuracy and
near-degenerate pairs to ~1e-5 through a local polynomial model, replacing
the square-root-of-backward-error floor of direct eigensolvers.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.integrate import solve_ivp

from .model import ConstrainedPade, MetricFunction, exact_horizon_coefficients


def pade_horizon_coefficients(pade: ConstrainedPade, order: int) -> tuple[float, ...]:
    """Taylor coefficients a_k of b = sum a_k x^k for a Pade geometry."""

    numerator = np.zeros(order)
    numerator[: len(pade.numerator)] = pade.numerator[:order]
    denominator = np.zeros(order)
    denominator[: len(pade.denominator)] = pade.denominator[:order]
    quotient = np.zeros(order)
    for k in range(order):
        quotient[k] = (
            numerator[k] - np.dot(denominator[1 : k + 1], quotient[k - 1 :: -1][:k])
        ) / denominator[0]
    return tuple(quotient)  # a_{k+1} = quotient[k] because b = x * (P/Q)


def horizon_series(
    a_coefficients: tuple[float, ...],
    omega_term: complex,
    momentum_term: complex,
    terms: int,
) -> np.ndarray:
    """Frobenius coefficients c_m of the regular solution, c_0 = 1.

    Uses the x = 1 - z form of the radial equation,
    P1 psi_xx + P2 psi_x + P3 psi = 0 with P1 = (1-x) b,
    P2 = -5 b + (1-x) b_x - 2 omega_term (1-x),
    P3 = -4 b_x + 5 omega_term - momentum_term (1-x).
    """

    padded = np.zeros(terms + 3)
    count = min(len(a_coefficients), terms + 2)
    padded[1 : count + 1] = a_coefficients[:count]

    p1 = np.zeros(terms + 2, dtype=complex)
    p2 = np.zeros(terms + 2, dtype=complex)
    p3 = np.zeros(terms + 2, dtype=complex)
    for k in range(terms + 2):
        p1[k] = padded[k] - (padded[k - 1] if k >= 1 else 0.0)
        p2[k] = -5.0 * padded[k] + (k + 1) * padded[k + 1] - k * padded[k]
        p3[k] = -4.0 * (k + 1) * padded[k + 1]
    p2[0] -= 2.0 * omega_term
    p2[1] += 2.0 * omega_term
    p3[0] += 5.0 * omega_term - momentum_term
    p3[1] += momentum_term

    coefficients = np.zeros(terms + 1, dtype=complex)
    coefficients[0] = 1.0
    a1 = p1[1]
    for m in range(terms):
        accumulator = 0.0 + 0.0j
        for j in range(2, m + 2):
            accumulator += p1[j] * (m + 2 - j) * (m + 1 - j) * coefficients[m + 2 - j]
        for j in range(1, m + 2):
            accumulator += p2[j] * (m + 1 - j) * coefficients[m + 1 - j]
        for j in range(0, m + 1):
            accumulator += p3[j] * coefficients[m - j]
        denominator = (m + 1) * (m * a1 + p2[0])
        coefficients[m + 1] = -accumulator / denominator
    return coefficients


@dataclass
class ShootingSolver:
    b: MetricFunction
    bp: MetricFunction
    n_factor: float
    momentum_squared: complex
    horizon_coefficients: tuple[float, ...] = field(default=())
    boundary_cut: float = 1e-3
    horizon_offset: float = 5e-3
    series_terms: int = 14
    rtol: float = 1e-10
    atol: float = 1e-12

    def wronskian(self, omega: complex) -> complex:
        """Source coefficient of the ingoing solution; zero at a QNM."""

        n_omega = 1j * self.n_factor * omega
        nq2 = self.n_factor**2 * self.momentum_squared

        def rhs(z: float, state):
            psi, dpsi = state
            b_value = float(np.real(self.b(z)))
            bp_value = float(np.real(self.bp(z)))
            second = -(
                (5.0 * b_value + z * bp_value + 2.0 * n_omega * z) * dpsi
                + (4.0 * bp_value + 5.0 * n_omega - nq2 * z) * psi
            ) / (z * b_value)
            return [dpsi, second]

        series = horizon_series(
            self.horizon_coefficients, n_omega, nq2, self.series_terms
        )
        x0 = self.horizon_offset
        powers = x0 ** np.arange(self.series_terms + 1)
        psi_start = np.dot(series, powers)
        dpsi_dx = np.dot(
            series[1:] * np.arange(1, self.series_terms + 1),
            x0 ** np.arange(self.series_terms),
        )
        solution = solve_ivp(
            rhs,
            (1.0 - x0, self.boundary_cut),
            [psi_start, -dpsi_dx],
            method="DOP853",
            rtol=self.rtol,
            atol=self.atol,
        )
        if not solution.success:
            raise RuntimeError(f"integration failed at omega={omega}")
        psi, dpsi = solution.y[:, -1]
        return complex(self.boundary_cut**5 * dpsi)

    def refine_root(
        self,
        omega_seed: complex,
        tolerance: float = 1e-10,
        max_iterations: int = 40,
        max_step: float = 0.25,
        max_wander: float = 1.5,
    ) -> complex:
        """Complex secant iteration on W starting from an eigenvalue seed."""

        first = complex(omega_seed)
        second = first + 1e-4 * (1.0 + 1.0j)
        w_first = self.wronskian(first)
        w_second = self.wronskian(second)
        for _ in range(max_iterations):
            denominator = w_second - w_first
            if denominator == 0:
                break
            step = -w_second * (second - first) / denominator
            if abs(step) > max_step:
                step *= max_step / abs(step)
            first, w_first = second, w_second
            second = second + step
            if abs(second - omega_seed) > max_wander:
                raise RuntimeError(
                    f"secant wandered from {omega_seed} to {second}"
                )
            w_second = self.wronskian(second)
            if abs(step) < tolerance:
                break
        return second

    def quadratic_pair(
        self,
        centroid: complex,
        stencil: float = 1e-3,
        iterations: int = 6,
        tolerance: float = 1e-9,
    ) -> np.ndarray:
        """Both W-roots near ``centroid`` from a local quadratic model.

        Plain secant iterations oscillate on a nearly double zero, but the
        quadratic Taylor model of W around the pair centroid recovers both
        roots at once with error linear in the W evaluation noise; the
        centroid update converges even at exact degeneracy.  The stencil is
        kept at ~1e-3 so the cubic-term bias stays below the ~1e-5 noise
        floor set by the next W zero a distance ~1.5 away.
        """

        center = complex(centroid)
        for _ in range(iterations):
            w_center = self.wronskian(center)
            w_plus = self.wronskian(center + stencil)
            w_minus = self.wronskian(center - stencil)
            slope = (w_plus - w_minus) / (2.0 * stencil)
            curvature = (w_plus + w_minus - 2.0 * w_center) / (stencil**2)
            if curvature == 0:
                break
            # Roots of (curvature/2) d^2 + slope d + w_center = 0.
            discriminant = np.sqrt(slope**2 - 2.0 * curvature * w_center)
            root_high = center + (-slope + discriminant) / curvature
            root_low = center + (-slope - discriminant) / curvature
            new_center = 0.5 * (root_high + root_low)
            moved = abs(new_center - center)
            if moved > 0.5:
                new_center = center + 0.5 * (new_center - center) / moved
            center = new_center
            if moved < tolerance:
                break
        return np.array([root_high, root_low])

    def pair(self, seed_pair, separated_gap: float = 0.8) -> np.ndarray:
        """Refine an approximate branch pair to shooting accuracy.

        Well-separated members are polished by independent secant
        iterations.  A close pair goes through the quadratic-model solver;
        if the recovered splitting is large enough, each member is then
        re-polished individually to remove the residual model bias.
        """

        seed = np.asarray(seed_pair, dtype=complex)
        gap = abs(seed[0] - seed[1])
        if gap > separated_gap:
            try:
                return np.array(
                    [self.refine_root(seed[0]), self.refine_root(seed[1])]
                )
            except RuntimeError:
                pass
        rough = self.quadratic_pair(complex(np.mean(seed)))
        if abs(rough[0] - rough[1]) > 5e-3:
            # Seeds from the quadratic model are already ~1e-5 accurate, so
            # a short polish suffices; a pair too close for the secant to
            # converge quickly simply keeps the quadratic-model roots.
            try:
                polished = np.array(
                    [
                        self.refine_root(rough[0], max_iterations=12),
                        self.refine_root(rough[1], max_iterations=12),
                    ]
                )
                if abs(polished[0] - polished[1]) > 1e-9:
                    return polished
            except RuntimeError:
                pass
        return rough


def exact_solver(
    coupling: float,
    b: MetricFunction,
    bp: MetricFunction,
    n_factor: float,
    momentum_squared: complex,
    **kwargs,
) -> ShootingSolver:
    return ShootingSolver(
        b,
        bp,
        n_factor,
        momentum_squared,
        horizon_coefficients=exact_horizon_coefficients(coupling, 24),
        **kwargs,
    )


def pade_solver(
    pade: ConstrainedPade,
    n_factor: float,
    momentum_squared: complex,
    **kwargs,
) -> ShootingSolver:
    return ShootingSolver(
        pade.b,
        pade.bp,
        n_factor,
        momentum_squared,
        horizon_coefficients=pade_horizon_coefficients(pade, 24),
        **kwargs,
    )


def pair_invariants(pair: np.ndarray) -> tuple[complex, complex]:
    """Symmetric-function coordinates (mu, rho) with omega = mu +- sqrt(rho)."""

    mu = complex(0.5 * (pair[0] + pair[1]))
    rho = complex((0.5 * (pair[0] - pair[1])) ** 2)
    return mu, rho
