# P21, the draining-bathtub vortex: frozen predictions (preregistration, 2026-09-09)

Frozen BEFORE any scan beyond the published, validated region. Each
prediction carries a kill criterion.

## Context

The draining bathtub (DBT) is the rotating acoustic black hole realized
in water tanks (Torres, Patrick, Richartz, Weinfurtner, PRL 2020:
counter-rotating QNM oscillations measured for m = -1 ... -25 at
circulation C = 151 cm^2/s, drain negligible in the observation region).
Its QNM spectrum was computed by Berti-Cardoso-Lemos (PRD 70, 124006,
2004; WKB) and Cardoso-Lemos-Yoshida (PRD 70, 124032, 2004; Leaver
continued fraction). CLY report, for counter-rotating modes (m < 0),
that each overtone n >= 1 reaches Re(omega) = 0 at a critical rotation
B_c(m, n) and that they "have not been able to follow the mode beyond
this point" (their Figs. 5-8), while the fundamental n = 0 approaches
Re(omega) -> 0 only asymptotically as B -> infinity. Twenty years later
this is still open (arXiv scan 2026-09-09: "draining bathtub" AND
exceptional: zero hits; the 2025 shallow-water pseudospectrum paper,
arXiv:2504.00107, treats a vorticity bump at B = 0 only).

The DBT potential has an inverse-square tail (2+1 dimensions, late-time
tails t^{-(2m+1)}, BCL sec. II.D), so the retarded Green's function has
a BRANCH CUT along the negative imaginary omega axis. A QNM trajectory
on the physical sheet cannot cross Re(omega) = 0 at Im(omega) < 0
without meeting the cut. The "unfollowable" counter-rotating overtones
are therefore modes arriving at the branch cut, the DBT analogue of the
Kerr mode sequences that approach the negative imaginary axis
(Cook-Zalutskiy 2016). Whether they pass to the second sheet, are
absorbed at a special point, or collide with a second-sheet partner is
the question, and it is testable in a tank with a drain.

## Instruments (frozen)

- Instrument of record: Leaver continued fraction with the CLY four-term
  recurrence (`src/recoverability_ep/dbt.py`), Nollert-seeded tail,
  n-th inversion, mpmath 20-30 digits, kmax 400-800, with a RESIDUAL
  GUARD (|f| < 1e-18 at the root) and rejection of on-axis roots
  (branch-cut artifacts: the first run produced a stalled "root" at
  -3.26566i with |f| = 2e-14 whose Frobenius series does not terminate;
  the true n = 3 mode of m = 1 at B = 0 is 0.034974 - 3.259712i).
  Validated at B = 0 against BCL Table I (m = 3, 4 to 1e-3, WKB6
  accuracy) and at B = 0 and B = 0.2 against the CLY figures (n = 0, 1
  for m = +-1, +-2).
- Coarse seeding map: Chebyshev collocation in Leaver's variable with the
  regular-singular reduction (N = 60-80, double precision; reproduces
  the fundamental to 4e-7 at N = 60 but degrades with N because of the
  branch cut). Never a source of a claim on its own.
- Tracking by continuation in B with step halving on failure; the
  symmetry S(-m, B) = -conj S(m, B) is used as a cross-check.

## Predictions

P21.1 (arrival at the cut). For m = -1 and m = -2, every overtone
n = 1, 2, 3 reaches Re(omega) = 0 at a finite B_c(m, n) with a LINEAR
approach: the local exponent of Re(omega) against (B_c - B), estimated
from the last decade before B_c, is 1.0 +- 0.15, and Im(omega) is
smooth (no kink) through B_c. Beyond B_c no root exists on the
principal sheet within |omega - omega(B_c)| < 0.3 (exhaustive local
search with inversions n = 0..5 from a 5x5 grid of starts): the mode is
absorbed by the branch cut.
KILL: exponent 0.5 +- 0.12 (a fold on the cut: collision with a
second-sheet partner, an "EP on the cut"), or a principal-sheet root
continuing past B_c.

P21.2 (no EP at real rotation). On the principal sheet, for m in
{+-1, +-2}, n <= 3 and B in (0, 10], there is NO genuine EP-2 between
two modes of the same m: every closest approach is an avoided crossing
with minimal gap > 1e-3, and the large-B "coalescence" of the
co-rotating overtones (CLY Figs. 1-2) is a clustering of real parts
with imaginary parts separated by more than 0.3.
KILL: a pair with gap < 1e-6 passing the wall + splitting
classification (ERRATA E3 criterion).

P21.3 (complex-rotation EPs behind avoided crossings). Any avoided
crossing with minimal gap < 0.1 found in P21.2 is the shadow of an EP-2
at complex B_c with |Im B_c| < 0.5, found by continuation in complex B,
and the real-B gap follows the Puiseux law
gap(B) = 2 sqrt(|c| |B - B_c|) with R^2 > 0.99 across the crossing.
KILL: an avoided crossing with gap < 0.1 and no complex-B EP within
|Im B| < 0.5 (a non-EP avoided crossing: new class).
VOID if P21.2 finds no gap below 0.1.

P21.4 (the fundamental never arrives). For m = -1 and m = -2, n = 0:
Re(omega)(B) has no zero at finite B; on B in [10, 100] it follows a
power law with exponent -1.0 +- 0.2 (CLY's WKB expectation omega ~ k/B).
KILL: finite B_c for n = 0, or exponent outside the window.

P21.5 (reachability). B_c(m = -1, n = 1) lies in [0.2, 0.5] (CLY Fig. 5
suggests ~ 0.3) and B_c(m = -2, n = 1) in [0.3, 1.0]. With B/A = C/D,
a tank at C ~ 0.015 m^2/s needs D ~ 0.03-0.07 m^2/s: a strong but
feasible drain. KILL: B_c(m = -1, n = 1) < 0.1 or > 1.

## Declared risks

- Close to the cut the continued fraction loses its convergence
  discrimination (equal-modulus solutions); the last ~10% of the
  approach may need kmax 2000+ and 30 digits. Exponents are read from
  the decade BEFORE that zone.
- The second sheet is reachable only by analytic continuation of the
  continued fraction (flipped Nollert branch) and is NOT required for
  any verdict above; if it works, it is a bonus.
- Overtone labels can swap at avoided crossings; the invariants
  (mu, rho) of adjacent pairs are tracked instead of labels.
