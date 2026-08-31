"""P16 instrument v2 for P16.1 and P16.2 (P16.3 came straight from solver
data and is unaffected).

Fixes over v1: the secular-model envelope bound no longer clips the true
parameter (b bound 50, was 10 while b_true ~ 19.6 after normalization),
and the CRB is computed from the SVD of the design matrix J instead of
inverting the double-precision Gram matrix (cond(Gram) = cond(J)^2 had
reached 1e24; the flat sigma of v1 was the pinv-masking red flag).
Trajectory is reused from results/p16_decoherence.json.
"""
import json
import pathlib

import numpy as np
from scipy.optimize import least_squares

RNG = np.random.default_rng(16)
NOISE = 1e-3

res = json.loads(pathlib.Path("results/p16_decoherence.json").read_text())
omega_ep = complex(res["omega_ep"][0], res["omega_ep"][1])
gamma_ep = -omega_ep.imag
under_key = next(k for k, v in res["sides"].items() if v == "under")
rows = res["traj"][under_key]
T = np.linspace(0.0, 4.0 / gamma_ep, 400)


def signal(pair):
    w1, w2 = pair
    if abs(w1 - w2) < 1e-9:
        return np.imag(-1j * T * np.exp(-1j * w1 * T))
    return np.imag((np.exp(-1j * w1 * T) - np.exp(-1j * w2 * T)) / (w1 - w2))


def chi2(r):
    return float(np.sum(r ** 2) / NOISE ** 2)


def fit_sec(y):
    def model(p):
        a, b, w = p[0] + 1j * p[1], p[2] + 1j * p[3], p[4] + 1j * p[5]
        return np.imag((a + b * T) * np.exp(-1j * w * T)) - y
    best = None
    for br in (-25.0, -19.6, 25.0):
        r = least_squares(model, [0, 0, br, 0, 0.0, -gamma_ep],
                          bounds=([-50, -50, -50, -50, -20, -30],
                                  [50, 50, 50, 50, 20, -1e-2]))
        if best is None or r.cost < best.cost:
            best = r
    return chi2(best.fun)


def fit_nosec(y, pair):
    w1, w2 = pair
    d = w1 - w2 if abs(w1 - w2) > 1e-6 else 1e-6

    def model(p):
        A1, A2 = p[0] + 1j * p[1], p[2] + 1j * p[3]
        u1, u2 = p[4] + 1j * p[5], p[6] + 1j * p[7]
        return (np.imag(A1 * np.exp(-1j * u1 * T)
                        + A2 * np.exp(-1j * u2 * T)) - y)
    lo = [-10, -10, -10, -10, -20, -30, -20, -30]
    hi = [10, 10, 10, 10, 20, -1e-2, 20, -1e-2]
    best = None
    scale = np.max(np.abs(signal(pair)))
    a1 = np.clip([(1 / d).real / scale, (1 / d).imag / scale], -9.9, 9.9)
    for f1, f2 in [(w1, w2), (w1 * 1.02, w2 * 0.98),
                   (-1j * gamma_ep * 0.8, -1j * gamma_ep * 1.25)]:
        x0 = [a1[0], a1[1], -a1[0], -a1[1],
              np.clip(f1.real, -19, 19), np.clip(f1.imag, -29, -2e-2),
              np.clip(f2.real, -19, 19), np.clip(f2.imag, -29, -2e-2)]
        r = least_squares(model, x0, bounds=(lo, hi))
        if best is None or r.cost < best.cost:
            best = r
    return chi2(best.fun)


# ---- P16.1 v2 ----
p161 = []
targets = [("EP", None)]
for label, ratio in [("near", 0.05), ("far", 0.5)]:
    best = min(rows, key=lambda r: abs(r["gap"] / gamma_ep - ratio))
    targets.append((label, best))
for label, row in targets:
    if row is None:
        pair = np.array([omega_ep, omega_ep])
        ratio = res["gap_min"] / gamma_ep
    else:
        pair = np.array([complex(*row["pair"][0]), complex(*row["pair"][1])])
        ratio = row["gap"] / gamma_ep
    y0 = signal(pair)
    y0 = y0 / np.max(np.abs(y0))
    y = y0 + RNG.normal(0.0, NOISE, y0.size)
    dof = y.size - 8
    c_sec, c_nosec = fit_sec(y), fit_nosec(y, pair)
    dchi = (c_nosec - c_sec) / dof
    p161.append({"label": label, "gap_over_gamma": float(ratio),
                 "chi2_sec": c_sec, "chi2_nosec": c_nosec,
                 "dchi2_dof": float(dchi)})
    print(f"P16.1v2 {label}: gap/g={ratio:.4f} chi2_sec={c_sec:.1f} "
          f"chi2_nosec={c_nosec:.1f} dchi2/dof={dchi:.2f}", flush=True)

# ---- P16.2 v2: CRB via SVD of the design matrix ----
p162 = {"points": []}
for i in range(1, len(rows) - 1):
    row = rows[i]
    pair = np.array([complex(*row["pair"][0]), complex(*row["pair"][1])])
    pm = np.array([complex(*rows[i - 1]["pair"][0]),
                   complex(*rows[i - 1]["pair"][1])])
    pp = np.array([complex(*rows[i + 1]["pair"][0]),
                   complex(*rows[i + 1]["pair"][1])])
    dq = rows[i + 1]["delta"] - rows[i - 1]["delta"]
    dw = (pp - pm) / dq
    w1, w2 = pair
    d = w1 - w2
    A = np.array([1 / d, -1 / d])
    E = [np.exp(-1j * w1 * T), np.exp(-1j * w2 * T)]
    # Mirror pair makes the four naive amplitude columns exactly rank-2
    # (Im E2 = -Im E1, Re E2 = Re E1), so the honest nuisance space is the
    # two real envelope amplitudes of one member.
    cols = [np.imag(A[0] * (-1j * T) * dw[0] * E[0]
                    + A[1] * (-1j * T) * dw[1] * E[1]),
            np.imag(E[0]), np.real(E[0])]
    J = np.column_stack(cols)
    scale = np.max(np.abs(signal(pair)))
    U, S, Vt = np.linalg.svd(J, full_matrices=False)
    condJ = float(S[0] / S[-1])
    if condJ > 1e14:
        print(f"P16.2v2 d={row['delta']:.2e}: cond(J)={condJ:.1e} SKIP "
              "(beyond double precision)", flush=True)
        continue
    # var_theta = [V S^-2 V^T]_00 = sum_k (Vt[k,0]/S[k])^2
    var = float(np.sum((Vt[:, 0] / S) ** 2)) * (NOISE * scale) ** 2
    sigma = float(np.sqrt(var))
    p162["points"].append({"delta": row["delta"], "gap": row["gap"],
                           "sigma": sigma, "condJ": condJ,
                           "gapT": float(row["gap"] * T[-1])})
    print(f"P16.2v2 d={row['delta']:.2e} gap={row['gap']:.3e} "
          f"sigma={sigma:.3e} cond(J)={condJ:.1e}", flush=True)

pts = p162["points"]
if len(pts) >= 5:
    x = np.log([q["gap"] for q in pts])
    y = np.log([q["sigma"] for q in pts])
    p162["exponent_p"] = float(-np.polyfit(x, y, 1)[0])
    sub = [q for q in pts if q["gapT"] < 0.5]
    if len(sub) >= 5:
        xs = np.log([q["gap"] for q in sub])
        ys = np.log([q["sigma"] for q in sub])
        p162["exponent_p_unresolved"] = float(-np.polyfit(xs, ys, 1)[0])
    print(f"P16.2v2 exponent p = {p162['exponent_p']:.3f} "
          f"(unresolved-window subset: "
          f"{p162.get('exponent_p_unresolved', float('nan')):.3f}; "
          "frozen prediction 1.0, kill outside [0.6,1.5])", flush=True)

res["p16_1_v2"] = p161
res["p16_2_v2"] = p162
pathlib.Path("results/p16_decoherence.json").write_text(
    json.dumps(res, indent=1))
print("done", flush=True)
