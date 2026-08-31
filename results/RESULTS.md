# Numerical validation of the critical complexity law

**Date:** 2026-08-28 · **Benchmark:** 5D Einstein–Gauss–Bonnet black brane, λ_GB = 0.08 · **Verdict: the three preregistered structural predictions were confirmed; the frozen number of 1.47 levels/decade was measured at 1.45 ± 0.02.**

## 1. What was frozen

At turn 112 of the original conversation (the "Critical complexity law" node of the graph), before any calculation, it was preregistered that, for geometric reconstruction with error ε_g(N) ~ e^{−αN}:

| # | Prediction | Frozen form |
|---|----------|-----------------|
| P1 | amplification away from the EP | ε_ω(N,d) ∝ e^{−αN}/√d |
| P2 | rate at the EP falls by half | ε_ω(N,0) ∝ e^{−αN/2} |
| P3 | logarithmic informational cost | N_ε(d) = A + (1/2α)·ln(1/d) |
| P4 | numerical value | ≈ 1.47 extra levels per decade |

## 2. The exceptional point

The relevant EP is the collision of the fundamental scalar mode with its mirror partner (ω → −ω̄) on the real axis of q² (spatial momentum): the propagating → overdamped transition. The symmetry keeps the EP on the axis and makes ρ = ((ω₁−ω₂)/2)² a real function with a simple zero: a genuine second-order EP.

- **q²_c = −16.147205102**, **ω_c = −5.6738278 i** (horizon-radius units, boundary time normalization).
- Check: the ω₀/ω₁ pair used as the initial candidate **never collides**: the gap decays only asymptotically (~|q|^{−1/3}); the mirror collision is the nearest finite critical structure.

### Numerical method (the real obstacle)

Chebyshev collocation has an eigenvalue condition number ~10¹⁰ in this momentum region: a noise floor ~10⁻² in double precision, unusable at the EP. The validation uses a **shooting solver**: order-14 Frobenius series at the horizon, integration to z = 10⁻³, QNM = zero of the Wronskian W(ω) = z⁵ψ′. Nearly degenerate pairs are extracted by a local quadratic model of W (linear conditioning in the W noise, not √). Precision: ~10⁻⁹ far from the EP, ~10⁻⁵ at the EP (confirmed by robustness to rtol, horizon offset and boundary cutoff; ω_c stable to ~10⁻⁶). External validation: the AdS₅ fundamental (λ=0) reproduces the literature value 3.119452 − 2.746676i to 10⁻⁸.

## 3. Data

13 admissible Padé geometries (N = 2..12, 14, 15 near-horizon coefficients; N = 13 and 16 have a physical pole and are rejected by the preregistered protocol). For each N: error of the QNM pair at d = |q²−q²_c| ∈ {10⁻¹ … 10⁻⁴} and at d = 0. Exact channel decomposition via ω± = μ ± √ρ:

- **regular channel** = |μ_N − μ| (flat in d);
- **critical channel** = |√ρ_N − √ρ| (the object of the predictions);
- δρ_N = geometric perturbation in the critical channel, measured at d=0.

## 4. Results

### P1: 1/√d amplification: **CONFIRMED**

Free exponent fitted in the critical channel, window d ∈ [3×10⁻³, 10⁻⁴] (between the large-d branch, where the slope difference δa·d dominates, and the saturation):

> **γ = 0.498 ± 0.062** (predicted: 0.5), consistent across all N = 5..15.

The total error shows the TWO components the theory itself predicted: the regular plateau (the refined law κ_O·e^{−2Ng_O} of turn 110) and the critical term growing as d^{−1/2} until it saturates.

### P2: rate halved at the EP: **CONFIRMED**

| rate | value | R² |
|------|-------|-----|
| α_ρ (critical channel δρ_N) | 0.851 ± 0.130 | 0.83 |
| α_EP (spectral error at d=0) | 0.438 ± 0.068 | 0.82 |
| **ratio 2·α_EP/α_ρ** | **1.03 ± 0.22** | predicted: 1 |

And stronger: the square-root structure with **unit coefficient**, point by point over ~5 decades of δρ:

> **ε_ω(N,0) / √δρ_N = 1.03 ± 0.09** for all N = 4..15.

Internal contrast predicted by the theory: the **position** of the EP converges at the full rate (α_shift = 0.848 ≈ α_ρ), while the **spectrum at the EP** converges at half: exactly the √ sensitivity signature of a second-order EP.

### P3: logarithmic cost: **CONFIRMED**

N*(d) measured by per-distance regression of the critical channel (target ε = 10⁻⁵): 5 points aligned on a straight line (R² = 0.999) between 2 and 4 decades of approach.

### P4: levels per decade: **1.45 ± 0.02**

> Frozen: **≈ 1.47** (with α = 0.784 from the exploratory fit) · Derived from the measured α_ρ: **1.35** · **Measured: 1.450 ± 0.019**

The structural part (logarithmic growth, coefficient 1/2α) is confirmed; the frozen numerical value came out within 1.4% of the measured one.

### Universal collapse (beyond the preregistered)

The whole (N, d) dataset collapses onto the curve **with no free parameters** g(u) = √(u+1) − √u, with u = a·d/δρ_N: the closed form implicit in the turn 112 model. Deviations only where the δa·d branch takes over (u ≳ 10³), as expected.

## 5. Refinement the data demand

The naive version "α = rate of the metric in sup norm" fails: α_geom(sup) = 0.57 ≠ α_ρ = 0.85. What enters the predictions is the rate **of the critical channel** (the projection δρ), exactly as turn 110 had already corrected with the sensitivity kernel K_O. That is: the strong version "one universal α" dies (as the conversation already knew), and the channel/kernel version is the one the data confirm quantitatively.

## 6. Honest limitations

- Padé oscillations (N = 7 and 10 anomalously good, N = 8 bad) are correlated across all channels; the fits use all admissible N, with no selection.
- Numerical floor ~10⁻⁵ at the EP: the ε(0) points of N = 14, 15 (~3×10⁻⁴) are within a factor ~3 of the worst robustness case: the rates do not change when they are excluded.
- A single benchmark (EGB λ=0.08) and a single EP; the natural extension is qBTZ and EPs at complex q².
- N_ε as a literal staircase is coarse (jumps in Padé quality); the continuous regression measure is the quantitative one.

## 7. Reproduction

```bash
cd theory-validation
uv run pytest                     # 13 tests
uv run python scripts/run_validation.py    # ~6 min, resumes if interrupted
uv run python scripts/analyze_validation.py
```

Outputs: `results/validation.json` (raw data, full pairs), `results/fits.json` (all fits), `results/figures/fig1..fig5`.
