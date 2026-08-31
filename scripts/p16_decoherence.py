"""P16 - decoherence as the fourth task class (frozen 2026-08-31).

Probe pure-dephasing channel = Green's function of the fundamental QNM
pair at the mirror EP (lambda = 0.105):

  r(t) = Im[(e^{-i w1 t} - e^{-i w2 t}) / (w1 - w2)]

P16.1 secular-channel rescue (bounded amplitudes; compensator trap fix).
P16.2 CRB exponent for delta-q^2 estimation, free complex amplitudes.
P16.3 past-EP protection: Gamma_slow kink with sqrt exponent.

See results/FROZEN_P16_DECOHERENCE.md for predictions and kill criteria.
"""
import json
import pathlib

import numpy as np
from scipy.optimize import least_squares

from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients
from recoverability_ep.shooting import ShootingSolver

LAM = 0.105
# Anchored EP from shooting_ep_hunt.json (lam=0.105), already refined there.
Q2_C = -34.385584013122106
OMEGA_C = 6.304792860228959e-07 - 7.164147056680743j
RNG = np.random.default_rng(16)
NOISE = 1e-3

b0, bp0, nf = exact_gb_metric(LAM)
hc0 = tuple(np.array(exact_horizon_coefficients(LAM, 24)))


def pair_at(q2, seed):
    s = ShootingSolver(b0, bp0, nf, q2, horizon_coefficients=hc0)
    p = s.pair(seed)
    p = np.array(sorted(p, key=lambda w: (round(w.real, 6), w.imag)))
    # gates (lesson from kernel_compare): mirror structure or both on the
    # imaginary axis; and no identity jump of the centroid vs the seed
    mirror = abs(p[0] + np.conj(p[1]))
    axis = max(abs(p[0].real), abs(p[1].real))
    if min(mirror, axis) > 5e-3:
        raise RuntimeError(f"mirror gate ({mirror:.1e}/{axis:.1e})")
    if abs(np.mean(p) - np.mean(np.asarray(seed))) > 0.1:
        raise RuntimeError("identity jump")
    return p


def gap_of(p):
    return float(abs(p[0] - p[1]))


# ---- verify the anchor ----
pair_c = pair_at(Q2_C, np.array([OMEGA_C + 1e-4, OMEGA_C - 1e-4]))
q2_c, gap_min = Q2_C, gap_of(pair_c)
omega_ep = complex(np.mean(pair_c))
gamma_ep = -omega_ep.imag
print(f"EP anchor: q2_c={q2_c:.8f} omega_ep={omega_ep:.6f} "
      f"gap={gap_min:.2e} gamma_EP={gamma_ep:.6f}", flush=True)
assert gap_min < 1e-3, "EP refinement did not converge"

# ---- stage 2: trajectory on both sides, log-spaced offsets ----
deltas = np.logspace(-4, -0.5, 22)
traj = {"+1": [], "-1": []}
for sgn in (+1, -1):
    seed = pair_c
    for d in deltas:
        q2 = q2_c + sgn * d
        try:
            p = pair_at(q2, seed)
        except Exception as exc:
            print(f"traj sgn={sgn:+d} d={d:.2e}: FAIL {exc}", flush=True)
            break
        seed = p
        re_split = abs(p[0].real - p[1].real)
        im_split = abs(p[0].imag - p[1].imag)
        kind = "under" if re_split > im_split else "over"
        traj[f"{sgn:+d}"].append(
            {"delta": float(d), "q2": float(q2), "kind": kind,
             "pair": [[p[0].real, p[0].imag], [p[1].real, p[1].imag]],
             "gap": gap_of(p), "re_split": float(re_split),
             "im_split": float(im_split),
             "gamma_slow": float(min(-p[0].imag, -p[1].imag))})
        print(f"sgn={sgn:+d} d={d:.3e} kind={kind} gap={gap_of(p):.3e} "
              f"G_slow={min(-p[0].imag, -p[1].imag):.5f}", flush=True)

sides = {}
for key, rows in traj.items():
    if rows:
        kinds = [r["kind"] for r in rows if r["delta"] > 3e-3]
        sides[key] = max(set(kinds), key=kinds.count) if kinds else "?"
print(f"side classification: {sides}", flush=True)
under_key = next((k for k, v in sides.items() if v == "under"), None)
over_key = next((k for k, v in sides.items() if v == "over"), None)
result = {"lam": LAM, "q2_c": q2_c, "gap_min": gap_min,
          "omega_ep": [omega_ep.real, omega_ep.imag], "sides": sides,
          "traj": traj}


def loglog_slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = (x > 0) & (y > 0) & np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 4:
        return None
    return float(np.polyfit(np.log(x[ok]), np.log(y[ok]), 1)[0])


# ---- P16.3: splitting exponents, protection, kink ----
p163 = {}
if under_key:
    rows = traj[under_key]
    p163["h_under_split"] = loglog_slope([r["delta"] for r in rows],
                                         [r["re_split"] for r in rows])
    gs = np.array([r["gamma_slow"] for r in rows])
    ds = np.array([r["delta"] for r in rows])
    p163["under_gslow_rel_range"] = float((gs.max() - gs.min()) / gamma_ep)
    p163["under_gslow_slope_norm"] = float(
        np.polyfit(ds, gs, 1)[0] * ds.max() / gamma_ep)
if over_key:
    rows = traj[over_key]
    p163["h_over_split"] = loglog_slope([r["delta"] for r in rows],
                                        [r["im_split"] for r in rows])
    prot = np.array([gamma_ep - r["gamma_slow"] for r in rows])
    p163["protection_all_positive"] = bool(np.all(prot > 0))
    p163["h_protection"] = loglog_slope([r["delta"] for r in rows], prot)
    p163["max_protection_rel"] = float(prot.max() / gamma_ep)
print(f"P16.3: {json.dumps(p163)}", flush=True)
result["p16_3"] = p163

# ---- signal machinery ----
T = np.linspace(0.0, 4.0 / gamma_ep, 400)


def signal(pair):
    w1, w2 = pair
    if abs(w1 - w2) < 1e-9:
        return np.imag(-1j * T * np.exp(-1j * w1 * T))
    return np.imag((np.exp(-1j * w1 * T) - np.exp(-1j * w2 * T)) / (w1 - w2))


def chi2(res):
    return float(np.sum(res ** 2) / NOISE ** 2)


def fit_sec(y):
    def model(p):
        a = p[0] + 1j * p[1]
        b = p[2] + 1j * p[3]
        w = p[4] + 1j * p[5]
        return np.imag((a + b * T) * np.exp(-1j * w * T)) - y
    best = None
    for fr, fi in [(0.0, -gamma_ep), (0.05, -0.95 * gamma_ep),
                   (-0.05, -1.05 * gamma_ep)]:
        r = least_squares(model, [0, 0, -1, 0, fr, fi],
                          bounds=([-10, -10, -10, -10, -20, -30],
                                  [10, 10, 10, 10, 20, -1e-2]))
        if best is None or r.cost < best.cost:
            best = r
    return chi2(best.fun)


def fit_nosec(y, pair):
    w1, w2 = pair
    d = w1 - w2 if abs(w1 - w2) > 1e-6 else 1e-6
    a1 = np.clip([( 1 / d).real, ( 1 / d).imag], -9.9, 9.9)
    a2 = np.clip([(-1 / d).real, (-1 / d).imag], -9.9, 9.9)

    def model(p):
        A1 = p[0] + 1j * p[1]
        A2 = p[2] + 1j * p[3]
        u1 = p[4] + 1j * p[5]
        u2 = p[6] + 1j * p[7]
        return (np.imag(A1 * np.exp(-1j * u1 * T) + A2 * np.exp(-1j * u2 * T))
                - y)
    lo = [-10, -10, -10, -10, -20, -30, -20, -30]
    hi = [10, 10, 10, 10, 20, -1e-2, 20, -1e-2]
    best = None
    for f1, f2 in [(w1, w2), (w1 * 1.02, w2 * 0.98),
                   (w1 + 0.05, w2 - 0.05)]:
        x0 = [a1[0], a1[1], a2[0], a2[1],
              np.clip(f1.real, -19, 19), np.clip(f1.imag, -29, -2e-2),
              np.clip(f2.real, -19, 19), np.clip(f2.imag, -29, -2e-2)]
        r = least_squares(model, x0, bounds=(lo, hi))
        if best is None or r.cost < best.cost:
            best = r
    return chi2(best.fun)


# ---- P16.1: secular rescue at gap/gamma ~ {EP, 0.05, 0.5} ----
p161 = []
targets = [("EP", None)]
if under_key:
    rows = traj[under_key]
    for label, ratio in [("near", 0.05), ("far", 0.5)]:
        best = min(rows, key=lambda r: abs(r["gap"] / gamma_ep - ratio))
        targets.append((label, best))
for label, row in targets:
    if row is None:
        pair = np.array([omega_ep, omega_ep])
        ratio = gap_min / gamma_ep
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
    print(f"P16.1 {label}: gap/g={ratio:.4f} chi2_sec={c_sec:.1f} "
          f"chi2_nosec={c_nosec:.1f} dchi2/dof={dchi:.2f}", flush=True)
result["p16_1"] = p161

# ---- P16.2: marginalized CRB for delta-q^2 vs gap (underdamped side) ----
p162 = {"points": []}
if under_key:
    rows = traj[under_key]
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
        cols = [np.imag(A[0] * (-1j * T) * dw[0] * E[0]
                        + A[1] * (-1j * T) * dw[1] * E[1])]
        for j in range(2):
            cols.append(np.imag(E[j]))
            cols.append(np.imag(1j * E[j]))
        J = np.column_stack(cols)
        scale = np.max(np.abs(signal(pair)))
        I = (J.T @ J) / (NOISE * scale) ** 2
        cond = float(np.linalg.cond(I))
        if cond > 1e12:
            import mpmath as mp
            mp.mp.dps = 50
            Im = mp.matrix(I.tolist())
            var = float((Im ** -1)[0, 0])
        else:
            var = float(np.linalg.inv(I)[0, 0])
        if var <= 0:
            print(f"P16.2 d={row['delta']:.2e}: var<=0 SKIP", flush=True)
            continue
        p162["points"].append({"delta": row["delta"], "gap": row["gap"],
                               "sigma": float(np.sqrt(var)), "cond": cond})
        print(f"P16.2 d={row['delta']:.2e} gap={row['gap']:.3e} "
              f"sigma={np.sqrt(var):.3e} cond={cond:.1e}", flush=True)
    pts = p162["points"]
    if len(pts) >= 5:
        p162["exponent_p"] = -loglog_slope([q["gap"] for q in pts],
                                           [q["sigma"] for q in pts])
        print(f"P16.2 exponent p = {p162['exponent_p']:.3f} "
              f"(frozen prediction 1.0, kill outside [0.6,1.5])", flush=True)
result["p16_2"] = p162

pathlib.Path("results/p16_decoherence.json").write_text(
    json.dumps(result, indent=1))
print("done", flush=True)
