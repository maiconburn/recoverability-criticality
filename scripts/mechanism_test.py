"""Mechanism test for the EP-pair annihilation threshold.

Hypothesis H_hor: annihilation happens when the horizon-coefficient ratio
r(lambda) = b''(1)/b'(1) crosses 2.  For the exact EGB brane r = 3 - 8*lambda,
so r = 2 at lambda = 1/8 -- consistent with the measured threshold.

Falsifiable prediction: deform the metric with

    b_eps(z) = b(z) + eps * (1 - z^4)^2

which keeps the horizon position and temperature (c(1) = c'(1) = 0) but shifts
b''(1) by 64*eps.  Then r = 2 moves to

    lambda*(eps) = 1/8 - 2*eps / n^2(lambda)   (approx. 1/8 - 2.343*eps near 1/8)

while the null hypothesis (threshold pinned at the undeformed value) predicts
no shift.  This script scans one (eps, lambda) point: walks the mirror pair
down in q^2 and reports whether a rho sign-crossing (real EP dip) exists.

Deformation kinds (to separate horizon from boundary effects):
  orig: c = (1-z^4)^2   -- shifts a2 AND b(0) (confounded; round 1)
  hor:  c = (1-z)^2 z^6 -- shifts a2 only, b(0) untouched
  bnd:  c = (1-z^4)^3   -- shifts b(0) and a3, a2 untouched (c''(1)=0)

Usage: mechanism_test.py KIND EPS LAMBDA [Q2_FLOOR]
"""
import json
import pathlib
import sys

import numpy as np

from recoverability_ep.criticality import SpectralFamily, match_pair, mirror_seed, track_pair
from recoverability_ep.model import exact_gb_metric

KIND = sys.argv[1]
EPS = float(sys.argv[2])
LAM = float(sys.argv[3])
FLOOR = float(sys.argv[4]) if len(sys.argv) > 4 else -40.0
DQ = 0.02
GATE = 1e-4

b0, bp0, n_factor = exact_gb_metric(LAM)

DEFORMATIONS = {
    "orig": (
        lambda z: (1.0 - z**4) ** 2,
        lambda z: -8.0 * z**3 * (1.0 - z**4),
    ),
    "hor": (
        lambda z: (1.0 - z) ** 2 * z**6,
        lambda z: z**5 * (1.0 - z) * (6.0 - 8.0 * z),
    ),
    "bnd": (
        lambda z: (1.0 - z**4) ** 3,
        lambda z: -12.0 * z**3 * (1.0 - z**4) ** 2,
    ),
}
c_fn, cp_fn = DEFORMATIONS[KIND]

def b(z):
    return b0(z) + EPS * c_fn(np.asarray(z))

def bp(z):
    return bp0(z) + EPS * cp_fn(np.asarray(z))

fam = SpectralFamily(b, bp, n_factor, collocation_order=88)
pair = track_pair(fam, [0.0, -3.0], seed=mirror_seed(fam), max_step=0.04)

rho_min, q2_min, crossings, last_rho = np.inf, None, 0, None
valid = total = 0
q2 = -3.0
while q2 > FLOOR:
    pair = match_pair(fam.spectrum(q2), pair)
    ok = abs(pair[0] + np.conj(pair[1])) < GATE
    total += 1
    if ok:
        valid += 1
        rho = (((pair[0] - pair[1]) / 2.0) ** 2).real
        if last_rho is not None and last_rho * rho < 0:
            crossings += 1
        if rho < rho_min:
            rho_min, q2_min = rho, q2
        last_rho = rho
    else:
        last_rho = None
    q2 -= DQ

row = {
    "kind": KIND, "eps": EPS,
    "lam": LAM,
    "rho_min": rho_min if np.isfinite(rho_min) else None,
    "q2_min": q2_min,
    "crossings": crossings,
    "valid": valid / max(total, 1),
    "has_dip": bool(crossings > 0 or (rho_min is not None and np.isfinite(rho_min) and rho_min < 1e-6)),
}
print(json.dumps(row), flush=True)

out = pathlib.Path("results/mechanism_test.json")
data = json.loads(out.read_text()) if out.exists() else []
data.append(row)
out.write_text(json.dumps(data, indent=1))
