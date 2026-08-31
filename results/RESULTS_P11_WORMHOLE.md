# P11: wormhole doublets, an instructive death from bad modeling

Predictions frozen in FROZEN_P11_WORMHOLE.md; two rounds:
- v1 (bilateral shooting): VOID due to instrument (roots with Im ω > 0,
  non-physical; exponential growth in the forbidden regions swallowed
  the integration). The instrument-vs-physics distinction was kept.
- v2 (analytic transfer matrix of the sech² barrier, r/t validated
  against numerical integration at 10⁻¹⁰; all modes physical):
  **P11.1 KILLED as formulated**: the measured "splitting" GROWS and
  saturates (0.046→0.098 for L=6→16), consistent with a cavity tower
  spacing (~π/2L_eff), not with an exponential doublet.

Diagnosis: a modeling error in the freeze. The symmetric/antisymmetric
doublet with splitting e^{-κL} belongs to the BOUND double well; the
wormhole is an OPEN cavity between two barriers, whose signature is the
TOWER of cavity modes (the "echoes") under the barrier mode: a
multi-mode structure, not a fine doublet. P11.2/P11.3: void by premise.

What the death teaches (candidate for P11', NOT frozen yet): wormhole
detectability is the task of detecting small-amplitude cavity modes
under the barrier ringdown: "amplitudes with free frequencies" from the
hierarchy, applied to a tower. It requires honest modeling of the
excitation (relative amplitudes of the cavity modes) before freezing
again.

Data: results/p11_wormhole.json (v1, void), p11_wormhole_v2.json.
Scripts: p11_wormhole.py, p11_wormhole_v2.py.

## P11': final verdicts (simulated excitation; three modeling lessons)

Honest 1+1D wave simulation (Gaussian pulse, absorbing boundaries,
reference = single barrier). Lesson 3: the frozen U0 = 0.15 is
SUB-CRITICAL (nearly transparent barrier, no echo train): documented
physical regime: U0 = 0.5.

| Prediction | Verdict | Numbers (U0=0.5) |
|---|---|---|
| P11'.1 echo train, Δt = 2L ± 15% | killed at U0=0.15; **CONFIRMED for L≥12 in the physical regime** | Δt = 26.1/34.0/42.0/50.0 vs 2L = 24/32/40/48 (errors 4–9%; offset +2 ≈ crossing of the barriers) |
| P11'.2 SNR_min grows with L | **KILLED** | SNR_template(L) FLAT (0.74–0.76): fixed reflectivity ⇒ constant echo energy; L controls resolvability, not detectability |
| P11'.3 template ≥ 10× better | **KILLED** | ratio 4.5→5.9× (grows with L, right direction, smaller magnitude) |

Detectors: raw and envelope autocorrelation fail (they stick to the
edge of the window); peak-finding with height ≥ 25% of the maximum and
distance ≥ L/2 works. Data: results/p11_prime{,_echo,_u05}.json.

State of the line: paused with a balance = validated train + template/
agnostic ratio ~5× quantified with physical amplitudes. Heirs on the
radar: SPATIAL tower of photon rings (lensing/EHT) and
traversability↔Petz (ER=EPR): see the program memory.
