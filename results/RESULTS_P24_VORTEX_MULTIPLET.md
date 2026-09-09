# P24, the borderline tower member: no multiplet, the mode escapes continuously (verdicts 2026-09-10)

Preregistration: `FROZEN_P24_VORTEX_MULTIPLET.md` (commit 3c40ecf).
Instrument: `find_qnm` / `leaver_function` (Leaver fraction of the
draining bathtub) at 50 digits with kmax 8000 to 64000, residual guard
1e-8, inversions 5 and 6. Scripts: `p23_m7_n5_track.py`,
`p23_m7_n5_track2.py` (deep tracks from B = 2.0 and 2.5),
`p23_m7_n5_deepprobe.py` (B = 2.5, 3.0, 3.5 with 32000 terms),
`p24_gap_check.py` (B = 3.0, 3.5, 4.0 from tightly placed seeds),
`p24_crossing.py` (secant continuation across the crossing),
`p24_reemerge.py` (B = 6, 8). Data: the JSON files of the same names.

## Summary

The m = -7, n = 5 counter-rotating overtone, whose pure-vortex tower
member c_5 = 0.0696 - 2.4303i has the smallest positive real part of
any member computed, does reach that member: at B = 6 and B = 8 a
principal-sheet root sits at omega B = 0.0799 - 2.424i and
0.0753 - 2.427i (within 0.012 and 0.007 of c_5), kmax-independent to
7e-4 at B = 6. The mode is on the principal sheet with a converged
root up to B = 2.68 (Re omega = 0.0447, 8000/16000 terms) and was
reported absent at B = 3.0, 3.5, 4.0 by every Muller search (seeds
within 0.02 of its expected position, 16000 to 64000 terms: the
iteration converges to the n = 4 or n = 2 modes instead). A secant
continuation with a 1e-4 initial step follows the root without a break
from B = 2.68 to 3.06 (Re omega 0.0447 -> 0.0354, 16000 and 32000
terms agreeing to 1e-5 at every point, omega B = 0.1083 - 2.405i at
the end), through the very spins where Muller found nothing. There is
no crossing and no gap: the frozen multiplet reading (P24.1) dies by
its own kill clause, which named exactly this possibility, and the
escape rule of P21h holds at its most delicate test with the mode
collapsing continuously, if slowly, onto c_5. The Muller false
negatives are an instrument lesson, recorded below.

## Verdict table

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P24.1 absorption at B_c in (2.5, 3.0), linear approach, Im at crossing within 0.05 of -2.43/B_c | KILL: root persists with Re > 0.01 to B = 3.0 | root followed continuously to B = 3.06 with Re(omega) = 0.0354 (0.0366 at B = 2.999), 16000/32000-term agreement 1e-5; slopes dRe/dB -0.029 to -0.020, still decelerating; omega B drifts smoothly from 0.1197 - 2.397i (2.68) to 0.1083 - 2.405i (3.06), then 0.0799 - 2.424i (6) and 0.0753 - 2.427i (8) | KILLED (by the frozen kill clause: the B = 3.0 absence was a solver failure) |
| P24.2 re-emergence: root near c_5/B at B = 6 and 8, kmax-independent (32000 vs 64000) to 1e-3, omega B within 0.05 of c_5 at B = 8 | KILL: none at B = 6 or 8 | B = 6: 0.013147 - 0.404215i (32000) vs 0.013310 - 0.403985i (64000), relative change 7e-4, omega B = 0.0799 - 2.4239i (0.012 from c_5); B = 8: 0.010240 - 0.303408i vs 0.009415 - 0.303363i, relative change 2.7e-3 (the real part, 3% of the modulus, still moves 8%), omega B = 0.0753 - 2.4269i (0.007 from c_5); both seed-independent | CONFIRMED (the 1e-3 kmax clause met at B = 6, missed at 2.7e-3 at B = 8 where Re/|omega| = 0.03) |
| P24.3 neither endpoint pinned | expectation | void: there are no endpoints | VOID |

## The trajectory

| B | Re(omega) | Im(omega) | omega B | instrument |
|---|---|---|---|---|
| 2.00 | 0.078452 | -1.184744 | 0.1569 - 2.3695i | kmax 3000/6000/12000 agree (3 inversions) |
| 2.30 | 0.059424 | -1.036919 | 0.1367 - 2.3849i | kmax 4000/8000 (gate 2e-3) |
| 2.50 | 0.050719 | -0.956869 | 0.1268 - 2.3922i | kmax 8000/16000/32000 agree to 1e-7 |
| 2.679 | 0.044666 | -0.894802 | 0.1197 - 2.3972i | kmax 8000/16000 (gate 2e-3, last point that passes) |
| 2.699 | 0.044070 | -0.888359 | 0.1189 -2.3978i | secant continuation, 16000/32000 agree to 1e-06 |
| 2.759 | 0.042367 | -0.869565 | 0.1169 -2.3992i | secant continuation, 16000/32000 agree to 2e-06 |
| 2.819 | 0.040780 | -0.851536 | 0.1150 -2.4006i | secant continuation, 16000/32000 agree to 3e-06 |
| 2.879 | 0.039300 | -0.834229 | 0.1131 -2.4018i | secant continuation, 16000/32000 agree to 4e-06 |
| 2.939 | 0.037915 | -0.817602 | 0.1114 -2.4030i | secant continuation, 16000/32000 agree to 7e-06 |
| 2.999 | 0.036619 | -0.801616 | 0.1098 -2.4041i | secant continuation, 16000/32000 agree to 1e-05 |
| 3.059 | 0.035403 | -0.786234 | 0.1083 -2.4052i | secant continuation, 16000/32000 agree to 1e-05 |
| 3.059 | 0.035403 | -0.786234 | 0.1083 -2.4052i | secant continuation, 16000/32000 agree to 1e-05 |
| 3.0, 3.5, 4.0 | none | | | seeds within 0.02 of the expected position; 16000-64000 terms converge to n = 4 (B = 3.0) or n = 2 (3.5, 4.0) |
| 6.0 | 0.013310 | -0.403985 | 0.0799 - 2.4239i | 32000/64000 agree to 7e-4 |
| 8.0 | 0.009415 | -0.303363 | 0.0753 - 2.4269i | 32000/64000 agree to 2.7e-3 |

The slopes dRe/dB before the crossing decelerate steadily (-0.077 at
B = 2.0, -0.048 at 2.33, -0.030 at 2.68): the approach to the axis is
not the constant-slope arrival of the m = -1 overtones (P21.1) but the
curved, analytic arrival seen in Kerr (P22), here on the vortex side.

The slopes dRe/dB decelerate steadily (-0.077 at B = 2.0, -0.048 at
2.33, -0.030 at 2.68, -0.020 at 3.06): the real part is heading for
zero only as 1/B, the collapse of an escaping mode, not the linear
arrival of an absorbed one. A three-term fit omega B = c + d/B + e/B^2
to the points at B = 3.06, 6 and 8 gives c = 0.066 against the tower's
0.0696.

## What it means

The escape rule "overtone n escapes iff Re c_n(m) > 0" (P21h) holds at
its most delicate test: the member with Re c_5 = 0.07, three times
closer to the axis than any earlier one, is reached by a continuous
principal-sheet trajectory, and the multiplet structure of Kerr
(P22) has no counterpart here. With P23's count law this closes the
vortex program: 1, 2, 2, 3, 4, 5, 6 overtones escape for |m| = 1..7
(all seven now measured at finite B), the count is
floor(0.8008 |m| + 1/2) from the light-ring action, and the modes that
do not escape are absorbed linearly by the cut (m = -7, n = 6 at
B_c = 0.795).

Instrument lesson 12 (the false negative behind this freeze): mpmath's
Muller iteration, started within 0.02 of a near-axis root
(Re/|omega| ~ 0.04), converged to a neighbouring mode with larger real
part in every one of 36 attempts at B = 3.0 to 4.0 and up to 64000
terms, while a secant with a 1e-4 initial step followed the root
without difficulty. Absence of a root under Muller-only searches near
the axis is not evidence of absence; continuation with a local method
is the instrument, and the P24 freeze was written on a Muller-only
result (its kill clause, which named the solver failure, is what
saved the record).
