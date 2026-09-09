# P24, a Kerr-like multiplet in the vortex at a borderline tower member (freeze, 2026-09-09, night)

Frozen BEFORE any probe of the m = -7, n = 5 mode beyond B = 3.5.

## Evidence in hand

- The pure-vortex tower member c_5(-7) = 0.0696 - 2.4303i (complex-ray
  solver, action-WKB 0.0681 - 2.4245i) has the smallest positive real
  part of any member tested; the escape rule (P21h) says the finite-B
  overtone n = 5 escapes onto it.
- The finite-B n = 5 mode is on the principal sheet with a
  kmax-independent root up to B = 2.5 (0.0507194719 - 0.956868877i,
  kmax 8000 / 16000 / 32000 agree to 1e-7; omega B = 0.1268 - 2.392i,
  0.06 from c_5) with Re(omega) decreasing at a decelerating rate
  (slopes -0.077 at B = 2.0 to -0.048 at B = 2.33).
- At B = 3.0 no root exists near c_5/B (or anywhere within 0.5 of
  omega B ~ 0.13 - 2.39i) for 32000 terms at 50 digits, from three
  seeds and two inversions; at B = 3.5 the same probe returns
  kmax-dependent values (0.031 - 0.688i, 0.013 - 0.809i,
  0.0095 - 0.674i for 8000, 16000, 32000 terms), not a root by the
  lesson-6 standard.
- The second-leg track from B = 2.5 (`p23_m7_n5_track2.py`, running at
  the time of this freeze) will locate the crossing if Re(omega)
  reaches the axis before B = 3.

## Reading

The absorption exponent argument of P22 (arrival at the cut is analytic
continuation onto the second sheet) allows a trajectory to cross the
cut and come back, which is what Kerr's {2, 0, 9_0} / {2, 0, 9_1} does
(death at a = 0.3057, rebirth at 0.4047). The escape rule concerns the
B -> infinity fate; a member with Re c_n small and positive can be
reached only after a finite excursion onto the second sheet.

## Predictions

P24.1 (absorption): the n = 5 track reaches the axis at
B_c in (2.5, 3.0) with a linear approach (last slopes constant to
within 30%), and Im(omega) at the crossing is within 0.05 of
-2.43 / B_c (the tower's damping scaled to B_c).
KILL: the root persists with Re(omega) > 0.01 to B = 3.0 (then the
B = 3.0 probe was a solver failure, not a crossing).

P24.2 (re-emergence): a principal-sheet root with Re(omega) > 0
exists near c_5/B at B = 6 and B = 8 (within 0.1 |c_5/B| + 0.01 of
(0.0696 - 2.4303i)/B), kmax-independent between 32000 and 64000 terms
at 50 digits to 1e-3 relative, with omega B within 0.05 of c_5 at
B = 8. The birth spin B' lies in (3.5, 6).
KILL: no such root at B = 6 or at B = 8. Then the tower member c_5 is
not reached by any finite-B mode, the escape rule as stated in P21h
fails at its borderline, and the count law N(m) has to be read as
"members with Re c_n > threshold" with the threshold set by the
finite-B structure; the m = -7 count would be 5, not 6, and the
freeze P21h.2 (N(7) = 6) dies.

P24.3 (analogy, recorded expectation): the gap (B_c, B') is the
vortex counterpart of Cook-Zalutskiy's overtone multiplets; since the
vortex has no polynomial modes on the axis (P21b lemma), neither
endpoint is pinned to a special frequency.

Instrument: `find_qnm` at 50 digits with resid_max 1e-8, kmax 32000
and 64000, inversions 5 and 6, seeds c_5/B and 0.6 c_5/B in real part.
