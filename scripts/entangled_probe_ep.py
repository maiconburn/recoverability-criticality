"""P9 question: does an entangled ancilla buy back any of the gap^-p
estimation cost near an exceptional point?

Channel: postselected PT qubit, K(t) = exp(-i H_eff t),
H_eff = [[0, J], [J, -i gamma/2]], EP at J = gamma/4.

Strategies (fixed total shot budget; noise scales with the square root of
the number of measured quantities):
  A: product probe |0>          -> column 0 of K(t)      (2 complex / t)
  B: entangled probe (Phi+)     -> both columns of K(t)  (4 complex / t)
  C: product probes |0> and |+> -> both columns, 2 settings, no ancilla
     (same information as B classically; separates "entanglement" from
     "input diversity")

Tasks (CRB, marginalized): splitting s with all amplitudes free
(exponent 2 for product) and one amplitude with frequencies free
(exponent 3 for product).
"""
import json
import pathlib

import numpy as np
from scipy.linalg import expm

gamma = 1.0
ts = np.linspace(0.2, 8.0, 120)
NOISE0 = 0.01

def kmat(J, t):
    H = np.array([[0, J], [J, -0.5j*gamma]])
    return expm(-1j*H*t)

def lambdas(J):
    d = np.sqrt(complex(J**2 - gamma**2/16))
    return -1j*gamma/4 + d, -1j*gamma/4 - d

def crb_tasks(J, columns, noise):
    """CRB for splitting (amps free) and amplitude (freqs free), using the
    requested K columns as data channels."""
    lp, lm = lambdas(J)
    Ep, Em = np.exp(-1j*lp*ts), np.exp(-1j*lm*ts)
    # each channel c has representation a_c+ Ep + a_c- Em; get exact a's by
    # projecting K elements (they are exact combos of the two exponentials)
    chans = []
    for (i, j) in columns:
        y = np.array([kmat(J, t)[i, j] for t in ts])
        M = np.vstack([Ep, Em]).T
        coef, *_ = np.linalg.lstsq(M, y, rcond=None)
        chans.append(coef)
    d_lp = (-1j*ts)*Ep
    d_lm = (-1j*ts)*Em
    cols_amp, cols_freq_s, cols_freq_mu = [], None, None
    freq_s = np.zeros(2*len(ts))
    freq_mu = np.zeros(2*len(ts))
    blocks = []
    for coef in chans:
        ap, am = coef
        # per-channel basis functions
        base = {
            "s": 0.5*(ap*d_lp - am*d_lm),
            "mu": ap*d_lp + am*d_lm,
            "xp": Ep, "yp": 1j*Ep, "xm": Em, "ym": 1j*Em,
        }
        blocks.append(base)
    def stackreal(v):
        return np.concatenate([v.real, v.imag])
    n_ch = len(blocks)
    zero = np.zeros(2*len(ts))
    def col(vecs):  # vecs: list per channel (or None -> zeros)
        return np.concatenate([stackreal(v) if v is not None else zero
                               for v in vecs])
    # global params: s, mu (shared); per-channel amplitudes (4 real each)
    cols = []
    cols.append(col([b["s"] for b in blocks]))
    cols.append(col([1j*b["s"] for b in blocks]))
    cols.append(col([b["mu"] for b in blocks]))
    cols.append(col([1j*b["mu"] for b in blocks]))
    amp_index = len(cols)  # first amplitude param of channel 0
    for k, b in enumerate(blocks):
        for key in ("xp", "yp", "xm", "ym"):
            vecs = [None]*n_ch
            vecs[k] = b[key]
            cols.append(col(vecs))
    X = np.vstack(cols).T
    F = X.T @ X / noise**2
    Finv = np.linalg.pinv(F)
    crb_s = np.sqrt(Finv[0, 0])
    crb_amp = np.sqrt(Finv[amp_index, amp_index])
    return crb_s, crb_amp

STRATS = {
    "A_product_col0":  ([(0, 0), (1, 0)], 1.0),
    "B_entangled":     ([(0, 0), (1, 0), (0, 1), (1, 1)], np.sqrt(2.0)),
    "C_two_settings":  ([(0, 0), (1, 0), (0, 1), (1, 1)], np.sqrt(2.0)),
}
# B and C access the same K elements under this noise model; they are
# computed identically here, and that IS the finding if it holds: the
# ancilla gives single-setting convenience, not a new scaling resource.

rows = {}
Js = [0.50, 0.40, 0.325, 0.29, 0.27, 0.26, 0.255, 0.2525]
for name, (columns, nscale) in STRATS.items():
    out = []
    for J in Js:
        lp, lm = lambdas(J)
        gap = abs(lp - lm)
        s_, a_ = crb_tasks(J, columns, NOISE0*nscale)
        out.append([float(gap), float(s_), float(a_)])
        print(f"{name} J={J:.4f} gap={gap:.4f} crb_s={s_:.4g} crb_amp={a_:.4g}", flush=True)
    rows[name] = out
    g = np.log([r[0] for r in out]); 
    for k, lab in ((1, "splitting"), (2, "amplitude")):
        v = np.log([r[k] for r in out])
        print(f"  {name} {lab} exponent: {np.polyfit(g, v, 1)[0]:+.2f}", flush=True)

pathlib.Path("results/entangled_probe_ep.json").write_text(json.dumps(rows, indent=1))
print("done", flush=True)
