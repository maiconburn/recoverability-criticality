# Cross-family test of the critical-cost law (deep family, λ=0.120): QUARANTINED FINDING

Status: measured in one session (2026-08-30); same-day quarantine rule
applies: reported as data + candidate reading, NOT as a claim.

## Setup
Anchor: the wall-classified deep-family mirror EP at λ = 0.120
(q²_c = −32.285, ω_c = −9.730063i, anchor gap 3.1×10⁻⁶). Constrained-Padé
reconstruction ladder, full validation driver adapted
(`scripts/run_validation_deep.py`, forest guard |Δq²| < 0.5), per-level EP
relocation. Data: `results/validation_deep.json`, `results/deep_ladder_final.json`.

## What is solid
- **The exponential structure transfers**: α(d) = 0.805 constant across
  three decades of distance (d ∈ [3.2×10⁻⁴, 10⁻¹]), like the fundamental
  family.
- Anchor floor ~3×10⁻⁶ saturates d = 10⁻⁴ and the N = 15 EP point: bounded
  and understood.

## What did NOT reproduce
- **Rate halving at the EP**: α_off/α_EP ≈ 0.7–1.1 measured (prediction 2),
  using the clean odd-N subsequence (5, 7, 11, 13).
- Strong parity systematic: even-N reconstructions give ε(EP) ~ O(1)
  (0.85/0.42/0.88 at N = 8/10/12) even with relocation |shift| ≤ 0.09,
  while odd-N decays five decades. Unexplained; contaminates any strong
  conclusion. N = 3, 6, 9, 14 lost to relocation failures (forest guard or
  no EP).

## Candidate readings (to be arbitrated later)
1. **Isolation condition**: the halving derivation assumes an ISOLATED
   EP-2; the deep EP sits in the dense near-degenerate forest (E3), which
   can contaminate the Puiseux structure. Halving would then be a property
   of isolated EPs, a scope refinement of the law, testable by measuring
   halving vs distance-to-nearest-neighbor structure.
2. Family-specific law (halving only for the fundamental pair): a weaker
   prior, would require understanding why.
3. Measurement artifact tied to the parity systematic: must be excluded
   first before any physics reading.

## Next stress tests (not run)
- Diagnose the even-N pathology (pair identity at the reconstructed EP).
- Repeat at a second deep-family point (λ = 0.117 needle) and at a
  fundamental-family EP with an artificially crowded neighborhood.

## Addendum (same session): parity diagnosed; anti-halving persists

Re-measurement of the even N with the mirror gate and correct seed
(`results/even_fix.json`): N=6 → 4.9e-3 and N=10 → 6.4e-5 CLEAN UP
(secant basin artifact confirmed); N=8 converges to a DIFFERENT mirror
pair at ω = ±0.226 − 8.91i: a NEIGHBOR from the forest, direct
contamination observed; N=12 has no mirror pair near −9.73i. Clean series
(N=5,6,7,10,11): α_EP ≈ 1.24. With α_off = 0.80: **ratio
α_off/α_EP ≈ 0.65, anti-halving** (at the EP it converges FASTER; the
fundamental halves, ratio 2). Still quarantined; the leading reading
remains the isolation condition, now with the N=8 neighbor as direct
evidence of contamination. Discriminating test launched: same protocol at
the λ=0.117 point (narrower needle ⇒ more contaminated ⇒ even smaller
ratio, if reading 1 is right).

## Second point (λ=0.117): replicates the non-halving

Genuine mirrored anchor (gap 4.1×10⁻⁵, ω=−10.2945i, mirror at 1.5×10⁻⁶),
all 13 levels clean (no parity pathology here):
α_off ≈ 0.74 (d=10⁻¹, N=6→15, 3 decades); α_EP ≈ 0.89 (N=6→10, before the
anchor floor ~1.1×10⁻⁴ that dominates N≥11). **Ratio ≈ 0.83, no halving**,
consistent with λ=0.120 (0.65). Two independent measurements in the forest
region: the EP factor-2 does NOT appear in the deep stratum; the ratio
stays at 0.65–0.9. The isolation reading remains the leader; remaining
discriminator (not run): halving at a fundamental EP with an artificially
crowded neighborhood, which separates physics (isolation) from
measurement artifact.
Data: results/validation_deep_0.117.json.

## CORRECTION (same session, channel-separated analysis): "non-halving" is VOID; test INDETERMINATE

Separating the channels of the saved pairs (μ = mean, ρ = ((ω₁−ω₂)/2)²):
1. **The 0.65–0.83 ratios measured the μ channel**, not the critical
   channel: |δμ| decays with α_μ = 1.15 (λ=0.120) and dominates the
   pair_error of the clean levels. The law's halving is a statement about
   the ρ channel (2α_EP/α_ρ), as in the original validation: my
   simplified test measured the wrong thing.
2. **The ρ channel sits under the anchor floor**: |δρ| ≈ 8×10⁻¹² flat from
   N=5 to 15: exactly (anchor_gap)² = (3.1×10⁻⁶)². The true δρ is smaller
   than what is measurable already at N=5. There is no evidence of
   non-halving nor of halving: **INDETERMINATE due to floor**. Measuring
   it would require an anchor with gap ≲ 10⁻⁸.
3. The isolation hypothesis died by independent data and stays dead:
   Δω to the nearest neighbor is SMALLER in the fundamentals that halve
   (0.55, 0.62) than in the deep ones (2.71, 1.09): the proposed
   discriminator is inverted in the data.

Final state of this line: transfer of the exponential structure (α_off
constant over 3 decades) CONFIRMED at the two deep points; halving in the
deep stratum: OPEN (instrument-limited, not decided). The
claim→refutation→correction cycle of this section (non-halving → void
within hours) is one more case of the quarantine rule working.

## Deep-stratum kernel: decoupling bound (closure of the line)

Bernstein bumps in three ε regimes (1e-6, 1e-3, 1e-9), mirror and
identity gates (`scripts/kernel_compare.py`, `results/kernel_compare_*.json`):
- Fundamental (λ=0.105): horizon-dominated kernel reproduced
  (K = 50–483 at z ≥ 0.5, centroid 0.752: matches P4). Tool validated.
- Deep (λ=0.120): ALL measurable ρ response sits at the anchor floor
  (δρ ~ 1e-11) at any ε of the linear regime; the apparent peaks
  (z=0.5/0.875 in the run without the gate) do not reproduce across
  ε's: identity artifacts. Floor-proof result: **K_deep < 10⁻² at every
  accessible z ⇒ the deep critical channel is ≥4 orders less coupled to
  the interior metric data than the fundamental one.**

Final state of the line on this machine: (i) the exponential structure
transfers (α_off constant, 2 points); (ii) halving: indeterminate due to
floor; (iii) deep ρ channel metrically decoupled (bound); (iv) isolation
hypothesis dead; (v) address of the deep channel: not resolvable with
the current solver (would require floor ≲ 1e-16). Future measurements
require an instrument with ρ precision beyond rtol 1e-10.
