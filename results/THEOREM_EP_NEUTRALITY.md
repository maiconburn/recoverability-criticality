# Theorem of control parameter neutrality at the EP (2026-08-31)

Motivation: three independent measurements gave a FLAT cost for
estimating the control parameter at the EP: P14-LZ (σ(μ)/μ = 0.03%),
the LEP3 design (all configs sitting on the EP line), P16.2 (p = −0.07
over 1.5 decades of gap). Here is the analytic explanation, with
high-precision numerical verification (script `p17_theorem_check.py`,
predictions declared BEFORE running: section "Verifications").

## Statement

Let H(θ) be an analytic family of N×N matrices with an EP of order N at
θ = 0, and let the data be y(t) = Re[A·g(t; θ)] + white noise, with
A ∈ ℂ a nuisance and g an analytic SYMMETRIC function of the spectrum
{ω_j(θ)}, which includes every linear response channel: the scalar
Green's function is the divided difference of order N−1 of e^{−iωt}
over the spectrum,

  g(t; θ) = Σ_j e^{−iω_j t} / Π_{k≠j}(ω_j − ω_k) = Δ^{N−1}[e^{−iω·t}],

symmetric by construction and ENTIRE in the invariants. Then the Fisher
information marginalized for θ is analytic at θ = 0 and, under the
genericity conditions below, σ(θ̂) → a finite positive constant at the
EP: **the critical exponent of the control parameter is exactly 0.**

## Proof (EP-2; the general case is identical with e₁…e_N)

1. (Symmetry ⇒ analyticity.) Eigenvalues ω± = μ ± √ρ with μ = tr H/2,
   ρ = μ² − det H, both analytic in θ. An analytic symmetric function
   of the eigenvalues is an analytic function of the elementary
   symmetric polynomials (classical theorem), so
   g(t; θ) = ĝ(t; μ(θ), ρ(θ)) is analytic in θ THROUGH the EP.
   Explicit example (Green channel):
   ĝ = −i e^{−iμt} · sin(√ρ t)/√ρ = −i e^{−iμt} (t − ρt³/6 + ρ²t⁵/120 − …),
   an even series in √ρ ⇒ entire in ρ. The square root of the
   unfolding simply does not appear.

2. (Analytic Fisher.) The columns of the design J are ∂y/∂θ and the 2
   amplitude columns, all analytic in θ. I(θ) = JᵀJ/σ² is analytic;
   the marginalized I_eff = I_θθ − I_θA I_AA⁻¹ I_Aθ (Schur complement)
   is analytic wherever I_AA is invertible.

3. (Genericity.) (i) transversality: ρ'(0) ≠ 0 (the control actually
   unfolds the EP); (ii) the direction ∂g/∂θ|₀ ∉ span of the amplitude
   columns: for the Green channel, ∂ĝ/∂ρ|₀ ∝ t³e^{−iμt}, which is
   linearly independent of e^{−iμt} and t e^{−iμt}: holds; (iii) I_AA
   invertible on the nuisance space of correct rank (lesson from
   P16.2: with a mirror pair the rank drops to 2, reparametrize
   first). Under (i)-(iii), I_eff(0) > 0 and σ(θ̂) is finite and
   continuous. ∎

## Corollary A: the Jacobian ladder (where the exponents come from)

All the spectral divergence is change-of-variable bookkeeping on top of
an analytic Fisher. The CRB transforms as I_η = I_ρ·(dρ/dη)²:

- gap s = 2√ρ: σ(ŝ) = σ(ρ̂)·|ds/dρ| ∝ s⁻¹: exponent 1.
  (Measured Kerr: extraction cost ∝ gap^−1.11.)
- EP-N: symmetric coefficient c ∝ s^N ⇒ σ(ŝ) ∝ s^{−(N−1)}: the FIRST
  step {p−1} of the P15 ladder {p−1, 2p−2, 2p−1}, now derived.
- Labeled quantities (individual eigenvalue, residue, eigenvector) are
  not symmetric ⇒ they pay the critical cost. Physical: no apparatus
  measures a label; apparatuses measure response (symmetric). The
  critical cost is a property of the QUESTION, not of the signal.

## Corollary B: free-amplitude step (heuristic, verification C3)

With PER-MODE free amplitudes (agnostic observer, without the Green
constraint), the basis functions e^{−iω₁t}, e^{−iω₂t} degenerate
linearly in s and marginalizing the near-null direction costs one extra
Jacobian: prediction σ(ŝ) ∝ s⁻²: the second exponent of the measured
hierarchy (task 2 = 2.12). The task hierarchy is a ladder of KNOWLEDGE
about amplitudes: Green constraint ⇒ s⁻¹; free amplitudes ⇒ s⁻².

## Validity boundary (honest)

- Motion ALONG the EP manifold (ρ ≡ 0): the channel only informs
  through μ(θ); cost anisotropy there is mundane variation of I_μμ,
  consistent with the P15.4 verdict (LEP3 anisotropy dominated by γ
  scale).
- Failure of genericity (iii) requires rank reduction of the nuisance
  before marginalization (P16.2 v1 vs v2).
- Non-white noise or sampling that kills ∂ĝ/∂ρ|₀ changes constants,
  not the exponent 0 (the analyticity is structural).

## Numerical verifications (predictions declared before running)

EP-2 model: ω± = (a − i)θ_μ-drift + … concretely μ = −i + 0.3θ,
ρ = θ; damped Green channel, t ∈ [0, 4], 200 points, mpmath 50 dps.
- C1: marginalized σ(θ̂) at θ = 10⁻¹…10⁻⁸: local log-log slope → 0
  (|slope| < 0.05 for θ ≤ 10⁻⁴) and σ → positive constant.
- C2: direct parametrization in s (nuisance μ, A): slope → −1.00 ± 0.05.
- C3: per-mode free-amplitude model (8 real parameters):
  σ(ŝ) slope → −2.00 ± 0.15 (corollary B).
- C4: EP-3 (μ = −i, ω_j = μ + ε_j s, s = θ^{1/3}, channel = 2nd-order
  divided difference): σ(θ̂) slope → 0; σ(ŝ) slope → −2.00 ± 0.15
  (= −(N−1)).
KILL of the theorem: C1 or C4-control with slope outside ±0.05 (the
analyticity is exact: there is no margin). C2/C3/C4-gap outside the
ranges kills the corresponding corollary, not the theorem.

## Verdicts (2026-08-31, `p17_theorem_check.json`)

| check | frozen prediction | measured (last slopes) | verdict |
|---|---|---|---|
| C1 σ(control), EP-2 | slope 0, σ → const | 0.0000; σ → 0.77958 | CONFIRMED |
| C2 σ(gap), Green constraint | −1.00 | −1.0000 | CONFIRMED |
| C3 σ(gap), free amplitudes | −2.00 | −2.0000 | CONFIRMED |
| C4 σ(control), EP-3 | slope 0 | −0.0000 | CONFIRMED |
| C4 σ(gap), EP-3 | −2.00 (= −(N−1)) | −2.0000 | CONFIRMED |

4-digit precision on all of them, as it should be for an exact
statement. Scope of C3: antisymmetric truth (A₁ = −A₂, Green-like), as
frozen in the script header; symmetric truth falls on the −1 step (the
amplitude-knowledge ladder depends on the source configuration: an
open refinement, does not affect the theorem).

Instrument note: the first run used a purely imaginary μ (mode with no
oscillating part); with that phase, the Green channel is purely
imaginary and Re[A·g] with real A projects out the entire ρ channel:
exactly singular Fisher matrix, spurious σ ∝ 1/θ from inverting 1e-60
residuals. Third appearance of rank collapse by phase/symmetry (P16.2
mirror, here phase); an inversion-residual guard was added and generic
phases (μ = 0.7 − i) were used in the final run.

Consequences for the program: P14-LZ, the LEP3 design and P16.2 are
the same fact: critical exponent 0 of the control parameter.

## The complete ladder (2026-08-31, same session)

The three steps {p−1, 2p−2, 2p−1} derive from a single object: row
norms of the inverse Vandermonde. Model tangents in the monomial basis
t^k e^{−iμt}: amplitude direction of node j = column (δ_j^k/k!);
frequency direction = A_j × column shifted by one order. With a
generic positive-definite Gram on the monomials,
CRB(parameter) ≍ ‖corresponding row of V⁻¹‖, and the exponent is the
dominant order in s of that row:

- Task A (amplitudes, known frequencies): SIMPLE p×p Vandermonde
  ⇒ rows ~ s^{−(p−1)}.
- Tasks B and C (everything free): CONFLUENT 2p×2p system (double
  nodes: the same confluent structure as the EP) ⇒ amplitude rows
  ~ s^{−(2p−1)}, frequency rows ~ s^{−(2p−2)} (the A_j·t factor of the
  frequency column costs exactly one degree).

Exact symbolic verification (sympy, `p17b_ladder_symbolic.py`):
p=2 → {−1, −2, −3}; p=3 → {−2, −4, −5}. Six out of six, exact integer
orders. Matches the program's entire numerical history: measured EP-2
hierarchy {1.03, 2.12, 3.12}, P15.1 at EP-3 {−2.01, −3.98, −5.01},
C2/C3 of this document.

Prior art (verified on the arXiv API): the 2p−2 and 2p−1 steps are the
super-resolution theorems of Batenkov–Goldman–Yomdin
(arXiv:1904.09186) and the conditioning of Fourier matrices with
clustered nodes of Batenkov–Demanet–Goldman–Yomdin (arXiv:1809.00658),
cited in the P15 freeze. Ours: the EP ⇄ confluent cluster
identification, step A, the exponent 0 of the control, and the
unification of the three steps in a single matrix.

The program's analytic backbone (CRB hierarchy) is COMPLETE:
exponent 0 (control, theorem), p−1 / 2p−2 / 2p−1 (Vandermonde),
N−1 (symmetric Jacobian). The RECONSTRUCTION cost law
(ε ~ e^{−αN}/√d, halving at the EP) is a separate law and proceeds
with its own EGB validation: not covered by this document.

## Extension to counting statistics and the quantum Fisher information (P20, 2026-09-09)

The theorem above assumes additive Gaussian noise, where the Fisher
matrix is J^T J and analyticity of the channel is the whole story. Under
photon counting the Fisher information carries a 1/n_k factor per
detection mode, and Tsang, Nair and Lu (PRX 6, 031033, 2016) showed that
a mode whose population vanishes LINEARLY in the parameter gives a
Fisher information that stays finite for the separation of two
incoherent sources (constant Fisher for the gap: exponent 0 instead of
1). P20 (`FROZEN_P20_RAYLEIGH_EP.md`, `RESULTS_P20_RAYLEIGH_EP.md`) asks
whether this can happen at an EP.

Statement. Let epsilon be the physical unfolding parameter
(rho ~ epsilon, transversal), and let the source have second-order
statistics analytic in epsilon and positive semidefinite. Then the
population of every fixed detection mode is a nonnegative analytic
function of epsilon, hence either nonzero at the EP or vanishing to
EVEN order; the counting Fisher information for epsilon is finite at
the EP, the control exponent stays 0 and the gap exponent stays 1, for
any mode-resolved or direct photon-counting measurement and for the
quantum Fisher information of classical (zero-mean Gaussian) light.

Proof. A nonnegative real-analytic function with a zero at epsilon = 0
has a zero of even order 2m; then (dn/depsilon)^2 / n ~ epsilon^{2m-2}
is finite. The quantum Fisher information of a Gaussian state with
analytic, full-rank-regularized covariance is analytic; the dark-mode
contribution is the same even-order ratio. QED.

Loophole. Tsang's linear population requires a source whose statistics
are fixed in the eigenmode amplitudes as s -> 0: since the eigenmode
amplitudes of any finite source scale as 1/s, this is a statement about
s = sqrt(epsilon), non-analytic in the physical parameter. It is the
only loophole found; partial coherence does not close it (the curse
resurges only at exactly full coherence).

Verification (P20, four-digit): coherent source 0.0000 / -1.0000 under
counting, direct detection and QFI; eigenmode-incoherent fixed-variance
source +0.5000 / 0.0000 (Tsang reproduced in the time domain, classical
counting and QFI agree); port-incoherent analytic source in four
configurations 0.0000 / -1.0000, with the tuned configuration's total
population vanishing with slope 2.0000 (even order, as the proof says).
