"""Total Hermitian model, emission amplitudes, detector head (spec 1.1, 3.1, 2.1)."""

from __future__ import annotations

import hashlib

import numpy as np

from bath import BathConfig, nodes_weights, sigma_closed


def build_total(g, delta, config: BathConfig, m_modes: int):
    _, _, omega, delta_m, couplings = nodes_weights(m_modes, config)
    dim = m_modes + 2
    h = np.zeros((dim, dim))
    h[0, 0] = delta
    h[0, 1] = h[1, 0] = g
    h[2:, 2:] = np.diag(omega)
    h[0, 2:] = h[2:, 0] = couplings
    return h, omega, delta_m, couplings


def emitted_amplitudes(g, delta, config: BathConfig, m_modes: int, t_final: float):
    """gamma^(i)[m] for i in {a, b}: evolve basis columns, strip free phases."""

    h, omega, delta_m, couplings = build_total(g, delta, config, m_modes)
    energies, vectors = np.linalg.eigh(h)
    phases = np.exp(-1j * energies * t_final)
    gamma = np.zeros((m_modes, 2), dtype=complex)
    residual = 0.0
    for i in range(2):
        start = np.zeros(m_modes + 2)
        start[i] = 1.0
        psi = vectors @ (phases * (vectors.T @ start))
        residual = max(residual, float(np.linalg.norm(psi[:2])))
        gamma[:, i] = np.exp(+1j * omega * t_final) * psi[2:]
    return gamma, residual, omega, delta_m, couplings


def analytic_amplitudes(g, delta, config: BathConfig, m_modes: int):
    """gamma^(i)[m] = g_m G_{a,i}(omega + i0): spec 3.1 closed form."""

    _, _, omega, delta_m, couplings = nodes_weights(m_modes, config)
    sigma = sigma_closed(omega + 1e-14j, config, sheet=1)
    denominator = (omega - delta - sigma) * omega - g**2
    gamma = np.zeros((m_modes, 2), dtype=complex)
    gamma[:, 0] = couplings * omega / denominator
    gamma[:, 1] = couplings * g / denominator
    return gamma


def chebyshev_modes(n_modes: int, config: BathConfig, m_modes: int):
    """Family-1 detector modes: u_k[m] = sqrt(lam_m) U_k(x_m), exactly orthonormal."""

    x, lam, _, _, _ = nodes_weights(m_modes, config)
    modes = np.zeros((m_modes, n_modes))
    u_prev = np.ones_like(x)
    u_curr = 2.0 * x
    for k in range(n_modes):
        if k == 0:
            poly = u_prev
        elif k == 1:
            poly = u_curr
        else:
            poly = 2.0 * x * u_curr - u_prev
            u_prev, u_curr = u_curr, poly
        modes[:, k] = np.sqrt(lam) * poly
    return modes


def head(gamma, modes, n_keep):
    """A_N (n_keep x 2) plus its SHA-256 (spec 2.1)."""

    a_n = modes[:, :n_keep].T @ gamma
    digest = hashlib.sha256(np.ascontiguousarray(a_n).tobytes()).hexdigest()[:16]
    return a_n, digest
