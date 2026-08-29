# Cross-family test of the critical-cost law (deep family, λ=0.120) — QUARANTINED FINDING

Status: measured in one session (2026-08-30); same-day quarantine rule
applies — reported as data + candidate reading, NOT as a claim.

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
- Anchor floor ~3×10⁻⁶ saturates d = 10⁻⁴ and the N = 15 EP point — bounded
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
   of isolated EPs — a scope refinement of the law, testable by measuring
   halving vs distance-to-nearest-neighbor structure.
2. Family-specific law (halving only for the fundamental pair) — weaker
   prior, would require understanding why.
3. Measurement artifact tied to the parity systematic — must be excluded
   first before any physics reading.

## Next stress tests (not run)
- Diagnose the even-N pathology (pair identity at the reconstructed EP).
- Repeat at a second deep-family point (λ = 0.117 needle) and at a
  fundamental-family EP with an artificially crowded neighborhood.
