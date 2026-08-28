"""Fits and figures for the preregistered exceptional-point validation.

The measured error decomposes into the two components the theory itself
predicted: a d-independent regular term (turn 110's kappa e^{-2Ng}) and the
critical term of turn 112 that grows as 1/sqrt(d) and saturates at the
exceptional point.  The fits below quantify each frozen prediction:

  P1  free-exponent fit of the growing part -> gamma ~ 1/2
  P2  decay rate at the EP = half the critical-channel geometric rate
  P3  levels needed grow logarithmically approaching the EP
  P4  extra levels per decade = ln10 / (2 alpha)
"""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
FIGURES = RESULTS / "figures"

INK = "#1f2430"
MUTED = "#6b7280"
GRID = "#e5e7eb"
ACCENT = "#4f46e5"
WARM = "#d97706"
TEAL = "#0891b2"

plt.rcParams.update(
    {
        "figure.dpi": 150,
        "font.size": 11,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "axes.titlecolor": INK,
        "axes.titlesize": 11,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "savefig.bbox": "tight",
        "savefig.facecolor": "white",
        "axes.facecolor": "white",
    }
)


def line_fit(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    predicted = slope * x + intercept
    residual = y - predicted
    total = np.sum((y - y.mean()) ** 2)
    r_squared = 1.0 - np.sum(residual**2) / total if total > 0 else np.nan
    dof = max(len(x) - 2, 1)
    slope_error = float(
        np.sqrt(np.sum(residual**2) / dof / np.sum((x - x.mean()) ** 2))
    )
    return float(slope), float(intercept), slope_error, float(r_squared)


def main() -> None:
    data = json.loads((RESULTS / "validation.json").read_text())
    distances = sorted(data["distances"], reverse=True)
    levels = data["levels"]
    FIGURES.mkdir(exist_ok=True)

    def err(entry, distance):
        return entry["errors"][f"{distance:.6e}"]

    def pair_of(encoded):
        return np.array([complex(re, im) for re, im in encoded])

    omega_c = complex(*data["ep_exact"]["omega"])

    # Slope a of the exact rho(d) = a d near the EP.
    exact_rho = []
    for distance in distances:
        pair = pair_of(data["exact_pairs"][f"{distance:.6e}"])
        exact_rho.append(((pair[0] - pair[1]) / 2.0) ** 2)
    a_slope, _, _, _ = line_fit(distances, [rho.real for rho in exact_rho])

    orders = np.array([entry["N"] for entry in levels])
    geometry = np.array([entry["geometry_error"] for entry in levels])
    ep_shift = np.array(
        [abs(entry["ep_q2"] - data["ep_exact"]["q2"]) for entry in levels]
    )
    eps_ep = np.array([err(entry, 0.0) for entry in levels])
    delta_rho = np.array(
        [
            abs((((p := pair_of(entry["pairs"][f"{0.0:.6e}"]))[0] - p[1]) / 2.0) ** 2)
            for entry in levels
        ]
    )
    delta_mu = np.array(
        [
            abs(np.mean(pair_of(entry["pairs"][f"{0.0:.6e}"])) - omega_c)
            for entry in levels
        ]
    )

    asymptotic = orders >= 4

    alpha_geom, _, alpha_geom_err, r2_geom = line_fit(
        orders[asymptotic], np.log(geometry[asymptotic])
    )
    alpha_geom = -alpha_geom
    alpha_shift, _, alpha_shift_err, r2_shift = line_fit(
        orders[asymptotic], np.log(ep_shift[asymptotic])
    )
    alpha_shift = -alpha_shift
    alpha_rho, _, alpha_rho_err, r2_rho = line_fit(
        orders[asymptotic], np.log(delta_rho[asymptotic])
    )
    alpha_rho = -alpha_rho
    alpha_ep, _, alpha_ep_err, r2_ep = line_fit(
        orders[asymptotic], np.log(eps_ep[asymptotic])
    )
    alpha_ep = -alpha_ep
    plateau_values = np.array([err(entry, 1e-1) for entry in levels])
    alpha_plateau, _, alpha_plateau_err, r2_plateau = line_fit(
        orders[asymptotic], np.log(plateau_values[asymptotic])
    )
    alpha_plateau = -alpha_plateau

    ratio = 2.0 * alpha_ep / alpha_rho
    ratio_err = ratio * np.sqrt(
        (alpha_ep_err / alpha_ep) ** 2 + (alpha_rho_err / alpha_rho) ** 2
    )

    # Point-by-point sqrt structure: eps(0) vs sqrt(delta_rho).
    sqrt_check = eps_ep[asymptotic] / np.sqrt(delta_rho[asymptotic])

    # ----- channel decomposition straight from the measured pairs --------
    # omega_pm = mu +- sqrt(rho): the regular channel is |mu_N - mu_E| and
    # the critical channel |sqrt(rho_N) - sqrt(rho_E)|; the total pair
    # error is their coherent (phase-dependent) combination, which is why a
    # power-law fit on the total alone inflates the exponent.
    exact_mu = {}
    exact_sqrt_rho = {}
    for distance in distances + [0.0]:
        pair = pair_of(data["exact_pairs"][f"{distance:.6e}"])
        exact_mu[distance] = complex(np.mean(pair))
        exact_sqrt_rho[distance] = (pair[0] - pair[1]) / 2.0

    regular_channel = {}
    critical_channel = {}
    for entry in levels:
        regular_row = {}
        critical_row = {}
        for distance in distances + [0.0]:
            pair = pair_of(entry["pairs"][f"{distance:.6e}"])
            mu = complex(np.mean(pair))
            half_split = (pair[0] - pair[1]) / 2.0
            # Pick the sign that matches the exact half-split branch.
            if abs(half_split - exact_sqrt_rho[distance]) > abs(
                -half_split - exact_sqrt_rho[distance]
            ):
                half_split = -half_split
            regular_row[distance] = abs(mu - exact_mu[distance])
            critical_row[distance] = abs(half_split - exact_sqrt_rho[distance])
        regular_channel[entry["N"]] = regular_row
        critical_channel[entry["N"]] = critical_row

    # P1: free exponent on the pure critical channel, fitted in the window
    # between the large-d slope-mismatch branch (delta_a * d dominates above
    # d ~ 1e-2, giving the V shape) and the saturation at the EP.
    scaling_window = distances[3:]  # 3.16e-3 .. 1e-4
    per_level_fits = []
    for entry in levels:
        if entry["N"] < 5:
            continue
        eps = np.array(
            [critical_channel[entry["N"]][distance] for distance in scaling_window]
        )
        slope, intercept, slope_err, r2 = line_fit(
            np.log(scaling_window), np.log(eps)
        )
        per_level_fits.append(
            {
                "N": entry["N"],
                "gamma": -slope,
                "gamma_err": slope_err,
                "r2": r2,
                "critical_coefficient": float(np.exp(intercept)),
                "plateau": float(
                    np.mean(
                        [regular_channel[entry["N"]][d] for d in distances[:3]]
                    )
                ),
            }
        )
    gammas = np.array([item["gamma"] for item in per_level_fits])
    gamma_mean = float(np.mean(gammas))
    gamma_std = float(np.std(gammas))

    critical_orders = np.array([item["N"] for item in per_level_fits])
    critical_coefficients = np.array(
        [item["critical_coefficient"] for item in per_level_fits]
    )
    alpha_b, _, alpha_b_err, r2_b = line_fit(
        critical_orders, np.log(critical_coefficients)
    )
    alpha_b = -alpha_b

    # ----- P3: complexity staircases -------------------------------------
    staircases = {}
    for target in (3e-3, 1e-4, 5e-5):
        staircase = {}
        critical_staircase = {}
        for distance in distances + [0.0]:
            needed = None
            needed_critical = None
            for entry in levels:
                if needed is None and err(entry, distance) < target:
                    needed = entry["N"]
                if (
                    needed_critical is None
                    and critical_channel[entry["N"]][distance] < target
                ):
                    needed_critical = entry["N"]
            staircase[f"{distance:.6e}"] = needed
            critical_staircase[f"{distance:.6e}"] = needed_critical
        staircases[f"{target:g}"] = {
            "total": staircase,
            "critical": critical_staircase,
        }
    predicted_decade = np.log(10.0) / (2.0 * alpha_rho)

    fits = {
        "a_slope_rho": a_slope,
        "alpha_geometry": alpha_geom,
        "alpha_geometry_err": alpha_geom_err,
        "r2_geometry": r2_geom,
        "alpha_ep_shift": alpha_shift,
        "alpha_ep_shift_err": alpha_shift_err,
        "r2_ep_shift": r2_shift,
        "alpha_rho": alpha_rho,
        "alpha_rho_err": alpha_rho_err,
        "r2_rho": r2_rho,
        "alpha_at_ep": alpha_ep,
        "alpha_at_ep_err": alpha_ep_err,
        "r2_at_ep": r2_ep,
        "alpha_plateau": alpha_plateau,
        "alpha_plateau_err": alpha_plateau_err,
        "alpha_critical_coefficient": alpha_b,
        "alpha_critical_coefficient_err": alpha_b_err,
        "ratio_2alphaEP_over_alphaRho": ratio,
        "ratio_err": ratio_err,
        "sqrt_check_eps0_over_sqrt_drho": {
            "mean": float(np.mean(sqrt_check)),
            "std": float(np.std(sqrt_check)),
            "values": {
                int(n): float(v)
                for n, v in zip(orders[asymptotic], sqrt_check)
            },
        },
        "per_level_fits": per_level_fits,
        "gamma_mean": gamma_mean,
        "gamma_std": gamma_std,
        "staircases": staircases,
        "p4_predicted_per_decade_from_alpha_rho": predicted_decade,
        "p4_frozen_prediction": 1.47,
        "delta_mu_at_ep": {
            int(entry["N"]): float(value)
            for entry, value in zip(levels, delta_mu)
        },
    }
    (RESULTS / "fits.json").write_text(json.dumps(fits, indent=2))

    for key in (
        "alpha_geometry",
        "alpha_rho",
        "alpha_at_ep",
        "alpha_ep_shift",
        "alpha_plateau",
        "ratio_2alphaEP_over_alphaRho",
        "gamma_mean",
        "gamma_std",
        "p4_predicted_per_decade_from_alpha_rho",
    ):
        print(f"{key}: {fits[key]:.4f}")
    print("sqrt check eps0/sqrt(drho):", fits["sqrt_check_eps0_over_sqrt_drho"]["mean"], "+/-", fits["sqrt_check_eps0_over_sqrt_drho"]["std"])
    print("staircases:", json.dumps(staircases))

    # ================= figures ==========================================
    mask = asymptotic

    # Fig 1: three channels, three rates.
    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    ax.semilogy(orders, geometry, "o-", color=ACCENT, lw=1.5, ms=5,
                label=f"métrica $\\|b_N-b\\|_\\infty$  ($\\alpha={alpha_geom:.2f}$)")
    ax.semilogy(orders, delta_rho, "D-", color=WARM, lw=1.5, ms=5,
                label=f"canal crítico $\\delta\\rho_N$  ($\\alpha={alpha_rho:.2f}$)")
    ax.semilogy(orders[ep_shift > 0], ep_shift[ep_shift > 0], "s--", color=TEAL, lw=1.3, ms=5,
                label=f"deslocamento do EP  ($\\alpha={alpha_shift:.2f}$)")
    ax.set_xlabel("N  (coeficientes near-horizon)")
    ax.set_ylabel("magnitude")
    ax.set_title("Cada canal converge exponencialmente, com taxa própria")
    ax.legend(fontsize=9)
    fig.savefig(FIGURES / "fig1_channels.png")
    plt.close(fig)

    # Fig 2: rate halving at the EP.
    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    ax.semilogy(orders, plateau_values, "o-", color=ACCENT, lw=1.5, ms=5,
                label=f"longe do EP ($d=10^{{-1}}$):  $\\alpha={alpha_plateau:.2f}$")
    ax.semilogy(orders, eps_ep, "D-", color=WARM, lw=1.8, ms=6,
                label=f"no EP ($d=0$):  $\\alpha_{{EP}}={alpha_ep:.2f}$")
    ax.semilogy(orders, np.sqrt(delta_rho), "s:", color=TEAL, lw=1.2, ms=4,
                label="$\\sqrt{\\delta\\rho_N}$ (estrutura prevista)")
    ax.set_xlabel("N")
    ax.set_ylabel("$\\epsilon_\\omega$")
    ax.set_title(
        f"P2: taxa cai pela metade no EP — $2\\alpha_{{EP}}/\\alpha_\\rho = {ratio:.2f}\\pm{ratio_err:.2f}$ (previsto 1)"
    )
    ax.legend(fontsize=9)
    fig.savefig(FIGURES / "fig2_rate_halving.png")
    plt.close(fig)

    # Fig 3: the two channels of the error at fixed N.
    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    picks = [item for item in per_level_fits if item["N"] in (5, 9, 12, 15)]
    shades = plt.cm.Blues(np.linspace(0.45, 0.9, len(picks)))
    for color, item in zip(shades, picks):
        critical = [critical_channel[item["N"]][d] for d in distances]
        regular = [regular_channel[item["N"]][d] for d in distances]
        ax.loglog(distances, critical, "o-", color=color, lw=1.2, ms=5,
                  label=f"N={item['N']} crítico ($\\gamma={item['gamma']:.2f}$)")
        ax.loglog(distances, regular, "s:", color=color, lw=0.9, ms=3, alpha=0.6)
    guide_x = np.array([1e-4, 1e-1])
    ax.loglog(guide_x, 2e-5 * guide_x**-0.5, "--", color=WARM, lw=1.7,
              label="inclinação $-1/2$ prevista")
    ax.set_xlabel("$d=|q^2-q^2_c|$")
    ax.set_ylabel("erro por canal")
    ax.set_title(
        f"P1: canal crítico cresce como $d^{{-1/2}}$ ($\\gamma={gamma_mean:.2f}\\pm{gamma_std:.2f}$); "
        "canal regular (quadrados) fica plano"
    )
    ax.legend(fontsize=8)
    fig.savefig(FIGURES / "fig3_distance.png")
    plt.close(fig)

    # Fig 4: parameter-free universal collapse of the critical channel.
    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    shades = plt.cm.Blues(np.linspace(0.35, 0.95, len(per_level_fits)))
    for color, item in zip(shades, per_level_fits):
        index = list(orders).index(item["N"])
        rho_n = delta_rho[index]
        for distance in distances + [0.0]:
            eps = critical_channel[item["N"]][distance]
            u = a_slope * distance / rho_n
            ax.loglog(max(u, 3e-2), eps / np.sqrt(rho_n), "o", color=color, ms=4)
        ax.loglog([], [], "o", color=color, label=f"N={item['N']}")
    u_grid = np.logspace(-1.6, 4, 200)
    ax.loglog(
        u_grid,
        np.sqrt(u_grid + 1) - np.sqrt(u_grid),
        "-",
        color=WARM,
        lw=1.8,
        label="$\\sqrt{u+1}-\\sqrt{u}$ (sem parâmetros livres)",
    )
    ax.set_xlabel("$u = a\\,d/\\delta\\rho_N$")
    ax.set_ylabel("$|\\sqrt{\\rho_N}-\\sqrt{\\rho}|/\\sqrt{\\delta\\rho_N}$")
    ax.set_title("Colapso universal do canal crítico na curva prevista")
    ax.legend(fontsize=8, ncol=2, loc="lower left")
    fig.savefig(FIGURES / "fig4_collapse.png")
    plt.close(fig)

    # Fig 5: continuous complexity from per-distance regressions of the
    # critical channel.  For each d, fit ln eps_crit(N) over the admissible
    # levels and read off the (interpolated) N* where the target is met;
    # the growth of N* per decade is then a measurement with real scatter.
    target_star = 1e-5
    fit_orders = orders[orders >= 5]
    star_points = []
    for distance in distances[2:]:  # inside the critical-scaling regime
        eps = np.array(
            [
                critical_channel[int(n)][distance]
                for n in fit_orders
            ]
        )
        slope, intercept, slope_err, r2 = line_fit(fit_orders, np.log(eps))
        n_star = (np.log(target_star) - intercept) / slope
        star_points.append((np.log10(1.0 / distance), float(n_star), r2))
    xs = [p[0] for p in star_points]
    ys = [p[1] for p in star_points]
    p3_slope, p3_intercept, p3_slope_err, p3_r2 = line_fit(xs, ys)

    fits["p3_nstar_target"] = target_star
    fits["p3_nstar_points"] = [
        {"decades": x, "n_star": y, "r2": r2} for x, y, r2 in star_points
    ]
    fits["p3_measured_per_decade"] = p3_slope
    fits["p3_measured_per_decade_err"] = p3_slope_err
    fits["p3_r2"] = p3_r2
    (RESULTS / "fits.json").write_text(json.dumps(fits, indent=2))
    print(
        f"p3 measured per decade: {p3_slope:.3f} +/- {p3_slope_err:.3f} "
        f"(predicted {predicted_decade:.2f})"
    )

    fig, ax = plt.subplots(figsize=(6.6, 4.3))
    ax.plot(xs, ys, "o", color=ACCENT, ms=7, label="$N_*$ medido (canal crítico, $\\epsilon=10^{-5}$)")
    xs_line = np.linspace(min(xs) - 0.2, max(xs) + 0.4, 10)
    ax.plot(
        xs_line,
        p3_intercept + p3_slope * xs_line,
        "-",
        color=ACCENT,
        lw=1.4,
        label=f"ajuste: +{p3_slope:.2f} níveis/década",
    )
    ax.plot(
        xs_line,
        (p3_intercept + p3_slope * xs[0] - predicted_decade * xs[0])
        + predicted_decade * xs_line,
        "--",
        color=WARM,
        lw=1.5,
        label=f"previsto $\\ln 10/(2\\alpha_\\rho)$ = {predicted_decade:.2f}",
    )
    ax.set_xlabel("décadas de aproximação  $\\log_{10}(1/d)$")
    ax.set_ylabel("níveis necessários  $N_*$")
    ax.set_title(
        f"P3/P4: +{p3_slope:.2f}$\\pm${p3_slope_err:.2f} níveis/década "
        f"(previsto {predicted_decade:.2f})"
    )
    ax.legend(fontsize=9)
    fig.savefig(FIGURES / "fig5_complexity.png")
    plt.close(fig)

    print(f"figures written to {FIGURES}")


if __name__ == "__main__":
    main()
