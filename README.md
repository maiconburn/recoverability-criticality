# Critical Reconstruction Cost near Exceptional Points

**From a Gauss–Bonnet black brane to real Kerr ringdowns and a cloud QPU — one numerical program, six systems.**

Maicon Esteves (independent researcher, Brazil) · August 2026
Code, analysis and text produced with heavy AI assistance (Anthropic Claude); all key numbers cross-validated against literature anchors as documented below. Contact: maicon.burn@gmail.com

---

## Abstract

We quantify the *information cost* of reconstructing a system's parameters near a second-order exceptional point (EP) of its spectrum, and show the resulting law is universal across six very different systems. In the 5D planar Einstein–Gauss-Bonnet (EGB) black brane, the fundamental scalar quasinormal mode collides with its mirror partner (ω → −ω̄) at real spacelike momentum, forming a genuine EP-2. Reconstructing the metric from N near-horizon Taylor coefficients (a proxy for pole-skipping data), the spectral error obeys ε ~ e^(−αN)/√d at distance d from the EP, with the rate **halving exactly at the EP** — measured as 2α_EP/α = {1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.03} across nine couplings λ_GB ∈ [−0.10, 0.105], including two couplings *beyond* the string-causality window. All (N, d) data collapse onto the parameter-free curve √(u+1) − √u. The rate α(λ) itself is a **zero-fit-parameter prediction** (linear response at the EP × Padé approximation error): R² = 0.9988 on measured couplings and 4-decimal agreement on two virgin couplings predicted before measurement. We further find: (i) the EP is **extinct** for λ_GB > λ_ext = 0.1091 ± 0.0002, strictly above the causality bound 9/100 — bulk spectral structure is independent of boundary consistency; (ii) the cost functional has **two informational saddles** (near-horizon and near-boundary) whose dominance switches with the information budget; (iii) on **real numerical-relativity waveforms** (six SXS simulations spanning remnant spins 0.75–0.897), the extraction cost of the Kerr (2,2,5)/(2,2,6) overtone pair follows σ ∝ gap^(−1.11) (corr 0.959) through the known avoided crossing at a ≈ 0.8975; (iv) on a **real cloud QPU** (ibm_fez) and in public superconducting-qubit data (Murch lab), the spectral-estimation cost and the physical Petz state-recovery cost from the *same record* are independent — the spectral cost is enhanced ~4× near the EP while recovery fidelity stays flat — refuting, in these systems, "single-currency" informational ontologies while remaining consistent with thermodynamic (Jacobson-type) and two-address (Python's-Lunch-type) frameworks.

---

## 1. Main results

### 1.1 The critical-cost law (EGB benchmark, λ_GB = 0.08)

Frozen before measurement; all confirmed:

| Prediction | Frozen | Measured |
|---|---|---|
| Amplification exponent γ (critical channel, ε ∝ d^(−γ)) | 0.5 | **0.498 ± 0.062** |
| Rate halving at the EP, 2α_EP/α_ρ | 1 | **1.03 ± 0.22** |
| √-structure ε(N,0)/√(δρ_N) | 1 | **1.03 ± 0.09** (point-by-point, ~5 decades) |
| Levels per decade of approach | ≈1.47 | **1.450 ± 0.019** (R² = 0.9995) |

Universal collapse: `results/figures/fig4_collapse.png`. Full report: `results/RESULTS.md`.

### 1.2 Zero-parameter rate prediction

α_ρ(λ) = decay rate of the linear functional D_ρ[δb_N] (response kernel at the EP × constrained-Padé error of the metric function alone — no QNM ladder in the loop).

- Five measured couplings: slope 1.040, **R² = 0.9988**
- Two virgin couplings, frozen before measurement: 1.1596 → measured 1.1595 ± 0.077; 0.9239 → 0.9244 ± 0.073

Report: `results/RESULTS_V2.md`. Structure behind it: empirical Stahl–Green rate profile α_pt(z) and an observable "bulk address" — which turns out to be **two** addresses (window-dependent saddle, rate crossover 1.46 → 0.68 verified): `results/RESULTS_P4.md`.

### 1.3 EP spectroscopy of the EGB family (new spectral data)

- Mirror-EP trajectory q²_c(λ), ω_c(λ) for nine couplings (`results/sweep.json`, `results/sweep_acausal.json`)
- **EP extinction at λ_ext = 0.1091 ± 0.0002** (order-72 verified; the candidate closed form 7/64 is excluded), strictly above the D=5 causality bound λ_GB ≤ 9/100 (Brigante–Liu–Myers–Shenker–Yaida) — and the halving law holds unchanged at λ = 0.095, 0.105 *inside the acausal band*
- The λ→λ_ext approach shows q²_c diving from −16 to −35 before extinction

### 1.4 Real Kerr ringdowns (SXS catalog)

Six clean public simulations across the (2,2,5)–(2,2,6) avoided crossing (min gap 0.0667 at a\* ≈ 0.8975; the true EP sits at complex spin):

σ(A₅, A₆) ∝ gap^(−1.11), corr(log σ, −log gap) = **0.959**, while low-overtone extraction stays flat (~750× channel contrast at the crossing). Figure: `results/figures/fig_sxs_real.png`; data: `results/sxs_layer.json`. One simulation (SXS:BBH:2525) excluded as an outlier (2× elevated noise floor; mode mixing) — flagged, not hidden.

### 1.5 Two tasks, one record: no locking (QPU + public transmon data)

Protocol: dilated non-Hermitian qubit (Sz.-Nagy), Task A = spectral estimation from post-selected populations, Task B = **physical Petz recovery circuit**, same shot budget, nine distances to the EP.

- **ibm_fez (real QPU)**: σ_spectral elevated 4.0× in the EP band; Petz fidelity flat (−0.007, within shot noise), tracking the frozen simulator reference point-by-point (`prelab/REPORT_QPU.md`)
- **Public Murch-lab data** (101 drive amplitudes, 18k averages): the two costs *anti-correlate* through the EP (`prelab/REPORT_MURCH.md`)
- Same-spectrum collapse-vs-decoherence demo: Petz recovery F → 0.9999 with the environment record vs ceiling 0.500 without one (`p6/fig_collapse_vs_decoherence.png`) — the Petz axis, not the spectral one, is what discriminates objective collapse from decoherence

## 2. Methods (short)

- **Shooting QNM solver** (`src/recoverability_ep/shooting.py`): Frobenius series at the horizon, Wronskian W = z⁵ψ′ at a boundary cutoff; near-degenerate pairs via a local quadratic model of W (error linear in W-noise, not √). Built because Chebyshev collocation has eigenvalue condition numbers ~10¹⁰ at the relevant spacelike momenta. Anchor validations: AdS₅ fundamental 3.119452 − 2.746676i reproduced to 1e-8; collocation cross-checks throughout.
- **Constrained Padé reconstruction** from N horizon Taylor coefficients (`src/recoverability_ep/model.py`), admissibility tests preregistered.
- **Symmetric-invariant extraction** (μ, ρ) with ω± = μ ± √ρ: EPs found as simple real zeros of ρ; λ-continuation with Puiseux member seeds.
- **QPU pipeline** (`prelab/ibm_pipeline.py`, `prelab/qpu_run.py`): per-time Sz.-Nagy dilation; Petz map of the post-selected channel as a second dilated circuit; frozen Aer+noise reference before hardware.

## 3. What we do **not** claim

- Nothing here proves or refutes string theory or any quantum-gravity proposal. The EGB brane at finite λ_GB is a bottom-up laboratory (finite λ_GB requires a higher-spin tower; controlled string vacua give λ ~ 1/N).
- The λ_ext ≠ 9/100 result is an *independence* statement inside a model.
- The "no-locking" results retire a speculative informational ontology *in the systems tested*; they are consistency checks, not discoveries about nature beyond standard QM.
- A dedicated-lab version of the two-task test (protocol frozen in `p6/SPEC.md`) remains the only place the ontology could still win; three consecutive negative arbitrations set the prior strongly against.

## 4. Limitations / provenance

Produced in a single day of AI-assisted work by an independent researcher; no external code review yet. Preregistration was session-internal (files timestamped before measurements; see `results/sweep_predictions.json`, `results/v2_frozen_fresh.json`, `prelab/FROZEN_MURCH.md`) — real discipline, not a formal registry. Known soft spots are stated inline: SXS outlier, order-56/72 sensitivity ~2×10⁻⁴ in λ_ext, model-dependent bootstrap on the Murch reanalysis, QPU fit-robustness artifacts at two ladder points. Independent replication is invited — everything below reproduces on a laptop.

## 5. Reproduce

```bash
uv sync            # or: pip install -e . plus qnm sxs qiskit qiskit-aer
uv run pytest      # 13 tests
uv run python scripts/run_validation.py     # EGB anchor (~6 min)
uv run python scripts/analyze_validation.py
uv run python scripts/sweep_predictions.py  # freeze BEFORE running the sweep
uv run python scripts/run_sweep.py          # 7 couplings (~15 min)
uv run python scripts/run_sxs_layer.py      # real SXS waveforms (downloads)
```

Third-party data (not re-hosted): Murch-lab repositories (github.com/murchlab), SXS catalog (sxs-collaboration), Kerr QNM tables (duetosymmetry/qnm). IBM jobs: da904i9qtnsc73d10u30, da904ihqtnsc73d10u3g (ibm_fez, 2026-08-28).

## 6. License

Code: MIT. Text and figures: CC-BY 4.0.
