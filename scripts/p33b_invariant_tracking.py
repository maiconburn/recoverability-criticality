"""P33 stage 2: track the INVARIANTS, not the labels.

The stage-1 tracker followed omega_+ and omega_- by nearest match and blew
up past the EP (at q^2 = -5.75 on the real axis, and on the radius-1.0
monodromy circle it ran away to omega ~ -4148). The reason is the content
of the cycle: past the EP the pair sits on the imaginary axis and the
labels are not continuous functions of q^2, while mu = (om_+ + om_-)/2 and
rho = ((om_+ - om_-)/2)^2 are. So predict mu and rho by extrapolation and
seed the solver with mu +- sqrt(rho).

Three products:
  1. the invariant tracker, validated past the EP;
  2. corrected radius-of-convergence estimates (the frozen |a_n|^(-1/n)
     estimator is biased at n <= 14; use the ratio test with the n^(-3/2)
     prefactor of a square-root branch point removed, and a
     |a_n| = C n^-p R^-n fit);
  3. P33.3 evaluated at a test momentum between the two radii.
Output: results/p33b_invariant_tracking.json
"""
import json
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, "src")
from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients  # noqa
from recoverability_ep.shooting import ShootingSolver, pair_invariants  # noqa

B, BP, NF = exact_gb_metric(0.0)
HC = exact_horizon_coefficients(0.0, 24)
Q2C = -5.0123755
OUT = {"q2_c": Q2C}


def pair_at(q2, seed):
    return ShootingSolver(B, BP, NF, complex(q2), horizon_coefficients=HC).pair(np.asarray(seed, dtype=complex))


def invariant_track(q2s, mu0, rho0, q2_0):
    """March in q^2 seeding from extrapolated invariants. Returns list of
    (q2, mu, rho, pair, validation error)."""
    hist = [(q2_0, mu0, rho0)]
    out = []
    for q2 in q2s:
        if len(hist) >= 3:
            xs = np.array([h[0] for h in hist[-3:]])
            mu_p = np.polyval(np.polyfit(xs, [h[1] for h in hist[-3:]], 2), q2)
            rho_p = np.polyval(np.polyfit(xs, [h[2] for h in hist[-3:]], 2), q2)
        elif len(hist) == 2:
            (x1, m1, r1), (x2, m2, r2) = hist[-2:]
            w = (q2 - x2) / (x2 - x1)
            mu_p, rho_p = m2 + (m2 - m1) * w, r2 + (r2 - r1) * w
        else:
            mu_p, rho_p = hist[-1][1], hist[-1][2]
        s = np.sqrt(complex(rho_p))
        seed = np.array([mu_p + s, mu_p - s])
        pair = pair_at(q2, seed)
        mu, rho = pair_invariants(pair)
        err = abs(mu - mu_p) + abs(rho - rho_p)
        hist.append((q2, mu, rho))
        out.append((q2, mu, rho, pair, err))
    return out


# ---- 1. march through the EP on the spacelike axis
t0 = time.time()
p0 = pair_at(0.0, np.array([3.119452 - 2.746676j, -3.119452 - 2.746676j]))
mu0, rho0 = pair_invariants(p0)
q2s = np.arange(-0.1, -9.001, -0.1)
tr = invariant_track(q2s, mu0, rho0, 0.0)
print("  q^2      mu                     rho                   pair gap      pred error")
rows = []
for q2, mu, rho, pair, err in tr:
    gap = abs(pair[0] - pair[1])
    rows.append([float(q2), [mu.real, mu.imag], [rho.real, rho.imag], float(gap), float(err)])
    if abs(q2 % 1.0) < 1e-9 or abs(abs(q2) - 5.0) < 0.05:
        print(f"  {q2:6.2f}  {mu.real:+.7f}{mu.imag:+.7f}j  {rho.real:+.7f}{rho.imag:+.7f}j  {gap:.6f}  {err:.1e}")
OUT["spacelike_march"] = rows
maxerr = max(r[4] for r in rows)
print(f"  invariant tracker reached q^2 = {rows[-1][0]:.2f} past the EP at {Q2C:.4f}; worst prediction error {maxerr:.1e}  ({time.time()-t0:.0f}s)", flush=True)

# ---- 2. monodromy at radius 1.0 with the invariant tracker
t0 = time.time()
radius = 1.0
start = Q2C + radius
tr_in = invariant_track(np.linspace(-0.1, start, 60), mu0, rho0, 0.0)
mu_s, rho_s = tr_in[-1][1], tr_in[-1][2]
before = tr_in[-1][3]
theta = np.linspace(0, 2 * np.pi, 121)[1:]
circle = Q2C + radius * np.exp(1j * theta)
tr_c = invariant_track(circle, mu_s, rho_s, start)
after = tr_c[-1][3]
mu_a, rho_a = tr_c[-1][1], tr_c[-1][2]
rec = dict(radius=radius, before=[[z.real, z.imag] for z in before], after=[[z.real, z.imag] for z in after],
           swap_error=float(max(abs(after[0] - before[1]), abs(after[1] - before[0]))),
           label_motion=float(abs(after[0] - before[0])),
           mu_shift=float(abs(mu_a - mu_s)), rho_shift=float(abs(rho_a - rho_s)),
           worst_pred_error=float(max(x[4] for x in tr_c)), seconds=time.time() - t0)
OUT["monodromy_r1_invariant"] = rec
print(f"\nmonodromy r=1.0 (invariant tracker): before {before[0]:.7f} -> after {after[0]:.7f}", flush=True)
print(f"   swap error {rec['swap_error']:.2e}, |omega_+ moved| {rec['label_motion']:.4f}, mu shift {rec['mu_shift']:.2e}, rho shift {rec['rho_shift']:.2e}, worst prediction error {rec['worst_pred_error']:.1e}  ({rec['seconds']:.0f}s)", flush=True)

# ---- 3. corrected radii from the stage-1 coefficients
st1 = json.load(open("results/p33_hydro_labels.json"))
OUT["radii_corrected"] = {}
for name in ("omega_plus", "mu", "rho"):
    a = np.array(st1["radii"]["4.5"]["estimates"][name]["coeffs_abs"])
    rat = a[:-1] / a[1:]
    corr = {k: float(rat[k] / (1 + 1.5 / k)) for k in range(5, min(14, len(rat)))}
    sel = np.arange(5, min(14, len(a)))
    A = np.vstack([np.ones(len(sel)), -np.log(sel), -sel]).T
    coef, *_ = np.linalg.lstsq(A, np.log(a[sel]), rcond=None)
    A2 = np.vstack([np.ones(len(sel)), -sel]).T
    c2, *_ = np.linalg.lstsq(A2, np.log(a[sel]) + 1.5 * np.log(sel), rcond=None)
    plateau = [v for k, v in corr.items() if 7 <= k <= 11]
    OUT["radii_corrected"][name] = {"ratio_raw": rat.tolist(), "ratio_corrected": corr,
                                    "free_fit_R": float(np.exp(coef[2])), "free_fit_p": float(coef[1]),
                                    "p32_fit_R": float(np.exp(c2[1])),
                                    "R_plateau_mean": float(np.mean(plateau)), "R_plateau_spread": float(np.ptp(plateau))}
    print(f"  {name}: corrected-ratio plateau (n = 7..11) {np.mean(plateau):.3f} +- {np.ptp(plateau)/2:.3f}; p=3/2 fit {np.exp(c2[1]):.3f}; free fit R {np.exp(coef[2]):.3f} p {coef[1]:.2f}", flush=True)
R_om = OUT["radii_corrected"]["omega_plus"]["R_plateau_mean"]
R_rho = OUT["radii_corrected"]["rho"]["ratio_raw"][8]      # rho's raw ratio plateaus (not a sqrt branch point)
OUT["R_omega"], OUT["R_rho"] = R_om, R_rho
print(f"  => R_omega = {R_om:.3f} (|q^2_c| = {abs(Q2C):.4f}, ratio {R_om/abs(Q2C):.3f}), R_rho = {R_rho:.3f}, R_rho/R_omega = {R_rho/R_om:.3f}", flush=True)

# ---- 4. P33.3 with the invariant tracker for the true values
q2t = -(R_om + R_rho) / 2
theta = np.linspace(0, 2 * np.pi, 128, endpoint=False)
ser = {}
for name in ("omega_plus", "rho"):
    # rebuild complex coefficients from the stage-1 circle (r0 = 4.5)
    pass
# recompute the r0 = 4.5 circle with the invariant tracker to get complex coefficients
q2s_c = 4.5 * np.exp(1j * theta)
tr_in = invariant_track(np.linspace(0.1, 4.5, 24), mu0, rho0, 0.0)
mu_s, rho_s = tr_in[-1][1], tr_in[-1][2]
tr_c = invariant_track(q2s_c[1:], mu_s, rho_s, 4.5)
mus = np.array([mu_s] + [x[1] for x in tr_c])
rhos = np.array([rho_s] + [x[2] for x in tr_c])
oms = mus + np.sqrt(rhos)
coef_rho = np.array([np.mean(rhos * np.exp(-1j * n * theta)) / 4.5 ** n for n in range(13)])
coef_om = np.array([np.mean(oms * np.exp(-1j * n * theta)) / 4.5 ** n for n in range(13)])
tr_t = invariant_track(np.arange(-0.1, q2t - 1e-9, -0.05), mu0, rho0, 0.0)
mu_t, rho_t, pair_t = tr_t[-1][1], tr_t[-1][2], tr_t[-1][3]
pred_rho = sum(coef_rho[n] * q2t ** n for n in range(13))
pred_om = sum(coef_om[n] * q2t ** n for n in range(13))
err_rho = abs(pred_rho - rho_t) / abs(rho_t)
err_om = abs(pred_om - pair_t[0]) / abs(pair_t[0])
OUT["P33_3"] = {"q2_test": float(q2t), "R_omega": R_om, "R_rho": R_rho,
                "true_rho": [rho_t.real, rho_t.imag], "true_omega_plus": [pair_t[0].real, pair_t[0].imag],
                "series_rho": [pred_rho.real, pred_rho.imag], "series_omega": [pred_om.real, pred_om.imag],
                "rel_err_rho": float(err_rho), "rel_err_omega": float(err_om),
                "tracker_worst_error": float(max(x[4] for x in tr_t))}
print(f"\nP33.3 at q^2 = {q2t:.4f} (between {R_om:.2f} and {R_rho:.2f}):", flush=True)
print(f"   true rho    = {rho_t:+.7f}, order-12 series = {pred_rho:+.7f}, relative error {err_rho:.2%}", flush=True)
print(f"   true omega_+ = {pair_t[0]:+.7f}, order-12 series = {pred_om:+.7f}, relative error {err_om:.2%}", flush=True)
pathlib.Path("results/p33b_invariant_tracking.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
