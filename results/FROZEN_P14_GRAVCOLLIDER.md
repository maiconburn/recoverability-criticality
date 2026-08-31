# P14, gravitational collider (ultralight dark matter), frozen
# before measuring, 2026-08-30

Context: clouds of ultralight bosons (dark matter candidates) around
black holes ("gravitational atoms") evolve by superradiance and go
through LEVEL CROSSINGS during binary inspirals (the "gravitational
collider" program, Baumann–Chia–Porto). Measuring the cloud parameters
(boson mass α = μM, quantum numbers) from the GW signal near a
crossing is a spectral estimation task near degeneracy: our metrology.

Frozen minimal model: two cloud levels |a⟩,|b⟩ with energies
E_a(t), E_b(t) swept linearly by the binary's orbital frequency Ω(t)
(Landau–Zener): H(t) = [[−Δ(t)/2, η],[η, +Δ(t)/2]],
Δ(t) = c₁(Ω(t) − Ω_res), coupling η fixed by the tidal perturbation.
Observable: GW phase/frequency carrying the cloud's "backreaction"
(frozen proxy: transferred population P_LZ and its derivative with
respect to the parameters). Parameters to estimate: (η, Ω_res) from a
record with white noise in the phase.

P14.1 (hierarchy at the crossing): the CRB of η with Ω_res free scales
as gap⁻ᵖ with p ∈ [1.5, 2.5] when the crossing is traversed slowly
(adiabatic regime, gap = 2η), measured by varying η.
KILL: outside the window.

P14.2 (speed signature): the total information about η is
NON-MONOTONIC in the sweep rate (maximal near the critical
Landau–Zener regime v ~ η², where the transition is most sensitive),
with max/asymptotic ratio > 3.
KILL: monotonic or ratio ≤ 3.

P14.3 (the dark matter number): translating to α = μM via
Ω_res ∝ μ·f(α): the relative error of μ (boson mass) achievable in a
clean crossing with phase SNR = 100: σ(μ)/μ < 5%.
KILL: > 20%.

## P14' (frozen 2026-08-30, BEFORE measuring): GW phase observable

Model: binary with quadrupolar chirp dΩ/dt = k·Ω^{11/3} + backreaction
−β·dP_b/dt; two-level cloud with Δ(t) = c·(Ω(t) − Ω_res), Ω_res ∝ μ
(boson mass); observed phase Φ(t) = 2∫Ω dt with white phase noise
σ_φ = 0.1 rad per sample, 2000 samples, Ω sweeping 0.8→1.2 (Ω_res = 1).
Fiducial: k such that the local sweep near the resonance is slow
(v_eff ≈ 0.02·c), η = 0.05, c = 5, β = 0.01. 6×6 Fisher on the
parameters {Ω_res, η, β, k, Ω₀, φ₀}, with σ(μ)/μ = σ(Ω_res)/Ω_res
marginalized.

P14'.1 (the honest forecast): marginalization over the binary
parameters degrades the naive σ(μ)/μ (0.03%) by a factor > 10, but the
result stays < 5%.
KILL: > 20% (the crossing does not measure μ in practice) or < 0.1%
(marginalization costs nothing: would indicate an error).

P14'.2 (localization): ≥ 60% of the Fisher information about Ω_res
comes from the window |Ω − Ω_res| < 5·η (the information lives in the
crossing).
KILL: < 40%.

P14'.3 (robustness to the chirp mass): |corr(Ω_res, k)| < 0.9 in the
marginalized Fisher (the cloud signature is not absorbable by the
chirp rate).
KILL: ≥ 0.95.

## P14'' (frozen 2026-08-30, BEFORE measuring): multi-crossing

Model: 3 resonances of the same cloud, Ω_res,k = μ·c_k(χ) with
c_k(χ) = c⁰_k·(1 + d_k·χ), c⁰ = (1.0, 1.35, 1.80), d = (0.05, 0.12, 0.20)
(distinct spin dependencies per mode, hyperfine style); three
independent two-level systems (η_k = 0.05), summed backreaction
−β·Σ dP_k/dt; chirp Ω: 0.8 → 2.2; phase with σ_φ = 0.1 rad, 3000
samples. 9×9 Fisher: {μ, χ, η₁, η₂, η₃, β, k, Ω₀, φ₀}.

P14''.1 (coherent gain): the joint σ(μ) of the 3 crossings beats the
best single crossing by a factor > √3.
KILL: gain < 0.8·√3.

P14''.2 (spin resolved by the ratios): with χ unknown, σ(μ) degrades
less than 2× vs known χ.
KILL: degradation > 5×.

P14''.3 (LISA-grade number): with k such that each crossing
accumulates ~30+ cycles (k = 0.005), σ(μ)/μ < 0.1%.
KILL: > 1%.
