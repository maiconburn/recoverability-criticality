"""P33.4: the cost ladder in the holographic instrument.

Inject relative noise eta into the Wronskian and measure the error in the
labelled roots omega_+- against the error in the invariants mu, rho, at a
fixed distance d from the EP. The theorem's first rung: labelled errors
scale as sqrt(eta) once eta exceeds the square of the splitting, invariant
errors scale as eta. Output: results/p33d_noise_scaling.json
"""
import json
import pathlib
import sys
from dataclasses import dataclass

import numpy as np

sys.path.insert(0, "src")
from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients  # noqa
from recoverability_ep.shooting import ShootingSolver, pair_invariants  # noqa

B, BP, NF = exact_gb_metric(0.0)
HC = exact_horizon_coefficients(0.0, 24)
Q2C = -5.0123755


@dataclass
class NoisySolver(ShootingSolver):
    eta: float = 0.0
    seed: int = 0
    scale: float = 1.0

    def wronskian(self, omega):
        w = super().wronskian(omega)
        if self.eta == 0.0:
            return w
        # ADDITIVE noise: a multiplicative perturbation W -> W(1 + eta xi) leaves
        # the zeros of W exactly where they were (first version of this script did
        # that and measured a flat 1e-13 error at every eta).
        rng = np.random.default_rng((self.seed, int(np.real(omega) * 1e8) % 2**31, int(np.imag(omega) * 1e8) % 2**31))
        return w + self.eta * self.scale * (rng.normal() + 1j * rng.normal())


def clean_pair(q2):
    s = ShootingSolver(B, BP, NF, complex(q2), horizon_coefficients=HC)
    cur = np.array([3.119452 - 2.746676j, -3.119452 - 2.746676j])
    for x in np.linspace(0.0, q2, 40)[1:]:
        new = s.__class__(B, BP, NF, complex(x), horizon_coefficients=HC).pair(cur)
        if abs(new[0] - cur[0]) + abs(new[1] - cur[1]) > abs(new[1] - cur[0]) + abs(new[0] - cur[1]):
            new = new[::-1]
        cur = new
    return cur


OUT = {}
# distances chosen so that the noise-induced error crosses the half-splitting inside the
# eta range: splitting = sqrt(3.205 d), and the linear-regime error is about 20 eta.
for d in (1e-6, 1e-4, 0.05):
    q2 = Q2C + d
    ref = clean_pair(q2)
    mu_r, rho_r = pair_invariants(ref)
    split = abs(ref[0] - ref[1]) / 2
    base = ShootingSolver(B, BP, NF, complex(q2), horizon_coefficients=HC)
    scale = float(np.mean([abs(base.wronskian(complex(mu_r) + off)) for off in (1.0, -1.0, 1.5j, -1.5j)]))
    print(f"\nd = {d} (q^2 = {q2:.5f}): reference pair {ref[0]:.8f} / {ref[1]:.8f}, half-splitting {split:.6f}, |W| scale {scale:.3e}", flush=True)
    rows = []
    for eta in (1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2):
        errs_om, errs_mu, errs_rho = [], [], []
        for sd in range(12):
            ns = NoisySolver(B, BP, NF, complex(q2), horizon_coefficients=HC, eta=eta, seed=sd + 1, scale=scale)
            try:
                p = ns.pair(ref)
            except Exception:
                continue
            if abs(p[0] - ref[0]) + abs(p[1] - ref[1]) > abs(p[1] - ref[0]) + abs(p[0] - ref[1]):
                p = p[::-1]
            mu, rho = pair_invariants(p)
            errs_om.append(max(abs(p[0] - ref[0]), abs(p[1] - ref[1])))
            errs_mu.append(abs(mu - mu_r))
            errs_rho.append(abs(rho - rho_r))
        if not errs_om:
            continue
        row = dict(eta=eta, err_omega=float(np.median(errs_om)), err_mu=float(np.median(errs_mu)), err_rho=float(np.median(errs_rho)), n=len(errs_om))
        rows.append(row)
        print(f"  eta = {eta:.0e}: |d omega| = {row['err_omega']:.3e}, |d mu| = {row['err_mu']:.3e}, |d rho| = {row['err_rho']:.3e}", flush=True)
    if len(rows) >= 3:
        x = np.log([r["eta"] for r in rows])
        sl = {k: float(np.polyfit(x, np.log([max(r[k], 1e-300) for r in rows]), 1)[0]) for k in ("err_omega", "err_mu", "err_rho")}
        # split the fit at the crossover: rows whose omega error exceeds the half-splitting
        hi = [r for r in rows if r["err_omega"] > split]
        lo = [r for r in rows if r["err_omega"] <= split]
        for tag, sub in (("below crossover (err < splitting)", lo), ("above crossover (err > splitting)", hi)):
            if len(sub) >= 3:
                xx = np.log([r["eta"] for r in sub])
                ss = {k: float(np.polyfit(xx, np.log([max(r[k], 1e-300) for r in sub]), 1)[0]) for k in ("err_omega", "err_mu", "err_rho")}
                sl[tag] = ss
                print(f"  {tag}: omega {ss['err_omega']:+.3f}, mu {ss['err_mu']:+.3f}, rho {ss['err_rho']:+.3f}  ({len(sub)} points)", flush=True)
        print(f"  slopes over the whole range: omega {sl['err_omega']:+.3f} (theorem 1/2 near the EP, 1 away), mu {sl['err_mu']:+.3f}, rho {sl['err_rho']:+.3f}", flush=True)
        OUT[str(d)] = {"q2": q2, "W_scale": scale, "half_splitting": float(split), "rows": rows, "slopes": sl}
pathlib.Path("results/p33d_noise_scaling.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
