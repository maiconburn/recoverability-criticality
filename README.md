# Critical Reconstruction Cost near Exceptional Points

**From a Gauss–Bonnet black brane to real Kerr ringdowns and a cloud QPU — one numerical program, six systems.**

Maicon Esteves (independent researcher, Brazil) · August 2026
Code, analysis and text produced with heavy AI assistance (Anthropic Claude); all key numbers cross-validated against literature anchors as documented below. Contact: maicon.burn@gmail.com

---

## Abstract

We quantify the *information cost* of reconstructing a system's parameters near a second-order exceptional point (EP) of its spectrum. To our knowledge no prior work combines the ingredients below into a single predictive law, although each ingredient has classical roots (see Relation to prior work). In the 5D planar Einstein–Gauss-Bonnet (EGB) black brane, the fundamental scalar quasinormal mode collides with its mirror partner (ω → −ω̄) at real spacelike momentum, forming a genuine EP-2. Reconstructing the metric from N near-horizon Taylor coefficients (a proxy for pole-skipping data), the spectral error obeys ε ~ e^(−αN)/√d at distance d from the EP, with the rate **halving exactly at the EP** — measured as 2α_EP/α = {1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.01, 1.03} across nine couplings λ_GB ∈ [−0.10, 0.105], including two couplings *beyond* the string-causality window. All (N, d) data collapse onto √(u+1) − √u — the classical Green's-function factor for a square-root branch point (Stahl; Gonchar–Rakhmanov), here derived rather than discovered, with the novelty residing in the composite predictive law and its measured exact factor-2 rate change. The rate α(λ) itself is a **zero-fit-parameter prediction** (linear response at the EP × Padé approximation error): R² = 0.9988 on measured couplings and 4-decimal agreement on two virgin couplings predicted before measurement. We further find: (i) the EP is **extinct** for λ_GB > λ_ext = 0.1091 ± 0.0002 — it survives the entire D=5 causality window and (2.0 ± 0.2)×10⁻² beyond the 9/100 bound (a numerical juxtaposition; no mechanism relating the two is claimed); (ii) the cost functional has **two informational saddles** (near-horizon and near-boundary) whose dominance switches with the information budget; (iii) on **real numerical-relativity waveforms** (six SXS simulations spanning remnant spins 0.75–0.897), the extraction cost of the Kerr (2,2,5)/(2,2,6) overtone pair follows σ ∝ gap^(−1.11) (corr 0.959) through the known avoided crossing at a ≈ 0.8975; (iv) on a **real cloud QPU** (ibm_fez) and in public superconducting-qubit data (Murch lab), the spectral-estimation cost and the physical Petz state-recovery cost from the *same record* are independent — the spectral cost is enhanced ~4× near the EP while recovery fidelity stays flat — refuting, in these systems, "single-currency" informational ontologies while remaining consistent with thermodynamic (Jacobson-type) and two-address (Python's-Lunch-type) frameworks.

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
- **EP extinction at λ_ext = 0.1091 ± 0.0002** (order-72 verified; the candidate closed form 7/64 is excluded). The EP survives the entire D=5 causality window λ_GB ≤ 9/100 (Brigante–Liu–Myers–Shenker–Yaida) and (2.0 ± 0.2)×10⁻² beyond it — a numerical juxtaposition, with no mechanism claimed; the halving law holds unchanged at λ = 0.095, 0.105 *inside the acausal band*. Open points, stated as such: relation to the eikonal-instability threshold |λ_GB| = 1/8 (Konoplya–Zhidenko), and whether "extinction" is migration of the collision to complex q² (operational definition here: no coalescence at any real q² down to −60)
- The λ→λ_ext approach shows q²_c diving from −16 to −35 before extinction

### 1.4 Real Kerr ringdowns (SXS catalog)

Six clean public simulations across the (2,2,5)–(2,2,6) avoided crossing (min gap 0.0667 at a\* ≈ 0.8975; the true EP sits at complex spin):

σ(A₅, A₆) ∝ gap^(−1.11), corr(log σ, −log gap) = **0.959**, while low-overtone extraction stays flat (~750× channel contrast at the crossing). Figure: `results/figures/fig_sxs_real.png`; data: `results/sxs_layer.json`. One simulation (SXS:BBH:2525) excluded as an outlier (2× elevated noise floor; mode mixing) — flagged, not hidden. Caveats: current LVK detections concern n = 0/1, not n = 5/6, and these are noise-injected fits of noiseless NR waveforms — transfer to detector pipelines requires demonstration at low-n crossings with realistic noise. Our measured exponent (−1.11, amplitude-extraction conditioning) should be contrasted with the Fisher-forecast exponent −2 of Imafuku–Oshita–Takeda (arXiv:2605.16199), a different but related quantity.

### 1.5 Two tasks, one record: no locking (QPU + public transmon data)

Protocol: dilated non-Hermitian qubit (Sz.-Nagy), Task A = spectral estimation from post-selected populations, Task B = **physical Petz recovery circuit**, same shot budget, nine distances to the EP.

- **ibm_fez (real QPU)**: σ_spectral elevated 4.0× in the EP band; Petz fidelity flat (−0.007, within shot noise), tracking the frozen simulator reference point-by-point (`prelab/REPORT_QPU.md`)
- **Reanalysis of public Murch-lab data** (101 drive amplitudes, 18k averages; Naghiloo-lineage platform): the two costs *anti-correlate* through the EP (`prelab/REPORT_MURCH.md`)
- Same-spectrum collapse-vs-decoherence demo: Petz recovery F → 0.9999 with the environment record vs ceiling 0.500 without one (`p6/fig_collapse_vs_decoherence.png`) — the Petz axis, not the spectral one, is what discriminates objective collapse from decoherence

## 2. Methods (short)

- **Shooting QNM solver** (`src/recoverability_ep/shooting.py`): Frobenius series at the horizon, Wronskian W = z⁵ψ′ at a boundary cutoff; near-degenerate pairs via a local quadratic model of W (error linear in W-noise, not √). Built because Chebyshev collocation has eigenvalue condition numbers ~10¹⁰ at the relevant spacelike momenta. Anchor validations: AdS₅ fundamental 3.119452 − 2.746676i reproduced to 1e-8; collocation cross-checks throughout.
- **Constrained Padé reconstruction** from N horizon Taylor coefficients (`src/recoverability_ep/model.py`), admissibility tests preregistered.
- **Symmetric-invariant extraction** (μ, ρ) with ω± = μ ± √ρ: EPs found as simple real zeros of ρ; λ-continuation with Puiseux member seeds.
- **QPU pipeline** (`prelab/ibm_pipeline.py`, `prelab/qpu_run.py`): per-time Sz.-Nagy dilation; Petz map of the post-selected channel as a second dilated circuit; frozen Aer+noise reference before hardware.

## 2b. Relation to prior work (what is and is not new here)

Every ingredient has lineage; the claims are the syntheses.

- **Approximation theory.** Exponential-in-N Padé convergence with rate set by the Green's function of the branch cut is classical (Stahl 1997; Gonchar–Rakhmanov 1987); √(u+1)−√u is the standard square-root-branch-point factor. The √d Puiseux behaviour at an EP-2 is textbook (Kato 1966). New here: the composite law ε ~ e^(−αN)/√d with the *measured* exact halving, the cross-coupling collapse, and the zero-fit-parameter α (linear-response kernel × Padé error) validated on virgin couplings.
- **Holography.** QNM level collisions setting convergence radii: Grozdanov–Kovtun–Starinets–Tadić, PRL 122, 251601 (2019); collision points tracked vs λ_GB non-perturbatively (metric channels, complex momentum): Grozdanov–Starinets–Tadić, arXiv:2104.11035; QNM/bulk reconstructability from pole-skipping: PRD 108, L101901 (2023) and the 2025–26 line (arXiv:2506.12890 et seq.). We promote the radius statement to a full error law and add the cost/convergence analysis those programs lack. The mirror-mode propagating→overdamped transition type is known (k-gap literature); EP language in holographic QNMs appears in arXiv:2605.27641. New here: the resolved EP map of the EGB *scalar* family at real spacelike momentum, the extinction threshold λ_ext = 0.1091(2), and its juxtaposition with the 9/100 bound. Open point we flag: relation of λ_ext to the eikonal-instability threshold |λ_GB| = 1/8 (Konoplya–Zhidenko, arXiv:1705.07732), and whether extinction is migration of the collision to complex q² (not yet determined).
- **Near-colliding poles.** Prony/matrix-pencil super-resolution gives *algebraic, fixed-N* conditioning laws for coalescing nodes (Batenkov–Goldman–Yomdin, arXiv:1904.09186); our law is exponential-in-N at parametric distance d from a true EP — a different regime, stated here to avoid confusion.
- **EP sensing debate.** Our C1 concerns inverse-problem cost vs number of information levels, not Fisher sensitivity of a single readout; it neither relies on nor contradicts EP sensitivity enhancement (Am-Shallem–Kosloff–Moiseyev 2015; Lau–Clerk 2018; Loughlin–Sudhir 2024; Liu et al. 2024).
- **QPU ingredients.** Dilated non-Hermitian qubits on hardware: Dogra et al. 2021; QFI at a dilated EP on a cloud QPU: Waghela–Dasgupta (arXiv:2304.12181); Petz recovery on hardware: 2024–26 implementations (e.g. PRR 6, 043034; arXiv:2504.20399); information retrieval across EPs as passive backflow: Kawabata–Ashida–Ueda, PRL 2017. New here: the *dual-task design* — spectral cost and physically executed Petz-circuit fidelity from the same record at an EP, measured jointly.

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

## 7. Where this could be used today (direct → indirect)

1. **EP-sensor design** (photonic gyros/nanoparticle sensing): a third, noise-independent quantity for the enhancement debate — inverse-reconstruction cost, with a testable zero-parameter α recipe.
2. **LVK ringdown pipelines / black-hole spectroscopy**: gap-dependent priors for overtone model selection; spin bands where posteriors are structurally ill-conditioned (with the n=5/6 vs n=0/1 caveat above).
3. **Kerr non-Hermitian spectral program** (avoided crossings, pseudospectra): the inference-cost half the spectral characterization lacks; λ_ext independently checkable.
4. **Superconducting-device calibration near TLS crossings / Liouvillian EPs**: σ ∝ gap^(−1.1) as a shot-budget law; the no-locking result says operational tasks need not pay the spectral-characterization tax.
5. **Petz-based error mitigation**: recovery does not inherit the ill-conditioning of channel identification near spectral degeneracy.
6. **Hamiltonian/Lindbladian learning**: an a-priori sample-budget law and a falsifiable EP-limited vs noise-limited diagnostic (residuals in the collapse variable).

## 8. License

Code: MIT. Text and figures: CC-BY 4.0.
