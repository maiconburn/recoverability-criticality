# P10: frequency layers and the cost law (author's question, full cycle)

Origin: a layman's question from the author, 2026-08-30: "what if the
quantum world had layers or frequency? like schemes that vibrate at the
same frequency and one influences the other". Translation: Floquet
replicas (layers) + resonance. Predictions frozen BEFORE each measurement
(FROZEN_P10_FLOQUET.md, separate timestamped commits).

System: post-selected PT qubit, γ=1, drive Ω_d=0.8; quasi-energy replicas
= the "layers".

## Verdicts

| Prediction | Verdict | Number |
|---|---|---|
| P10.1: Hermitian drive (σ_z) creates an EP at the replica resonance | **KILLED** | anticrossing: quasi-gap ∝ A (Rabi between layers), collinearity ~0.55 |
| P10.2: cost law blind to the layer | **CONFIRMED** | exponent −1.531 (Floquet) vs −1.398 (static), diff 0.134 ≤ 0.5 |
| P10.3: drive = wire between layers, minimum → J* as A→0 | **CONFIRMED exact** | J_min(A→0) = 0.47170 = J* (5 places); gap ∝ A monotonic |
| P10.4 (sharpened by the kill of P10.1): DISSIPATIVE drive (γ(t)) collides the layers | **CONFIRMED** | two Floquet EPs: (J=0.4842769, A=0.100226) and (J=0.4466490, A=0.202121), gap ~7–9×10⁻¹⁰, collinearity 1.000000 |

## The physics in one sentence

Resonant frequency layers couple through the drive; Hermitian coupling
OPENS the gap between them (anticrossing), dissipative coupling makes them
COLLIDE (Floquet EP), and at the layer EP the same cost law of the static
EP holds.

## Novelty calibration (not audited in full text)

Audit (arXiv API, 25 papers, 2026-08-30): Floquet EPs are well established
(photonics, Lindblad with periodic drive 2011.02054/2306.12322, Floquet
dissipative coupling 2504.13616, multiple FEPs 2509.02556). NOT found:
(i) the explicit contrast Hermitian-opens vs dissipative-collides at the
same replica resonance; (ii) ANY Fisher/Cramér-Rao/estimation-cost
analysis at a Floquet EP: the metrology layer remains unclaimed here as
well. Full text not swept; calibrate mechanism claims as "not found in
abstracts".

Process note: P10.4 was declared "KILLED" by the weak refiner (coordinate
descent, gap 5.6e-3) and confirmed by the correct refiner (Nelder-Mead,
gap 7e-10): the frozen criteria never changed; the search did. Scripts:
p10_floquet.py, p10_dissipative.py; data: p10_floquet.json,
p10_dissipative.json, p10_costlaw.json.

## Addendum: the wedge of EPs (complete map)

Two lines of genuine EPs in the (J, A) plane, 23 points with gap ~10⁻⁹
(Nelder-Mead on the log-gap, NSTEP=600):
- lower branch: J_EP(A) = 0.4655→0.3987 for A = 0.05→0.60 (dJ/dA ≈ −0.121)
- upper branch: J_EP(A) = 0.4843→0.5483 for A = 0.10→0.60 (dJ/dA ≈ +0.128)
Both extrapolate to J* = 0.4717 as A→0: the static replica resonance is
the VERTEX of the wedge, and the dissipative drive opens it into two
lines of EPs with a Floquet PT-broken band between them: the exact
dynamical analogue of the pair of static EPs flanking the overdamped
band. Data: results/p10_ep_line.json, p10_ep_line2.json.
