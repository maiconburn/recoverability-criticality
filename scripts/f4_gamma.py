"""F4: amplification exponent gamma of the critical channel AT the
annihilation point (frozen prediction: gamma_meta = 1.0 vs 0.5 at EP-2)."""
import sys, json
import numpy as np
from recoverability_ep.criticality import SpectralFamily, match_pair, mirror_seed, track_pair
from recoverability_ep.model import build_constrained_pade, exact_gb_metric, exact_horizon_coefficients
from recoverability_ep.shooting import ShootingSolver, pair_invariants, pade_horizon_coefficients

LAM = float(sys.argv[1]); Q2M = float(sys.argv[2])
DS = [0.5, 0.3, 0.15, 0.08, 0.04]
NS = [4, 6, 8, 10, 12]

def gated_pair(b, bp, n, hc, q2, seed):
    s = ShootingSolver(b, bp, n, float(q2), horizon_coefficients=hc)
    ps = s.pair(seed)
    if abs(ps[0] + np.conj(ps[1])) > 1e-4:
        raise RuntimeError("symmetry gate")
    return ps

b, bp, n = exact_gb_metric(LAM)
hc = exact_horizon_coefficients(LAM, 24)
fam = SpectralFamily(b, bp, n, collocation_order=88)

# exact pairs along the d-ladder (collocation identity + gate)
pair_c = track_pair(fam, [0.0, Q2M + max(DS)], seed=mirror_seed(fam), max_step=0.04)
exact = {}
for d in sorted(DS, reverse=True):
    q2 = Q2M + d
    pair_c = match_pair(fam.spectrum(q2), pair_c)
    exact[d] = gated_pair(b, bp, n, hc, q2, pair_c)
    print(f"exact d={d}: pair={exact[d]}", flush=True)

rows = []
for N in NS:
    p = build_constrained_pade(exact_horizon_coefficients(LAM, N))
    if not p.is_admissible():
        continue
    hcN = pade_horizon_coefficients(p, 24)
    for d in DS:
        try:
            psN = gated_pair(p.b, p.bp, n, hcN, Q2M + d, exact[d])
            sqE = (exact[d][0]-exact[d][1])/2.0
            sqN = (psN[0]-psN[1])/2.0
            if abs(sqN - sqE) > abs(-sqN - sqE): sqN = -sqN
            rows.append(dict(N=N, d=d, eps_crit=float(abs(sqN - sqE))))
            print(f"N={N} d={d}: eps_crit={rows[-1]['eps_crit']:.4e}", flush=True)
        except Exception as e:
            print(f"N={N} d={d}: FAIL {e}", flush=True)
json.dump(rows, open('results/f4_gamma.json','w'), indent=1)
# per-N gamma fits
import collections
byN = collections.defaultdict(list)
for r in rows: byN[r['N']].append((r['d'], r['eps_crit']))
gs=[]
for N, pts in sorted(byN.items()):
    if len(pts) >= 4:
        x=np.log([p[0] for p in pts]); y=np.log([p[1] for p in pts])
        sl,_=np.polyfit(x,y,1); gs.append(-sl)
        print(f"gamma(N={N}) = {-sl:.2f}", flush=True)
if gs: print(f"GAMMA_META = {np.mean(gs):.2f} +/- {np.std(gs):.2f}  (congelado: 1.0; EP-2 comum: 0.5)", flush=True)
print("done", flush=True)
