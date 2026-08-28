"""Structured bath: spectral density, discretization, closed-form self-energy.

Spec: p6/SPEC.md sections 1.2-1.3.  J(w) = (Gamma/2pi) sqrt(1-(w/W)^2)(1-q w/W)
on [-W, W]; Gauss-Chebyshev-U nodes; Sigma on both sheets with the branch rule
sqrt(z-W)*sqrt(z+W) (never sqrt(z^2-W^2)).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BathConfig:
    gamma: float = 1.0
    w_band: float = 2.0
    q: float = 0.9

    @property
    def mu0(self) -> float:
        return self.gamma * self.w_band / 4.0

    def alpha_chain(self) -> float:
        return 2.0 * np.log(1.0 / self.q + np.sqrt(1.0 / self.q**2 - 1.0))


def spectral_density(omega, config: BathConfig):
    x = np.asarray(omega) / config.w_band
    inside = np.abs(x) <= 1.0
    density = np.zeros_like(np.asarray(omega, dtype=float))
    density[inside] = (
        (config.gamma / (2.0 * np.pi))
        * np.sqrt(1.0 - x[inside] ** 2)
        * (1.0 - config.q * x[inside])
    )
    return density


def nodes_weights(m_modes: int, config: BathConfig):
    """Gauss-Chebyshev-U nodes, quadrature weights, couplings (spec 1.3)."""

    m = np.arange(1, m_modes + 1)
    x = np.cos(m * np.pi / (m_modes + 1))
    lam = (2.0 / (m_modes + 1)) * np.sin(m * np.pi / (m_modes + 1)) ** 2
    omega = config.w_band * x
    w_ref = (2.0 / (np.pi * config.w_band**2)) * np.sqrt(
        config.w_band**2 - omega**2
    )
    delta_m = lam / w_ref
    couplings = np.sqrt(spectral_density(omega, config) * delta_m)
    return x, lam, omega, delta_m, couplings


def band_root(z, w_band):
    """sqrt(z-W)*sqrt(z+W) with principal branches of EACH factor (spec 7.4-3)."""

    return np.sqrt(z - w_band) * np.sqrt(z + w_band)


def sigma_closed(z, config: BathConfig, sheet: int = 1):
    """Closed-form self-energy on sheet 1 (physical) or 2 (spec 1.2)."""

    u = np.asarray(z, dtype=complex) / config.w_band
    r = band_root(u, 1.0)
    signed = -r if sheet == 1 else +r
    return (config.gamma / 2.0) * ((u + signed) * (1.0 - config.q * u) + config.q / 2.0)


def det_f(z, g, delta, config: BathConfig, sheet: int = 2):
    """F(z) = (z - delta - Sigma_sheet(z)) z - g^2 (spec 1.4)."""

    return (z - delta - sigma_closed(z, config, sheet)) * z - g**2
