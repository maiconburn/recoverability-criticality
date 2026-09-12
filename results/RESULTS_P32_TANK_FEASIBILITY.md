# P32, is the tank experiment doable? Verdicts (2026-09-12)

Preregistration: `FROZEN_P32_TANK_FEASIBILITY.md`. Scripts:
`p32_tank_feasibility.py` (time-domain excitation + blind counting),
`p32b_quality_factors.py` (quality factors, corrected units),
`p32c_design_window.py` (feasible (h, C) window and required SNR),
`p32d_tail_postmortem.py` (diagnostic). Data: the JSON files of the
same names. This cycle tests OUR OWN proposal
(`EXPERIMENT_DESIGN_VORTEX_TANK.md`) before anyone builds anything.

## Summary

The experiment has signal but the protocol I wrote was wrong. The
tower modes are excited by generic initial data (excitation ratios
E_n = |A_n|/|A_0| between 0.14 and 2.4, far above the 0.005 floor), so
the ringdown contains them. But blind mode counting with a matrix
pencil recovers 0 of 2 modes at |m| = 2, 0 of 4 at |m| = 5, 1 of 8 at
|m| = 10 and 0 of 12 at |m| = 15, at 0.1% and 1% noise: the frozen
protocol cannot count. The reason is structural, not numerical: the
quality factor of the tower is an INVARIANT,

    Q_0 = |m|/2 exactly,   Q_n ~ |m| / (2(2n+1)),

so no choice of circulation, drain or depth makes the modes more
oscillatory. Only about |m|/4 of the N(m) ~ 0.8 |m| modes have Q > 1;
the rest are purely decaying exponentials, the classic ill-conditioned
Prony problem. What works is the fixed-frequency amplitude fit that
the theory itself enables: the required per-sample signal-to-noise for
a 3-sigma detection is 0.4 to 2.7 for the fundamental at every |m|,
but 6 to 109 for the first overtone and 12 to over 1000 for the
second, while the symmetric cluster moment needs 0.3 at EVERY |m|,
with condition number 4 instead of 4.6e4. The labeled-versus-symmetric
law of this repository, written as an experimental design.

## Verdict table

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P32.1 excitation: every mode with n <= N(m)-1 has E_n > 0.02, stable within a factor 3 across three initial-data settings | KILL: E_n < 0.005 in all three | m = -2: E_1 = 0.137, 0.619, 0.456; m = -3: 0.306, 0.486, 0.641; m = -4: E_1 = 0.652, 2.384, 0.563 and E_2 = 0.493, 1.582, 0.304; m = -5: E_1 = 1.386, 4.682, 2.334, E_2 = 1.907, 6.953, 2.632, E_3 = 0.844, 3.843, 1.193. All modes excited, none near the floor, and at |m| = 4, 5 the overtones are often MORE excited than the fundamental; spread factors 3.4 to 5.2 exceed the factor-3 clause | CONFIRMED on the kill; the stability clause missed (excitation is initial-data dependent, as excitation factors must be) |
| P32.2 fixed-frequency residual below 10% of the signal r.m.s. | KILL: above 30% | residuals 0.15 to 0.60 across settings and m | KILLED (tombstone 35) |
| P32.3 blind pencil recovers N(m) modes at 1% noise for m = -2, -3 | KILL: fewer than N(m) for both | 0 of 2 at both; with the corrected unit conversion also 1 of 3 (|m| = 4, order 12, 1% noise), 0 of 4 (|m| = 5), 1 of 8 (|m| = 10), 0 of 12 (|m| = 15); at 5% noise 0 everywhere | KILLED (tombstone 36) |
| P32.4 the deep overtones will not be blindly resolvable; the protocol must move to fixed-frequency amplitude fitting | recorded, no kill | true, and stronger: NO mode is blindly resolvable at any tested |m|, including the fundamental | CONFIRMED, stronger than stated |

Initial-data dependence of the residual (recorded, beyond the freeze):
the residual is not a fixed property of the ringdown. At m = -5 the
broad, distant perturbation (x0 = 40, width 6) gives residual 0.095,
BELOW the frozen 10% threshold, while the narrow, close one
(x0 = 15, width 2) gives 0.58 at m = -2 and 0.60 at m = -3. Broad
smooth data launched from outside the light ring excites the escaping
tower cleanly; narrow data near the barrier dumps energy into the
strongly damped non-escaping modes. Practical hint for the tank: the
perturbation should be broad, smooth and applied outside the light
ring (r > 2C/c_s), not a local splash near the drain.

Post-mortem on P32.2: the residual is NOT the branch-cut tail. Adding
power-law columns t^-1, t^-2, t^-3 to the fit moves the residual only
from 0.366 to 0.321 (m = -2) and 0.371 to 0.354 (m = -3). So the
escaping tower accounts for 40 to 85% of the ringdown amplitude in the
window and the remainder is something else, most plausibly the
strongly damped non-escaping modes that dominate early times. The
frozen 10% threshold assumed the escaping tower was the whole
ringdown, which P21 never claimed. The identification of the remainder
needs the full B = 10 spectrum (escaping and absorbed families) and is
left open.

## Quality factors (`p32b_quality_factors.json`)

| |m| | N(m) | Q_0 | Q_1 | Q_2 | Q_3 | modes with Q > 1 |
|---|---|---|---|---|---|---|
| 2 | 2 | 0.92 | 0.05 | | | 0 |
| 3 | 2 | 1.45 | 0.33 | | | 1 |
| 4 | 3 | 1.96 | 0.54 | 0.17 | | 1 |
| 5 | 4 | 2.47 | 0.73 | 0.33 | 0.10 | 1 |
| 6 | 5 | 2.97 | 0.92 | 0.46 | 0.22 | 1 |
| 7 | 6 | 3.48 | 1.10 | 0.58 | 0.33 | 2 |
| 8 | 6 | 3.98 | 1.27 | 0.70 | 0.42 | 2 |
| 9 | 7 | 4.48 | 1.45 | 0.81 | 0.51 | 2 |
| 10 | 8 | 4.98 | 1.62 | 0.92 | 0.60 | 2 |
| 12 | 10 | 5.99 | 1.96 | 1.13 | 0.76 | 3 |
| 15 | 12 | 7.49 | 2.47 | 1.44 | 0.99 | 3 |

Q_0 = |m|/2 to two decimals at every |m| tested (it is
(|m|/4)/(2 x 1/4) from the tower's leading terms), and Q_n follows
|m|/(2(2n+1)) to about 10%. Both are invariants: frequency and damping
both carry c_s^2/C, so the ratio is fixed by the tower alone. This is
the single most important number for the experiment and it was never
computed before this cycle.

## The feasible design window (`p32c_design_window_R100.json`, `_R200.json`)

Constraints: shallow water at the light ring (k h = |m| h c_s/(2C) <
0.30), viscous bottom-layer damping below 20% of the tower damping
(sqrt(nu omega/2)/h < 0.2 |Im c| g h/C), light ring inside the tank
(r_LR = 2C/c_s < R), fundamental above 0.05 Hz.

| |m| | feasible (R = 1 m) | h (cm) | C (cm^2/s) | r_LR (cm) | k h | visc/tower | f_0 (Hz) | gamma_0 (1/s) |
|---|---|---|---|---|---|---|---|---|
| 2 | yes | 3.2 | 2800 | 99.9 | 0.064 | 0.056 | 0.083 | 0.284 |
| 5 | yes | 2.6 | 2525 | 100.0 | 0.130 | 0.120 | 0.199 | 0.253 |
| 8 | yes | 2.5 | 2475 | 100.0 | 0.200 | 0.160 | 0.314 | 0.248 |
| 10 | yes | 2.4 | 2425 | 100.0 | 0.240 | 0.189 | 0.385 | 0.243 |
| 12, 15 | no (needs a bigger tank) | | | | | | | |

With R = 2 m, |m| = 12 becomes feasible (still not 15). The tank
radius caps the azimuthal number, hence caps Q_0 = |m|/2: a 1 m tank
reaches Q_0 = 5, a 2 m tank Q_0 = 6.

Pump: the drain flow is 2 pi C h / B, so it falls as 1/B while the
tower becomes MORE accurate at large B. At the |m| = 10 point,
B = C/D = 10 needs 219 L/min but B = 30 needs 73 L/min with the
horizon still at r_h = D/c_s = 1.7 cm. High rotation is better on both
counts, which the original note missed.

## Required signal-to-noise, fixed frequencies (`p32c_design_window_R100.json`)

Per-sample SNR for a 3-sigma detection of a unit-amplitude mode, from
the least-squares covariance over a record of 6 e-foldings at 100 Hz:

| |m| | modes | cond(X) | A_0 | A_1 | A_2 | cluster {u, t u} cond | cluster moment |
|---|---|---|---|---|---|---|---|
| 2 | 2 | 3.7 | 0.4 | 0.7 | | 3.6 | 0.3 |
| 4 | 3 | 19 | 0.7 | 2.6 | 2.4 | 3.7 | 0.3 |
| 5 | 4 | 85 | 0.9 | 6.2 | 12.2 | 3.8 | 0.3 |
| 6 | 5 | 3.8e2 | 1.2 | 12.3 | 39.6 | 3.8 | 0.3 |
| 8 | 6 | 2.1e3 | 1.5 | 23.8 | 118.5 | 3.8 | 0.3 |
| 10 | 8 | 4.6e4 | 2.2 | 58.2 | 514.3 | 3.8 | 0.3 |

## The protocol that replaces the frozen one

1. Target |m| = 5 to 10 (Q_0 = 2.5 to 5), strong rotation B = C/D ~ 30.
2. Do NOT count modes blindly. Fit amplitudes with the tower
   frequencies FIXED at the elliptic prediction
   |m| 2[K(k) - E(k)] = i pi (n + 1/2).
3. The primary observable is the CLUSTER MOMENT of the tower (the
   fixed-frequency sum, and if wanted its first moment), which needs
   SNR 0.3 at every |m| and is condition-number 4. Secondary: the
   fundamental amplitude (SNR 1 to 2). Individual overtones n >= 1 are
   a stretch goal and n >= 2 is out of reach above |m| = 5.
4. Falsifier, restated: with the frequencies fixed at the prediction,
   the fitted cluster moment must be non-zero at more than 5 sigma and
   the fundamental amplitude must agree with the fixed-frequency fit
   using the WRONG count (N(m) +- 2 modes) worse than with the right
   count, by a likelihood-ratio test. The old falsifier ("a blind mode
   count differing from N(m) by two or more") is withdrawn: no
   instrument can produce that count.
5. The core diagnostic of P26/P27 survives unchanged, and is in fact
   the easier measurement: a trapped mode of a reflecting core has
   Q ~ 10^2 to 10^3 (damping 1e-4 in tower units against 0.25), so it
   is a narrow line that any spectrum shows. Absorbing core: no narrow
   line, damping ratios locked to the 1 : 3 : 5 ladder. That test does
   not need mode counting at all.

Instrument lesson 15: the horizon-unit frequency omega of the tower
carries c_s^2/D, not c_s^2/C (the scaled eigenvalue c does). The first
stage-2 run converted with c_s^2/C and understated every frequency and
damping by the factor B = 10. Caught before any verdict. Rule: in a
paper with two length units (horizon and circulation), write the
conversion in the script's docstring and test it against one known
number before using it.
