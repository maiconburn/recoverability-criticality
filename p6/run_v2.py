"""P6 v2 hardening: learned-channel leg, second detector family, noise
replicate, and discretization audit (spec 3.6, 2.5, 2.4, K3-e).

Run on the sharpest-separation configuration S-B (q=0.5, W=2) plus the EP
leg; each block reports pass/fail against the frozen gates.
"""

import json
import time
from pathlib import Path

import numpy as np

from bath import BathConfig, nodes_weights
from fitspec import extend_theta, fit_chain, forward_head
from model import analytic_amplitudes, chebyshev_modes, head
from petz import average_fidelity
from run_p6 import find_config_ep, rate_fit, N_GRID, WINDOW

HERE = Path(__file__).resolve().parent
OUT = HERE / "results_v2.json"


def legendre_modes(n_modes, config, m_modes):
    _, lam, omega, delta_m, _ = nodes_weights(m_modes, config)
    x = omega / config.w_band
    flat_weight = 1.0 / (2.0 * config.w_band)
    columns = []
    p_prev = np.ones_like(x)
    p_curr = x.copy()
    for k in range(n_modes):
        if k == 0:
            poly = p_prev
        elif k == 1:
            poly = p_curr
        else:
            poly = ((2 * k - 1) * x * p_curr - (k - 1) * p_prev) / k
            p_prev, p_curr = p_curr, poly
        norm = np.sqrt((2 * k + 1) / 2.0)
        columns.append(np.sqrt(delta_m * flat_weight) * poly * norm * np.sqrt(2.0 * config.w_band))
    modes = np.column_stack(columns)
    q_matrix, _ = np.linalg.qr(modes)
    return q_matrix


def mixed_fidelity(a_true, a_model):
    """F-bar of (learned recovery) o (true channel), spec 3.6."""

    s_kept_model = a_model @ a_model.conj().T / 2.0
    vals, vecs = np.linalg.eigh(s_kept_model)
    keep = vals > 1e-13 * max(vals.max(), 1e-300)
    inv_sqrt = (vecs[:, keep] / np.sqrt(vals[keep])) @ vecs[:, keep].conj().T
    r0 = a_model.conj().T @ inv_sqrt / np.sqrt(2.0)

    b_true = np.eye(2) - a_true.conj().T @ a_true
    kt, vt = np.linalg.eigh(b_true)
    kt = np.clip(kt.real, 0.0, None)
    b_model = np.eye(2) - a_model.conj().T @ a_model
    km, vm = np.linalg.eigh(b_model)
    km = np.clip(km.real, 0.0, None)
    s_flag_model = 0.5 * float(km.sum())

    f_e = 0.25 * abs(np.trace(r0 @ a_true)) ** 2
    if s_flag_model > 1e-15:
        for i in range(2):
            for j in range(2):
                overlap = vt[:, j].conj() @ vm[:, i]
                f_e += 0.125 * (km[i] * kt[j] / s_flag_model) * abs(overlap) ** 2
    return (2.0 * f_e + 1.0) / 3.0


def petz_curve(gamma, modes, f_complete, mixed_with=None, noise=None, rng=None):
    rows = []
    for n_keep in N_GRID:
        a_n, _ = head(gamma, modes, n_keep)
        if noise is not None:
            a_n = a_n + noise[:n_keep, :]
        if mixed_with is None:
            eps = f_complete - average_fidelity(a_n)
        else:
            eps = f_complete - mixed_fidelity(a_n, mixed_with[n_keep])
        rows.append(eps)
    return np.array(rows)


def spec_curve(gamma, modes, g, delta_ep, cfg, omega, delta_m, reference, noise=None):
    from fitspec import eigenpair
    theta = np.array([cfg.mu0, 0.0, 0.0, cfg.w_band / 2.0])
    errors, thetas = [], {}
    for n_keep in N_GRID:
        a_n, _ = head(gamma, modes, n_keep)
        if noise is not None:
            a_n = a_n + noise[:n_keep, :]
        theta, _ = fit_chain(a_n, g, delta_ep, cfg, modes, omega, delta_m, theta)
        thetas[n_keep] = theta.copy()
        pair, _ = eigenpair(theta, g, delta_ep, cfg, reference)
        errors.append(0.5 * (abs(pair[0] - reference[0]) + abs(pair[1] - reference[1])))
        theta = extend_theta(theta, cfg)
    return np.array(errors), thetas


def main():
    started = time.time()
    q, w = 0.5, 2.0
    cfg = BathConfig(1.0, w, q)
    m_modes = 1200
    g_ep, delta_ep, lam_ep, gap = find_config_ep(q, w)
    d = 0.1
    g = g_ep * (1.0 + d)
    from refs import lambda_reference
    reference = lambda_reference(d, g_ep, delta_ep, lam_ep, cfg)
    _, _, omega, delta_m, _ = nodes_weights(m_modes, cfg)
    gamma = analytic_amplitudes(g, delta_ep, cfg, m_modes)
    modes1 = chebyshev_modes(max(N_GRID), cfg, m_modes)
    gram = gamma.conj().T @ gamma
    f_complete = average_fidelity(np.linalg.cholesky(gram + 1e-18 * np.eye(2)).conj().T)

    report = {}

    # --- baseline (family 1) ---
    eps_p1 = petz_curve(gamma, modes1, f_complete)
    eps_s1, thetas = spec_curve(gamma, modes1, g, delta_ep, cfg, omega, delta_m, reference)
    a_p1, se_p1, _ = rate_fit(N_GRID, eps_p1)
    a_s1, se_s1, _ = rate_fit(N_GRID, eps_s1)
    report["baseline"] = dict(alpha_petz=a_p1, alpha_spec=a_s1, ratio=a_p1 / a_s1)

    # --- learned-channel leg ---
    learned_heads = {}
    for n_keep in N_GRID:
        model_head = forward_head(
            thetas[n_keep], g, delta_ep, cfg, modes1[:, :n_keep], omega, delta_m
        )
        learned_heads[n_keep] = model_head
    eps_learned = petz_curve(gamma, modes1, f_complete, mixed_with=learned_heads)
    a_learned, se_l, _ = rate_fit(N_GRID, np.abs(eps_learned))
    report["learned_leg"] = dict(
        alpha_petz_learned=a_learned,
        gate_S5_within_10pct=bool(abs(a_learned - a_p1) < 0.1 * a_p1),
    )

    # --- second family (Legendre) ---
    modes2 = legendre_modes(max(N_GRID), cfg, m_modes)
    eps_p2 = petz_curve(gamma, modes2, f_complete)
    eps_s2, _ = spec_curve(gamma, modes2, g, delta_ep, cfg, omega, delta_m, reference)
    a_p2, _, _ = rate_fit(N_GRID, eps_p2)
    a_s2, _, _ = rate_fit(N_GRID, eps_s2)
    ratio_shift = abs((a_p2 / a_s2) / (a_p1 / a_s1) - 1.0)
    report["family2"] = dict(
        alpha_petz=a_p2, alpha_spec=a_s2, ratio=a_p2 / a_s2,
        gate_ratio_invariance_10pct=bool(ratio_shift < 0.10),
        ratio_shift=ratio_shift,
    )

    # --- noise replicate sigma = 1e-8 ---
    rng = np.random.default_rng(20260828)
    noise = (rng.normal(size=(max(N_GRID), 2)) + 1j * rng.normal(size=(max(N_GRID), 2))) * 1e-8
    eps_pn = petz_curve(gamma, modes1, f_complete, noise=noise)
    eps_sn, _ = spec_curve(gamma, modes1, g, delta_ep, cfg, omega, delta_m, reference, noise=noise)
    valid = [n for n, e in zip(N_GRID, eps_s1) if e > 100 * 1e-8]
    window = (WINDOW[0], max(valid)) if valid else WINDOW
    a_pn, _, _ = rate_fit(N_GRID, np.abs(eps_pn), window=window)
    a_sn, _, _ = rate_fit(N_GRID, np.abs(eps_sn), window=window)
    report["noise"] = dict(
        window=list(window), alpha_petz=a_pn, alpha_spec=a_sn,
        gate_within_5pct=bool(
            abs(a_pn - rate_fit(N_GRID, eps_p1, window=window)[0])
            < 0.05 * rate_fit(N_GRID, eps_p1, window=window)[0]
            and abs(a_sn - rate_fit(N_GRID, eps_s1, window=window)[0])
            < 0.05 * rate_fit(N_GRID, eps_s1, window=window)[0]
        ),
    )

    # --- discretization audit M -> 2M ---
    m2 = 2400
    _, _, omega2, delta_m2, _ = nodes_weights(m2, cfg)
    gamma2 = analytic_amplitudes(g, delta_ep, cfg, m2)
    modes1b = chebyshev_modes(max(N_GRID), cfg, m2)
    gram2 = gamma2.conj().T @ gamma2
    f_complete2 = average_fidelity(np.linalg.cholesky(gram2 + 1e-18 * np.eye(2)).conj().T)
    eps_p_audit = petz_curve(gamma2, modes1b, f_complete2)
    eps_s_audit, _ = spec_curve(gamma2, modes1b, g, delta_ep, cfg, omega2, delta_m2, reference)
    a_pa, _, _ = rate_fit(N_GRID, eps_p_audit)
    a_sa, _, _ = rate_fit(N_GRID, eps_s_audit)
    report["discretization"] = dict(
        alpha_petz_2M=a_pa, alpha_spec_2M=a_sa,
        gate_within_3pct=bool(
            abs(a_pa - a_p1) < 0.03 * a_p1 and abs(a_sa - a_s1) < 0.03 * a_s1
        ),
    )

    report["runtime_s"] = time.time() - started
    OUT.write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
