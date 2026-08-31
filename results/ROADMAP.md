# Prioritized Research Program: Recoverability Geometry

## 1. Diagnosis: what the theory has and what is missing

**What is solid.** Of the 17 statements audited in the corpus, about half is established physics rewritten in saturation/information vocabulary (Misner-Sharp, Smarr, QES/Engelhardt-Wall, surface gravity); most of the rest is derivable with modest work from non-Hermitian perturbation theory (Kato/Puiseux), catastrophe theory, and Padé/Stahl convergence theory. The 2026-08-28 validation established three real things: (i) a new and possibly publishable spectral result: the genuine EP-2 of the fundamental scalar QNM with its mirror partner at q²c = -16.1472 on the EGB brane λ=0.08, including the useful negative that the ω₀/ω₁ pair never collides; (ii) a real numerical feat: the shooting solver (14th-order Frobenius) getting around the ~1e10 conditioning of Chebyshev collocation; (iii) the quantitative confirmation of P1-P4, frozen at turn 112 (γ = 0.498±0.062; rate halving 1.03±0.22; parameter-free collapse; logarithmic law with R²=0.999). The methodological discipline (prior freezing, honest fits, self-falsification of the "one universal α" version) is genuine and rare.

**What is missing for it to be revolutionary.** The audit's verdict is unambiguous: the confirmed structure is a corollary of two textbook pieces (√ sensitivity of a generic EP-2 + exponential Padé convergence), and any exponentially convergent scheme applied to any EP-2 (in photonics, random matrices, whatever) would produce the same laws. Since the ontology and the deflationary reading predict identical numbers, the likelihood ratio is ~1 and the Bayesian update on the ontology was **zero**. The specific gaps:

1. **No quantum information quantity does load-bearing work**: Petz fidelity, relative entropy, CMI: none of these appears in the derivation or in the pipeline.
2. **α is fitted, not predicted**: no a priori prediction from the analytic structure.
3. **Sufficiency, not necessity**: the log law is an upper bound achieved by one scheme; "cost of emergence" asserts necessity, and there is no Cramér-Rao-type lower bound.
4. **No inverse problem solved**: N counts Taylor coefficients of a *known* metric, not operational resources of a noisy boundary.
5. **Universality untested**: one background, one EP, one channel.
6. The only genuinely falsifiable claim against nature (a₀(z) ∝ H(z), turn 044) does not depend on the recoverability ontology and has thin priority (Milgrom, Verlinde, Hossenfelder-Mistele).

**The white space is real.** The literature sweep confirms that no one has quantified reconstruction *cost*: the Lu-Ran-Wu program (arXiv:2506.12890, PRL 2026; arXiv:2604.14638) proves order-by-order existence but not a convergence rate; the pseudospectrum/EP program (Jaramillo et al., PRX 2021; Motohashi, PRL 134, 141401; arXiv:2605.17840) characterizes spectral instability but never connects EP proximity to reconstruction cost; and holographic recoverability only has the coarse Python's Lunch dichotomy (arXiv:1912.00228). The "critical complexity law" occupies unoccupied territory, but occupying it with relabeled standard mathematics is not a revolution. The program below is designed to force, at every step, a bifurcation where the informational reading and the deflationary reading disagree.

---

## 2. The program: six projects, from short to long term

### Phase 1: weeks, existing code, cheap decision

**P1. Coupling sweep with a priori rates: predict α(λ) from the complex branch point before measuring.**
*What:* repeat the frozen pipeline at λ_GB ∈ {0.02 … 0.225}. The branch point of b(z) is closed-form (1-4λ(1-z⁴)=0); for each λ, compute **beforehand** the Stahl/capacity rate α_pred(λ) and the kernel-corrected critical channel rate, freeze the seven triples in a dated file, and only then measure. Byproducts: the EP trajectory q²c(λ), ω_c(λ) (new spectral data in itself) and the test of persistence of the 0.85/0.57 splitting at large N.
*Why decisive:* α stops being a fitted parameter and becomes a zero-free-parameter prediction, tested seven times with a predicted divergence as λ → 1/4. It simultaneously stresses the only refinement with content of its own that survived: per-observable rates fixed by sensitivity kernels.
*Difference from standard physics:* Stahl fixes only the asymptotic sup-norm rate and predicts equalization of the channels at large N; the kernel version predicts persistent splitting with a computable dependence on λ. If the splitting decays, the framework reduces to relabeled Stahl theory, and the design would establish that cleanly.
*Kill criterion:* splitting α_ρ/α_sup → 1 with N (slope ≠ 0 at 3σ); or levels/decade fails to track ln10/(2α_pred(λ)) in ≥5 couplings (R² < 0.9); or missing divergence as λ → 1/4.
*Effort:* weeks (~200 new lines + ~6 min of runtime per λ). Judges' caveat: λ_GB > 0.09 violates boundary causality; the points are mathematically valid, the duals pathological.

**P2. Operational informational depth: invert the noisy pole-skipping tower (projects 2 and 8 merged; both judges point out they are one and the same).**
*What:* compute the exact tower {q²_n} from the Frobenius recursion already in shooting.py, add Gaussian noise σ ∈ {1e-10 … 1e-2}, invert via the Lu-Ran-Wu triangular system, resum by constrained Padé, and measure the spectral error at distance d from the EP. Freeze beforehand: the optimal truncation wall N*(σ) = (1/2α_ρ)ln(1/σ); the noise-floor exponent (1/2 in the ω channel, 1 in the ρ channel); and the Cramér-Rao/Fisher benchmark: does a direct estimator that ignores the tower beat the levels-per-decade law?
*Why decisive:* it is the first time N counts a measured operational resource, not coefficients of a known metric; it directly answers the audit's sharpest gap. And the Fisher arm is where ontology and deflation finally diverge: the recoverability reading requires the law to be a bound over *all* estimators; pure mathematics only makes it an upper bound for one scheme.
*Difference from standard physics:* the √σ amplification at the EP is standard Petermann physics (Wang et al., Nature 2020) and Lau-Clerk (Nat. Commun. 9:4320) already showed the absence of a Fisher advantage in *sensing*, but neither of those literatures contains a noise-floor law or a truncation wall for *metric* reconstruction, nor any statement of necessity.
*Kill criterion:* the tower fails to converge before the wall for σ > 1e-8 (the law only exists in exact arithmetic); the floor exponent at the EP consistent with 1 and not 1/2 at 3σ; the ρ channel also with exponent ~1/2 (channel decomposition buys nothing); or the direct estimator beats the law by a factor >10, in which case the "cost" language must be withdrawn.
*Effort:* weeks.

**P3. Adversarial twin networks: a constructive lower bound of necessity.**
*What:* a discrete analogue of the benchmark: a non-Hermitian tridiagonal network with a mirrored EP-2, boundary spectral tower = poles/residues of the edge Green's function (inverse Jacobi problem). Numerically construct pairs of networks whose first N levels coincide exactly while maximizing the difference δ*(N,d) in a target observable: a constructive minimax bound that no estimator evades. Test δ* ~ e^(-αN)/√d with the *same* α as the Padé scheme.
*Why decisive:* it converts sufficiency into necessity by construction. And there is real mathematical risk for the theory: minimax width exponents (capacity/Chebyshev) need not equal the Stahl rate of one scheme; α* ≠ α would demote "informational depth of the observable" to "truncation order of an algorithm".
*Difference from standard physics:* no discrepancy expected if the law is tight, but no one has ever computed this minimax width near an EP, so any result is new information: α* = α elevates the law to a genuine resource bound; α* ≠ α is a discrepancy the frozen theory does not absorb.
*Kill criterion:* α* differs from α at >3σ, or amplification exponent outside 0.5±0.1 → publish the negative and abandon the "cost of emergence" language. (Skip the bench phase; numerical Phase 1 suffices.)
*Effort:* weeks.

### Phase 2: months, where quantum information must do load-bearing work

**P4. Boundary-CMI rate theorem: derive α from the analytic structure of J(u), not from the bulk metric.**
*What:* make the Abel relation of turns 078-080 (B(u) as a functional of J(u)) carry weight: (i) derive the general map between complex singularities of J and of B under the √ kernel (which generically *changes the type* of singularity); (ii) compute J(u) for the EGB brane via strip entanglement entropy with the Jacobson-Myers functional; (iii) locate J's nearest singularity by Padé/Stahl and **freeze** α_CMI before comparing with the already measured α_ρ = 0.851±0.130.
*Why decisive:* it is the first place where a quantum information quantity (boundary CMI) would *predict* a number so far only fitted, refuting or confirming the audit's central objection ("recoverability does zero load-bearing work").
*Difference from standard physics:* Stahl says the rate is fixed by B's singularity (known); HEE is irrelevant. The postulate says J is primary. The two predictions only coincide if the Abel functional preserves singularities one-to-one, which the √ kernel generically violates. The measured rate picks a side.
*Kill criterion:* |α_CMI − α_measured| > 2σ in both channels; or the derivation proves the predictions always coincide (the CMI layer is mathematically redundant: publish the deflationary theorem and stop); or the Abel identity fails at 1e-6 in Gauss-Bonnet (the framework's only bulk-boundary bridge breaks).
*Effort:* months; the judges agree that "weeks" was optimistic: the Jacobson-Myers extremizer is a new solver, and extracting Taylor coefficients of a numerical J(u) with enough precision to locate singularities is delicate.

**P5. DPI vs NEC: is channel monotonicity a strictly stronger energy condition?**
*What:* if the depth u is an emergent direction of a coarse-graining channel, the data processing inequality (DPI) must hold along u. Push these constraints through the Abel relation into sign inequalities on a₁…a_N and compare, coefficient by coefficient, with the Lu-Ran-Wu algebraic reformulation of the NEC (arXiv:2506.12890). Three outcomes: DPI ⟺ NEC (clean theorem, postulate redundant); weaker (no content); **strictly stronger** (new physics). If stronger: construct a background that satisfies the NEC and violates the DPI and test the predicted spectral pathology.
*Why decisive:* it is the only route in which the ontology *produces* gravitation instead of describing it; an energy-condition-type law derived from information would be exactly the proprietary, falsifiable prediction the audit says is missing. Even the deflationary outcome ("DPI is equivalent to the NEC in this class") is a publishable theorem in confirmed white space.
*Difference from standard physics:* RG+QFT admits every NEC-satisfying background with a normal pole-skipping tower; the postulate predicts that a strict subset is encodable, and DPI violators must be spectrally pathological despite being RG-healthy.
*Kill criterion:* (a) the DPI inequality provably implied by NEC + AdS conditions (no separating background: publish the equivalence and stop); (b) the DPI generates no definite constraint because the channel is not specifiable beyond the worked example, which confirms the audit's charge of operational underdefinition and closes this route; (c) a NEC-ok/DPI-violating background with a completely normal tower: direct falsification of the postulate's only dynamical consequence.
*Effort:* months, high variance. Fund only alongside the cheap Phase 1 projects, never alone.

### Phase 3: long term, the only experiment that separates the ontologies

**P6. Petz recovery rate vs spectral reconstruction rate in a dissipative qubit with an EP.**
*What:* on the only platform where "recoverability" is measurable (post-selected superconducting qubit with a quantum EP-2, Naghiloo class), measure two rates as a function of the number N of retained levels of the measurement record: α_Petz (decay of the infidelity of Petz recovery via tomography) and α_spec (convergence of parameter reconstruction from the same truncated record), with the jump operator engineered so that channel contraction and the Puiseux rate differ by ≥2× by design. Test α_Petz = α_spec and the halving of both at the EP, with the protocol and numbers frozen before the data.
*Why decisive:* it is the only project on the whole list in which a positive result would *surprise standard physics*: no theorem locks the Petz decay to the Fisher-governed estimation rate; the generic expectation is α_Petz ≠ α_spec. An observed locking would be a new law and the first evidence that recoverability, and not just approximation theory, governs reconstruction cost. The null retires the ontology cleanly.
*Kill criterion (preregistered):* α_Petz/α_spec outside 1±0.2 at ≥3 values of d, or a Petz rate without halving at the EP (outside 1±0.25) → retire the ontology as a physical claim, keep the validated mathematics, reframe the program as non-Hermitian spectral approximation theory.
*Effort:* the simulation dry-run of the full protocol costs days in the existing code and **must be done now**; the experiment requires a partner lab and ~1 year. Both judges: a real hardware campaign, not a "cloud device".

**Discarded or postponed, with the reason recorded:** the Petermann correction à la Fawzi-Renner (proposal 5) has a fatal statistical flaw: the "residual" 1.450 vs 1.35±0.21 is at ~0.5σ, there is nothing to explain until P1 tightens α_ρ by ~5×; phase coherence (proposal 3) has marginal statistical power with ~13 values of N and the Padé asymptotics is *not* silent about phases; the high-z BTFR test (proposal 9) has a signal the size of the systematics budget, blinding already partially compromised (MUSE data seen before the freeze), and does not test the depth ontology; the Kerr ringdown (proposal 7) and the EP-3 bench (proposal 11) are valuable but depend on unsharpened transpositions ("N as decades of SNR") or on a lab that does not exist: reassess after Phase 1.

---

## 3. The sharpest next move

**The coupling sweep (P1), starting this week.** Three reasons, in order of strength:

1. **Best cost/decision ratio on the table** (consensus of both judges): ~200 new lines on a verified pipeline, ~6 minutes per coupling, and *any* outcome is decisive: either α becomes the program's first zero-parameter prediction, confirmed seven times with a predicted divergence at λ → 1/4, or the channel splitting decays and the framework is convincingly reduced to relabeled Stahl theory, which would honestly close the holographic phase.

2. **It is a logical prerequisite for the rest.** P2 needs a tight α_ρ for the frozen exponents; the residual analysis that would motivate any informational correction (Petermann or otherwise) only exists after the error on α_ρ drops from ±0.130 to something useful; and the splitting persistence test decides whether the kernel version, the only surviving proprietary quantitative statement, deserves the P4 investment.

3. **It produces science independent of the theory.** The trajectory q²c(λ), ω_c(λ) of the mirrored EP in Einstein-Gauss-Bonnet does not exist in the literature (the nearest neighbor, arXiv:2605.17840, is Kerr and purely phenomenological), and it is publishable even if all the frozen predictions fail.

The decision rule at the exit: if P1 confirms the a priori rates and the persistent splitting, move immediately to P2+P3 in parallel (weeks) and unlock P4; if P1 kills the kernel, still run P2 (the Fisher arm and the noise wall keep operational value of their own), run the P6 simulation dry-run, and rewrite the program as what it will then provably be: spectral approximation theory of non-Hermitian systems, without the ontological layer, which is, notably, the same outcome the corpus's own self-falsification discipline has been practicing since turn 110.
