"""Test #2 final: PT-transition sweep (101 amplitudes) from murchlab pickle.

Observable: n(t) = P_f/(P_e+P_f), init |e>, postselected non-Hermitian
ef qubit H = [[ -i*gamma, J], [J, 0]] (population-only: convention-free).
Global gamma, per-amplitude J.  Deliverables: EP location, eigenvalue-pair
bootstrap uncertainty vs distance (P_A: 1/sqrt-d amplification), initial
condition recovery uncertainty vs distance (P_B: flat), secular-form BIC at
the EP (P_A2).  Frozen predictions: FROZEN_MURCH.md.
"""

import json
import pickle
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import least_squares

HERE = Path(__file__).resolve().parent
data = pickle.load(open(HERE / "nonlinear-qubit/pf_pe_pg_july2nd.pkl", "rb"))
P_F = np.array(data["all_P_f"])[1:]
P_E = np.array(data["all_P_e"])[1:]
AMPS = np.array(data["amplitude"])[1:]
T_US = np.array(data["time_vals_ns"]) * 1e-3
_denominator = P_F + P_E
N_OBS = np.where(_denominator > 1e-6, P_F / np.where(_denominator > 1e-6, _denominator, 1.0), np.nan)
FINITE = np.isfinite(N_OBS)


def n_model(j_coupling, gamma, n0, t_values):
    h = np.array([[-1j * gamma, j_coupling], [j_coupling, 0.0]], complex)
    vals, vecs = np.linalg.eig(h)
    inv = np.linalg.inv(vecs)
    psi0 = np.array([np.sqrt(max(1.0 - n0, 0.0)), np.sqrt(max(n0, 0.0))], complex)
    c0 = inv @ psi0
    out = np.zeros(len(t_values))
    for i, t in enumerate(t_values):
        psi = vecs @ (np.exp(-1j * vals * t) * c0)
        p = np.abs(psi) ** 2
        out[i] = p[1] / (p[0] + p[1])
    return out


def fit_one(n_data, gamma=None, seed_j=0.1, n0_free=True):
    def resid(theta):
        if gamma is None:
            j, g, n0 = theta
        else:
            j, n0 = theta
            g = gamma
        if not n0_free:
            n0 = 0.0
        m = np.isfinite(n_data)
        return n_model(abs(j), abs(g), np.clip(n0, 0, 1), T_US[m]) - n_data[m]
    theta0 = [seed_j, 0.3, 0.0] if gamma is None else [seed_j, 0.0]
    sol = least_squares(resid, theta0, method="lm", max_nfev=3000)
    return sol


def main():
    # stage 1: per-amp (J, gamma) to find the gamma plateau
    gammas, js = [], []
    for k in range(len(AMPS)):
        sol = fit_one(N_OBS[k], seed_j=max(0.02, 300 * AMPS[k]))
        j, g, _ = np.abs(sol.x)
        js.append(j)
        gammas.append(g)
    js = np.array(js)
    gammas = np.array(gammas)
    strong = js > 1.5 * gammas
    gamma_star = float(np.median(gammas[~strong & (js > 0.01)])) if np.any(~strong) else float(np.median(gammas))
    gamma_star = float(np.median(gammas[(js > 0.05) & (js < 0.6)]))
    print(f"gamma plateau estimate: {gamma_star:.4f} "
          f"(spread {np.std(gammas[(js>0.05)&(js<0.6)]):.4f})")

    # stage 2: fixed gamma, per-amp J; bootstrap over time points
    rng = np.random.default_rng(20260828)
    rows = []
    for k in range(len(AMPS)):
        sol = fit_one(N_OBS[k], gamma=gamma_star, seed_j=max(js[k], 0.01))
        j = abs(sol.x[0])
        resid_sd = float(np.std(sol.fun))
        eig = np.linalg.eigvals(
            np.array([[-1j * gamma_star, j], [j, 0]], complex))
        gap = float(abs(eig[0] - eig[1]))
        j_boot, n0_boot = [], []
        n_t = len(T_US)
        for _ in range(30):
            idx = np.sort(rng.integers(0, n_t, n_t))
            def rb(theta):
                jj, nn = theta
                m = np.isfinite(N_OBS[k][idx])
                return n_model(abs(jj), gamma_star, np.clip(nn, 0, 1),
                               T_US[idx][m]) - N_OBS[k][idx][m]
            sb = least_squares(rb, [j, 0.0], method="lm", max_nfev=1200)
            j_boot.append(abs(sb.x[0]))
            n0_boot.append(sb.x[1])
        eig_boot = []
        for jb in j_boot:
            eb = np.linalg.eigvals(
                np.array([[-1j * gamma_star, jb], [jb, 0]], complex))
            eig_boot.append(np.sort_complex(eb))
        sig_eig = float(np.mean(np.std(np.array(eig_boot), axis=0)))
        sig_n0 = float(np.std(np.array(n0_boot)))
        rows.append(dict(amp=float(AMPS[k]), J=float(j), gap=gap,
                         sigma_eig=sig_eig, sigma_state=sig_n0,
                         resid_sd=resid_sd))
    out = dict(gamma=gamma_star, rows=rows)
    (HERE / "sweepJ_results.json").write_text(json.dumps(out, indent=1))
    # locate EP: J crosses gamma
    j_arr = np.array([r["J"] for r in rows])
    cross = np.where(np.diff(np.sign(j_arr - gamma_star)))[0]
    print("EP crossing near amp index:", cross[:4],
          "amps:", [f"{AMPS[c]:.5f}" for c in cross[:4]])
    for r in rows[::7]:
        print(f"amp={r['amp']:.5f} J={r['J']:.4f} gap={r['gap']:.4f} "
              f"sig_eig={r['sigma_eig']:.5f} sig_state={r['sigma_state']:.5f}")


if __name__ == "__main__":
    main()
