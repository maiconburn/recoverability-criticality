# Session 2026-08-29 (post-E2): gaps, needle, forest, dS (NOT COMMITTED)

Local state, by the author's order: nothing committed until release.

## 1. The λ_ext crisis continues: needle and forest

- Micro-grid (dq=2e-4) at λ=0.1155: **THE EP STILL EXISTS** (2 crossings,
  ρ_min=−2e-12, q²=−33.329, ω=−8.23i). E2's λ_ext=0.1150(5) is already
  outdated: 0.1091 → 0.1248 → 0.1150 → >0.1155.
- Pattern: the ρ<0 valley narrows fast with λ; every finite resolution declares
  a false extinction. Half-width ~0.015 at λ=0.113 (dq=0.01 catches it), <2e-4 of
  structure at 0.1155.
- Aggravating factor: complex Newton and the micro-grid find near-zeros at the SAME q² with
  DIFFERENT ω (−7.8i vs −8.2i): multiple nearly-degenerate pairs
  coexist ("forest"). The "fundamental pair" identity dissolves there.
- Working hypothesis: the "annihilation" is not a clean fold; it is absorption of the pair
  into a forest of crossings between families. If confirmed, E2 needs an
  E3 reformulating the nature of the threshold (not just the number).
- In progress: forest_scan.py (census without identity, grid of ω seeds,
  λ∈{0.117, 0.120, 0.1235}) to decide whether ANY mirror pair still crosses
  zero at those heights.
- Killed today: the turning-point hypothesis (real V_eff without turning points in the
  bulk; the structure is complex Stokes; open).
- Known junk: normal_form_map with different continuation chains gives
  path-dependent results (0.114: +0.05 vs 0.1143: −9e-14), which
  confirms branch multiplicity; do not use for exponents.

## 2. P8 step 1, POSITIVE VERDICT: the dS tower has a mirrored EP-2

Setup: massive scalar in the static patch of dS4 (L=1), ℓ=0, Chebyshev
collocation with ansatz (1−x²)^{−iω/2} → quadratic eigenvalue problem.
Derived equation: x(1−x²)u'' + (2iωx²+2−4x²)u' + (ω²x+3iωx−m²x−εx³(1−x²))u=0.
Validation: ν=0.9 → −0.6i, −2.4003i, −2.599i (analytic: −0.6, −2.4, −2.6). ✓

Test at the degenerate point ν=1 (m²=5/4), collision Ω=2.5, perturbation εx²(1−x²):

| ε | split |
|---|---|
| 0.64 | 1.479 |
| 0.32 | 1.192 |
| 0.16 | 0.949 |
| 0.08 | 0.726 |
| 0.04 | 0.536 |
| 0.02 | 0.400 |

- The pair leaves the imaginary axis as a **mirror pair (ω, −ω̄)**: the signature of
  an EP (a diabolic pair of real eigenvalues of a real operator would repel ALONG
  the axis).
- Local log-log slopes: 0.31→0.44, rising toward 0.5 as ε→0; fit
  s²=c₁ε+c₂ε²: c₁=6.0>0 dominant → √ε opening. **EP-2 (Jordan block)
  CONFIRMED.** Preregistered kill criterion (DIRECAO_P8): PASSED.
- Implication: the cosmological horizon carries the same mirrored EP class
  as the program; a candidate for a NETWORK of EPs at ν∈ℤ (m²L²=9/4−k²).
- Numerical limit: the deeper points of the network (ν=2/Ω=3.5; ν=1/Ω=4.5)
  are inaccessible to collocation of order ≤120 (steep (1−x)^{−Ω/2} mode; not even
  the ε=0 pair appears). The network beyond the first point: OPEN, requires an adapted basis.
- Data: results/ds_jordan_test.json. Scripts: ds_jordan_v2.py (bisection,
  failed validation; keep as a record), inline QEP collocation (move
  to a script when consolidating).

## 3. Queue

- Forest scans (running) → decide E3.
- If the forest confirms living pairs: reformulate the threshold as the "λ of absorption
  into the forest" and measure crossing density vs λ.
- P8 step 2 (when activated): adapted basis for the network; quasi-dS with
  physical slow-roll as the deformation; distance to the EP as a function of (ε₁, η).
