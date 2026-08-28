"""QPU campaign for pre-lab test #1 (two tasks, dilated non-Hermitian qubit).

Reads credentials from ibmq_setup/.env via the user's connection helper —
nothing is persisted (no save_account); deactivation after the run =
deleting .env.  Budget: 2 batched jobs (72 spectral + 54 Petz circuits,
4096 shots each) — well inside the Open Plan monthly allowance.

Frozen reference and verdict criteria: REPORT_IBM_SIM.md /
ibm_sim_reference.json (Aer + Heron-like noise).
"""

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "ibmq_setup"))

from connection import get_service  # noqa: E402
from qiskit import QuantumCircuit, transpile  # noqa: E402
from qiskit_ibm_runtime import SamplerV2  # noqa: E402

import ibm_pipeline as pipe  # noqa: E402  (reuses physics + analysis)


def build_spectral_circuits():
    jobs = []
    for r_ratio in pipe.R_LADDER:
        j_val = r_ratio * pipe.J_EP
        for t in pipe.T_GRID:
            qc = QuantumCircuit(2, 2)
            pipe.apply_dilated(qc, pipe.contraction(j_val, t), 0, 1)
            qc.measure([0, 1], [0, 1])
            jobs.append((r_ratio, float(t), qc))
    return jobs


def build_petz_circuits():
    jobs = []
    for r_ratio in pipe.R_LADDER:
        j_val = r_ratio * pipe.J_EP
        m = pipe.contraction(j_val, pipe.T_STAR)
        rec = pipe.petz_kraus(m)
        for label, amp in pipe.CARDINALS.items():
            qc = QuantumCircuit(3, 3)
            qc.initialize(np.array(amp, complex), 0)
            pipe.apply_dilated(qc, m, 0, 1)
            pipe.apply_dilated(qc, rec, 0, 2)
            from qiskit.quantum_info import Statevector
            prep = QuantumCircuit(1)
            prep.initialize(np.array(amp, complex), 0)
            undo = Statevector.from_instruction(prep).data
            basis = np.array([[undo[0].conjugate(), undo[1].conjugate()],
                              [-undo[1], undo[0]]], complex)
            qc.unitary(basis, [0], label="undo")
            qc.measure([0, 1, 2], [0, 1, 2])
            jobs.append((r_ratio, label, qc))
    return jobs


def main():
    service = get_service()
    backend = service.least_busy(operational=True, simulator=False)
    print(f"backend: {backend.name} (queue={backend.status().pending_jobs})")

    spectral = build_spectral_circuits()
    petz = build_petz_circuits()
    compiled_s = transpile([c for *_, c in spectral], backend, optimization_level=2)
    compiled_p = transpile([c for *_, c in petz], backend, optimization_level=2)
    depths = [c.depth() for c in compiled_s + compiled_p]
    print(f"circuits: {len(compiled_s)}+{len(compiled_p)}, depth median "
          f"{int(np.median(depths))}, max {max(depths)}")

    sampler = SamplerV2(mode=backend)
    job_s = sampler.run(compiled_s, shots=pipe.SHOTS)
    print("spectral job:", job_s.job_id())
    job_p = sampler.run(compiled_p, shots=pipe.SHOTS)
    print("petz job:", job_p.job_id())

    results = {"backend": backend.name,
               "job_spectral": job_s.job_id(), "job_petz": job_p.job_id()}
    (HERE / "qpu_jobs.json").write_text(json.dumps(results, indent=1))

    # block until done (Open Plan queues can be long; safe to re-run analysis
    # later from the saved job ids)
    res_s = job_s.result()
    res_p = job_p.result()

    rows = {}
    for (r_ratio, t, _), pub in zip(spectral, res_s):
        counts = pub.data.c.get_counts() if hasattr(pub.data, "c") else pub.data.meas.get_counts()
        kept = {k: v for k, v in counts.items() if k[-2] == "0" or len(k) == 2 and k[0] == "0"}
        kept = {k: v for k, v in counts.items() if k[0] == "0"}
        total = sum(kept.values())
        rows.setdefault(r_ratio, {"ns": [], "keeps": []})
        rows[r_ratio]["ns"].append(kept.get("01", 0) / max(total, 1))
        rows[r_ratio]["keeps"].append(total)

    petz_rows = {}
    for (r_ratio, label, _), pub in zip(petz, res_p):
        counts = pub.data.c.get_counts() if hasattr(pub.data, "c") else pub.data.meas.get_counts()
        kept = {k: v for k, v in counts.items() if k[0] == "0" and k[1] == "0"}
        total = sum(kept.values())
        petz_rows.setdefault(r_ratio, []).append(
            kept.get("000", 0) / max(total, 1))

    rng = np.random.default_rng(20260828)
    out = []
    for r_ratio in pipe.R_LADDER:
        ns = np.array(rows[r_ratio]["ns"])
        keeps = np.array(rows[r_ratio]["keeps"])
        j_hat, g_hat, eig = pipe.fit_spectral(ns, keeps)
        boot = []
        for _ in range(20):
            res = rng.binomial(np.maximum(keeps, 1), np.clip(ns, 0, 1)) / np.maximum(keeps, 1)
            boot.append(pipe.fit_spectral(res, keeps)[2])
        sig = float(np.mean(np.std(np.array(boot), axis=0)))
        f_petz = float(np.mean(petz_rows[r_ratio]))
        out.append(dict(r=r_ratio, sigma_eig=sig, F_petz=f_petz,
                        J_hat=float(j_hat), g_hat=float(g_hat)))
        print(f"r={r_ratio:4.2f} sig_eig={sig:.4f} F_petz={f_petz:.4f}")
    results["rows"] = out
    (HERE / "qpu_results.json").write_text(json.dumps(results, indent=1))
    print("wrote qpu_results.json — compare with ibm_sim_reference.json")


if __name__ == "__main__":
    main()
