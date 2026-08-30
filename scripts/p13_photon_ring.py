"""P13: photon-ring subring tower as spatial echoes; CRB hierarchy for the
Lyapunov exponent. Frozen in results/FROZEN_P12_P13.md."""
import json
import pathlib

import numpy as np

D_INF = 40.0e-6 / 206265.0   # 40 uas in radians... keep units abstract:
# work in scaled units: u in Glambda, d in uas with 2*pi*d*u dimensionless
# using d[uas]*u[Glambda]*(pi/180/3600/1e6*1e9) — absorb constants: use
# x_n = d_n (uas), u in units where phase = 2*pi*d_n*u*KAPPA, KAPPA fixed.
KAPPA = 4.8481e-3   # rad per (uas*Glambda): 1 uas = 4.8481e-12 rad; u Glambda = 1e9 lambda
# phase = 2*pi * d[rad] * u[lambda] = 2*pi * d_uas*4.8481e-12 * u_G*1e9
#       = 2*pi * d_uas * u_G * 4.8481e-3  -> KAPPA correct.

A0, C, DINF = 1.0, 0.3, 40.0
NRING = 4
US = np.linspace(2.0, 40.0, 200)
NOISE = 0.01   # SNR=100 per point

def d_n(gamma, n):
    return DINF*(1 + C*np.exp(-gamma*n))

def signal(gamma):
    w = np.exp(-gamma)
    out = np.zeros_like(US)
    for n in range(1, NRING+1):
        out += A0 * w**n * np.cos(2*np.pi*KAPPA*d_n(gamma, n)*US)
    return out

def crbs(gamma, dg=1e-6):
    # basis of derivatives for tasks
    w = np.exp(-gamma)
    comps, dcomps = [], []
    for n in range(1, NRING+1):
        ph = 2*np.pi*KAPPA*d_n(gamma, n)*US
        comps.append(np.cos(ph))
        # d/dgamma of component n (freq part only; amplitude free separately)
        dphi = 2*np.pi*KAPPA*DINF*C*(-n)*np.exp(-gamma*n)*US
        dcomps.append(A0*w**n*(-np.sin(ph))*dphi)
    d_gamma_freq = np.sum(dcomps, axis=0)
    amps = comps
    def crb(cols, idx=0):
        X = np.vstack(cols).T
        F = X.T @ X / NOISE**2
        return np.sqrt(np.linalg.pinv(F)[idx, idx])
    t_gamma_ampsfree = crb([d_gamma_freq] + amps)      # gamma with amps free
    t_amp_gammafree = crb(amps + [d_gamma_freq])       # a_1 with gamma free
    t_amp_fixed = crb(amps)                            # a_1 with gamma known
    # effective gap: spacing between adjacent tower phases at band center
    ub = US.mean()
    gaps = [2*np.pi*KAPPA*abs(d_n(gamma, n) - d_n(gamma, n+1))*ub
            for n in range(1, NRING)]
    gap = min(gaps)
    return gap, t_amp_fixed, t_gamma_ampsfree, t_amp_gammafree

rows = []
for gamma in (0.3, 0.45, 0.6, 0.75, 0.9, 1.05, 1.2):
    g, t1, t2, t3 = crbs(gamma)
    rows.append([gamma, g, t1, t2, t3])
    print(f"gamma={gamma:.2f} gap={g:.4f}  amp|fixed={t1:.4g}  gamma|ampsfree={t2:.4g}  amp|gammafree={t3:.4g}", flush=True)
rows = np.array(rows)
lg = np.log(rows[:, 1])
exps = [np.polyfit(lg, np.log(rows[:, k]), 1)[0] for k in (2, 3, 4)]
print(f"P13.1 exponents vs gap: amp|fixed={exps[0]:.3f} gamma|free={exps[1]:.3f} amp|free={exps[2]:.3f}", flush=True)
i = int(np.argmin(np.abs(rows[:, 0]-1.0)))
rel = rows[i, 3]/1.0
print(f"P13.2: sigma(gamma)/gamma at gamma=1.0: {rel*100:.2f}%  -> {'CONFIRMED' if rel < 0.10 else ('KILLED' if rel > 0.30 else 'inconclusive band')}", flush=True)
json.dump({"rows": rows.tolist(), "exponents": exps},
          open("results/p13_photon_ring.json","w"), indent=1)
print("done", flush=True)
