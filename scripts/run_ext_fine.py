"""(B) Fine bisection of lambda_ext; test 7/64 = 0.109375."""
import numpy as np
from recoverability_ep.criticality import SpectralFamily, match_pair, mirror_seed, track_pair
from recoverability_ep.model import exact_gb_metric

def has_collision(lam, floor=-60.0):
    b, bp, n = exact_gb_metric(lam)
    fam = SpectralFamily(b, bp, n, collocation_order=56)
    pair = track_pair(fam, [0.0, -3.0], seed=mirror_seed(fam))
    q2, last = -3.0, None
    while q2 > floor:
        pair = match_pair(fam.spectrum(q2), pair)
        rho = (((pair[0]-pair[1])/2)**2).real
        if last is not None and last > 0 >= rho:
            return True, q2
        last = rho; q2 -= 0.2
    return False, q2

lo, hi = 0.10875, 0.11000
for _ in range(6):
    mid = 0.5*(lo+hi)
    ok, q2c = has_collision(mid)
    print(f"lambda={mid:.6f}: colisao={ok}" + (f" q2~{q2c:.1f}" if ok else ""), flush=True)
    if ok: lo = mid
    else: hi = mid
print(f"FINO: lambda_ext in [{lo:.6f}, {hi:.6f}]")
print(f"7/64 = {7/64:.6f} -> {'DENTRO' if lo <= 7/64 <= hi else 'FORA'} do intervalo")
