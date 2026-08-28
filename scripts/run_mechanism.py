"""(C) Extinction mechanism: asymptotic Re(omega) of the mirror pair at deep
spacelike q^2 as order parameter vs lambda."""
import numpy as np
from recoverability_ep.criticality import SpectralFamily, match_pair, mirror_seed, track_pair
from recoverability_ep.model import exact_gb_metric

Q2_DEEP = -45.0
for lam in (0.06, 0.08, 0.09, 0.10, 0.105, 0.109, 0.111, 0.115, 0.12, 0.13):
    b, bp, n = exact_gb_metric(lam)
    fam = SpectralFamily(b, bp, n, collocation_order=56)
    pair = track_pair(fam, [0.0, -3.0], seed=mirror_seed(fam))
    q2, collided = -3.0, None
    while q2 > Q2_DEEP:
        pair = match_pair(fam.spectrum(q2), pair)
        rho = (((pair[0]-pair[1])/2)**2).real
        if collided is None and rho <= 0:
            collided = q2
        q2 -= 0.2
    re_inf = abs(pair[0].real)
    print(f"lambda={lam:.3f}: Re_omega({Q2_DEEP})={re_inf:.4f} "
          + (f"COLIDIU em q2~{collided:.1f}" if collided else "sem colisao"), flush=True)
