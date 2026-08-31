"""Numerical verification of the EP control-neutrality theorem.

Predictions frozen in results/THEOREM_EP_NEUTRALITY.md before this run:
  C1 EP-2 Green channel, marginalized sigma(theta): slope -> 0
  C2 same channel, gap parametrization: slope -> -1
  C3 free per-mode amplitudes, antisymmetric truth (A = +1/-1): slope -> -2
  C4 EP-3: control slope -> 0, gap slope -> -2

All Fisher matrices in mpmath (60 dps), derivatives by central
differences with step 1e-15 (truncation 1e-30), explicit inversion.
"""
import json
import pathlib

import mpmath as mp

mp.mp.dps = 60
T = [mp.mpf(4) * k / 199 for k in range(200)]
H = mp.mpf("1e-15")
MU = mp.mpc(0, -1)
I1 = mp.mpc(0, 1)


def green2(theta, mu_drift=mp.mpf("0.3")):
    """EP-2 Green channel: mu = MU + 0.3*theta, rho = theta."""
    mu = MU + mu_drift * theta
    s = mp.sqrt(mp.mpc(theta))
    out = []
    for t in T:
        core = t if abs(s) == 0 else mp.sin(s * t) / s
        out.append(-I1 * mp.e ** (-I1 * mu * t) * core)
    return out


def green2_musrho(mu, s):
    out = []
    for t in T:
        core = t if abs(s) == 0 else mp.sin(s * t) / s
        out.append(-I1 * mp.e ** (-I1 * mu * t) * core)
    return out


def green3(theta):
    """EP-3: omega_j = MU + eps_j * theta^(1/3), 2nd divided difference."""
    s = mp.mpc(theta) ** (mp.mpf(1) / 3)
    eps = [mp.e ** (2 * mp.pi * I1 * j / 3) for j in range(3)]
    ws = [MU + e * s for e in eps]
    out = []
    for t in T:
        acc = mp.mpc(0)
        for j in range(3):
            denom = mp.mpc(1)
            for k in range(3):
                if k != j:
                    denom *= ws[j] - ws[k]
            acc += mp.e ** (-I1 * ws[j] * t) / denom
        out.append(acc)
    return out


def green3_s(s):
    return green3(s ** 3)


def fisher_sigma(yfun, p0, comb=None):
    """sigma of parameter 0 (or of combination `comb`) from central-diff
    Jacobian at true params p0; unit noise."""
    cols = []
    for i in range(len(p0)):
        pp, pm = list(p0), list(p0)
        pp[i] = pp[i] + H
        pm[i] = pm[i] - H
        yp, ym = yfun(pp), yfun(pm)
        cols.append([(a - b) / (2 * H) for a, b in zip(yp, ym)])
    n = len(cols)
    I = mp.matrix(n, n)
    for a in range(n):
        for b in range(a, n):
            v = mp.fsum(cols[a][k] * cols[b][k] for k in range(len(T)))
            I[a, b] = v
            I[b, a] = v
    C = I ** -1
    if comb is None:
        return mp.sqrt(C[0, 0])
    v = mp.matrix(comb)
    return mp.sqrt((v.T * C * v)[0, 0])


def slopes(xs, ss):
    out = []
    for i in range(1, len(xs)):
        out.append(float((mp.log(ss[i]) - mp.log(ss[i - 1]))
                         / (mp.log(xs[i]) - mp.log(xs[i - 1]))))
    return out


results = {}

# ---- C1: control parameter, EP-2 ----
def y_c1(p):
    th, ar, ai = p
    A = mp.mpc(ar, ai)
    return [mp.re(A * g) for g in green2(th)]

thetas = [mp.mpf(10) ** (-k) for k in range(1, 9)]
sig = [fisher_sigma(y_c1, [th, mp.mpf(1), mp.mpf(0)]) for th in thetas]
sl = slopes(thetas, sig)
results["C1"] = {"sigma_last": float(sig[-1]), "slopes": sl}
print(f"C1 sigma(theta): {[f'{float(s):.4e}' for s in sig]}", flush=True)
print(f"C1 slopes: {[f'{x:.4f}' for x in sl]}", flush=True)

# ---- C2: gap parametrization, EP-2 (nuisance mu complex + A complex) ----
def y_c2(p):
    s, mr, mi, ar, ai = p
    A = mp.mpc(ar, ai)
    return [mp.re(A * g) for g in green2_musrho(mp.mpc(mr, mi), s)]

gaps = [mp.mpf(10) ** (-k / mp.mpf(2)) for k in range(1, 9)]
sig = [fisher_sigma(y_c2, [s, mp.mpf(0), mp.mpf(-1), mp.mpf(1), mp.mpf(0)])
       for s in gaps]
sl = slopes(gaps, sig)
results["C2"] = {"slopes": sl}
print(f"C2 slopes sigma(s): {[f'{x:.4f}' for x in sl]}", flush=True)

# ---- C3: free per-mode amplitudes, antisymmetric truth ----
def y_c3(p):
    w1 = mp.mpc(p[0], p[1])
    w2 = mp.mpc(p[2], p[3])
    A1 = mp.mpc(p[4], p[5])
    A2 = mp.mpc(p[6], p[7])
    return [mp.re(A1 * mp.e ** (-I1 * w1 * t) + A2 * mp.e ** (-I1 * w2 * t))
            for t in T]

sig = []
for s in gaps:
    p0 = [s, mp.mpf(-1), -s, mp.mpf(-1),
          mp.mpf(1), mp.mpf(0), mp.mpf(-1), mp.mpf(0)]
    comb = [mp.mpf("0.5"), 0, mp.mpf("-0.5"), 0, 0, 0, 0, 0]
    sig.append(fisher_sigma(y_c3, p0, comb=comb))
sl = slopes(gaps, sig)
results["C3"] = {"slopes": sl}
print(f"C3 slopes sigma(split): {[f'{x:.4f}' for x in sl]}", flush=True)

# ---- C4: EP-3 control and gap ----
def y_c4(p):
    th, ar, ai = p
    A = mp.mpc(ar, ai)
    return [mp.re(A * g) for g in green3(th)]

thetas3 = [mp.mpf(10) ** (-k) for k in range(1, 10)]
sig = [fisher_sigma(y_c4, [th, mp.mpf(1), mp.mpf(0)]) for th in thetas3]
sl = slopes(thetas3, sig)
results["C4_control"] = {"sigma_last": float(sig[-1]), "slopes": sl}
print(f"C4 control slopes: {[f'{x:.4f}' for x in sl]}", flush=True)

def y_c4s(p):
    s, ar, ai = p
    A = mp.mpc(ar, ai)
    return [mp.re(A * g) for g in green3_s(s)]

gaps3 = [mp.mpf(10) ** (-k / mp.mpf(2)) for k in range(1, 7)]
sig = [fisher_sigma(y_c4s, [s, mp.mpf(1), mp.mpf(0)]) for s in gaps3]
sl = slopes(gaps3, sig)
results["C4_gap"] = {"slopes": sl}
print(f"C4 gap slopes: {[f'{x:.4f}' for x in sl]}", flush=True)

pathlib.Path("results/p17_theorem_check.json").write_text(
    json.dumps(results, indent=1))
print("done", flush=True)
