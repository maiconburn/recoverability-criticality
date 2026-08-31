# Our work and the "11 dimensions": an honest map

> **SUPERSESSION NOTICE (2026-08-30):** this is a dated HISTORICAL document.
> The λ_ext values cited here (0.1091 and derived) have been RETRACTED:
> see `ERRATA.md` E1–E3: there is no single threshold; extinction is
> family-by-family, with genuine EPs up to at least λ = 0.120.

Short question: **does our work touch string theory? And the theories that unify the quantum with the macroscopic?** Short answer: it touches string theory at one real, well-delimited technical point (and we have just obtained an interesting *negative* result exactly at that point); on "quantum-macro unification", our results say concrete things about **collapse models** and about **emergent gravity programs**, but almost always in the form of constraints and independences, not confirmations. Below, the map without exaggeration.

---

## 1. Where we (really) touch string theory

**First, the vocabulary.** M-theory has **11 spacetime dimensions** (10 of space + 1 of time), not "11 universes". The construction comes from 11D supergravity (Cremmer-Julia-Scherk, 1978) and Witten's insight (1995) that the five 10D superstring theories and 11D supergravity are limits of a single theory. "Multiverse" and "parallel universes" are distinct concepts (different vacua of the same theory; brane scenarios): confusing the count of dimensions with the count of universes is the classic popular-science mistake. And the "5D" of our Einstein-Gauss-Bonnet brane **is not an extra dimension in the laboratory**: it is the holographic bulk (4 dimensions of the boundary theory + 1 emergent radial direction).

**The genuine connection: Gauss-Bonnet is the first-order string correction.** Zwiebach (1985) showed that the Gauss-Bonnet combination is the only ghost-free quadratic-curvature extension, and it appears at order α′ of the **heterotic** string (in type II strings, the first correction only appears at α′³R⁴). That is: the model we study is, structurally, "Einstein gravity + the first correction that string theory predicts". Mandatory honesty: in every controlled string construction, λ_GB ~ 1/N, orders of magnitude below the 0.08–0.12 we explore. Our brane with finite λ_GB is a **bottom-up phenomenological laboratory**, not the limit of a controlled string compactification (Camanho-Edelstein-Maldacena-Zhiboedov, 2014, showed that finite λ_GB is only consistent with an infinite tower of higher-spin states, the quintessential "stringy" signature).

**The causality window.** Causal consistency restricts −7/36 ≤ λ_GB ≤ 9/100 in 5D (Brigante-Liu-Myers-Shenker-Yaida 2008; Buchel et al. 2010). Above 9/100 = 0.09, the dual boundary theory propagates signals faster than light: a consistent theory ceases to exist.

**What we found there, and what that does and does not mean.** Our new transition (the mirrored exceptional point of the scalar QNM exists on the real axis of spacelike momentum for λ ≤ 0.08 and is extinct for λ ≥ 0.12) initially placed the threshold in an interval that contained 0.09. **If** the threshold converged to exactly 9/100, we would have the first statement that an exceptional-point transition of the spectrum *detects* the string causality boundary: a zero-parameter prediction, testable on a laptop. That would **not** mean "proof of string theory": it would be a structural link within one model, between two consistency properties. Well: the numerical refinement has already decided. The local log (`extinction_hunt.log (local session log, not distributed)`) closes the threshold at **λ_ext ∈ [0.10875, 0.11000]**: strictly *above* 0.09, about 20% beyond the last consistent boundary theory. The exceptional point, and with it the half-rate complexity law, **survives the death of boundary causality**. This is a negative result with content: the spectral-informational structure of the bulk is *indifferent* to the consistency of the boundary theory (see section 3). Speculative footnote, duly labeled as numerology until someone derives it: 7/64 = 0.109375 falls inside the current interval; the Konoplya-Zhidenko eikonal instability threshold, 1/8 = 0.125, appears to be excluded.

---

## 2. Collapse models: what we say and what we do not say

Objective collapse models (GRW/CSL, Diósi-Penrose) are the most direct attempt to "unify quantum and macro": they postulate that quantum superposition truly dies above a certain scale. Experimental status in 2026: the original GRW point is still alive (the Majorana Demonstrator limits, 2022, killed Adler's values but not GRW); the parameter-free Diósi-Penrose model is killed (Gran Sasso, 2021) and the version with a parameter is squeezed into a window of ~4 orders of magnitude, hemmed in on both sides: a situation structurally identical to our λ_GB window.

**What our results say.** At the density-matrix level, white-noise CSL *is* exactly a Lindblad equation: the same mathematical object whose spectra and exceptional points we study. Hard consequence: **no spectral measurement on the system alone distinguishes collapse from environmental decoherence**. All proposed experiments (e.g., Horchani's 2026 blueprint) discriminate by energy and mass scales, never by information. Our second result (spectral reconstruction cost and Petz recoverability cost are **independent** invariants) provides exactly the missing axis: decoherence is recoverable-in-principle from environment fragments (the Petz map works; it is the "redundancy plateau" of quantum Darwinism, which Torvinen-Keski-Vakkuri-Pranzini published in 2026); true collapse leaves no fragment holding the record. And our independence says this axis is **orthogonal** to spectral criticality: two genuinely independent discriminators.

**What our results do not say.** We did not test collapse: our transmon and QPU data constrain neither λ_CSL nor R₀. And the surviving collapse models are necessarily *non-Markovian* (colored noise), a regime where our formalism of Markovian exceptional points would need an extension: an open question, not a result.

---

## 3. Emergent gravity: where each verdict bites

We have three verdicts: **(a)** the "address" of the exceptional point, q²_c(λ), is not fixed by the boundary entanglement scale (the measured trajectory is non-monotonic in λ; every candidate entanglement scale is monotonic: a monotonic function cannot parametrize a non-monotonic target); **(b)** no "locking" between spectral cost and Petz cost (three consecutive defeats); **(c)** the extinction of the EP at ~0.109, not at 0.09: a third independence, now between bulk structure and boundary consistency.

- **Verlinde 2010 (entropic gravity, "information is a single currency")**: this is the ontology that verdicts (b) and (c) hit head-on. If all dynamics were a single entropy ledger, the two costs should be interconvertible; we measured that they are not. In our model systems, that ontology is refuted. (In the sky it was already doing badly: it fails rotation curves and Solar System ephemerides by 7 orders of magnitude, although it passes weak lensing of isolated galaxies.)
- **It-from-qubit / quantum error correction**: the *naive* version ("informational properties are properties of the consistent code and must die at the consistency edge, 0.09") is refuted by verdict (c). But the refined version, two addresses per observable: recoverability (Petz) and decoding complexity (Susskind et al.'s Python's Lunch; Pastawski-Preskill's "price vs distance"), is **strongly supported** by (a) and (b): our pair of independent invariants is a laboratory instance of exactly that structure.
- **Jacobson (thermodynamic gravity, 1995/2016)**: derived for *any* Lovelock coupling, it makes no claim about locking. It is the only program that **predicted** indifference to the 0.09 edge, and that is what we measured. Untouched, and weakly supported.

Caveat without hype: all of this is in model systems (holographic brane, qubits, QPU). We did not measure real gravity; we measured which *logical structure* emergent-gravity ontologies would need to have to survive our data.

---

## 4. What can still be computed on this laptop tonight (ordered)

1. **Bisect λ_ext down to width < 0.0005** and test 7/64 = 0.109375 against the interval (label as numerology until derived). Decides whether there is a closed-form value to explain.
2. **Effective potential / front velocity of the scalar channel at large q vs λ**: if the qualitative transition of the scalar channel itself falls at ~0.109 (and not at the 0.09 of the tensor channel), the EP *re-locks* to causality channel-by-channel: it would overturn the "bulk autonomy" reading. It is the most decisive test on the list.
3. **Halving law at λ = 0.095 and 0.105** (acausal band, EP alive): turns "the complexity law survives boundary inconsistency" into a measured number.
4. **Pipeline validations**: tensor potential well exactly at 0.09 (BLMSY) and shear collision at q²_c ≈ 1.18544, ω_c ≈ −1.63793i at λ ≈ −0.04956 (Grozdanov-Starinets-Tadić).
5. **Regression of q²_c(λ) against a(λ), c(λ), c/a and the entanglement entropy coefficient** (closed formulas of Buchel et al.): quantifies verdict (a) with an R².
6. **corr(α_ρ, Petz cost) with bootstrap CI** over `results/sweep_fits.json`: the "no locking" becomes a single citable number.
7. **Numerical demo-theorem**: the same channel as a unitary dilation vs a stochastic unraveling with the record discarded: identical spectra, maximally different Petz. It is the clean bridge between our results and the collapse/decoherence discrimination of section 2.

Relevant files: `extinction_hunt.log (local session log, not distributed)`, `/Users/maiconesteves/fisica/theory-validation/results/RESULTS_SWEEP.md`, `/Users/maiconesteves/fisica/theory-validation/results/sweep_fits.json`.
