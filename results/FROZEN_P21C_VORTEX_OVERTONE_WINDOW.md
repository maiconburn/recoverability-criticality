# P21c, overtone-resolving time-domain window (addendum freeze, 2026-09-09)

Frozen BEFORE the run. P21b.2 and P21b.3 came out VOID by instrument
design: the window frozen in P21b opens 37 time units after the
excitation, and the n = 1 counter-rotating overtone at B_c(m = -1, n = 1)
has |Im omega| = 1.16 (e-folding time 0.86), so it had decayed by 1e-19
before the window opened. P21b.1 (continuity, exponent 1.000) is
unaffected and stands. This addendum re-freezes b.2 and b.3 with a
window that can see the overtone.

Instrument (frozen): same solver; Gaussian datum at r* = 10 with width
0.7 and carrier 0.3; observer at r* = 3 (between the datum and the
potential peak near r* ~ 0); window t in [14, 26] (the ingoing pulse
passes the observer at t ~ 7, the scattered ringdown reaches it from
t ~ 13); matrix-pencil order 8. Gate: at B = B_c - 0.04 = 0.2494 the
pencil must return the counter-rotating n = 1 frequency within 0.03 of
the continued-fraction value 0.025129 - 1.171928i AND the fundamental
within 0.03 of its continued-fraction value at that B; if the gate
fails, the overtone is not resolvable by this instrument and b.2 is
declared untestable (not killed).

P21c.2 (the ghost): on both sides of B_c (B_c +- 0.01) the pencil
returns a damped component within 0.1 of -1.1616 i (the arrival
frequency), with amplitude ratio (B_c + 0.01)/(B_c - 0.01) in [0.5, 2].
KILL: component absent on the B_c + 0.01 side while present on the
B_c - 0.01 side, or amplitude ratio outside [0.2, 5] (a 2x window is
too tight for a pencil on a fast-decaying mode; the kill window is set
at 5x, the confirmation window at 2x, both frozen now).

P21c.3 (mutual gate): as P21b.3 with the new window.
