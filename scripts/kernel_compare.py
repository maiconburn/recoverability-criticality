"""Informational address of the deep mirror family vs the fundamental one.

Motivation: at the deep EP (lambda=0.120) the reconstruction-induced rho
shift is ~1e-11 at N=5, while the fundamental EP shows ~1e-2 — nine orders
less sensitivity to horizon-Taylor data.  Hypothesis H_addr: the deep
family's response kernel K(z) = delta_rho / eps for localized metric bumps
is boundary-weighted, unlike the horizon-dominated fundamental kernel
(P4 phase 2: centroid 0.74-0.90).

Method: Bernstein bumps B_{k,8}(z) = C(8,k) z^k (1-z)^{8-k}, k=1..7 (vanish
at both ends), amplitude eps = 1e-6; measure rho at the anchored EP of each
family; K(z_k) = |delta rho| / eps at the bump's peak z_k = k/8.
"""
import json
import pathlib
from math import comb

import numpy as np

from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients
from recoverability_ep.shooting import ShootingSolver, pair_invariants

import sys
EPS = float(sys.argv[1]) if len(sys.argv) > 1 else 1e-6
CASES = [
    ("deep", 0.120, -32.285, np.array([2.3e-07 - 9.7300637j, 3.5e-07 - 9.7300695j])),
    ("fundamental", 0.105, -34.3856, np.array([0.02 - 7.1641j, -0.02 - 7.1641j])),
]

def bump(k, n=8):
    c = comb(n, k)
    f = lambda z: c * z**k * (1 - z)**(n - k)
    fp = lambda z: c * (k * z**(k-1) * (1 - z)**(n - k)
                        - (n - k) * z**k * (1 - z)**(n - k - 1))
    # horizon Taylor in u = 1-z: c*(1-u)^k u^(n-k)
    coeffs = np.zeros(25)
    binom = [comb(k, j) * (-1)**j for j in range(k + 1)]
    for j, bj in enumerate(binom):
        m = (n - k) + j
        if 1 <= m <= 24:
            coeffs[m] += c * bj
    return f, fp, coeffs

out = {}
for label, lam, q2, seed in CASES:
    b0, bp0, nf = exact_gb_metric(lam)
    hc0 = np.array(exact_horizon_coefficients(lam, 24))
    s0 = ShootingSolver(b0, bp0, nf, q2, horizon_coefficients=tuple(hc0))
    pair0 = s0.pair(seed)
    _, rho0 = pair_invariants(pair0)
    rows = []
    for k in range(1, 8):
        f, fp, cf = bump(k)
        b = lambda z, f=f: b0(z) + EPS * f(np.asarray(z))
        bp = lambda z, fp=fp: bp0(z) + EPS * fp(np.asarray(z))
        hc = tuple(hc0 + EPS * cf[1:25])
        s = ShootingSolver(b, bp, nf, q2, horizon_coefficients=hc)
        try:
            pair = s.pair(pair0)
            if abs(pair[0] + np.conj(pair[1])) > 1e-3:
                raise RuntimeError("mirror gate")
            if abs(np.mean(pair) - np.mean(pair0)) > 0.05:
                raise RuntimeError("identity jump")
            _, rho = pair_invariants(pair)
            K = abs(complex(rho) - complex(rho0)) / EPS
        except Exception as exc:
            K = None
        rows.append([k / 8, K])
        print(f"{label} z={k/8:.3f}: K={K:.4e}" if K is not None else f"{label} z={k/8}: FAIL", flush=True)
    good = [(z, K) for z, K in rows if K]
    if good:
        zs = np.array([g[0] for g in good]); Ks = np.array([g[1] for g in good])
        cen = float(np.sum(zs * Ks) / np.sum(Ks))
        print(f"{label}: centroid z* = {cen:.3f}  (z=1 horizon, z=0 boundary)", flush=True)
        out[label] = {"rows": rows, "centroid": cen}

pathlib.Path(f"results/kernel_compare_{EPS:.0e}.json").write_text(json.dumps(out, indent=1))
print("done", flush=True)
