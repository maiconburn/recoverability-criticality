"""P15.1/P15.3: synthetic EP-3 cluster hierarchy (frozen in FROZEN_P15_EPN.md)."""
import json
import pathlib

import numpy as np

ts = np.linspace(0.2, 60.0, 600)
NOISE = 0.01
L0 = 1.0 - 0.15j          # cluster center
AMPS = np.array([0.6, -0.4, 0.35]) * np.exp(1j*np.array([0.3, 1.7, -1.1]))

def lambdas(g):
    # EP-3 Puiseux pattern: three cube-root directions
    w = np.exp(2j*np.pi*np.arange(3)/3)
    return L0 + g*w*np.exp(1j*0.4)

def crbs(g):
    lam = lambdas(g)
    E = [np.exp(-1j*l*ts) for l in lam]
    dE = [AMPS[k]*(-1j*ts)*E[k] for k in range(3)]
    sr = lambda v: np.concatenate([v.real, v.imag])
    amp_cols = []
    for k in range(3):
        amp_cols += [sr(E[k]), sr(1j*E[k])]
    # frequency parameters: cluster center (2 real) + 2 relative splittings (4 real)
    d_center = sum(dE)
    d_g1 = dE[0]*np.exp(2j*np.pi*0/3) - dE[1]  # generic independent directions
    d_g2 = dE[1] - dE[2]
    freq_cols = [sr(d_center), sr(1j*d_center), sr(d_g1), sr(1j*d_g1),
                 sr(d_g2), sr(1j*d_g2)]
    def crb(cols, idx=0):
        X = np.vstack(cols).T
        F = X.T @ X / NOISE**2
        return np.sqrt(np.linalg.pinv(F)[idx, idx])
    t1 = crb(amp_cols)                       # amplitudes | freqs fixed
    t2 = crb([freq_cols[2]] + freq_cols[:2] + freq_cols[3:] + amp_cols)  # a splitting, all free
    t3 = crb(amp_cols + freq_cols)           # amplitude | everything free
    return t1, t2, t3

gs = np.geomspace(0.3, 0.01, 9)
rows = []
for g in gs:
    t1, t2, t3 = crbs(g)
    rows.append([g, t1, t2, t3])
    print(f"g={g:.4f}: amp|fixed={t1:.4g}  split|free={t2:.4g}  amp|free={t3:.4g}", flush=True)
rows = np.array(rows)
lg = np.log(rows[:, 0])
exps = [np.polyfit(lg, np.log(rows[:, k]), 1)[0] for k in (1, 2, 3)]
pred = [-2, -4, -5]
print(f"P15.1 exponents: amp|fixed={exps[0]:.3f} (pred -2), "
      f"split|free={exps[1]:.3f} (pred -4), amp|free={exps[2]:.3f} (pred -5)", flush=True)
ok = all(abs(e - p) <= 0.6 for e, p in zip(exps, pred))
print("P15.1:", "CONFIRMED" if ok else "KILLED", flush=True)

# P15.3: response of the splitting to a physical parameter epsilon
# (EP-3 unfolding: lambda shifts ~ eps^{1/3})
def split_of_eps(eps):
    # perturb the defective matrix: companion of (lambda-L0)^3 = eps
    roots = L0 + eps**(1/3)*np.exp(2j*np.pi*np.arange(3)/3)
    return min(abs(roots[0]-roots[1]), abs(roots[1]-roots[2]))
es = np.geomspace(1e-6, 1e-2, 7)
ss = np.array([split_of_eps(e) for e in es])
slope = np.polyfit(np.log(es), np.log(ss), 1)[0]
print(f"P15.3 response exponent: {slope:.4f} (pred 1/3)", flush=True)
print("P15.3:", "CONFIRMED" if abs(slope - 1/3) <= 0.1 else "KILLED", flush=True)
json.dump({"rows": rows.tolist(), "exps": exps, "resp": slope},
          open("results/p15_ep3.json","w"), indent=1)
print("done", flush=True)
