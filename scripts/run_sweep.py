"""P1 — coupling sweep with a-priori frozen rate predictions.

For each lambda in the frozen ladder: locate the mirror-pair EP, run the
distance/N ladder with the shooting solver (same protocol as the validated
lambda=0.08 run), and extract alpha_rho (critical channel), alpha_sup
(geometry), alpha_EP, and the measured levels-per-decade.  Results saved
incrementally; predictions were frozen beforehand in sweep_predictions.json.
"""

import json
import time
from pathlib import Path

import numpy as np

import run_validation as rv
from recoverability_ep.criticality import SpectralFamily, mirror_seed, track_pair
from recoverability_ep.model import (
    build_constrained_pade,
    exact_gb_metric,
    exact_horizon_coefficients,
)
from recoverability_ep.shooting import pade_horizon_coefficients, pair_invariants

RESULTS = Path(__file__).resolve().parent.parent / "results"
OUT = RESULTS / "sweep.json"
LADDER = [-0.10, -0.05, 0.02, 0.05, 0.12, 0.16, 0.20]  # anchor 0.08 already done
N_LEVELS = range(2, 16)


def line_fit(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    slope, intercept = np.polyfit(x, y, 1)
    resid = y - (slope * x + intercept)
    r2 = 1.0 - resid.var() / y.var() if y.var() > 0 else np.nan
    dof = max(len(x) - 2, 1)
    se = float(np.sqrt(resid @ resid / dof / ((x - x.mean()) ** 2).sum()))
    return float(slope), float(intercept), se, float(r2)


def analyze_lambda(coupling, q2_ep, exact_pairs, levels):
    distances = sorted(rv.DISTANCES, reverse=True)
    orders = np.array([e["N"] for e in levels])

    def pair_of(encoded):
        return np.array([complex(re, im) for re, im in encoded])

    exact_sq = {}
    for d in distances + [0.0]:
        pair = pair_of(exact_pairs[f"{d:.6e}"])
        exact_sq[d] = (pair[0] - pair[1]) / 2.0
    geometry = np.array([e["geometry_error"] for e in levels])
    delta_rho = np.array(
        [
            abs((((p := pair_of(e["pairs"][f"{0.0:.6e}"]))[0] - p[1]) / 2.0) ** 2)
            for e in levels
        ]
    )
    eps_ep = np.array([e["errors"][f"{0.0:.6e}"] for e in levels])
    mask = orders >= 4
    a_sup, _, a_sup_se, r2_sup = line_fit(orders[mask], np.log(geometry[mask]))
    a_rho, _, a_rho_se, r2_rho = line_fit(orders[mask], np.log(delta_rho[mask]))
    a_ep, _, a_ep_se, r2_ep = line_fit(orders[mask], np.log(eps_ep[mask]))

    # critical channel per (N, d) and levels-per-decade via per-d regressions
    critical = {}
    for e in levels:
        row = {}
        for d in distances + [0.0]:
            pair = pair_of(e["pairs"][f"{d:.6e}"])
            half = (pair[0] - pair[1]) / 2.0
            ref = exact_sq[d]
            if abs(half - ref) > abs(-half - ref):
                half = -half
            row[d] = abs(half - ref)
        critical[e["N"]] = row
    fit_orders = orders[orders >= 5]
    star = []
    for d in distances[2:]:
        eps = np.array([critical[int(n)][d] for n in fit_orders])
        s, i, _, _ = line_fit(fit_orders, np.log(eps))
        star.append((np.log10(1.0 / d), (np.log(1e-5) - i) / s))
    slope, _, slope_se, r2_star = line_fit([p[0] for p in star], [p[1] for p in star])

    return dict(
        alpha_sup=-a_sup, alpha_sup_se=a_sup_se, r2_sup=r2_sup,
        alpha_rho=-a_rho, alpha_rho_se=a_rho_se, r2_rho=r2_rho,
        alpha_ep=-a_ep, alpha_ep_se=a_ep_se, r2_ep=r2_ep,
        dn_per_decade=slope, dn_per_decade_se=slope_se, r2_dn=r2_star,
        ratio_2aep_over_arho=2.0 * a_ep / a_rho if a_rho else np.nan,
        splitting_rho_over_sup=a_rho / a_sup if a_sup else np.nan,
    )


def run_lambda(coupling):
    started = time.time()
    b_exact, bp_exact, n_factor = exact_gb_metric(coupling)
    geometry = (b_exact, bp_exact, exact_horizon_coefficients(coupling, 24))
    grid = np.linspace(0.0, 1.0, 4001)

    def locate(b, bp, geom):
        for start in (rv.WALK_START, -8.0, -5.0, -3.0, -20.0):
            family = SpectralFamily(b, bp, n_factor, collocation_order=56)
            walk = track_pair(family, [0.0, start], seed=mirror_seed(family))
            try:
                return rv.find_ep_global(geom, n_factor, walk, q2_start=start)
            except RuntimeError:
                continue
        raise RuntimeError(f"no EP found for lambda={coupling}")

    q2_ep, omega_ep, gap, near_pair = locate(b_exact, bp_exact, geometry)
    exact_pairs = rv.ladder(geometry, n_factor, q2_ep, near_pair)
    levels = []
    for order in N_LEVELS:
        pade = build_constrained_pade(exact_horizon_coefficients(coupling, order))
        if not pade.is_admissible():
            continue
        geom_n = (pade.b, pade.bp, pade_horizon_coefficients(pade, 24))
        pairs_n = rv.ladder(
            geom_n, n_factor, q2_ep, None, per_distance_seeds=exact_pairs
        )
        levels.append(
            dict(
                N=order,
                geometry_error=float(np.max(np.abs(pade.b(grid) - b_exact(grid)))),
                pairs={
                    f"{d:.6e}": [rv.complex_pair(p) for p in pairs_n[d]]
                    for d in rv.DISTANCES + [0.0]
                },
                errors={
                    f"{d:.6e}": rv.pair_error(pairs_n[d], exact_pairs[d])
                    for d in rv.DISTANCES + [0.0]
                },
            )
        )
    encoded_exact = {
        f"{d:.6e}": [rv.complex_pair(p) for p in exact_pairs[d]]
        for d in rv.DISTANCES + [0.0]
    }
    fits = analyze_lambda(coupling, q2_ep, encoded_exact, levels)
    return dict(
        coupling=coupling,
        ep=dict(q2=q2_ep, omega=rv.complex_pair(omega_ep), gap=gap),
        n_admissible=len(levels),
        fits=fits,
        exact_pairs=encoded_exact,
        levels=levels,
        runtime_s=time.time() - started,
    )


def main():
    data = {"couplings": []}
    if OUT.exists():
        data = json.loads(OUT.read_text())
    done = {round(c["coupling"], 4) for c in data["couplings"]}
    for coupling in LADDER:
        if round(coupling, 4) in done:
            continue
        try:
            entry = run_lambda(coupling)
        except Exception as error:  # keep sweeping; report failures
            entry = dict(coupling=coupling, error=str(error))
        data["couplings"].append(entry)
        OUT.write_text(json.dumps(data, indent=1))
        fits = entry.get("fits", {})
        print(
            f"lambda={coupling:+.3f} "
            + (
                f"alpha_rho={fits['alpha_rho']:.3f}±{fits['alpha_rho_se']:.3f} "
                f"dN/dec={fits['dn_per_decade']:.3f}±{fits['dn_per_decade_se']:.3f} "
                f"split={fits['splitting_rho_over_sup']:.2f} "
                f"2aEP/arho={fits['ratio_2aep_over_arho']:.2f} "
                f"[{entry['runtime_s']:.0f}s]"
                if "fits" in entry
                else f"FAILED: {entry.get('error')}"
            )
        )
    print("wrote", OUT)


if __name__ == "__main__":
    main()
