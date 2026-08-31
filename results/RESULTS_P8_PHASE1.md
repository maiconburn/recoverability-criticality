# P8 phase 1: the cosmological exceptional point

Date: 2026-08-29/30. Status: internal chain complete; NOVELTY NOT AUDITED
(external claims forbidden before the literature audit; cosmological
collider: Arkani-Hamed-Maldacena and follow-ups; ν∈ℤ degeneracies and log
terms may be partly known).

## Chain (each link machine-verified in this session)

### Link 1: EP-2 at the de Sitter horizon: DEMONSTRATED
Massive scalar, static patch dS₄, ℓ=0, QEP collocation with ansatz
(1−x²)^{−iω/2} (equation: x(1−x²)u''+(2iωx²+2−4x²)u'+(ω²x+3iωx−m²x)u=0;
validated against the analytic tower at ~10⁻³).
At the point ν=1 (m²=5/4, units H=L=1), ω₀=−5i/2:
- smallest singular value of L(ω₀): 9.4e-13 (rank deficiency 1 ⇒
  geometric multiplicity 1, NOT diabolical);
- Jordan condition ⟨w₀|L'(ω₀)|u₀⟩ = 1.3e-12 (scale O(1)) ⇒ EP-2;
- opening under δV = εx²(1−x²): perturbation theory of the quadratic pencil
  gives (δω)² = (9/4)ε EXACT (c₁ = 2.25000 numerical) ⇒ s = 3√ε; the
  numerical splitting series converges: s²/ε = 8.0 (ε=0.02) → 9 (ε→0). ✓

### Link 2: observable signature: logarithmic term in the squeezed bispectrum
The squeezed expansion carries the towers (k_L/k_S)^{Δ±+2n}, Δ± = 3/2±ν.
At ν=1: Δ−+2 = Δ+ = 5/2, two terms coincide; the standard mechanism of
degenerate exponents + Jordan block forces
    log(k_L/k_S)·(k_L/k_S)^{5/2}.
(Analytic derivation of the coefficient: pending, next task; the mechanism
is standard, the new content is the identification with the EP-2 of the
static patch.)

### Link 3: cost law in the observable: σ(ν̂) ∝ |ν−1|^{−1}
Exact Cramér-Rao (3-parameter Fisher (ν, A₊, A₋) marginalized), signal
S(r) = A₊r^{3/2+ν} + A₋r^{7/2−ν}, r∈[0.05,0.6], 80 points:
global exponent −1.022, local slopes → −1.001 monotonic. Clean cost
divergence at the critical point. (Naive MC gives an optimizer artifact:
piling up at ν=1 with bias +0.3; use CRB/likelihood profiling.)

## Candidate statement (calibrate after the audit)
Spectator fields with m² = 5/4·H² (ν=1) are a critical point of
cosmological spectroscopy: mass estimation from squeezed correlators has
divergent cost ∝ 1/|ν−1|, and exactly at criticality the bispectrum
develops logarithmic running, an observational fingerprint of an
exceptional point of the cosmological horizon. Direct connection to the
cosmological collider program (CMB-S4, LSS, 21cm).

## Pending items
1. Novelty audit (blocking for any external claim).
2. Analytic coefficient of the log term (link 2).
3. ν=2,3,... network: adapted numerical basis (collocation loses deep modes).
4. Quantitative link to physical slow-roll (effective ν of the spectator in
   quasi-dS; distance to the EP as a function of inflation parameters).
5. Map the link-3 task onto the program's 1/2/3 hierarchy (here: real
   exponents + free amplitudes ⇒ −1; formalize).

## Addendum (same session): link 2 EXACT

Soft factor of the ν=1 spectator (dS mode function, H_1):
    (π²/4)·x³·|H₁(x)|² = x + [−ln x + c₃]·x³ + [¼·ln²x + …]·x⁵ + …
verified against mpmath at 10⁻²⁴. The log enters at relative order (k_L/k_S)²
with EXACT coefficient −1; the next order carries ln² (double tower
collision), a fingerprint specific to the Jordan chain, which an accidental
log does not produce. Calibration note: logs at integer ν are a classical
Bessel fact; the new content is (i) the identification with the EP-2 of the
static patch (rank proof + 9/4), (ii) the ln² as chain signature, (iii) the
cost law σ ∝ |ν−1|⁻¹ in estimation; the composite does not appear in
abstract searches (WebFetch/arXiv API; full-text audit pending).

## Addendum 2: FULL NETWORK + critical window formula

Direct rank test on L(ω₀) at the analytic network points (orders 140 and
200, stable): ν=1 (Ω=2.5, 4.5), ν=2 (Ω=3.5, 5.5), ν=3 (Ω=4.5), ALL with
rank deficiency 1 and ⟨w₀|L'|u₀⟩ ~ 10⁻¹²–10⁻¹⁴. **Every static-patch tower
degeneracy at ν ∈ ℤ is an EP-2** (EP lines: infinitely many collisions per
ν). The only non-tachyonic point: ν=1 ⇔ m² = 5/4·H².
(The earlier failure to "see" the deep points was in the global eigenvalue
solver; the rank test at the analytic ω₀ does not suffer from that.)

Cost-law constant (from the CRB table, r∈[0.05,0.6], 80 modes):
σ_CRB·|ν−1| = 10.2 (constant to <1% for |ν−1| ≤ 0.06). Hence, with total
signal-to-noise S in the squeezed sector:
    σ(ν̂) = 10.2 / (S·|ν−1|)   ⇒   irresolvability window
    |ν−1|* = √(10.2/S)
Inside it the error exceeds the distance to the critical point: the
spectator mass is IRRESOLVABLE. (S=100 → window 0.32; S=1000 → 0.10. The
constant 10.2 depends on the r window and the number of modes; recalibrate
per experiment; the STRUCTURE 1/(S·|ν−1|) is the content.)

## Addendum 3: EXACT THEOREM (Γ algebra) and internal corrections

Exact hypergeometric reduction of the validated equation (z=x²):
z(1−z)g'' + [3/2 − (5/2−iω)z]g' − [(m²−ω²−3iω)/4]g = 0, with
a,b = 3/4 ∓ ν/2 − Ω/2, c = 3/2 (ω = −iΩ). QNM condition (vanishing of the
ingoing branch in the connection formula): W(Ω) ∝ 1/[Γ(a)Γ(b)]. Towers
Ω = 3/2 ∓ ν + 2n (= López-Ortega ✓).

**Theorem (complete EP map):** the Jordan order of each QNM is the order of
the zero of W. Hence: (i) generic ν: all simple; (ii) ν ∈ ℤ⁺: each tower
collision is a double zero ⇒ EP-2, and NEVER of higher order (there are
only two Γ factors); (iii) ν=0: a≡b ⇒ the whole tower is EP-2 level by
level (the AHM logarithmic operator is level n=0). Exact unfolding at ν=1:
W ∝ [(ν−1)² − (Ω−5/2)²]/4 ⇒ Ω± = 5/2 ± (ν−1).

**Internal corrections (my own artifacts, caught by the theorem before any
external registration):** the numerical exploration of "EP-3/EP-4/order-7"
at ν=0 was an artifact of the matrix chain test (null-component
contamination in lstsq beyond k=2), WITHDRAWN; the "simple eigenvalue" at
Ω=1.5 was the collocation truncation splitting the degenerate pair. The ln²
observed at x⁵ in the soft factor is |mode function with log|², consistent
with EP-2.

Final status of phase 1: the EP structure of the scalar in the static patch
of dS resolved EXACTLY; the metrology layer (σ = C/(S·d), window
√(C/S), rescue through the log channel) verified numerically on that base.

## Addendum 4: slow-roll drift through the EP (pending item 4 closed, analytic)

In quasi-dS, ν² = 9/4 − m²/H² with H decreasing (ε₁ = −Ḣ/H²):
    dν/dN_e = −(m²/H²)·ε₁/ν = −(9/4 − ν²)·ε₁/ν  ⇒  at ν=1: dν/dN = −(5/4)ε₁.
A spectator near the EP is SWEPT through it at (5/4)ε₁ per e-fold. The time
(in e-folds) inside the irresolvability window |ν−1| < √(C/S):
    ΔN = (8/5)·√(C/S)/ε₁ ,
and since each mode k freezes at a different ν(N), the log signature is
LOCALIZED in a band Δln k = ΔN of the spectrum. Example: S=10³, ε₁=0.005 →
window |δν|<0.10, ΔN ≈ 32 e-folds, a wide band; S=10⁵, ε₁=0.02 → ΔN ≈ 0.8
e-fold, a narrow, localized feature. The band position measures WHEN
m²/H² crossed 5/4; the width measures ε₁/√S. This turns the EP into a
CLOCK: a log feature localized in k ↔ the instant of the critical crossing.
(Phase 2: do the honest mode-by-mode matching in quasi-dS; here it is the
adiabatic limit.)

## Addendum 5: closed form of C: attempt refuted

Natural hypothesis C = 1/(|A₊−A₋|·√F⊥) (r^{3/2}ln r channel with weight
(A₊−A₋)ν in the ν→0 limit): REFUTED. It predicted C ∝ 1/|A₊−A₋|
(19.7/6.6/3.9 for D=0.1/0.3/0.5) and the measured value barely moves
(1.79/2.0/2.28). The dominant information does not come from the
linear-in-ν channel; C remains a window-dependent numerical constant
(recalibrate per experiment). Do NOT publish the naive derivation.

## Addendum 6: cross-family universality (EGB, partial)

Padé reconstruction ladder anchored at the EP of the DEEP FAMILY (λ=0.120,
ω_c=−9.730063i, q²_c=−32.285, anchor gap 3.1e-6):
**α_off = 0.805 constant across 3 decades of distance**
(d ∈ [3.2e-4, 1e-1]: 0.8051/0.8051/0.8050/0.8048/0.8041/0.8021): the
exponential structure of the cost law transfers to the second stratum of
the spectrum. Halving at the EP: OPEN. The measurement requires relocating
the EP per level N; the simplified version showed an even/odd pathology at
d=0 (even N: ε~O(1), loss of identity) and relocations that wander in the
forest; the full adapted driver (run_validation_deep.py, guard |Δq²|<0.5)
is running. d=1e-4 saturated (anchor floor). Data:
results/deep_ladder_final.json.

## Addendum 7: exact signature at ν=0 (complete table)

(π²/4)·x³·|H₀(x)|² = x³·[ln²x + 2(γ−ln2)·ln x + π²/4+(γ−ln2)²] + O(x⁵ln²)
verified numeric×analytic to 5 places (residual 4e-13). Contrast of the two
critical points:
- ν=0 (m=3H/2): ln² at LEADING order, exact coefficient 1.
- ν=1 (m²=5H²/4): simple ln at RELATIVE order (k_L/k_S)², coefficient −1;
  ln² one order higher.
Signatures distinguishable from each other and from any accidental log: a
closed pair of fingerprints for the two observational targets.

## Addendum 8: PHASE 2 DYNAMICS: the addendum 4 clock NOT confirmed (downgraded)

Two honest dynamical tests in quasi-dS (ε₁=0.005, m²/H² crossing 5/4 at
N*=8; modes evolved from Bunch-Davies x=50 to deep superhorizon,
scripts p8_phase2_clock.py / p8_phase2_towers.py):
1. Late-time spectrum |σ_k|²k³: smooth local index, residuals +0.0000 in
   the crossing window (observable dominated by one tower, does not probe
   the log).
2. Two-tower decomposition with running adiabatic exponents: |B/A|(k)
   perfectly smooth through N* (15.6→6.7 monotonic, resid ~1.3e-3
   uniform), NO localized anomaly.

Theoretical reading of the null: the mode ODE is analytic in ν; the
exponents 3/2±ν do not collide during the evolution of a single k. The
EP's log term lives in the squeezed correlator (two scales compared at the
same late time) and is ATTENUATED by the sweep dν/dN ~ ε₁; the adiabatic
heuristic of addendum 4 ("log feature localized in k" = clock) does NOT
survive as stated. Status: addendum 4 DOWNGRADED to unconfirmed heuristic;
the correct statement requires the theory of the dynamical squeezed limit
(in-in with two scales), beyond the reach of this phase. The other parts of
P8 (Γ theorem, static metrology, exact signatures in strict dS) do not
depend on the clock and remain intact. Data: results/p8_phase2_clock.json,
results/p8_towers.json.

## Addendum 9: P8-F2: exclusion of the free sector as carrier of the signature

Two designs frozen and killed, with diagnosis:
- v1 (integer-exponent basis in the fixed-time spectrum): killed by a
  basis artifact. With ν ≠ 1 the non-integer exponents turn the log term
  into a spurious compensator (the control WITHOUT the crossing gave
  Δχ² = 70, the crossing gave ~1.7, a diagnostic inversion).
- v2 (per-mode residual against the exact static Hankel form with local
  ν): the collective residuals are smooth ln + ln²(k) with coefficients
  ∝ ε₁ (0.0996/−0.0057 → 0.1914/−0.0102 when doubling ε₁), present EQUALLY
  with and without the crossing (ratio ~0.6): a global adiabatic
  correction, with no structure localized at ν = 1.

**Conclusion (exclusion):** in the free-field sector, no non-analyticity
of the EP survives the quasi-dS sweep, neither in single-k (phase 2) nor
in the fixed-time two-scale object (F2). If the logarithmic signature of
the exceptional point exists dynamically, it lives exclusively in the
INTERACTING correlator (in-in bispectrum with a vertex), which is the
computation this program cannot do on this machine. This delimits the next
theoretical step precisely, and protects the paper from overclaim: the
exact strict-dS signatures (ln, ln²) hold in the adiabatic/static limit;
the swept version is an open in-in question.
