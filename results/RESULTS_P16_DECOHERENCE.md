# P16, decoherence as the fourth task: verdicts (2026-08-31)

Preregistration: `FROZEN_P16_DECOHERENCE.md` (committed before any
measurement). Instrument: fundamental pair of QNMs at λ = 0.105, mirror
EP anchored from `shooting_ep_hunt.json` (q²_c = −34.385584,
ω_EP = −7.164147i, gap 1.3e-4), continuation with mirror gates and
identity-swap gate. Data: `p16_decoherence.json`; scripts
`p16_decoherence.py` (trajectory and P16.3) and `p16_fix.py` (v2
instrument for P16.1/P16.2).

## P16.3, post-EP protection: CONFIRMED (all frozen windows)

| measurement | frozen | measured |
|---|---|---|
| splitting exponent (under side) | 0.5 ± 0.1 | 0.495 |
| splitting exponent (over side) | 0.5 ± 0.1 | 0.501 |
| protection Γ_slow < γ_EP at every point | yes | yes (all) |
| kink exponent h | [0.4, 0.6] | 0.493 |
| flat under side, norm. slope | < 0.05 | 0.018 |

Crossing the critical coupling, one channel becomes LONGER lived:
Γ_slow = γ_EP − B·|δ|^0.49, maximum protection 3.1% in the measured
window (δ up to 0.0215; the continuation stops at the identity-swap
gate). Kink asymmetry at paired δ (0.0215): the overdamped side loses
0.223 in Γ_slow against 0.010 on the underdamped side: 22×. The ghost
worthy of the founding conjecture (tombstone 1): not "curvature
suppresses decoherence", but "crossing the spectral criticality
partially protects one channel, with a square-root kink". Channel
reading: Γ_slow is the slowest pole of the bath seen by the probe in
pure dephasing; the protection is a statement about the spectrum,
inherited by the late-time coherence envelope.

## P16.1, rescue by the secular channel: KILLED

With the correct instrument (v2), χ²/dof ≈ 1 for BOTH models at all
points, including at the EP (sec 387.8 vs nosec 385.5, dof 392): no
rejection. The secular channel t·e^{−γt} is mimicked at the 1e-3 noise
level by two free exponentials on a finite window (Prony-type
approximation): the trap was not the Petermann compensator
(neutralized by the bound), it was identifiability of the observable
class itself. Instructive contrast with P8.2: the log channel in a
SCALE VARIABLE (decades in k) is detectable at χ²/dof 1e5; the secular
channel in TIME with a ~4/γ window is not. Detectability of the Jordan
channel depends on the observable class: this is why secular EP
signatures in time-domain ringdown are hard.

## P16.2, exponent of the estimation task: KILLED (informative)

σ(δq²) ≈ 3.2e-3 FLAT over 1.5 decades of gap: p = −0.066
(under-resolved subset gap·T < 0.5: −0.029), against the frozen
prediction 1.0 and kill range outside [0.6, 1.5]. Reading: the
response gain of the √ unfolding (dω/dδq² ∝ gap⁻¹) EXACTLY cancels the
spectral resolution cost: estimating the CONTROL parameter (distance
to the EP in coupling space) is EP-neutral. Third independent
appearance of the pattern: P14-LZ (flat σ(μ)/μ), the LEP3 design
(configs on the EP line work), now here. Candidate general statement:
at an EP-2, estimation cost diverges for SPECTRAL parameters, not for
the control parameter that unfolds the EP.

## Instrument notes (honest trail)

v1 had three defects, all caught by the house red flags before any
verdict: (1) EP refinement by grid fell into the wrong basin (spurious
1e-9 gap from identity collapse), replaced by the already-refined
anchor from shooting_ep_hunt + gates; (2) CRB via the Gram matrix in
double precision (cond 1e24 = cond(J)², masked σ: the pinv pattern),
redone by SVD of J; (3) the amplitude bound of the secular model
clipped the true parameter (b_true 19.6 vs bound 10), fixed; and the
exact rank-2 degeneracy of the amplitude columns (mirror symmetry:
Im E₂ = −Im E₁) required reparametrizing the nuisance to 2 real
degrees. No verdict changes between v1 and v2 except the validity of
the P16.2 instrument.

## Tally

One new confirmation (P16.3, the post-EP protection), two tombstones
(P16.1, P16.2: numbers 16 and 17 in the graveyard), and two conceptual
byproducts: the observable-class dependence of Jordan-channel
detectability, and the EP-neutrality of control-parameter estimation
(pattern now seen 3×, candidate theorem: PROVEN the same day: see
`THEOREM_EP_NEUTRALITY.md`, exact exponent 0).
