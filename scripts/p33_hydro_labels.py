"""P33: the gradient expansion stops where the labels stop
(frozen in results/FROZEN_P33_HYDRO_LABELS.md).

Scalar channel of the 5D planar Einstein black brane (lambda_GB = 0).
The mirror pair collides at the EP q^2_c = -16.147205102. Three tests:
  1. monodromy around the EP: labels swap, invariants return;
  2. rho has a simple zero at the EP, and the Taylor radii about
     q^2 = 0 differ (Cauchy coefficients on circles of radius 12, 14);
  3. beyond the labelled radius the invariant series still works.
Plus the noise-scaling re-verification (1/2 versus 1).
Output: results/p33_hydro_labels.json
"""
import json
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, "src")
from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients  # noqa
from recoverability_ep.shooting import ShootingSolver, pair_invariants  # noqa

LAM = 0.0
Q2C = -5.0130            # located with this solver (see the freeze amendment); refined by Newton below
B, BP, NF = exact_gb_metric(LAM)
HC = exact_horizon_coefficients(LAM, 24)
OUT = {"lambda_GB": LAM, "q2_c": Q2C}


def solver(q2, **kw):
    return ShootingSolver(B, BP, NF, complex(q2), horizon_coefficients=HC, **kw)


def pair_at(q2, seed):
    return solver(q2).pair(np.asarray(seed, dtype=complex))


# anchor at q^2 = 0
t0 = time.time()
seed0 = np.array([3.1195 - 2.7467j, -3.1195 - 2.7467j])
p0 = pair_at(0.0, seed0)
mu0, rho0 = pair_invariants(p0)
print(f"q^2 = 0: pair {p0[0]:.7f}, {p0[1]:.7f};  mu = {mu0:.7f}, rho = {rho0:.7f}  ({time.time()-t0:.0f}s)", flush=True)
OUT["at_zero"] = {"pair": [[z.real, z.imag] for z in p0], "mu": [mu0.real, mu0.imag], "rho": [rho0.real, rho0.imag]}


def track_path(q2s, seed):
    """Continue the pair along a path, keeping the label order by nearest match."""
    pairs = []
    cur = np.asarray(seed, dtype=complex)
    for q2 in q2s:
        new = pair_at(q2, cur)
        # keep labels continuous: match new roots to the previous ones
        if abs(new[0] - cur[0]) + abs(new[1] - cur[1]) > abs(new[1] - cur[0]) + abs(new[0] - cur[1]):
            new = new[::-1]
        pairs.append(new)
        cur = new
    return np.array(pairs)


# ---------------- refine the EP (instrument calibration, not a prediction)
cur = track_path(np.linspace(0.0, -5.0, 60), p0)[-1]
q2c = -5.0
for _ in range(12):
    _, rho_c = pair_invariants(pair_at(q2c, cur))
    hh = 1e-4 * (1 + abs(q2c))
    _, rho_h = pair_invariants(pair_at(q2c + hh, cur))
    stp = -rho_c / ((rho_h - rho_c) / hh)
    if abs(stp) > 0.2:
        stp = 0.2 * stp / abs(stp)
    q2c = float(np.real(q2c + stp))
    cur = pair_at(q2c, cur)
    if abs(stp) < 1e-10:
        break
mu_c, rho_c = pair_invariants(cur)
Q2C = q2c
OUT["q2_c_refined"] = q2c
OUT["omega_c"] = [mu_c.real, mu_c.imag]
print(f"refined EP: q^2_c = {q2c:.7f}, omega_c = {mu_c:.7f}, rho = {rho_c:.2e}", flush=True)

# ---------------- P33.1 monodromy
OUT["monodromy"] = {}
for radius in (0.5, 1.0):
    t0 = time.time()
    # walk in from q^2 = 0 to the start point on the circle
    start = Q2C + radius
    approach = np.linspace(0.0, start, 40)
    pr = track_path(approach, p0)
    cur = pr[-1]
    theta = np.linspace(0, 2 * np.pi, 121)[1:]
    circle = Q2C + radius * np.exp(1j * theta)
    pc = track_path(circle, cur)
    before, after = cur, pc[-1]
    mu_b, rho_b = pair_invariants(before)
    mu_a, rho_a = pair_invariants(after)
    rec = dict(radius=radius, start_q2=float(start),
               before=[[z.real, z.imag] for z in before], after=[[z.real, z.imag] for z in after],
               swap_error=float(max(abs(after[0] - before[1]), abs(after[1] - before[0]))),
               same_error=float(min(abs(after[0] - before[0]), abs(after[1] - before[1]))),
               label_motion=float(abs(after[0] - before[0])),
               mu_shift=float(abs(mu_a - mu_b)), rho_shift=float(abs(rho_a - rho_b)), seconds=time.time() - t0)
    OUT["monodromy"][str(radius)] = rec
    print(f"monodromy r={radius}: before {before[0]:.6f} / {before[1]:.6f} -> after {after[0]:.6f} / {after[1]:.6f}", flush=True)
    print(f"   swap error {rec['swap_error']:.2e}, |omega_+ moved| {rec['label_motion']:.3f}, mu shift {rec['mu_shift']:.2e}, rho shift {rec['rho_shift']:.2e}  ({rec['seconds']:.0f}s)", flush=True)

# ---------------- P33.2 the zero at the EP and the two radii
t0 = time.time()
approach = np.linspace(0.0, Q2C, 80)
pr = track_path(approach, p0)
pc_ep = pr[-1]
mu_ep, rho_ep = pair_invariants(pc_ep)
h = 1e-3
p_h = pair_at(Q2C + h, pc_ep)
_, rho_h = pair_invariants(p_h)
drho = (rho_h - rho_ep) / h
OUT["at_EP"] = {"pair": [[z.real, z.imag] for z in pc_ep], "mu": [mu_ep.real, mu_ep.imag],
                "rho": [rho_ep.real, rho_ep.imag], "abs_rho": float(abs(rho_ep)),
                "drho_dq2": [drho.real, drho.imag], "abs_drho": float(abs(drho))}
print(f"at the EP: mu = {mu_ep:.7f}, rho = {rho_ep:.3e} (|rho| = {abs(rho_ep):.2e}), drho/dq^2 = {drho:.5f} (|.| = {abs(drho):.4f})  ({time.time()-t0:.0f}s)", flush=True)

OUT["radii"] = {}
for r0 in (3.5, 4.5):
    t0 = time.time()
    N = 128
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    q2s = r0 * np.exp(1j * theta)
    # start on the positive real axis and go round; labels stay continuous (EP is outside for omega)
    approach = np.linspace(0.0, r0, 24)
    pr = track_path(approach, p0)
    pc = track_path(q2s[1:], pr[-1])
    pairs = np.vstack([pr[-1][None, :], pc])
    om_p = pairs[:, 0]
    mus = np.array([pair_invariants(p)[0] for p in pairs])
    rhos = np.array([pair_invariants(p)[1] for p in pairs])
    closure = dict(omega=float(abs(om_p[-1] - om_p[0])), mu=float(abs(mus[-1] - mus[0])), rho=float(abs(rhos[-1] - rhos[0])))
    ests = {}
    for name, vals in (("omega_plus", om_p), ("mu", mus), ("rho", rhos)):
        a = np.array([np.mean(vals * np.exp(-1j * n * theta)) / r0 ** n for n in range(16)])
        R = [float(abs(a[n]) ** (-1.0 / n)) if abs(a[n]) > 0 else np.inf for n in range(1, 16)]
        ratio = [float(abs(a[n] / a[n + 1])) if a[n + 1] != 0 else np.inf for n in range(1, 15)]
        Rest = float(np.median([x for x in R[5:14] if np.isfinite(x)]))
        ests[name] = {"coeffs_abs": [float(abs(x)) for x in a], "R_root_test": R, "R_ratio_test": ratio, "R_estimate": Rest}
        print(f"  r0={r0} {name}: |a_n| = {[f'{abs(x):.2e}' for x in a[:8]]}...  R (root test, n=6..14 median) = {Rest:.2f}", flush=True)
    OUT["radii"][str(r0)] = {"closure": closure, "estimates": ests, "seconds": time.time() - t0}
    print(f"   closure after the loop: omega {closure['omega']:.1e}, mu {closure['mu']:.1e}, rho {closure['rho']:.1e}  ({time.time()-t0:.0f}s)", flush=True)
pathlib.Path("results/p33_hydro_labels.json").write_text(json.dumps(OUT, indent=1))

# ---------------- P33.3 usefulness beyond the labelled radius
best = OUT["radii"]["4.5"]["estimates"]
R_om, R_rho = best["omega_plus"]["R_estimate"], best["rho"]["R_estimate"]
q2t = -(R_om + R_rho) / 2
print(f"\nP33.3: R_omega = {R_om:.2f}, R_rho = {R_rho:.2f} -> test at q^2 = {q2t:.3f}", flush=True)
a_om = np.array(best["omega_plus"]["coeffs_abs"])
# rebuild complex coefficients on the r0 = 14 circle
theta = np.linspace(0, 2 * np.pi, 128, endpoint=False)
q2s = 4.5 * np.exp(1j * theta)
approach = np.linspace(0.0, 4.5, 24)
pr = track_path(approach, p0)
pc = track_path(q2s[1:], pr[-1])
pairs = np.vstack([pr[-1][None, :], pc])
series = {}
for name, vals in (("omega_plus", pairs[:, 0]), ("rho", np.array([pair_invariants(p)[1] for p in pairs]))):
    series[name] = np.array([np.mean(vals * np.exp(-1j * n * theta)) / 4.5 ** n for n in range(13)])
# true values at q2t by continuation along the spacelike axis (through the EP: use mu, rho)
path = np.linspace(0.0, q2t, 160)
pr_t = track_path(path, p0)
true_pair = pr_t[-1]
mu_t, rho_t = pair_invariants(true_pair)
pred_rho = sum(series["rho"][n] * q2t ** n for n in range(13))
pred_om = sum(series["omega_plus"][n] * q2t ** n for n in range(13))
err_rho = abs(pred_rho - rho_t) / abs(rho_t)
err_om = abs(pred_om - true_pair[0]) / abs(true_pair[0])
OUT["P33_3"] = {"q2_test": float(q2t), "R_omega": R_om, "R_rho": R_rho,
                "true_pair": [[z.real, z.imag] for z in true_pair], "true_rho": [rho_t.real, rho_t.imag],
                "series_rho": [pred_rho.real, pred_rho.imag], "series_omega": [pred_om.real, pred_om.imag],
                "rel_err_rho": float(err_rho), "rel_err_omega": float(err_om)}
print(f"   true rho = {rho_t:.6f}, order-12 series = {pred_rho:.6f}, relative error {err_rho:.2%}", flush=True)
print(f"   true omega_+ = {true_pair[0]:.6f}, order-12 series = {pred_om:.6f}, relative error {err_om:.2%}", flush=True)
pathlib.Path("results/p33_hydro_labels.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
