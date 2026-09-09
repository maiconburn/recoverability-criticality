# P28, the Kerr analogue of the escape rule: which m = 0 overtones survive extreme rotation (freeze, 2026-09-10)

Frozen BEFORE computing any extremal Kerr overtone beyond the cached
n <= 5 (l = 2), n <= 4 (l = 3), n <= 5 (l = 4).

## Evidence in hand

- Vortex (P21h, P23): the counter-rotating overtone n escapes
  absorption iff the large-rotation tower member has Re c_n > 0; the
  tower's real parts decrease with n by the light-ring anharmonicity
  and the count is N(m) = floor(0.8008 |m| + 1/2).
- Kerr, cached spectrum at a = 0.9999 (qnm package), l = 2, 3, 4,
  m = 0, s = -2: the damped modes (finite frequency at extremality)
  obey the same anharmonic law Re omega_n = Re omega_0 - kappa' n(n+1)
  with kappa' = 0.0111, 0.0078, 0.0060 (n <= 2) and kappa' falling
  slowly with n (0.0087 at n = 5, l = 2).
- Cook and Zalutskiy (2016): for m = 0 the sequences that reach or
  loop about the negative imaginary axis (the ZDM-like behaviour at
  high spin, many points of tangency) begin at n = 8 for l = 2, n = 18
  for l = 3, n = 25 for l = 4; lower overtones are single-segment
  sequences that keep a finite real part.

## The rule

The Schwarzschild overtone (l, m = 0, n) survives to extremality as a
damped mode iff the extremal damped-mode tower member n has
Re omega_n > 0; the tower's real part decreases with n (light-ring
anharmonicity) and crosses zero at an index n*(l); the overtones with
n >= n*(l) are the ones whose sequences die on, loop about, or are
born from the axis. Prediction: n*(l) coincides with Cook-Zalutskiy's
onsets.

P28.1: the extremal damped-mode towers of l = 2, 3, 4, m = 0,
computed at a = 0.9999 with the qnm root finder (three-inversion
agreement, truncation-cap gate 1e6 vs 4e6 at 1e-5) and seeded by the
anharmonic law, have Re omega_n > 0.02 for all n < n*(l) - 1 and
their first member with Re omega_n < 0.02 (or no converged damped
member) at n in [n*(l) - 1, n*(l) + 1], with n*(2) = 8, n*(3) = 18,
n*(4) = 25.
KILL: for any l the first such index differs from n*(l) by 3 or more.

P28.2 (the law): for each l the real parts of the tower members with
n < n*(l) - 1 are fitted to Re omega_0 - k a^2 + k' a^4 (a = n + 1/2)
with a residual below 0.01 in Re omega M, and k' > 0 (the curvature
that the crude quadratic fits of the cache could not determine).
KILL: residual above 0.03, or k' < 0 for two of the three l.

P28.3 (the damping law): Im omega_n is linear in n to 10% for
n < n*(l) - 1 (the light-ring ladder), with slope per unit n equal to
the extremal Lyapunov spacing of the (l, m = 0) photon orbit within
15% for l = 4 (eikonal limit).
KILL: nonlinear by more than 25%.

Instrument: `scripts/p28_kerr_survivors.py` (NearbyRootFinder at
a = 0.9999, seeds from the anharmonic fit of the previous members,
inversions n-1, n, n+1, Nr_max 1e6 gate 4e6). Cook-Zalutskiy's onsets
were read before the freeze (their Sec. III text); no member beyond
the cached ones has been computed.
