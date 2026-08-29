# ERRATA

## E1 (2026-08-29, corrected in v1.2): EP-extinction threshold

**v1.0–v1.1 claimed:** λ_ext = 0.1091 ± 0.0002, with no mechanism relating it
to any known threshold.

**Corrected result:** λ_ext = 0.12475 ± 0.00025 — numerically consistent (1σ)
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
