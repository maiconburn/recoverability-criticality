"""P6 dry run: Petz rate vs spectral rate across the EP ladder and knob configs.

Phase 0 freezes, per configuration: the EP (by continuation from the S-A
anchor), the Puiseux exponent, and the a-priori standard-theory rates
  alpha_spec = [alpha_chain - 2 ln rho_B(res)] / 2   (Green-corrected Szego)
  alpha_Petz = 2 ln rho_B(res)                        (Bernstein pole depth)
Production then measures both rates from the same head A_N on the distance
ladder plus d = 0, and evaluates K1 (rate locking) and K2 (Petz halving).
"""

import json
import time
from pathlib import Path

import numpy as np

from bath import BathConfig, nodes_weights
from fitspec import eigenpair, eigenpair_degenerate, extend_theta, fit_chain
from model import analytic_amplitudes, chebyshev_modes, emitted_amplitudes, head
from petz import average_fidelity
from refs import ep_newton, lambda_reference

M_MODES = 1200
N_GRID = list(range(4, 41, 2))
D_LADDER = [0.3, 0.1, 0.03, 0.01, 0.003]
WINDOW = (8, 36)
OUT = Path(__file__).resolve().parent / "results_p6.json"

ANCHOR = dict(q=0.9, w=2.0, g=0.286476417, delta=-0.312671129,
              lam=0.064561315 - 0.315207308j)


def bernstein_rho(z, w_band):
    u = np.asarray(z, dtype=complex) / w_band
    candidates = [abs(u + np.sqrt(u**2 - 1)), abs(u - np.sqrt(u**2 - 1))]
    return max(candidates)


def find_config_ep(q_target, w_target, steps=25):
    """Continuation in (q, W) from the verified anchor EP."""

    q_path = np.linspace(ANCHOR["q"], q_target, steps)
    w_path = np.linspace(ANCHOR["w"], w_target, steps)
    g, delta, lam = ANCHOR["g"], ANCHOR["delta"], ANCHOR["lam"]
    for q, w in zip(q_path, w_path):
        cfg = BathConfig(1.0, float(w), float(q))
        g, delta, lam, gap = ep_newton(g, delta, cfg, lam)
    return g, delta, lam, gap


def rate_fit(n_values, errors, window=WINDOW, floor=1e-12):
    n_values = np.asarray(n_values, dtype=float)
    errors = np.asarray(errors, dtype=float)
    mask = (n_values >= window[0]) & (n_values <= window[1]) & (errors > floor)
    if mask.sum() < 5:
        return np.nan, np.nan, np.nan
    slope, intercept = np.polyfit(n_values[mask], np.log(errors[mask]), 1)
    pred = slope * n_values[mask] + intercept
    resid = np.log(errors[mask]) - pred
    r2 = 1.0 - resid.var() / np.log(errors[mask]).var()
    dof = max(mask.sum() - 2, 1)
    se = float(np.sqrt(resid @ resid / dof / ((n_values[mask] - n_values[mask].mean()) ** 2).sum()))
    return -float(slope), se, float(r2)


def run_config(tag, q, w):
    started = time.time()
    cfg = BathConfig(1.0, w, q)
    g_ep, delta_ep, lam_ep, gap = find_config_ep(q, w)
    print(f"[{tag}] EP: g={g_ep:.9f} delta={delta_ep:.9f} lam={lam_ep:.9f} gap={gap:.1e}")

    # Puiseux gate
    splits = []
    for d in D_LADDER:
        pair = lambda_reference(d, g_ep, delta_ep, lam_ep, cfg)
        splits.append(abs(pair[0] - pair[1]))
    puiseux = np.polyfit(np.log(D_LADDER), np.log(splits), 1)[0]

    # a-priori standard rates
    alpha_chain = cfg.alpha_chain()
    rho = bernstein_rho(lam_ep, w)
    alpha_petz_pred = 2.0 * np.log(rho)
    alpha_spec_pred = 0.5 * (alpha_chain - 2.0 * np.log(rho))

    _, _, omega, delta_m, _ = nodes_weights(M_MODES, cfg)
    modes = chebyshev_modes(max(N_GRID), cfg, M_MODES)

    per_distance = {}
    for d in D_LADDER + [0.0]:
        g = g_ep * (1.0 + d)
        gamma = analytic_amplitudes(g, delta_ep, cfg, M_MODES)
        # cross-check gate against time evolution (once, at coarse tol)
        if d in (0.3, 0.0):
            gamma_t, resid_t, *_ = emitted_amplitudes(g, delta_ep, cfg, M_MODES, 150.0)
            gate_emission = float(np.max(np.abs(gamma - gamma_t)))
        else:
            gate_emission = None
        reference = (
            lambda_reference(d, g_ep, delta_ep, lam_ep, cfg)
            if d > 0
            else np.array([lam_ep, lam_ep])
        )
        gram_full = gamma.conj().T @ gamma
        a_full = np.linalg.cholesky(
            gram_full + 1e-18 * np.eye(2)
        ).conj().T
        f_complete = average_fidelity(a_full)

        theta = np.array([cfg.mu0, 0.0, 0.0, w / 2.0])
        rows = []
        for n_keep in N_GRID:
            a_n, digest = head(gamma, modes, n_keep)
            eps_petz = f_complete - average_fidelity(a_n)
            theta, head_res = fit_chain(
                a_n, g, delta_ep, cfg, modes, omega, delta_m, theta
            )
            if d > 0:
                pair, f_res = eigenpair(theta, g, delta_ep, cfg, reference)
                eps_spec = 0.5 * (
                    abs(pair[0] - reference[0]) + abs(pair[1] - reference[1])
                )
            else:
                pair, f_res = eigenpair_degenerate(theta, g, delta_ep, cfg, lam_ep)
                center = 0.5 * (pair[0] + pair[1])
                eps_spec = abs(center - lam_ep) + 0.5 * abs(pair[0] - pair[1])
            rows.append(
                dict(N=n_keep, eps_petz=float(eps_petz), eps_spec=float(eps_spec),
                     head_res=float(head_res), f_res=float(f_res), hash=digest)
            )
            theta = extend_theta(theta, cfg)
        a_petz, se_p, r2_p = rate_fit([r["N"] for r in rows], [r["eps_petz"] for r in rows])
        a_spec, se_s, r2_s = rate_fit([r["N"] for r in rows], [r["eps_spec"] for r in rows])
        per_distance[f"{d:g}"] = dict(
            rows=rows, alpha_petz=a_petz, alpha_petz_se=se_p, r2_petz=r2_p,
            alpha_spec=a_spec, alpha_spec_se=se_s, r2_spec=r2_s,
            ratio=(a_petz / a_spec) if a_spec and not np.isnan(a_spec) else np.nan,
            gate_emission=gate_emission, f_complete=float(f_complete),
        )
        print(
            f"[{tag}] d={d:<6g} a_petz={a_petz:.4f}±{se_p:.4f} "
            f"a_spec={a_spec:.4f}±{se_s:.4f} ratio={a_petz/a_spec if a_spec else float('nan'):.3f}"
        )

    return dict(
        tag=tag, q=q, w=w,
        ep=dict(g=g_ep, delta=delta_ep, lam=[lam_ep.real, lam_ep.imag], gap=gap),
        puiseux_exponent=float(puiseux),
        alpha_chain=float(alpha_chain),
        bernstein_rho=float(rho),
        alpha_petz_pred=float(alpha_petz_pred),
        alpha_spec_pred=float(alpha_spec_pred),
        ratio_pred=float(alpha_petz_pred / alpha_spec_pred),
        per_distance=per_distance,
        runtime_s=time.time() - started,
    )


def main():
    configs = [
        ("S-A(controle-acidental)", 0.9, 2.0),
        ("S-B", 0.5, 2.0),
        ("S-C", 0.5, 1.4),
    ]
    results = {"frozen_note": "standard a-priori rates from Green-corrected "
               "Szego and Bernstein laws, frozen before the grid runs",
               "configs": []}
    for tag, q, w in configs:
        results["configs"].append(run_config(tag, q, w))
        OUT.write_text(json.dumps(results, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
