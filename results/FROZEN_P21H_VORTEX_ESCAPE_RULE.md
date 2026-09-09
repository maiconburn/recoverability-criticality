# P21h, the escape rule: Re c_n(m) > 0 (freeze, 2026-09-09)

Frozen BEFORE the m = -6 finite-B run and before any m = -7 computation.

## Evidence in hand

- Finite-B escape counts 1, 2, 2, 3, 4 for |m| = 1..5 (P21d, P21e, P21g;
  at m = -5 the n = 3 overtone escapes along the trajectory of the
  fourth pure-vortex resonance c_3 = 0.296 - 1.586i, bridged from
  B = 4.8 to B = 20 with omega B = 0.31 - 1.59i throughout; n = 4
  arrives linearly, B_c ~ 4.2).
- The pure-vortex (scaled) tower has members with Re c > 0 numbering
  1, 2, 2, 3, 4, 5 for |m| = 1..6 (the m = -6 fifth member
  0.190 - 2.045i is a stable minimum of the Wronskian landscape, with a
  ~0.04 sensitivity to the inner cutoff), and the next member has
  Re c < 0 where it was looked for (m = -4: -0.203 - 1.512i).
- Deeper roots with Re c ~ 0.6 |m|, Im c ~ -3.6 found in one setting
  are NOT robust under changes of matching point and inner cutoff:
  artifacts, discarded.

## The rule

Overtone n of the counter-rotating family escapes absorption and
collapses onto the branch point as omega ~ c_n(m)/B if and only if the
n-th member of the pure-vortex tower has Re c_n(m) > 0. Overtones whose
pure-vortex partner has Re c_n(m) < 0 cannot reach it on the principal
sheet (the destination lies across the negative imaginary axis) and
are absorbed by the cut at finite B_c.

P21h.1: m = -6, robust tracker n = 0..5 to B = 10: exactly five
escaping modes (n = 0..4, omega B approaching 1.49-0.25i, 1.36-0.75i,
1.10-1.21i, 0.74-1.64i, 0.19-2.04i to within 10% at B = 10) and n = 5
absorbed at finite B_c < 5 (linear approach, Im finite).
KILL: n = 4 absorbed, or n = 5 escaping.

P21h.2: m = -7, scaled tower: the number of members with Re c > 0 is
N(7) (computed AFTER this freeze, reported as a prediction for the
finite-B run of m = -7, which is not part of this cycle).

P21h.3 (structure): across |m| = 1..6, Im c_n(m) for fixed n varies by
less than 15% with m (the tower damping is m-independent to that
accuracy: -0.25, -0.73, -1.18, -1.62, -2.04 for n = 0..4), while
Re c_n(m) decreases with n and increases with |m|.
KILL: a fixed-n damping varying by more than 30% across m.
