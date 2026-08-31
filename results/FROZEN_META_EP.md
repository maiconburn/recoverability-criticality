# Frozen prediction: EP annihilation point (2026-08-29, before the measurements)

Structural hypothesis: λ_ext is a PAIR ANNIHILATION of EP-2 (fold of ρ(q²)):
ρ(q²,λ) ≈ (ρ''/2)(q²−q²_m)² + μ·(λ−λ_ext) locally.

Predictions (to be measured next):
- F1: for λ<λ_ext, TWO nearby real crossings of ρ, collapsing at λ_ext;
  separation of the two EPs ∝ (λ_ext−λ)^{1/2}.
- F2: ρ_min(λ) linear in λ through λ_ext.
- F3: for λ>λ_ext, a pair of complex-conjugate zeros with Im q²_c ∝ (λ−λ_ext)^{1/2}.
- F4 (the consequence for the COST LAW, the central test): at the
  annihilation point (λ_ext, q²_m), the gap closes linearly in |q²−q²_m|,
  so the amplification exponent of the critical channel DOUBLES:
  γ_meta = 1.0 (vs 0.5 at the ordinary EP-2), WHILE the halving in N
  (√ response in δρ) REMAINS: ε(N, d=0) ~ e^{−αN/2} still.
Criteria: F1–F3 with exponents 0.5±0.1; F4 with γ_meta = 1.0±0.15 and a
halving ratio 1.0±0.2. Anything else: different structure; report as is.

## FINAL VERDICT (2026-08-30, documented closure: audit)

The object of these predictions (the "meta-EP": annihilation at a single
λ_ext) was dissolved by ERRATA E3: extinction is family-by-family and
there is no single threshold. Consequence for each frozen prediction:
- F1 (half-width exponent 0.5): E1-era measurements gave ~0.3 and were
  VOIDED by E2 (collocation artifacts); with E3, the very quantity
  "half-width of λ_ext" stopped being well defined. **Void by concept.**
- F2 (linearity of ρ_min(λ)): same fate: the shooting data
  (rho_profile.json) show ρ_min with a needle structure not captured by
  a linear fit; it never received a formal fit because the premise fell.
  **Void by concept.**
- F3 (migration to complex q²): remains genuinely OPEN
  (complex_migration.json was inconclusive near the boundary; README
  §1.3 lists it as not determined). **Open.**
- F4 (γ_meta = 1.0 at the annihilation): two measurement attempts failed
  due to identity/floor (documented in ERRATA E2 and
  RESULTS_DEEP_FAMILY); without a single annihilation point, the
  definition needs to be redone per family. **Void by concept.**

Nothing here changes the frozen texts above (kept for audit); this
addendum only closes the record that the 2026-08-30 audit flagged as
pending.
