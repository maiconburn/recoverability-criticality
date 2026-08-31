# Stahl capacity v2: the closed law (2026-08-28)

## Central result

**α_ρ(λ) is now a prediction with zero fitted parameters**, computable without any QNM ladder measurement:

> **α_ρ(λ) = decay rate of the linear functional δρ_lin(N) = D_ρ[δb_N]**,
> where δb_N = error of the constrained Padé of b (approximation theory only) and D_ρ = linear response of ρ at the EP (one cheap solve per N on the exact background).

### Validation on the 5 λ already measured (model built without using the rates)

| λ | α_lin (predicted) | α_ρ (measured) | z |
|---|---|---|---|
| −0.100 | 1.027 | 1.026 ± 0.093 | 0.0 |
| −0.050 | 1.172 | 1.173 ± 0.084 | 0.0 |
| +0.020 | 1.358 | 1.360 ± 0.121 | 0.0 |
| +0.050 | 1.062 | 1.063 ± 0.087 | 0.0 |
| +0.080 | 0.872 | 0.851 ± 0.130 | +0.2 |

Regression: slope 1.040, **R² = 0.9988** (the K1-v2 gate required ≥ 0.9).

### Preregistered test on virgin λ (frozen BEFORE measuring)

| λ | frozen | measured | z |
|---|---|---|---|
| 0.035 | 1.1596 | 1.1595 ± 0.077 | −0.00 |
| 0.065 | 0.9239 | 0.9244 ± 0.073 | +0.01 |

## The structure behind it (the physical content)

1. **Empirical Green profile**: α_pt(z) = pointwise rate of |δb_N(z)|: it grows monotonically from the edge (≈0.47) to the horizon (≈3.1). It is the Green's function of the Stahl set measured directly, without conformal mapping.
2. **Depth of the observable**: α_lin coincides with α_pt(z*) at **z* ≈ 0.30–0.40 for all λ**: the EP's critical channel "reads" the geometry in the middle of the bulk. The "informational depth of the observable" (turn 110) became a measurable number: z*.
3. **Why the v1 proxy died**: the distance to a branch point ignores the full Green profile and the location of the kernel. The rate is not a property of the singularity alone: it is the Green AT THE POINT where the observable lives.

## Round bonus

- **Universal halving extended: 7/7 backgrounds** (1.000, 1.000, 1.000, 1.001, 1.004, 1.001, 1.029).
- EP trajectory refined with the new points: q²_c smooth in λ (−18.27 → −17.83 → −17.34 → −17.02 → −16.79 → −16.15).
- Channel splitting: 1.24–1.56, persists across the whole family.

## Consequence for P4

The competition "singularity of B vs singularity of 𝒥" (phase 1) becomes **subsumed**: the exact predictor does not go through any distance-to-singularity: it goes through the Green profile + kernel. The live P4 question becomes: **does the boundary CMI predict z*?** (i.e., is the kernel's depth derivable from entanglement information?). That is the correct formulation for phase 2.

## Reproduction

`results/v2_linear.json` (5 λ), `results/v2_frozen_fresh.json` (freeze), `results/v2_fresh_test.json` (virgin test). Method: section B/C of this round's scripts (linear response via ShootingSolver at the EP; new EPs by continuation in λ with Puiseux seeds).
