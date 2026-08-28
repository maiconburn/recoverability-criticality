"""Petz recovery of the truncated emission channel (spec 3.2-3.5).

The channel keeps the first N detector modes; everything else collapses to a
flag state.  With reference sigma_ref = I/2 the average-fidelity deficit has
the exact closed form of spec 3.4 in terms of the two Gram eigenvalues.
"""

from __future__ import annotations

import numpy as np


def gram_eigenvalues(a_n):
    gram = a_n.conj().T @ a_n
    values = np.linalg.eigvalsh(gram)
    return np.clip(values.real, 0.0, 1.0)


def average_fidelity(a_n):
    s1, s2 = gram_eigenvalues(a_n)
    k1, k2 = 1.0 - s1, 1.0 - s2
    s_flag = 0.5 * (k1 + k2)
    entanglement = 0.25 * (np.sqrt(s1) + np.sqrt(s2)) ** 2
    if s_flag > 1e-15:
        entanglement += 0.125 * (k1**2 + k2**2) / s_flag
    else:
        entanglement = 0.5 * (np.sqrt(s1) + np.sqrt(s2)) ** 2 / 2.0
    return (2.0 * entanglement + 1.0) / 3.0


def kraus_check(a_n, rng=None, samples=200):
    """Monte-Carlo Haar cross-check of the closed form (spec 3.4)."""

    rng = rng or np.random.default_rng(7)
    n = a_n.shape[0]
    b = np.eye(2) - a_n.conj().T @ a_n
    k_vals, k_vecs = np.linalg.eigh(b)
    k_vals = np.clip(k_vals.real, 0.0, None)
    s_kept = a_n @ a_n.conj().T / 2.0
    vals, vecs = np.linalg.eigh(s_kept)
    keep = vals > 1e-13 * max(vals.max(), 1e-300)
    inv_sqrt = (vecs[:, keep] / np.sqrt(vals[keep])) @ vecs[:, keep].conj().T
    r0 = a_n.conj().T @ inv_sqrt / np.sqrt(2.0)
    s_flag = 0.5 * float(np.sum(k_vals))
    total = 0.0
    for _ in range(samples):
        z = rng.normal(size=2) + 1j * rng.normal(size=2)
        psi = z / np.linalg.norm(z)
        out_kept = a_n @ psi
        rho_kept = np.outer(out_kept, out_kept.conj())
        recovered = r0 @ rho_kept @ r0.conj().T
        if s_flag > 1e-15:
            weight_flag = float(np.real(psi.conj() @ b @ psi))
            rho_flag_rec = sum(
                (k_vals[i] / (2.0 * s_flag))
                * np.outer(k_vecs[:, i], k_vecs[:, i].conj())
                for i in range(2)
            )
            recovered = recovered + weight_flag * rho_flag_rec
        total += float(np.real(psi.conj() @ recovered @ psi))
    return total / samples
