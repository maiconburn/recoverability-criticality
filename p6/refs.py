"""Exceptional-point location and reference eigenvalues (spec 1.4).

The EP solves F(z) = (z - delta - Sigma_II(z)) z - g^2 = 0 with F'(z) = 0 on
the second sheet.  Frozen method: 2D Newton on the analytic collision
function s(g, delta) = (z1 - z2)^2, root pair tracked by a local quadratic
model of F, homotopy in W from the Markovian seed.
"""

from __future__ import annotations

import numpy as np

from bath import BathConfig, det_f


def quadratic_pair(function, center, stencil=1e-4, iterations=12, tol=1e-13):
    """Both roots of an analytic function near a centroid (quadratic model)."""

    center = complex(center)
    root_high = root_low = center
    for _ in range(iterations):
        f0 = function(center)
        fp = function(center + stencil)
        fm = function(center - stencil)
        slope = (fp - fm) / (2.0 * stencil)
        curvature = (fp + fm - 2.0 * f0) / stencil**2
        if curvature == 0:
            break
        disc = np.sqrt(slope**2 - 2.0 * curvature * f0)
        root_high = center + (-slope + disc) / curvature
        root_low = center + (-slope - disc) / curvature
        new_center = 0.5 * (root_high + root_low)
        moved = abs(new_center - center)
        center = new_center
        if moved < tol:
            break
    return np.array([root_high, root_low])


def newton_root(function, seed, tol=1e-13, iterations=60, step_h=1e-7):
    z = complex(seed)
    for _ in range(iterations):
        f = function(z)
        d = (function(z + step_h) - function(z - step_h)) / (2.0 * step_h)
        if d == 0:
            break
        dz = -f / d
        z += dz
        if abs(dz) < tol:
            break
    return z


def collision(g, delta, config, centroid):
    """s = (z1 - z2)^2 for the tracked resonance pair; returns (s, pair)."""

    pair = quadratic_pair(lambda z: det_f(z, g, delta, config, sheet=2), centroid)
    return (pair[0] - pair[1]) ** 2, pair


def ep_newton(g0, delta0, config, centroid, rounds=40, tol=1e-12):
    """2D Newton on Re s, Im s over (g, delta)."""

    g, delta = float(g0), float(delta0)
    center = complex(centroid)
    for _ in range(rounds):
        s0, pair = collision(g, delta, config, center)
        center = complex(np.mean(pair))
        hg = max(1e-8, 1e-7 * abs(g))
        hd = 1e-8
        sg, _ = collision(g + hg, delta, config, center)
        sd, _ = collision(g, delta + hd, config, center)
        jac = np.array(
            [
                [(sg - s0).real / hg, (sd - s0).real / hd],
                [(sg - s0).imag / hg, (sd - s0).imag / hd],
            ]
        )
        try:
            step = np.linalg.solve(jac, -np.array([s0.real, s0.imag]))
        except np.linalg.LinAlgError:
            break
        step_norm = np.linalg.norm(step)
        if step_norm > 0.05:
            step *= 0.05 / step_norm
        g += step[0]
        delta += step[1]
        if step_norm < tol:
            break
    s_final, pair = collision(g, delta, config, center)
    return g, delta, complex(np.mean(pair)), float(abs(pair[0] - pair[1]))


def find_ep(config: BathConfig, w_start=60.0, steps=20):
    """Homotopy in W from the Markovian seed down to the target band."""

    gamma, q, w_target = config.gamma, config.q, config.w_band
    g, delta = gamma / 4.0, -gamma * q / 4.0
    centroid = -0.5j * gamma / 2.0  # Markovian lambda_EP = -i gamma_eff/2? seed guess
    w_ladder = np.geomspace(w_start, w_target, steps)
    result = None
    for w in w_ladder:
        cfg = BathConfig(gamma=gamma, w_band=float(w), q=q)
        g, delta, centroid, gap = ep_newton(g, delta, cfg, centroid)
        result = (g, delta, centroid, gap)
    return result


def lambda_reference(distance, g_ep, delta_ep, lambda_ep, config):
    """Reference eigenvalue pair at d = (g - g_ep)/g_ep along the g axis.

    Quadratic-model seed, then one Newton polish per member (the quadratic
    model alone carries an O(split^2) bias for a well-separated pair).
    """

    g = g_ep * (1.0 + distance)

    def f(z):
        return det_f(z, g, delta_ep, config, sheet=2)

    pair = quadratic_pair(f, lambda_ep)
    if abs(pair[0] - pair[1]) > 1e-7:
        pair = np.array([newton_root(f, pair[0]), newton_root(f, pair[1])])
    return pair
