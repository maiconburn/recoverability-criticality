# P10: frozen BEFORE any measurement (author's question: "layers
# that vibrate at the same frequency and influence each other")

Freeze date: 2026-08-30. System: post-selected PT qubit with periodic
drive, H(t) = [[0, J], [J, -iγ/2]] + (A/2)·cos(Ω_d t)·σ_z,
γ = 1, Ω_d = 0.8. One-period propagator U(T), quasi-energies
λ_± = (i/T)·ln eig U(T), defined mod Ω_d (the "layers"/replicas).

## P10.1: layer EPs (resonance between replicas)
In the STATIC system, the real gap 2√(J²−1/16) = Ω_d occurs at J* = 0.4717.
Prediction: with A > 0, EP structure appears (quasi-energy collision with
eigenvector coalescence) in a neighborhood of J*, WHERE THE STATIC SYSTEM
HAS NO EP: distinct layers influencing each other through resonance.
KILL: no quasi-degeneracy with EP character (quasi-energy gap < 0.01 with
eigenvector collinearity > 0.99) found in J ∈ [0.35, 0.60], A ∈ (0, 0.6].

## P10.2: the cost law is blind to the layer
Near the Floquet EP, the CRB of the quasi-energy splitting (free
amplitudes, stroboscopic record c₁(nT)) diverges with the SAME exponent
as the analogous task at the static EP measured in the same gap window.
KILL: |exponent_Floquet − exponent_static| > 0.5.

## P10.3: the drive is the coupling between layers
The location of the minimum quasi-gap in J shifts continuously from J*
as A → 0⁺, and the width of the hybridization region grows monotonically
with A (role of effective coupling between replicas).
KILL: minimum does not connect to J* in the A→0 limit, or width
non-monotonic in A (beyond numerical error).

## P10.4 (frozen 2026-08-30, AFTER the kill of P10.1 and BEFORE measuring)
Mechanism learned from the kill: a Hermitian drive (real σ_z) opens a gap
between replicas (anticrossing, splitting ∝ A: P10.3 confirmed the wire).
Sharpened prediction: with a DISSIPATIVE drive, γ(t) = γ·(1 + A·cos Ω_d t)
(anti-Hermitian coupling between replicas), the same resonance
J ≈ J* = 0.4717 produces a COLLISION: quasi-gap < 10⁻³ with eigenvector
collinearity > 0.99 for some A ∈ (0, 0.6], J ∈ [0.44, 0.50].
KILL: no point of the plane satisfies both criteria.
