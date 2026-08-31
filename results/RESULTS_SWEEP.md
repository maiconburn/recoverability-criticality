# P1: coupling sweep, result (2026-08-28)

> **SUPERSESSION NOTICE (2026-08-30):** this is a dated HISTORICAL document.
> The λ_ext values cited here (0.1091 and derived) have been RETRACTED:
> see `ERRATA.md` E1–E3: there is no single threshold; extinction is
> family-by-family, with genuine EPs up to at least λ = 0.120.

Protocol: predictions frozen in `sweep_predictions.json` and `p4_predictions.json` BEFORE the measurements (λ=−0.1 seen before the P4 freeze: flagged). 5 couplings with a real EP: λ ∈ {−0.10, −0.05, 0.02, 0.05, 0.08}.

## What was confirmed (structural: the theory's claims)

1. **Universal halving at the EP**: 2α_EP/α_ρ = {1.00, 1.00, 1.00, 1.00, 1.03} on the five backgrounds. The turn 112 law is not an accident of λ=0.08: it is universal in the family. This is the central result of the sweep.
2. **Channel splitting persists**: α_ρ/α_sup ∈ [1.24, 1.49] (mean 1.38), never →1. The kernel refinement (turn 110) survives the K2 gate: the theory does NOT reduce to Stahl in sup norm.
3. **New spectroscopy**: trajectory of the mirrored EP q²_c(λ) = −5.71 → −5.45 → −18.27 → −17.34 → −16.15 (non-monotonic!), ω_c(λ) = −2.82i → −5.67i. Unprecedented in the literature.
4. **EP extinction**: for λ ≥ 0.12 the mirror collision does not exist in real q² up to q²=−40: the EP goes extinct or migrates to the complex plane. A new qualitative transition in the EGB family.

## What failed (the proxy: preregistered criterion K1 FIRED)

The analytic proxy "α ∝ Green's function of the nearest branch point" **does not predict α(λ) quantitatively**:

- Regression of measured vs predicted dN/dec: **R² = 0.40** (the gate required ≥ 0.9); slope 0.68±0.49.
- Regression of measured vs predicted α: R² = 0.52; systematic monotonic drift in λ (measured/predicted: 1.42→1.00).

Reading: the distance to ONE branch point is not enough: the real rate sees the 4 branch points + complex zeros + the channel's kernel weight (true Stahl capacity). The "zero-parameter α" path remains open, but requires the full capacity theory (v2 model, new freeze, new test λ, e.g. 0.03, 0.065, −0.075).

## P4 phase-1 (preliminary arbitration)

Analytic structure derived: under the Abel kernel, 𝒥 inherits singularities of B **plus the complex zeros of b** (z=±i, fixed in λ) → the α_B and α_CMI curves separate at λ=0.02. Measured: 1.360±0.121 → z(metric)=+1.8, z(CMI)=+3.3. **Direction: disfavors the CMI layer**: but since the base proxy failed K1, the final P4 verdict awaits the correct capacity baseline.

## Table

| λ | measured α_ρ | measured dN/dec | predicted dN/dec | halving | split |
|---|---|---|---|---|---|
| −0.100 | 1.026±0.093 | 1.208±0.036 | 1.600 | 1.000 | 1.35 |
| −0.050 | 1.173±0.084 | 1.011±0.006 | 1.323 | 1.000 | 1.44 |
| +0.020 | 1.360±0.121 | 0.817±0.003 | 1.008 | 1.000 | 1.24 |
| +0.050 | 1.063±0.087 | 1.135±0.013 | 1.202 | 1.004 | 1.40 |
| +0.080 | 0.851±0.130 | 1.450±0.019 | 1.353 | 1.029 | 1.49 |

Reproduction: `scripts/sweep_predictions.py` (freezes) → `scripts/run_sweep.py` (~15 min) → `scripts/analyze_sweep.py`. Data: `results/sweep.json`, `results/sweep_fits.json`.

## Addendum (2026-08-29): exponent reconciliation, the 1/2/3 ladder

A single experiment (same synthetic Kerr setup, pair (2,2,5)/(2,2,6))
measuring three tasks: amplitudes with fixed frequencies → exponent
**1.03** (explains our −1.11 in SXS); Cramér–Rao of free frequencies →
**2.12** (explains the −2 of Imafuku–Oshita–Takeda, arXiv:2605.16199);
amplitudes with free frequencies → **3.12** (matches Prony
super-resolution, Batenkov 2p−1, p=2). The apparent exponent conflict is
a PER-TASK HIERARCHY: each level of ignorance adds a power of 1/gap.
Data: `results/reconcile_exponents.json`.
