# ERRATA

**Current status: E3 supersedes E1 and E2. No single extinction threshold exists; see E3 for the current statement.**

## E1 (2026-08-29, corrected in v1.2): EP-extinction threshold

**v1.0–v1.1 claimed:** λ_ext = 0.1091 ± 0.0002, with no mechanism relating it
to any known threshold.

**Corrected result:** λ_ext = 0.1248 ± 0.0007 — numerically consistent (1σ)
with the **exact eikonal-instability threshold λ_GB = 1/8** of the D=5
Gauss–Bonnet black brane (Konoplya–Zhidenko, arXiv:1705.07732). The mirror-EP
pair annihilation therefore appears to BE the eikonal spectral reorganization,
seen through non-Hermitian (exceptional-point) structure. This upgrades the
extinction from "numerical juxtaposition, no mechanism" to a
mechanism-candidate statement; exactness (λ_ext ≡ 1/8) is conjectured, not
proven.

**Cause of the error:** for λ > 0.109 the negative dip of the split function
ρ(q²) becomes narrower (width ≲ 0.1 in q²) than the q²-scan step (0.2) used in
the original existence test, so the collision was stepped over. The corrected
hunt uses fine steps (0.02), collocation identity tracking at order 88, and a
mirror-symmetry gate |ω₂ + ω̄₁| < 1e-4 that rejects wrong-pair contamination.
Between λ ≈ 0.113 and 1/8 the dip skims zero (an extended near-marginal band)
— data: `results/threshold_fine.json`, `results/eikonal_test.json`.

**What is unaffected:** every other number in the repository (the cost law,
halving 9/9, the zero-parameter α, SXS, QPU, Murch reanalysis). The statement
"the EP survives the entire causality window and beyond" is strengthened: it
survives from the causal window all the way to the eikonal threshold.

Method lesson, stated plainly: existence scans must resolve the narrowest
feature they are probing; our own frozen-prediction discipline (F1–F3 of
`results/FROZEN_META_EP.md`) is what caught the artifact.

### E1 addendum (same date, later runs)

Repeat scans across the boundary show run-to-run scatter (one contradictory
point at λ=0.1251 in a degraded-tracking run); the quoted bar is widened to
λ_ext = 0.1248 ± 0.0007 accordingly. Exactness against 1/8 is OPEN: settling
it needs a method that does not fight the deep-q² tracking (a direct
eikonal-limit analysis of the radial equation is the planned route). Further
findings of the same campaign, reported as-is per the frozen protocol
(results/FROZEN_META_EP.md): the dip HALF-WIDTH is roughly λ-independent
(~0.05–0.09) rather than shrinking as a fold would predict (F1 exponent ~0.3,
not 0.5) — the structure is an extended near-marginal band, not a simple
fold; and the F4 exponent measurement at/inside the band is NOT reliable with
the current scanning method (multiple mirror pairs defeat identity tracking —
two failed attempts documented in the session logs). These are open problems,
not claims.

## E2 (2026-08-29) — λ_ext corrected AGAIN: 0.1150 ± 0.0005; the "≈ 1/8" coincidence of E1 is retracted

**Corrected statement.** The mirror-EP pair of the fundamental scalar QNM
annihilates at λ_ext = 0.1150 ± 0.0005. Both previously published values are
wrong: 0.1091 (v1.0–v1.1) and 0.1248 ± 0.0007 ≈ 1/8 (v1.2, errata E1). The
conjectured coincidence with the Konoplya–Zhidenko eikonal-instability
threshold λ_GB = 1/8 is therefore retracted in full.

**What went wrong, both times.** Both earlier numbers came from Chebyshev
collocation scans in the deep-spacelike region (q² ≈ −33), where the
collocation eigenproblem has conditioning ~1e10 — the exact pathology that
motivated building the shooting solver in the first place. The collocation
"ρ-dips" between λ = 0.116 and 0.1245 that E1 promoted to a corrected
threshold do not reproduce under the shooting solver: they were near-miss /
identity-tracking artifacts. E1 replaced one artifact with another.

**Arbitration method (trusted instrument).** The shooting solver (validated
against the AdS₅ literature value to 1e-8) marches the fundamental mirror
pair down in q² and profiles ρ(q²) = ((ω₁−ω₂)/2)², continued in λ
(`scripts/shooting_ep_hunt.py`, `scripts/rho_profile.py`; data
`results/shooting_ep_hunt.json`, `results/rho_profile.json`):

| λ | ρ_min over q² ∈ [−37, −31] | sign crossing (EP)? |
|---|---|---|
| 0.105 | EP at q²=−34.39 | yes |
| 0.108 | EP at q²=−34.10 | yes |
| 0.114 | −8.5e-16 (EP at q²=−33.49) | yes |
| 0.1145 | −4.1e-17 (q²=−33.45) | yes |
| 0.1150 | +4.5e-13 (grazing) | no |
| 0.1155 | +0.158 | no |
| 0.118 | +0.492 | no |
| 0.122 | +1.495 | no |

**What survives.** Everything built on shooting data is untouched: the
critical-cost law, the exact halving at the EP across nine couplings
(including λ = 0.095, 0.105 in the acausal band — both below the corrected
λ_ext), the zero-fit-parameter α prediction, the two-saddle structure, and
the EP trajectory q²_c(λ). What dies: the "extended near-marginal band
λ ∈ [~0.113, 1/8]" of E1 (collocation artifact) and any eikonal-threshold
unification. λ_ext = 0.1150(5) sits strictly between the causality bound
9/100 and the eikonal threshold 1/8 and, as far as we can tell, coincides
with neither. The E1 addendum's F1/F4 "band structure" measurements are void
for the same reason.

**Open at extinction.** The ρ(q²) profile near λ_ext is a narrow (< 0.05 in
q²) near-zero spike on a broad positive bowl; the annihilation normal form
(simple fold vs level-crossing between mode families) and the exact value of
λ_ext remain open. A horizon-algebra hypothesis (threshold at
b''(1)/b'(1) = 2, i.e. λ = 1/8 exactly) was formulated and is now refuted by
the same measurement — recorded here as a tested-and-killed mechanism.

**Process note.** This is the second correction of the same quantity, caught
by the project's own instrument-arbitration discipline (never let a claim
rest on the instrument with known pathology in the relevant regime). The
frozen predictions F1–F4 (`results/FROZEN_META_EP.md`) that E1's picture kept
failing were the tell.

## E3 (2026-08-30) — the single-threshold concept is retracted: EP extinction is family-by-family

**Corrected statement.** There is no single λ_ext at which "the" mirror EP of
the EGB scalar family is annihilated. What the shooting solver (trusted
instrument) shows: (i) the fundamental-pair EP survives at least to
λ = 0.1155 as a needle of width < 2×10⁻⁴ in q² (micro-grid dq = 2×10⁻⁴:
ρ_min = −2×10⁻¹², two sign crossings) — the E2 value λ_ext = 0.1150(5)
measured the instrument's resolution, the third consecutive number to fall
this way (0.1091 in v1.0–1.1; 0.1248 in v1.2; 0.1150 in v1.3); (ii) deeper
overdamped families carry GENUINE mirror EPs beyond every published value —
confirmed with full walls (ρ excursion ≈ 4, |Re ω| up to 2.0) and a zero
touch at λ = 0.120 (ω_c = −9.73i, q² ∈ [−32.300, −32.285]), with a near
touch at λ = 0.1245; (iii) at λ = 1/8 an identity-free census (16 ω-seeds ×
dq = 0.1, micro-refined at 2×10⁻⁴) found only trivial structures.

**Classification criterion (method lesson).** A ρ sign crossing is an EP
only if the profile has walls (ρ excursion ≳ 10⁻²) and real splitting
outside the collided band. Flat profiles (|ρ| ~ 10⁻⁷⁻¹⁰ over wide windows)
are near-parallel purely-imaginary towers crossing ON the axis — diabolic,
not exceptional. Naive censuses conflate the two.

**Final statement.** Genuine mirror EPs exist at least to λ = 0.120
(wall-classified) and nearly touch at 0.1245; none was found at 1/8 (finite
census — not an exhaustiveness proof). The deep spacelike sector is a
stratified forest of mirror families, each with its own EP curve and its own
termination. Nothing built on individual EPs (the cost law, the halving, the
zero-parameter rate, the two saddles) depends on where the last family ends.
Data: results/micro_needle.json, results/forest_scan.json,
results/wide_profile.json, results/deep_family.json.
