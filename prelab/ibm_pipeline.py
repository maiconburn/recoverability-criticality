"""Pre-lab test #1: two tasks from the same dilated non-Hermitian qubit,
Qiskit simulator first (frozen standard-QM reference), QPU-ready.

System: H = [[-i*gamma, J], [J, 0]] (Murch-anchored gamma = 0.3072 /us),
realized per time point by Sz.-Nagy dilation on (system + ancilla) with
post-selection on ancilla |0>.

Task A (spectral): fit (J, gamma) from post-selected populations vs t;
bootstrap uncertainty of the eigenvalue pair vs distance d to the EP.
Task B (recoverability, PHYSICAL): apply the Petz recovery of the
post-selected channel as a second dilated circuit; average fidelity over
the 6 cardinal states vs d.

Standard QM: sigma_spec peaks near/below the EP; F_Petz smooth in d.
Locking ontology: both share the EP feature.  Same shot budget per point.
"""

import json
from pathlib import Path

import numpy as np
from scipy.linalg import sqrtm
from scipy.optimize import least_squares

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError

HERE = Path(__file__).resolve().parent
GAMMA = 0.3072
J_EP = GAMMA / 2.0
R_LADDER = [0.2, 0.5, 0.8, 0.95, 1.0, 1.05, 1.2, 2.0, 4.0]
T_GRID = np.linspace(0.8, 12.0, 8)
T_STAR = 4.0
SHOTS = 4096
CARDINALS = {
    "z+": [1, 0], "z-": [0, 1],
    "x+": [1 / np.sqrt(2), 1 / np.sqrt(2)], "x-": [1 / np.sqrt(2), -1 / np.sqrt(2)],
    "y+": [1 / np.sqrt(2), 1j / np.sqrt(2)], "y-": [1 / np.sqrt(2), -1j / np.sqrt(2)],
}


def contraction(j_coupling, t):
    h = np.array([[-1j * GAMMA, j_coupling], [j_coupling, 0.0]], complex)
    vals, vecs = np.linalg.eig(h)
    m = vecs @ np.diag(np.exp(-1j * vals * t)) @ np.linalg.inv(vecs)
    norm = np.linalg.norm(m, 2)
    if norm > 1.0:
        m = m / (norm * (1 + 1e-12))
    return m


def dilation_unitary(m):
    """Sz.-Nagy: U = [[M, D1],[D2, -M^dag]] with defect operators."""
    eye = np.eye(2)
    d1 = sqrtm(eye - m @ m.conj().T)
    d2 = sqrtm(eye - m.conj().T @ m)
    u = np.block([[m, d1], [d2, -m.conj().T]])
    # unitarize (numerical polish)
    w, _, vt = np.linalg.svd(u)
    return w @ vt


def petz_kraus(m):
    """Petz recovery of E(rho) = M rho M^dag (post-selected), sigma_ref = I/2."""
    s = m @ m.conj().T / 2.0
    vals, vecs = np.linalg.eigh(s)
    inv_sqrt = (vecs / np.sqrt(np.maximum(vals, 1e-14))) @ vecs.conj().T
    r = m.conj().T @ inv_sqrt / np.sqrt(2.0)
    norm = np.linalg.norm(r, 2)
    return r / (norm * (1 + 1e-12))


def apply_dilated(circuit, operator, system, ancilla):
    u = dilation_unitary(operator)
    circuit.unitary(u, [system, ancilla], label="dil")


def noise_model():
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(3e-4, 1), ["u", "unitary"])
    nm.add_all_qubit_quantum_error(depolarizing_error(3e-3, 2),
                                   ["cx", "cz", "unitary"], warnings=False)
    nm.add_all_qubit_readout_error(ReadoutError([[0.99, 0.01], [0.02, 0.98]]))
    return nm


SIM = AerSimulator(noise_model=noise_model())


def run_counts(circuit, shots=SHOTS):
    compiled = transpile(circuit, SIM, optimization_level=1)
    return SIM.run(compiled, shots=shots).result().get_counts()


def spectral_record(j_coupling):
    """Post-selected populations of |f> vs t (init |e> = |0>_system)."""
    ns, keeps = [], []
    for t in T_GRID:
        qc = QuantumCircuit(2, 2)
        apply_dilated(qc, contraction(j_coupling, t), 0, 1)
        qc.measure([0, 1], [0, 1])
        counts = run_counts(qc)
        kept = {k: v for k, v in counts.items() if k[0] == "0"}  # ancilla=0
        total = sum(kept.values())
        n_f = kept.get("01", 0)  # system=1 -> |f>
        ns.append(n_f / max(total, 1))
        keeps.append(total)
    return np.array(ns), np.array(keeps)


def n_theory(j_coupling, gamma, t_values):
    out = []
    for t in t_values:
        h = np.array([[-1j * gamma, j_coupling], [j_coupling, 0.0]], complex)
        vals, vecs = np.linalg.eig(h)
        psi = vecs @ (np.exp(-1j * vals * t) * (np.linalg.inv(vecs) @ np.array([1, 0], complex)))
        p = np.abs(psi) ** 2
        out.append(p[1] / p.sum())
    return np.array(out)


def fit_spectral(ns, weights):
    def resid(theta):
        return (n_theory(abs(theta[0]), abs(theta[1]), T_GRID) - ns) * np.sqrt(weights / weights.max())
    sol = least_squares(resid, [J_EP, GAMMA], method="lm", max_nfev=2000)
    j, g = np.abs(sol.x)
    eig = np.linalg.eigvals(np.array([[-1j * g, j], [j, 0]], complex))
    return j, g, np.sort_complex(eig)


def petz_fidelity(j_coupling):
    m = contraction(j_coupling, T_STAR)
    r = petz_kraus(m)
    fidelities = []
    for label, amp in CARDINALS.items():
        qc = QuantumCircuit(3, 3)
        qc.initialize(np.array(amp, complex), 0)
        apply_dilated(qc, m, 0, 1)
        apply_dilated(qc, r, 0, 2)
        # measure in the prep basis: undo preparation
        prep = QuantumCircuit(1)
        prep.initialize(np.array(amp, complex), 0)
        undo = Statevector.from_instruction(prep).data
        basis = np.array([[undo[0].conjugate(), undo[1].conjugate()],
                          [-undo[1], undo[0]]], complex)
        qc.unitary(basis, [0], label="undo")
        qc.measure([0, 1, 2], [0, 1, 2])
        counts = run_counts(qc)
        kept = {k: v for k, v in counts.items() if k[0] == "0" and k[1] == "0"}
        total = sum(kept.values())
        good = kept.get("000", 0)
        fidelities.append(good / max(total, 1))
    return float(np.mean(fidelities))


def main():
    rng = np.random.default_rng(20260828)
    rows = []
    for r_ratio in R_LADDER:
        j_val = r_ratio * J_EP
        ns, keeps = spectral_record(j_val)
        j_hat, g_hat, eig = fit_spectral(ns, keeps)
        eig_boot = []
        for _ in range(20):
            resampled = rng.binomial(np.maximum(keeps, 1), np.clip(ns, 0, 1)) / np.maximum(keeps, 1)
            _, _, eb = fit_spectral(resampled, keeps)
            eig_boot.append(eb)
        sig_eig = float(np.mean(np.std(np.array(eig_boot), axis=0)))
        f_petz = petz_fidelity(j_val)
        gap = float(abs(eig[0] - eig[1]))
        rows.append(dict(r=r_ratio, J=j_val, J_hat=float(j_hat), g_hat=float(g_hat),
                         gap=gap, sigma_eig=sig_eig, F_petz=f_petz,
                         keep_frac=float(np.mean(keeps)) / SHOTS))
        print(f"r={r_ratio:4.2f} J={j_val:.4f} gap={gap:.4f} "
              f"sig_eig={sig_eig:.4f} F_petz={f_petz:.4f} keep={rows[-1]['keep_frac']:.2f}")
    (HERE / "ibm_sim_reference.json").write_text(json.dumps(
        dict(gamma=GAMMA, t_grid=list(T_GRID), t_star=T_STAR, shots=SHOTS,
             noise="depol 3e-4/3e-3 + readout 1-2%", rows=rows), indent=1))
    print("frozen standard-QM reference -> ibm_sim_reference.json")


if __name__ == "__main__":
    main()
