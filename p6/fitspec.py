"""Class-restricted chain fit and spectral estimator (spec 4.2-4.4).

theta = (mu0; a_0..a_{nJ-1}; b_1..b_{nJ-1}), Sigma_theta a continued fraction
closed by the transparent tail; the estimator matches the model head
A_N(theta) to the data head in least squares, then roots F on sheet 2.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares

from bath import BathConfig, nodes_weights
from refs import quadratic_pair


def transparent_tail(z, w_band, sheet=1):
    root = np.sqrt(z - w_band) * np.sqrt(z + w_band)
    return (z - root) / 2.0 if sheet == 1 else (z + root) / 2.0


def sigma_chain(theta, z, w_band, sheet=1):
    """Continued fraction with transparent termination."""

    mu0 = theta[0]
    n_sites = (len(theta) - 1 + 1) // 2  # a has n_sites entries, b has n_sites-1
    a = theta[1 : 1 + n_sites]
    b = theta[1 + n_sites :]
    tail = transparent_tail(z, w_band, sheet)
    value = z - a[-1] - tail
    for j in range(n_sites - 2, -1, -1):
        value = z - a[j] - b[j] ** 2 / value
    return mu0 / value


def reference_chain(config: BathConfig, n_sites: int, m_modes: int = 4000):
    """Exact Jacobi coefficients of the bath measure by grid Lanczos."""

    _, _, omega, delta_m, couplings = nodes_weights(m_modes, config)
    weights = couplings**2
    mu0 = weights.sum()
    p = np.sqrt(weights / mu0)
    a_list, b_list = [], []
    q_prev = np.zeros_like(p)
    q_curr = p.copy()
    beta = 0.0
    for _ in range(n_sites):
        a_val = float(np.sum(omega * q_curr**2))
        a_list.append(a_val)
        residual = omega * q_curr - a_val * q_curr - beta * q_prev
        residual -= q_curr * (q_curr @ residual)  # reorthogonalize
        residual -= q_prev * (q_prev @ residual)
        beta = float(np.linalg.norm(residual))
        b_list.append(beta)
        q_prev, q_curr = q_curr, residual / beta
    return float(mu0), np.array(a_list), np.array(b_list[:-1])


def forward_head(theta, g, delta, config: BathConfig, modes, omega, delta_m):
    sigma = sigma_chain(theta, omega + 1e-14j, config.w_band, sheet=1)
    j_theta = -sigma.imag / np.pi
    if np.min(j_theta) < -1e-12:
        return None
    denominator = (omega - delta - sigma) * omega - g**2
    root_j = np.sqrt(np.clip(j_theta, 0.0, None) * delta_m)
    gamma = np.zeros((len(omega), 2), dtype=complex)
    gamma[:, 0] = root_j * omega / denominator
    gamma[:, 1] = root_j * g / denominator
    return modes.T @ gamma


def fit_chain(a_data, g, delta, config: BathConfig, modes_full, omega, delta_m, theta_init):
    n_keep = a_data.shape[0]
    modes = modes_full[:, :n_keep]

    def residual(theta):
        model = forward_head(theta, g, delta, config, modes, omega, delta_m)
        if model is None:
            return np.full(4 * n_keep, 1e3)
        diff = model - a_data
        return np.concatenate([diff.real.ravel(), diff.imag.ravel()])

    solution = least_squares(
        residual, theta_init, method="lm", xtol=1e-14, ftol=1e-14, max_nfev=4000
    )
    return solution.x, float(np.max(np.abs(solution.fun)))


def eigenpair(theta, g, delta, config: BathConfig, seeds):
    """Roots of the fitted F on sheet 2, one Newton per seed (tol 1e-12)."""

    def f_sheet2(z):
        return (z - delta - sigma_chain(theta, z, config.w_band, sheet=2)) * z - g**2

    roots = []
    for seed in np.atleast_1d(seeds):
        z = complex(seed)
        for _ in range(80):
            f = f_sheet2(z)
            h = 1e-8
            d1 = (f_sheet2(z + h) - f_sheet2(z - h)) / (2.0 * h)
            if d1 == 0:
                break
            dz = -f / d1
            if abs(dz) > 0.1:
                dz *= 0.1 / abs(dz)
            z += dz
            if abs(dz) < 1e-13:
                break
        roots.append(z)
    roots = np.array(roots)
    residuals = [abs(f_sheet2(z)) for z in roots]
    return roots, max(residuals)


def eigenpair_degenerate(theta, g, delta, config: BathConfig, centroid):
    """Near-EP pair by the quadratic model of the fitted F (spec 4.4, d=0)."""

    def f_sheet2(z):
        return (z - delta - sigma_chain(theta, z, config.w_band, sheet=2)) * z - g**2

    pair = quadratic_pair(f_sheet2, centroid, stencil=1e-4)
    residuals = [abs(f_sheet2(pair[0])), abs(f_sheet2(pair[1]))]
    return pair, max(residuals)


def initial_theta(config: BathConfig, n_sites: int, reference=None):
    if reference is None:
        reference = reference_chain(config, n_sites + 1)
    mu0, a_ref, b_ref = reference
    theta = np.zeros(2 * n_sites)
    theta[0] = mu0
    theta[1 : 1 + n_sites] = a_ref[:n_sites]
    theta[1 + n_sites :] = b_ref[: n_sites - 1]
    return theta


def extend_theta(theta, config: BathConfig):
    """Continuation N -> N+2: add one site seeded at the free chain values."""

    n_sites = (len(theta)) // 2
    new = np.zeros(2 * (n_sites + 1))
    new[0] = theta[0]
    new[1 : 1 + n_sites] = theta[1 : 1 + n_sites]
    new[1 + n_sites] = 0.0
    new[2 + n_sites : 2 + 2 * n_sites - 1] = theta[1 + n_sites :]
    new[-1] = config.w_band / 2.0
    return new
