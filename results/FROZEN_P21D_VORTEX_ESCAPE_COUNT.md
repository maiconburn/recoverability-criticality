# P21d, how many counter-rotating modes escape the cut? (addendum freeze, 2026-09-09)

Frozen BEFORE any m = -3 run. Observed so far (P21 scan, continued-
fraction instrument with multi-inversion validation):

- m = -1: n = 1, 2, 3 arrive at the branch cut linearly at
  B_c = 0.2894, 0.1170, 0.0424; n = 0 never arrives and collapses onto
  the branch point omega = 0 as omega ~ (0.18 - 0.26 i)/B.
- m = -2: n = 2, 3 arrive at B_c = 0.425, 0.288; n = 0 AND n = 1 never
  arrive and collapse onto the origin as ~ c_n/B with
  c_0 ~ 0.46 - 0.25 i and c_1 ~ 0.11 - 0.68 i (the n = 1 inversion of
  the continued fraction loses the n = 1 mode at B ~ 1.01, but the
  other inversions hold it to B = 1.4 and the beyond-arrival search
  finds it at B = 1.67 - 1.75).

Conjecture to test: the number of escaping counter-rotating modes
equals |m| (one for m = -1, two for m = -2), the overtones n < |m| being
the light-ring-like long-lived family that survives fast rotation
(CLY's "omega ~ k/B" WKB branch), and every n >= |m| is absorbed by the
cut at finite B_c.

P21d.1: for m = -3, exactly the overtones n = 0, 1, 2 escape (no arrival
up to B = 10, Re omega and Im omega both decreasing towards 0) and
n = 3, 4 arrive linearly at finite B_c < 3.
KILL: n = 2 arriving, or n = 3 escaping, up to B = 10.

P21d.2 (ordering): among the arriving overtones of a given m, B_c
decreases with n (higher overtones arrive first), as for m = -1
(0.289 > 0.117 > 0.042) and m = -2 (0.425 > 0.288).
KILL: an inversion of the order for m = -3.

P21d.3 (collapse law): every escaping mode obeys omega ~ c_n/B for
B in [10, 100] with local exponents of Re and Im in [-1.2, -0.8].
KILL: an escaping mode with exponent outside the window (a different
asymptotic class).

Instrument: `scripts/p21_vortex_m2_robust.py` (inversion fallback,
two-inversion agreement, nearest-to-seed selection), seeds at B = 0
from eikonal guesses refined by the continued fraction; relative jump
guard 25% per step to prevent hopping between modes that are both
collapsing onto the origin (the fixed-inversion tracker hopped from
n = 0 to n = 1 of m = -2 between B = 3.8 and 6.7).
