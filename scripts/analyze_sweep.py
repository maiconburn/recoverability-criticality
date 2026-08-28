"""P1 + P4 verdicts: measured sweep rates vs the two frozen prediction curves."""

import json
from pathlib import Path

import numpy as np

RESULTS = Path(__file__).resolve().parent.parent / "results"


def line_fit(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    slope, intercept = np.polyfit(x, y, 1)
    resid = y - (slope * x + intercept)
    r2 = 1.0 - resid.var() / y.var() if y.var() > 0 else np.nan
    dof = max(len(x) - 2, 1)
    se = float(np.sqrt(resid @ resid / dof / ((x - x.mean()) ** 2).sum()))
    return float(slope), float(intercept), se, float(r2)


def main():
    sweep = json.loads((RESULTS / "sweep.json").read_text())
    preds = json.loads((RESULTS / "sweep_predictions.json").read_text())
    p4 = json.loads((RESULTS / "p4_predictions.json").read_text())
    validation = json.loads((RESULTS / "fits.json").read_text())

    pred_by_lambda = {round(r["coupling"], 4): r for r in preds["predictions"]}
    p4_by_lambda = {round(r["coupling"], 4): r for r in p4["rows"]}

    measured = []
    for entry in sweep["couplings"]:
        if "fits" not in entry:
            continue
        measured.append(
            dict(
                coupling=entry["coupling"],
                alpha_rho=entry["fits"]["alpha_rho"],
                alpha_rho_se=entry["fits"]["alpha_rho_se"],
                dn=entry["fits"]["dn_per_decade"],
                dn_se=entry["fits"]["dn_per_decade_se"],
                split=entry["fits"]["splitting_rho_over_sup"],
                halving=entry["fits"]["ratio_2aep_over_arho"],
                ep_q2=entry["ep"]["q2"],
                ep_omega=entry["ep"]["omega"],
            )
        )
    # add the anchor from the original validated run
    measured.append(
        dict(
            coupling=0.08,
            alpha_rho=validation["alpha_rho"],
            alpha_rho_se=validation["alpha_rho_err"],
            dn=validation["p3_measured_per_decade"],
            dn_se=validation["p3_measured_per_decade_err"],
            split=validation["alpha_rho"] / validation["alpha_geometry"],
            halving=validation["ratio_2alphaEP_over_alphaRho"],
            ep_q2=-16.147205102,
            ep_omega=[0.0, -5.6738278],
        )
    )
    measured.sort(key=lambda r: r["coupling"])

    print("lambda   alpha_meas    dN/dec_meas  dN_pred(B)  alpha_B  alpha_CMI  halving  split")
    rows = []
    for r in measured:
        key = round(r["coupling"], 4)
        pred = pred_by_lambda[key]
        p4row = p4_by_lambda[key]
        rows.append((r, pred, p4row))
        print(
            f"{r['coupling']:+.3f}  {r['alpha_rho']:.3f}±{r['alpha_rho_se']:.3f}  "
            f"{r['dn']:.3f}±{r['dn_se']:.3f}   {pred['dn_per_decade_pred']:.3f}     "
            f"{p4row['alpha_metric_pred']:.3f}    {p4row['alpha_cmi_pred']:.3f}     "
            f"{r['halving']:.3f}    {r['split']:.2f}"
        )

    # K1: measured dN/decade vs frozen prediction (regression through data)
    x = [p["dn_per_decade_pred"] for _, p, _ in rows]
    y = [r["dn"] for r, _, _ in rows]
    slope, intercept, se, r2 = line_fit(x, y)
    print(f"\nK1 regression dN_meas vs dN_pred: slope={slope:.3f}±{se:.3f} "
          f"intercept={intercept:.3f} R2={r2:.4f}  (gate: R2>=0.9)")

    # alpha-level regression too
    xa = [p["alpha_rho_pred"] for _, p, _ in rows]
    ya = [r["alpha_rho"] for r, _, _ in rows]
    sa, ia, sea, r2a = line_fit(xa, ya)
    print(f"K1 regression alpha_meas vs alpha_pred: slope={sa:.3f}±{sea:.3f} "
          f"intercept={ia:.3f} R2={r2a:.4f}")

    # K2: splitting persistence
    splits = [r["split"] for r, _, _ in rows]
    print(f"K2 channel splitting alpha_rho/alpha_sup: {['%.2f' % s for s in splits]} "
          f"(gate: stays > 1; mean={np.mean(splits):.2f})")

    # Universality of EP halving
    halvings = [r["halving"] for r, _, _ in rows]
    print(f"EP halving 2*alpha_EP/alpha_rho: {['%.2f' % h for h in halvings]} "
          f"(prediction: 1.00 at every coupling)")

    # P4 arbitration at the split point lambda=0.02
    r02 = next(r for r, _, _ in rows if abs(r["coupling"] - 0.02) < 1e-9)
    p02b = p4_by_lambda[0.02]["alpha_metric_pred"]
    p02c = p4_by_lambda[0.02]["alpha_cmi_pred"]
    zb = (r02["alpha_rho"] - p02b) / r02["alpha_rho_se"]
    zc = (r02["alpha_rho"] - p02c) / r02["alpha_rho_se"]
    print(f"\nP4 arbitration at lambda=0.02: measured {r02['alpha_rho']:.3f}±"
          f"{r02['alpha_rho_se']:.3f} -> z(metric)={zb:+.1f}, z(CMI)={zc:+.1f}")

    # EP trajectory (novel spectroscopic data)
    print("\nEP trajectory q2_c(lambda), omega_c(lambda):")
    for r, _, _ in rows:
        print(f"  lambda={r['coupling']:+.3f}: q2_c={r['ep_q2']:.4f} "
              f"omega_c={r['ep_omega'][0]:+.4f}{r['ep_omega'][1]:+.4f}i")

    out = dict(
        table=[dict(coupling=r["coupling"], alpha_meas=r["alpha_rho"],
                    alpha_se=r["alpha_rho_se"], dn_meas=r["dn"],
                    dn_pred=p["dn_per_decade_pred"],
                    alpha_metric_pred=q["alpha_metric_pred"],
                    alpha_cmi_pred=q["alpha_cmi_pred"],
                    halving=r["halving"], split=r["split"],
                    ep_q2=r["ep_q2"], ep_omega=r["ep_omega"])
               for r, p, q in rows],
        k1_dn=dict(slope=slope, se=se, intercept=intercept, r2=r2),
        k1_alpha=dict(slope=sa, se=sea, intercept=ia, r2=r2a),
        k2_splits=splits,
        halvings=halvings,
        p4_z_metric=float(zb), p4_z_cmi=float(zc),
        ep_extinction="no real-q2 mirror collision found down to q2=-40 "
                      "for lambda >= 0.12 (EP extinct or complex)",
    )
    (RESULTS / "sweep_fits.json").write_text(json.dumps(out, indent=1))
    print("\nwrote", RESULTS / "sweep_fits.json")


if __name__ == "__main__":
    main()
