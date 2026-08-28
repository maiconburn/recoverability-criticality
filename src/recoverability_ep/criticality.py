"""Exceptional-point tools for the scalar QNM family at complex momentum.

The preregistered prediction (transcript turn 112) is tested by tracking the
two lowest scalar quasinormal branches into the complex momentum plane,
locating their coalescence point (a second-order exceptional point), and
measuring how the spectral error of Pade-reconstructed geometries behaves as
the exceptional point is approached.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

import numpy as np
from scipy.linalg import eig
from scipy.optimize import minimize

from .model import MetricFunction, chebyshev_matrix

Array = np.ndarray


class SpectralFamily:
    """Scalar QNM generalized eigenproblem, linear in complex q^2."""

    def __init__(
        self,
        b: MetricFunction,
        bp: MetricFunction,
        n_factor: float,
        collocation_order: int = 72,
        max_abs_frequency: float = 60.0,
    ) -> None:
        derivative_x, x_nodes = chebyshev_matrix(collocation_order)
        z = (1.0 - x_nodes) / 2.0
        derivative_z = -2.0 * derivative_x
        derivative_zz = derivative_z @ derivative_z
        b_values = np.asarray(b(z), dtype=complex)
        bp_values = np.asarray(bp(z), dtype=complex)
        self.base_operator = (
            np.diag(z * b_values) @ derivative_zz
            + np.diag(5.0 * b_values + z * bp_values) @ derivative_z
            + np.diag(4.0 * bp_values)
        )
        self.z_diagonal = np.diag(z)
        self.frequency_operator = 2.0 * self.z_diagonal @ derivative_z + 5.0 * np.eye(
            collocation_order + 1
        )
        self.n_factor = float(n_factor)
        self.max_abs_frequency = max_abs_frequency

    def spectrum(self, momentum_squared: complex) -> Array:
        operator = (
            self.base_operator
            - self.n_factor**2 * momentum_squared * self.z_diagonal
        )
        eigenvalues = eig(operator, self.frequency_operator, right=False)
        frequencies = 1j * eigenvalues / self.n_factor
        mask = np.isfinite(frequencies) & (
            np.abs(frequencies) < self.max_abs_frequency
        )
        return frequencies[mask]

    def seed_pair(self) -> Array:
        """The two lowest physical modes at q^2=0 (positive-real, damped)."""

        frequencies = self.spectrum(0.0)
        selected = frequencies[
            (frequencies.real > 1e-7) & (frequencies.imag < -1e-7)
        ]
        selected = selected[np.argsort(np.abs(selected.imag))]
        return selected[:2]


def match_pair(spectrum: Array, reference: Array) -> Array:
    """Assign two distinct eigenvalues to the reference pair optimally."""

    distances = np.abs(spectrum[None, :] - np.asarray(reference)[:, None])
    candidate_indices = np.unique(
        np.concatenate([np.argsort(row)[:4] for row in distances])
    )
    best_cost = np.inf
    best = None
    for i, j in permutations(candidate_indices, 2):
        cost = distances[0, i] + distances[1, j]
        if cost < best_cost:
            best_cost = cost
            best = np.array([spectrum[i], spectrum[j]])
    return best


def pair_distance(pair_a: Array, pair_b: Array) -> float:
    """Optimal-permutation mean distance between two unordered pairs."""

    direct = 0.5 * (abs(pair_a[0] - pair_b[0]) + abs(pair_a[1] - pair_b[1]))
    swapped = 0.5 * (abs(pair_a[0] - pair_b[1]) + abs(pair_a[1] - pair_b[0]))
    return float(min(direct, swapped))


def track_pair(
    family: SpectralFamily,
    q2_path: Array,
    seed: Array | None = None,
    max_step: float = 0.05,
) -> Array:
    """Continue a branch pair along a piecewise-linear q^2 path."""

    pair = family.seed_pair() if seed is None else np.asarray(seed)
    q2_points = np.asarray(q2_path, dtype=complex)
    current = q2_points[0]
    pair = match_pair(family.spectrum(current), pair)
    for target in q2_points[1:]:
        distance = abs(target - current)
        steps = max(1, int(np.ceil(distance / max_step)))
        for step in range(1, steps + 1):
            q2 = current + (target - current) * step / steps
            pair = match_pair(family.spectrum(q2), pair)
        current = target
    return pair


@dataclass(frozen=True)
class ExceptionalPoint:
    momentum_squared: complex
    frequency: complex
    gap: float


def mirror_seed(family: SpectralFamily) -> Array:
    """Fundamental mode and its ω → −conj(ω) mirror partner at q^2=0."""

    omega0 = family.seed_pair()[0]
    return np.array([omega0, -np.conj(omega0)])


def find_mirror_ep(
    family: SpectralFamily,
    walk_start: float = -12.0,
    walk_limit: float = -30.0,
    coarse_step: float = 0.05,
) -> ExceptionalPoint:
    """Locate the collision of the fundamental mirror pair on the real q^2 axis.

    For real momentum-squared the spectrum is symmetric under ω → −conj(ω),
    so the split function s(q^2) = Re[(ω_a − ω_b)^2] is positive on the
    propagating side, negative on the overdamped side, and crosses zero at a
    second-order exceptional point.  The crossing is bracketed by a downward
    walk and polished with Brent's method.
    """

    from scipy.optimize import brentq

    pair = track_pair(family, [0.0, walk_start], seed=mirror_seed(family))
    q2_high = walk_start
    s_high = float(((pair[0] - pair[1]) ** 2).real)
    if s_high <= 0.0:
        raise RuntimeError("Walk started on the overdamped side; move walk_start up.")
    q2 = walk_start
    while q2 > walk_limit:
        q2_next = q2 - coarse_step
        pair = match_pair(family.spectrum(q2_next), pair)
        s_next = float(((pair[0] - pair[1]) ** 2).real)
        if s_next <= 0.0:
            break
        q2_high, s_high = q2_next, s_next
        q2 = q2_next
    else:
        raise RuntimeError("No mirror-pair collision found before walk_limit.")

    centroid = complex(np.mean(pair))

    def split_function(q2_value: float) -> float:
        spectrum = family.spectrum(q2_value)
        order = np.argsort(np.abs(spectrum - centroid))
        near_pair = spectrum[order[:2]]
        return float(((near_pair[0] - near_pair[1]) ** 2).real)

    root = brentq(split_function, q2_next, q2_high, xtol=1e-13, rtol=1e-14)
    spectrum = family.spectrum(root)
    order = np.argsort(np.abs(spectrum - centroid))
    near_pair = spectrum[order[:2]]
    return ExceptionalPoint(
        momentum_squared=complex(root),
        frequency=complex(np.mean(near_pair)),
        gap=float(abs(near_pair[0] - near_pair[1])),
    )


def refine_exceptional_point(
    family: SpectralFamily,
    q2_guess: complex,
    reference_pair: Array,
    rounds: int = 3,
    simplex_scale: float = 0.05,
    trust_radius: float = 1.0,
) -> ExceptionalPoint:
    """Minimize the branch gap around a coalescence candidate.

    The trust region keeps Nelder-Mead from escaping toward spurious
    high-overtone near-degeneracies far from the tracked pair.
    """

    centroid = complex(np.mean(reference_pair))
    q2_center = complex(q2_guess)
    q2_anchor = complex(q2_guess)
    scale = simplex_scale
    for _ in range(rounds):
        def gap_objective(parameters: Array) -> float:
            q2 = complex(parameters[0], parameters[1])
            if abs(q2 - q2_anchor) > trust_radius:
                return 1e3 + abs(q2 - q2_anchor)
            spectrum = family.spectrum(q2)
            order = np.argsort(np.abs(spectrum - centroid))
            pair = spectrum[order[:2]]
            return float(abs(pair[0] - pair[1]))

        result = minimize(
            gap_objective,
            x0=[q2_center.real, q2_center.imag],
            method="Nelder-Mead",
            options={
                "xatol": 1e-12,
                "fatol": 1e-12,
                "initial_simplex": np.array(
                    [
                        [q2_center.real, q2_center.imag],
                        [q2_center.real + scale, q2_center.imag],
                        [q2_center.real, q2_center.imag + scale],
                    ]
                ),
                "maxiter": 400,
            },
        )
        q2_center = complex(result.x[0], result.x[1])
        spectrum = family.spectrum(q2_center)
        order = np.argsort(np.abs(spectrum - centroid))
        pair = spectrum[order[:2]]
        centroid = complex(np.mean(pair))
        scale = max(1e-7, 0.02 * scale)
    return ExceptionalPoint(
        momentum_squared=q2_center,
        frequency=centroid,
        gap=float(abs(pair[0] - pair[1])),
    )


def scan_for_coalescence(
    family: SpectralFamily,
    real_min: float = -8.0,
    real_max: float = 12.0,
    imag_values: Array | None = None,
    step: float = 0.2,
) -> tuple[complex, Array, list[tuple[complex, float]]]:
    """Coarse scan of the complex q^2 plane for the minimal pair gap.

    Continuation runs along the imaginary axis and then outward along each
    horizontal half-row, so branch identity is preserved from the q^2=0 seed.
    """

    if imag_values is None:
        imag_values = np.arange(-8.0, 8.0 + 1e-9, 0.5)
    records: list[tuple[complex, float]] = []
    best_q2 = 0.0 + 0.0j
    best_pair = family.seed_pair()
    best_gap = np.inf
    for imag_part in imag_values:
        row_seed = track_pair(family, [0.0, 1j * imag_part], max_step=step)
        for real_grid in (
            np.arange(0.0, real_max + 1e-9, step),
            np.arange(0.0, -real_min + 1e-9, step) * -1.0,
        ):
            pair = row_seed
            for real_part in real_grid:
                q2 = complex(real_part, imag_part)
                pair = match_pair(family.spectrum(q2), pair)
                gap = float(abs(pair[0] - pair[1]))
                records.append((q2, gap))
                if gap < best_gap:
                    best_gap = gap
                    best_q2 = q2
                    best_pair = pair
    return best_q2, best_pair, records
