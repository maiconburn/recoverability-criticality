import numpy as np
from recoverability_ep.criticality import SpectralFamily, match_pair, mirror_seed, track_pair
from recoverability_ep.model import exact_gb_metric
def probe(lam):
    b, bp, n = exact_gb_metric(lam)
    fam = SpectralFamily(b, bp, n, collocation_order=72)
    pair = track_pair(fam, [0.0, -3.0], seed=mirror_seed(fam))
    q2, last = -3.0, None
    while q2 > -60:
        pair = match_pair(fam.spectrum(q2), pair)
        rho = (((pair[0]-pair[1])/2)**2).real
        if last is not None and last > 0 >= rho:
            return True, q2
        last = rho; q2 -= 0.15
    return False, q2
for lam in (0.1090, 0.10925, 0.10935, 0.1095):
    ok, q2c = probe(lam)
    print(f"order72 lambda={lam:.5f}: colisao={ok}" + (f" q2~{q2c:.1f}" if ok else ""), flush=True)
