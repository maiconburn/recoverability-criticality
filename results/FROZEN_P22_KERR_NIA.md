# P22, Kerr overtones arriving at the negative imaginary axis (freeze, 2026-09-09)

Frozen BEFORE tracking any Kerr sequence beyond spin a/M = 0.05.

## Context

Cook and Zalutskiy (PRD 94, 104074, 2016) showed that Kerr gravitational
overtone sequences with m <= 0 reach the negative imaginary axis (NIA)
at finite spin, vanish over a spin interval, and in many cases
re-emerge (overtone multiplets); for l = 2, m = 0 the n_0 segments
terminate at omega M = -i n/4 (algebraically special, polynomial modes),
and for n >= 27 no second segment exists. They tabulate the endpoints
to 1e-9 in Re(omega) but do not give the law of approach. P21 found,
in the analogue draining vortex, that the approach to the cut is
LINEAR in the rotation parameter (raw exponents 1.000, 1.004, 1.002)
and that nothing re-emerges. The question here is whether the Kerr
arrival law is the same, with the structural difference that Kerr has
polynomial modes on the axis and the vortex has none.

## Instrument (frozen)

The `qnm` package's NearbyRootFinder (Leaver radial continued fraction
coupled to the spectral angular problem), s = -2, l_max = 20, with our
discipline: a root is accepted only if the inversions n_inv = n-1, n,
n+1 agree to 1e-8 and the value is unchanged (1e-6 relative) between
truncation caps Nr_max = 4000 and 16000; classification of the approach
uses points that pass the gate (Re(omega) typically > 1e-3). Spin steps
adaptive, halving on failure, tracking from a/M = 0.05 upward.
Schwarzschild anchor: l = 2, n = 9 at a = 0.01 found at
0.063244 - 2.302605i by all three inversions.

## Predictions

P22.1 (linear arrival, m = 0): the {2, 0, 9_0} sequence reaches the
NIA at a_0/M = 0.3057 +- 0.002 (Cook-Zalutskiy: 0.305661) with
Im(omega M) = -2.250 +- 0.002 (the polynomial point -i n/4), and the
local exponent of Re(omega M) against (a_0 - a) over the last decade
that passes the gate is 1.0 +- 0.15 (dRe/da constant).
KILL: exponent 0.5 +- 0.12 (fold), or outside [0.7, 1.3].

P22.2 (linear arrival, m = -2): the {2, -2, 13_0} sequence reaches the
NIA at a_0/M = 0.6575 +- 0.003 with Im(omega M) = -3.390 +- 0.003 and
the same linear law, exponent 1.0 +- 0.15.
KILL: as P22.1.

P22.3 (the gap and the re-emergence, Kerr-only): no gate-passing
principal-sheet root exists for {2, 0, 9} in the band
Im(omega M) in (-2.45, -2.15), Re(omega M) < 0.05, for
a/M in (0.315, 0.395); a root re-appears near -2.388i just above
a/M = 0.4047 (Cook-Zalutskiy's 9_1 segment) with small positive real
part growing with spin.
KILL: a kmax-independent root inside the gap, or no re-emergence by
a/M = 0.42.

P22.4 (contrast with the vortex, recorded as expectation, no new
measurement): the Kerr arrival frequencies are pinned to polynomial
points, the vortex arrivals are not pinned (measured -1.1616, -2.2267,
-3.2541 for m = -1 and -1.8095, -2.9552 for m = -2, none rational);
this follows from the presence/absence of polynomial solutions of the
respective recurrences (P21b lemma) and is what P22.1's Im check
tests at 1e-3.
