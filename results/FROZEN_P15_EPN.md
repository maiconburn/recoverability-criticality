# P15, cost hierarchy at an EP of order N (frozen 2026-08-31,
# BEFORE any synthetic or real data)

Frozen derivation: near an EP-N, N frequencies form a CLUSTER of width
g. Estimation from the record is a Prony problem with a cluster of
size p = N. Predicted structure (generalizes the EP-2 hierarchy
measured in the program):

| task | predicted exponent | p=2 case (measured) | p=3 case (predicted) |
|---|---|---|---|
| amplitudes, fixed frequencies | p − 1 | 1 ✓ | **2** |
| frequencies (splitting), free amplitudes | 2p − 2 | 2 ✓ | **4** |
| amplitude, everything free | 2p − 1 (Batenkov) | 3 ✓ | **5** |

## P15.1 (synthetic EP-3)
Cluster of 3 exponentials with the EP-3 Puiseux pattern
(λ_k = λ₀ + g·e^{2πik/3}·(factor), k=0,1,2), record with white noise,
fixed window: measured CRB exponents within {2, 4, 5} ± 0.6 while
sweeping g over ≥ 2 decades.
KILL: any of them outside the window.

## P15.2 (real EP-3 data)
Cataloged sources: NV EP-3 (Nat. Nanotech 19, 160, Source Data) and
trapped-ion LEP3 (figshare 10.6084/m9.figshare.30343429). Prediction:
in the data that allow reconstructing at least ONE task from the
table, the measured exponent falls within ±0.75 of the predicted one.
KILL: an available exponent outside the window.
Declarable VOID: if the Source Data only contain aggregates without
records, report "not testable with public data" and keep P15.2 as an
open preregistration for laboratories.

## P15.3 (response consistency)
In the same synthetic, the RESPONSE of the splitting to the physical
parameter follows ε^{1/3} (the gain claimed by the EP-3 sensor
literature), coexisting with the costs in the table: the "sensing
debate" at order N is resolved by task separation, as in the EP-2.
KILL: response not consistent with 1/3 (±0.1) in the small-ε regime.

## P15.4 (frozen 2026-08-31, BEFORE computing): anisotropy along the EP line

Hypothesis: the estimation cost AT the EP, along the LEP3 line, is
controlled by the local non-orthogonality of the eigenvectors
(Petermann factor). Frozen operational measure: κ_V(α) = condition
number of the eigenvector matrix of the experiment's LH, evaluated at
a fixed relative offset δ=10⁻³ from the line (γ = γ_LEP3(α)·(1+δ),
ω=1): comparable across α's.
Observable: σ_γ/γ̄ from the public bootstraps (normalized by scale;
raw σ_γ reported as secondary).

Prediction: corr[ln(σ_γ/γ̄), ln κ_V] > 0.8 over the ≥9 usable
configurations, with a power law σ/γ ∝ κ_V^q, q ∈ (0, 1.5].
KILL: corr < 0.5.
Frozen control: if σ_γ/γ̄ correlates better with pure γ̄ than with κ_V
(|corr_γ| > |corr_κ| + 0.1), the Petermann hypothesis is NOT supported
even with high corr: report as confounded by scale.
