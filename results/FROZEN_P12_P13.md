# P12 + P13: frozen before measuring (big-theory radar, 2026-08-30)

## P12: traversability ↔ recoverability (operational ER=EPR)

Minimal Yoshida–Kitaev model of the traversable wormhole: 3+3 qubits,
Bell pairs (TFD at β=0), deterministic scrambler U (kicked Ising, fixed
seed: h_x=1.05, h_z=0.5, J=1, 6 steps), message on qubit 1 of the left
side, coupling exp(i g Σ Z_L Z_R), readout on the mirror qubit of the
right side. Sweep g ∈ [−1.5, 1.5].

P12.1 (reproduce GJW at the minimum): F_teleport(g) has a window: max at
g* ≠ 0 with F(g*) − F(0) > 0.15.
KILL: no shifted peak or contrast ≤ 0.15.

P12.2 (the ER=EPR↔Petz bridge): the fidelity of the Petz-recovered
channel (message→right-qubit channel, maximally mixed reference) tracks
the traversability: corr[F_tel(g), F_Petz(g)] > 0.9 over the sweep, and
the g that maximizes one maximizes the other (|Δg*| < 0.2).
KILL: corr < 0.5 or disagreeing peaks.

P12.3 (no-locking in the new arena): the spectral cost of ESTIMATING g
from the output statistics (CRB of g) does NOT lock in the window:
variation of σ_g within a factor 2 across the F peak.
KILL: σ_g dip/peak aligned with the F peak beyond a factor 2.

## P13: photon ring tower (spatial echoes; lensing/EHT)

Minimal model of the universal sub-ring signature: visibility
V(u) = Σ_{n=1..4} a·w^n · cos(2π d_n u + φ_n), diameters
d_n = d_∞(1 + c·e^{−γn}), w = e^{−γ} (Lyapunov), d_∞=40 μas, c=0.3,
φ_n = 0, band u ∈ [2, 40] Gλ, white noise per sample.

P13.1 (spatial hierarchy): the CRB of γ with free amplitudes scales as
gap⁻² and amplitudes with free γ as gap⁻³, where gap ≡ effective
separation of the tower harmonics (swept via γ ∈ [0.3, 1.2]); exponents
±0.5.
KILL: outside the windows.

P13.2 (EHT-like number): with SNR=100 per point and 200 points in the
band, σ(γ)/γ < 10% for γ = ln(e^π)≈π/… measure for γ=1.0 and report the
number (prediction: < 10%).
KILL: σ(γ)/γ > 30%.

## P12'' (frozen 2026-08-30, after the death of P12.1, BEFORE measuring)
Full probabilistic Hayden–Preskill/Yoshida–Kitaev protocol, 8 qubits:
Bell(REF,M) ⊗ Bell(L1,R1) ⊗ Bell(L2,R2) ⊗ Bell(M2,Mt); U
(kicked Ising, 8 steps, fixed seed) on (M,L1,L2); U* on (M2,R1,R2)
with index mirroring; post-selected Bell projection on the output pairs
(L1,R1) and (L2,R2); readout: F = ⟨φ+|ρ(REF,Mt)|φ+⟩.

P12''.1 (the decoder works): post-selected F > 0.8, with post-selection
success probability in [1/32, 1/4] (non-scrambled reference U=1:
F = 0.25).
KILL: F ≤ 0.5.

P12''.2 (the Petz bridge): the YK decoder fidelity tracks the Petz
recoverability of the M→R-side channel (without decoding):
F_YK ≥ 0.9·F_Petz (YK is near-optimal) and both fall together when the
scrambling is weakened (sweep of U steps: 1, 2, 4, 8):
corr(F_YK, F_Petz) > 0.9 over the sweep.
KILL: corr < 0.5 or F_YK < 0.5·F_Petz at some point.

## Amendment P12''-A1 (2026-08-30, BEFORE the re-test; original text kept)
P12''.2 compared F_YK with the Petz of the channel WITHOUT
post-selection, which is forbidden from carrying information by
no-signaling (and the data obeyed: F_Petz = 0.2500 exact, independent
of scrambling: an accidental verification of the theorem).
Reformulation: F_Petz of the channel CONDITIONED on the success of the
Bell projection (M → Mt | success), which is the object the YK decoder
approximates. Criteria kept: corr(F_YK, F_Petz_cond) > 0.9 over the
scrambling sweep and F_YK ≥ 0.5·F_Petz_cond.
Also: step sweep ∈ {2,3,4,5,6,8,12} to characterize the revival of the
small scrambler (P12''.1 evaluated at the MAXIMUM of the sweep, not at
a fixed 8: an operationalization amendment, kill if F_max ≤ 0.5).
