# P16, decoherence as the fourth task: frozen predictions (preregistration, 2026-08-31)

Frozen BEFORE any measurement. Standard protocol: each prediction with
a kill criterion.

## Context and motivation

The founding conjecture (tombstone 1: "can strong curvature suppress
decoherence?") is dead in its original form:
Danielson–Satishchandran–Wald proved that every Killing horizon
decoheres superpositions (arXiv:2205.06279, arXiv:2301.00026, titles
verified on the arXiv API on 2026-08-31). Refined and testable
reburial: the decoherence rate is not suppressed by curvature, it
INHERITS the spectral critical structure of the background.
Decoherence = fourth task in the exponent hierarchy.

Probe: a qubit in pure dephasing coupled to the field on the EGB
background; what the probe sees is the Green's function of the
fundamental QNM pair. Exact channel structure:
r(t) = Im[(e^{−iω₁t} − e^{−iω₂t})/(ω₁ − ω₂)]: a damped oscillator; at
the mirror EP it becomes the secular channel t·e^{−γt} (Jordan block),
the same log/polynomial channel as P8.

## Instrument (frozen)

Fundamental family, λ = 0.105, mirror EP anchored at q² ≈ −34.386
(seed pair [0.02−7.1641i, −0.02−7.1641i], kernel_compare). Shooting
with sequential continuation; EP refinement by zooming on |ω₁−ω₂|;
log-spaced sweep of δ = q² − q²_c on both sides. Frozen synthetic
noise: white, σ = 1e-3 of the signal maximum, rng seed 16. Grid
t ∈ [0, 4/γ_EP], 400 points.

## P16.1, rescue by the secular channel (open twin of P8.2)

Fit of the noisy signal with M_sec = Re[(a + bt)e^{−iwt}] vs
M_nosec = Re[A₁e^{−iω₁t} + A₂e^{−iω₂t}] with BOUNDED AMPLITUDES
(|A| ≤ 10·max|r|; lesson from P8-F2 v1: without the bound, divergent
±1/gap amplitudes compensate the secular term and the test is blind: a
known trap, neutralized in the freeze).
PREDICTION: Δχ²/dof(nosec − sec) > 4 at gap/γ_EP ≤ 0.01 and < 1 at
gap/γ_EP ≥ 0.5 (localization at the EP, like P8-F2.2).
KILL: no rejection at the EP, or equal rejection far from the EP
(artifact).

## P16.2, exponent of the decoherence estimation task

CRB for δq² estimated from the signal r(t) with the 2 complex
amplitudes free (nuisance, marginalized). Frozen derivation: the
splitting task has exponent 2 in the gap (EP-2 hierarchy {1,2,3}); the
√ unfolding gives a Jacobian |dδω/dδq²| ∝ gap⁻¹; composition:
σ(δq²) ∝ gap^(−1.0).
PREDICTION: exponent p ∈ [0.6, 1.5] in the log-log fit of σ(δq²) vs
gap (underdamped side).
KILL: p outside the range (new class: informative, but kills THIS
prediction). Conditioning gates: explicit inversion, cond(I) reported,
mpmath if cond > 1e12 (house rule post-P14/P15).

## P16.3, post-EP protection with a square-root kink (the new one)

On the overdamped side, one of the channels becomes LONGER lived:
Γ_slow(δ) = γ_EP − B·|δ|^h. The ghost worthy of the founding
conjecture: crossing the critical point partially protects the
coherence of one channel.
PREDICTION: h ∈ [0.4, 0.6] (square-root kink, dΓ/dδ → −∞ at the EP);
underdamped side with flat Γ_slow (|slope|/γ_EP < 0.05 in the same
window); splitting on both sides with exponent 0.5 ± 0.1.
KILL: no protection (Γ_slow ≥ γ_EP), or exponent outside [0.4, 0.6].

## Overlap risk (declared before measuring)

P16.2 may reduce to a confirmation of the hierarchy already measured
in another observable (value: universality across observable classes,
not discovery). P16.3 is the new claim. If EVERYTHING reduces to a
reanalysis of ringdown already published by us, the honest verdict =
"cross-observable confirmation", not discovery.
