"""P33.3, third attempt: continue the pair PAST the EP along the spacelike
axis with a tracker built for the post-collision regime.

Past q^2_c the two modes are both purely imaginary (mu is imaginary and
rho < 0, so omega_+- = i(Im mu +- sqrt|rho|)); the mirror symmetry maps each
onto itself. Neither the label tracker (stage 1) nor the invariant tracker
with a principal square root (stage 2) survives there, because both seed a
generic complex pair while the truth is two separate points on the
imaginary axis among the overdamped tower. Here each root is continued
INDEPENDENTLY with refine_root and small steps, validated by
|Re omega| < 1e-6 and a step bound.
Output: results/p33c_beyond_ep.json
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
Q2C, MU_C, DRHO = -5.0123755, -3.5387430j, 3.20485
OUT = {"q2_c": Q2C}


def solver(q2):
    return ShootingSolver(B, BP, NF, complex(q2), horizon_coefficients=HC)


# start just past the EP where the split is small but resolved
q2 = Q2C - 0.02
rho = -DRHO * 0.02
s = np.sqrt(complex(rho))
hi, lo = MU_C + s, MU_C - s
hi = solver(q2).refine_root(complex(hi))
lo = solver(q2).refine_root(complex(lo))
print(f"seeded past the EP at q^2 = {q2:.5f}: omega = {hi:.7f} and {lo:.7f}", flush=True)
rows = [(q2, hi, lo)]
step = 0.02
target = -7.6
while q2 > target:
    q2n = q2 - step
    if len(rows) >= 3:
        xs = np.array([r[0] for r in rows[-3:]])
        hp = np.polyval(np.polyfit(xs, [r[1] for r in rows[-3:]], 2), q2n)
        lp = np.polyval(np.polyfit(xs, [r[2] for r in rows[-3:]], 2), q2n)
    else:
        hp, lp = rows[-1][1], rows[-1][2]
    try:
        hn = solver(q2n).refine_root(complex(hp))
        ln = solver(q2n).refine_root(complex(lp))
    except Exception as e:
        step /= 2
        if step < 1e-4:
            print(f"  lost at q^2 = {q2n:.4f}: {str(e)[:60]}", flush=True)
            break
        continue
    ok = abs(hn.real) < 1e-6 and abs(ln.real) < 1e-6 and abs(hn - hp) < 0.2 and abs(ln - lp) < 0.2 and abs(hn - ln) > 1e-6
    if not ok:
        step /= 2
        if step < 1e-4:
            print(f"  validation failed at q^2 = {q2n:.4f}: {hn:.6f}, {ln:.6f}", flush=True)
            break
        continue
    q2, hi, lo = q2n, hn, ln
    rows.append((q2, hi, lo))
    step = min(step * 1.3, 0.05)
    if abs(q2 - round(q2 * 2) / 2) < 0.03:
        mu, rh = pair_invariants(np.array([hi, lo]))
        print(f"  q^2 = {q2:7.4f}: omega = {hi.imag:+.7f}i and {lo.imag:+.7f}i;  mu = {mu.imag:+.7f}i, rho = {rh.real:+.7f}", flush=True)
OUT["march"] = [[float(r[0]), [r[1].real, r[1].imag], [r[2].real, r[2].imag]] for r in rows]
print(f"  reached q^2 = {rows[-1][0]:.4f} ({len(rows)} points)", flush=True)

# P33.3 at the frozen test point, if reached
st2 = json.load(open("results/p33b_invariant_tracking.json"))
R_om, R_rho = st2["R_omega"], st2["R_rho"]
q2t = -(R_om + R_rho) / 2
best = min(rows, key=lambda r: abs(r[0] - q2t))
OUT["R_omega"], OUT["R_rho"], OUT["q2_test"] = R_om, R_rho, float(q2t)
if abs(best[0] - q2t) < 0.05:
    mu_t, rho_t = pair_invariants(np.array([best[1], best[2]]))
    # order-12 series about q^2 = 0 from the r0 = 4.5 circle, rebuilt with the label tracker (valid inside 4.5)
    st1 = json.load(open("results/p33_hydro_labels.json"))
    theta = np.linspace(0, 2 * np.pi, 128, endpoint=False)

    def circle_coeffs():
        p0 = solver(0.0).pair(np.array([3.119452 - 2.746676j, -3.119452 - 2.746676j]))
        cur = p0
        oms, rhos = [], []
        for q2c_ in np.linspace(0.0, 4.5, 24):
            new = solver(q2c_).pair(cur)
            if abs(new[0] - cur[0]) + abs(new[1] - cur[1]) > abs(new[1] - cur[0]) + abs(new[0] - cur[1]):
                new = new[::-1]
            cur = new
        for th in theta:
            q2c_ = 4.5 * np.exp(1j * th)
            new = solver(q2c_).pair(cur)
            if abs(new[0] - cur[0]) + abs(new[1] - cur[1]) > abs(new[1] - cur[0]) + abs(new[0] - cur[1]):
                new = new[::-1]
            cur = new
            m_, r_ = pair_invariants(new)
            oms.append(new[0]); rhos.append(r_)
        oms, rhos = np.array(oms), np.array(rhos)
        c_om = np.array([np.mean(oms * np.exp(-1j * n * theta)) / 4.5 ** n for n in range(13)])
        c_rho = np.array([np.mean(rhos * np.exp(-1j * n * theta)) / 4.5 ** n for n in range(13)])
        return c_om, c_rho

    c_om, c_rho = circle_coeffs()
    pred_rho = sum(c_rho[n] * q2t ** n for n in range(13))
    pred_om = sum(c_om[n] * q2t ** n for n in range(13))
    # the labelled series predicts omega_+ = mu + sqrt(rho); past the EP the true
    # "omega_+" of the analytic continuation is the root with the larger imaginary part
    true_om = best[1] if best[1].imag > best[2].imag else best[2]
    err_rho = abs(pred_rho - rho_t) / abs(rho_t)
    err_om = abs(pred_om - true_om) / abs(true_om)
    OUT["P33_3"] = {"q2_used": float(best[0]), "true_rho": [rho_t.real, rho_t.imag],
                    "true_omega_plus": [true_om.real, true_om.imag],
                    "series_rho": [pred_rho.real, pred_rho.imag], "series_omega": [pred_om.real, pred_om.imag],
                    "rel_err_rho": float(err_rho), "rel_err_omega": float(err_om)}
    print(f"\nP33.3 at q^2 = {best[0]:.4f} (target {q2t:.4f}; between R_omega = {R_om:.2f} and R_rho = {R_rho:.2f}):", flush=True)
    print(f"   true rho     = {rho_t.real:+.7f}, order-12 series = {pred_rho.real:+.7f}  ->  relative error {err_rho:.2%}", flush=True)
    print(f"   true omega_+ = {true_om.imag:+.7f}i, order-12 series = {pred_om:+.7f}  ->  relative error {err_om:.2%}", flush=True)
else:
    print(f"\nP33.3: test point q^2 = {q2t:.4f} not reached (best {best[0]:.4f})", flush=True)
pathlib.Path("results/p33c_beyond_ep.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
