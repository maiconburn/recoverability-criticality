# P4 phase 2: the measured kernel, the CMI hypothesis refuted, and the two saddles (2026-08-28)

## What was done

Sensitivity kernel K_λ(z) of the critical channel measured directly (Bernstein polynomial bumps, linear response at the EP) on the 7 backgrounds; entanglement dictionary z_t(ℓ) (RT strip) per background; frozen hypothesis H_CMI: z̄_K(λ) = z_t(κ/|q_c|) with a single κ calibrated at the anchor.

## Result 1: the kernel lives at the horizon

K(z) is **horizon-dominated** (centroid 0.74–0.90, typical peak z≈0.96), oscillating with nodes (complex phase of the mode). The v2 effective address z*≈0.35 is NOT where the kernel lives: it is a **saddle**, a competition between the kernel (which grows toward the horizon) and the approximation error (which decays toward the horizon).

## Result 2: H_CMI refuted

| λ | measured z̄_K | predicted z_t(κ/\|q_c\|) | residual |
|---|---|---|---|
| −0.100 | 0.878 | 0.965 | −0.087 |
| −0.050 | 0.865 | 0.967 | −0.102 |
| +0.020 | 0.868 | 0.792 | +0.076 |
| +0.035 | 0.899 | 0.796 | +0.103 |
| +0.050 | 0.893 | 0.801 | +0.092 |
| +0.065 | 0.737 | 0.806 | −0.070 |
| +0.080 | 0.813 | 0.813 | 0 (calibration) |

Systematic sign structure, opposite by branch: the prediction falls with |q_c| (a 1.8× lever), the measured value is flat. **The kernel's scale does not come from the boundary entanglement screening length: it comes from the mode structure at the horizon (flat in λ).** The route "CMI predicts the address" dies in its natural form.

## Result 3: the two saddles (discovery)

The product |K(z)|·|δb_N(z)| has **two maxima** (horizon bump and edge bump); dominance switches at N≈9. Derived prediction: the rate in split windows must fall from steep to shallow. Verified on the already measured data (λ=0.08):

> α(N∈[4,8]) = **1.460** · α(N∈[10,15]) = **0.677**

The "α_ρ = 0.851" of the earlier rounds was the window average of a **crossover between two informational addresses**. The v2 law remains exact (it computes the full functional); its correct reading: an observable can have **multiple informational depths, with dominance depending on the budget N**: a genuine and testable refinement of the turn 110 concept.

## P4 balance

- **The "approximation" half** of the law (Green profile of the Stahl set): derivable from classical theory; the 𝒥/Abel object from the conversation maps here: no informational content beyond the relabel.
- **The "kernel" half**: mode physics at the horizon; NOT derivable from the tested entanglement scale.
- Consequence: "information as source" does not survive in the tested holographic sector. The last experimental redoubt of the ontology remains the laboratory (P6), with the protocol ready.

## Reproduction

`results/p4_kernels.json` (kernels), `results/p4_predictions.json` (phase 1), scripts from this round. z_t dictionary: RT integral with exact b(z); JM correction O(λ) documented as a pending refinement (it does not change the sign structure of the verdict).
