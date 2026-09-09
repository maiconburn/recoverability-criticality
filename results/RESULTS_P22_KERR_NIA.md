# P22, Kerr overtones arriving at the negative imaginary axis: verdicts (2026-09-09)

Preregistration: `FROZEN_P22_KERR_NIA.md` (commit 65cc68a). Instrument:
the `qnm` package's NearbyRootFinder (Leaver radial continued fraction
with the spectral angular problem, s = -2, l_max = 20) under the P21
discipline: three-inversion agreement, truncation-cap gate,
classification only where the fraction converges. Scripts:
`p22_kerr_nia.py` (tracks with cap 16000/48000, gap search),
`p22_kerr_nia_deep.py` (caps 1e5, 4e5, 1e6, 4e6 toward the endpoints),
`p22_kerr_nia_reemerge.py` (deep downward track of the re-emerged
segment). Data: `p22_kerr_nia.json`, `p22_kerr_nia_deep.json`,
`p22_kerr_nia_reemerge.json`, logs alongside. Reference values: Cook
and Zalutskiy, PRD 94, 104074 (2016), Table II.

## Summary

The Kerr counter-rotating overtone sequences {2, 0, 9_0} and
{2, -2, 13_0} reach the negative imaginary axis (NIA) LINEARLY in the
spin, as the vortex overtones reach the branch cut, but with a
curvature the vortex does not have: the local exponent of Re(omega)
against (a_0 - a) rises monotonically from 0.63 at a_0 - a = 0.02 to
0.93 at a_0 - a = 0.002, the last-decade fits are 0.893 and 0.901
(frozen window 1.0 +- 0.15), and Re(omega)/(a_0 - a) is a smooth
polynomial in (a_0 - a) with a finite limit (1.87 and 1.81) at the
endpoint. No fold (exponent 1/2) anywhere. The endpoints and the
arrival frequencies agree with Cook-Zalutskiy to 2e-4 in spin and
2e-4 (m = 0, pinned to the polynomial point -9i/4) and 2e-3 (m = -2,
not rational) in Im(omega). The re-emergence of the {2, 0, 9_1}
segment is seen with the deep instrument (birth from the NIA at
a_1 = 0.40462 against Cook-Zalutskiy's 0.404696, linear emergence with
the same rising local slope), a process the vortex does not have
(P21g: nothing is born from the cut). The frozen gap prediction died
as written: the frozen band contains the {2, 0, 8_1} segment, which
emerges at -2.19086i at a = 0.315947 inside it; two gate-passing roots
at a = 0.34 and 0.36 sit on that segment.

## Verdict table

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P22.1 {2, 0, 9_0}: a_0 = 0.3057 +- 0.002, Im = -2.250 +- 0.002, last-decade exponent 1.0 +- 0.15 | as stated; KILL 0.5 +- 0.12 or outside [0.7, 1.3] | a_0 = 0.30583 by linear extrapolation of the last two converged points (a = 0.303, 0.304), Im(omega) = -2.25083 at a = 0.304 and -2.24977 by quadratic extrapolation to a_0; local exponents 0.633, 0.706, 0.784, 0.855, 0.895, 0.926 (a_0 - a from 0.026 to 0.0017); fit over a_0 - a in [1e-3, 1e-2]: 0.893 | CONFIRMED (linear endpoint, strong curvature before it) |
| P22.2 {2, -2, 13_0}: a_0 = 0.6575 +- 0.003, Im = -3.390 +- 0.003, exponent 1.0 +- 0.15 | as stated | a_0 = 0.65788 (last two converged: a = 0.652, 0.654), Im(omega) = -3.38443 at a = 0.654 and -3.38814 by quadratic extrapolation; local exponents 0.711, 0.809, 0.880, 0.914; last-decade fit 0.901 | CONFIRMED |
| P22.3a no gate-passing root in the band Im in (-2.45, -2.15), Re < 0.05, for a in (0.315, 0.395) | KILL: a kmax-independent root inside the gap | gate-passing roots at a = 0.34 (0.030474 - 2.176713i) and a = 0.36 (0.045009 - 2.167098i); none at 0.32, 0.38, 0.395. They are the {2, 0, 8_1} segment: Cook-Zalutskiy Table II has 8_1 emerging at -2.19086i at a = 0.315947, inside the frozen band and spin interval | KILLED as frozen (band drawn over a neighbouring segment; see graveyard) |
| P22.3b re-emergence near -2.388i just above a = 0.4047, small positive Re growing with spin | KILL: no re-emergence by a = 0.42 | cap-48000 search at 0.405, 0.41, 0.42 saw nothing (blind below Re ~ 0.03); deep downward track from a = 0.44 (0.042694 - 2.375658i): 0.023206 - 2.384473i at 0.42, 0.009254 - 2.387762i at 0.41, 0.005069 - 2.388182i at 0.4075, 0.003419 - 2.388266i at 0.40656 (cap 4e6); linear extrapolation a_1 = 0.40462, Im -2.38827 (Cook-Zalutskiy 0.404696, -2.38829i) | CONFIRMED with the deep instrument (the frozen instrument would have killed it) |
| P22.4 Kerr arrivals pinned to polynomial points, vortex arrivals not (expectation) | Im check at 1e-3 | m = 0: -2.2498 / -2.2501 (quadratic extrapolation / unconverged tail at a = 0.3053) against -9/4; m = -2: -3.388 against Cook-Zalutskiy's -3.38997, not rational | recorded: pinning holds where a polynomial mode exists (m = 0) and only there |

## The arrival curves

{2, 0, 9_0}, converged points (two consecutive caps agree to 2e-6
relative; cap = the smaller of the two):

| a | Re(omega M) | Im(omega M) | cap | Re/(a_0 - a) |
|---|---|---|---|---|
| 0.28 | 0.026578053 | -2.263054323 | 4e5 | 1.036 |
| 0.29 | 0.019445556 | -2.258497086 | 4e5 | 1.242 |
| 0.295 | 0.014824349 | -2.255900027 | 4e5 | 1.391 |
| 0.30 | 0.009023875 | -2.253089599 | 1e6 | 1.594 |
| 0.302 | 0.006216037 | -2.251939589 | 1e6 | 1.698 |
| 0.303 | 0.004672463 | -2.251374865 | 1e6 | 1.756 |
| 0.304 | 0.003020189 | -2.250828314 | 4e6 | 1.818 |

Unconverged tail at cap 4e6 (inversions spread 3e-10 to 2e-7, cap
1e6 vs 4e6 differ by more than 2e-6): a = 0.3045, 0.305, 0.3053 give
Re/(a_0 - a) = 1.851, 1.880, 1.927 and Im = -2.25057, -2.25031,
-2.25013.

{2, -2, 13_0}, converged points:

| a | Re(omega M) | Im(omega M) | cap | Re/(a_0 - a) |
|---|---|---|---|---|
| 0.63 | 0.032279988 | -3.368434668 | 4e5 | 1.175 |
| 0.64 | 0.023401951 | -3.372725522 | 4e5 | 1.339 |
| 0.65 | 0.011772990 | -3.379888610 | 1e6 | 1.576 |
| 0.652 | 0.008950573 | -3.381974515 | 1e6 | 1.636 |
| 0.654 | 0.005905358 | -3.384425987 | 4e6 | 1.701 |

Unconverged tail: a = 0.655, 0.656, 0.6565 give Re/(a_0 - a) = 1.735,
1.771, 1.674 with Im = -3.38583, -3.38737, -3.38822; at 0.657 and
0.6572 the cap-4e6 values (Re/(a_0 - a) = 2.7, 4.1) are not usable.

Shape of the law. In the vortex (P21) dRe/dB was constant to three
digits over the last decade. Here dRe/da is not: Re/(a_0 - a) grows
from 1.04 to 1.82 over the converged range and keeps growing in the
unconverged tail. A cubic Re = c_1 d + c_2 d^2 + c_3 d^3 with
d = a_0 - a fits the converged points to 1.7% (m = 0: c_1 = 1.873,
c_2 = -53.0, c_3 = 793) and 0.35% (m = -2: c_1 = 1.806, c_2 = -33.3,
c_3 = 375); a d ln d correction fits worse (12% for m = 0). The
arrival is therefore analytic and linear at the endpoint
(exponent 1, dRe/da -> -1.87 and -1.81), with a quadratic
correction large enough that the local exponent measured at
a_0 - a ~ 0.01 reads 0.7 to 0.8. The frozen window 1.0 +- 0.15 is
met by the last-decade fits (0.893, 0.901), but the honest reading
is: linear endpoint, non-asymptotic curvature over the whole
accessible range. The curvature scale (c_2/c_1 ~ 20 to 30 per unit
spin) has no vortex counterpart; whether it is set by the distance
to the polynomial point on the axis (m = 0) or by the neighbouring
segments (8_1 emerges at 0.3159, ten thousandths above the 9_0
endpoint) is not decided here.

## The gap and the re-emergence

Main run, gated search (cap 48000, inversions 8, 9, 10, 18 seeds per
spin), roots in the frozen band:

| a | roots found |
|---|---|
| 0.32 | none |
| 0.34 | 0.030474 - 2.176713i |
| 0.36 | 0.045009 - 2.167098i |
| 0.38, 0.395, 0.405, 0.41, 0.42 | none |
| 0.44 | 0.042694 - 2.375658i |

The a = 0.34 and 0.36 roots grow linearly from the {2, 0, 8_1}
emergence point of Cook-Zalutskiy (a = 0.315947, -2.19086i): Re(omega)
= 0.030 and 0.045 at distances 0.024 and 0.044 from it (slopes 1.27
and 1.02, the same rising-slope shape as the arrivals seen from the
other side), and Im(omega) moves up from -2.191. They are not a
{2, 0, 9} root, but the frozen statement was about the band, and the
band was drawn without checking the 8_1 row of the reference table.
Killed as written; tombstone in `GRAVEYARD.md`.

The a = 0.44 root is the {2, 0, 9_1} segment. Tracked downward with
the deep caps (`p22_kerr_nia_reemerge.py`):

| a | Re(omega M) | Im(omega M) | cap |
|---|---|---|---|
| 0.44 | 0.042694461 | -2.375657695 | 1e5 |
| 0.435 | 0.038526110 | -2.377942436 | 4e5 |
| 0.43 | 0.033955594 | -2.380195253 | 4e5 |
| 0.425 | 0.028890686 | -2.382389871 | 4e5 |
| 0.42 | 0.023206013 | -2.384473427 | 4e5 |
| 0.415 | 0.016732026 | -2.386338305 | 4e5 |
| 0.41 | 0.009253746 | -2.387762376 | 1e6 |
| 0.4075 | 0.005069433 | -2.388181793 | 1e6 |
| 0.40656 | 0.003418576 | -2.388266173 | 4e6 |

Emergence slope dRe/da rises from 0.83 (a = 0.44) to 1.76 (a = 0.4066)
toward the axis, mirroring the arrival curves (local exponents
against a - a_1: 0.78, 0.83, 0.90, 0.96, 1.00 from a = 0.44 inward);
the birth spin by linear extrapolation of the last two converged
points is a_1 = 0.40462 and the birth frequency -2.38827i
(Cook-Zalutskiy: 0.404696, -2.38829i; differences 7e-5 and 2e-5).
Below a = 0.4066 the cap-4e6 fraction no longer converges
(Re(omega) < 3e-3).

The shallow instrument (cap 48000) could not see this segment at
a = 0.405 to 0.42, where Re(omega) < 0.023: the frozen kill
criterion "no re-emergence by a = 0.42" would have fired on an
instrument artifact. The deep track is the record.

## What differs from the vortex, and why

| | draining vortex (P21) | Kerr (P22) |
|---|---|---|
| arrival law | linear, dRe/dB constant to 3 digits over a decade | linear at the endpoint, local exponent 0.63 -> 0.93 over the last decade, cubic in (a_0 - a) |
| arrival frequency | not rational (no polynomial solution: P21b lemma) | m = 0: pinned to -i n/4 (polynomial modes on the axis) |
| beyond the arrival | nothing on the principal sheet; nothing born from the cut (P21g) | segments re-emerge from the axis (9_1 at 0.4047) |
| the axis | branch cut of the 1/r^2 tail only | branch cut plus modes on the NIA (Cook-Zalutskiy Sec. IV) |

The common core is the theorem's: the sequence reaches the axis
linearly in the control parameter, never with a fold, because the
axis is not an exceptional point of the spectrum but a place where
the mode label loses its meaning (the quasinormal mode merges into
the branch-cut continuum). The structural difference is that Kerr's
axis carries polynomial (algebraically special) modes and the vortex's
does not: in Kerr, sequences can end on such a mode and other
sequences can begin there, so the label bookkeeping (Cook-Zalutskiy's
overtone multiplets) is richer, while the vortex has only absorption.
The response continuity through the arrival (P21b.1 in the vortex,
exponent 1.000) was not measured in Kerr in this cycle.

## Instrument lessons (recorded)

Lesson 8 (Kerr near the axis): the radial fraction needs a
truncation cap of roughly 30 to 80 / Re(omega)^2 (4e6 at
Re(omega) = 3e-3; 1e6 at 9e-3; 4e5 at 2e-2). The 48000 cap of the
main run stalls at Re(omega) ~ 0.025 to 0.033 and is blind to any
segment within ~0.02 in spin of its birth or death. Classify arrivals
and emergences only where two consecutive caps agree (2e-6 relative);
the three unconverged points nearest each endpoint are reported as
unconverged and excluded from the fits.

Lesson 9 (freezing a "no root in the band" prediction): check every
neighbouring segment of the reference table against the band before
freezing. P22.3a died on the 8_1 row that was three lines above the
9_0 row used to set the band.

## Why the arrival is analytic (theory addendum, 2026-09-09)

Leaver's radial function F(omega, a), the continued fraction or
equivalently the Wronskian of the two admissible solutions, is built
from the minimal solution of a recurrence whose large-k behaviour
carries a square root of omega: u_1(omega) in Cook-Zalutskiy's
Eqs. 19-20 for Kerr, the Nollert tail (-2 i omega)^{1/2} in the vortex
fraction. The sign choice Re(u_1) < 0 selects the minimal solution and
makes F single-valued on the plane cut along the negative imaginary
axis; F is analytic in (omega, a) on that sheet, and its analytic
continuation across the cut is the same expression with the other
sign of u_1, analytic as well, because every ingredient is analytic
in u_1 and u_1 is analytic in omega away from the branch point
omega = 0. A quasinormal mode is a root F(omega(a), a) = 0. Wherever
dF/d omega is nonzero (no exceptional point) the implicit function
theorem makes omega(a) analytic in a, including at the spin a_0
where Re omega(a_0) = 0: the cut is a property of the sheet labelling,
not a singularity of the continued function. Therefore

    Re omega(a) = c_1 (a_0 - a) + c_2 (a_0 - a)^2 + ...

with c_1 nonzero generically: exponent 1, never 1/2, and the mode does
not stop at the axis but continues onto the second sheet, where it is
no longer a pole of the retarded Green's function on the physical
sheet. The response stays continuous because the pole's contribution
passes continuously into the cut integral (P21b.1, exponent 1.000 in
the vortex). The measured curvature (c_2/c_1 of order -30 per unit
spin in Kerr, about zero in the vortex) is the size of the second
Taylor coefficient of an analytic function and carries no critical
content.

Two caveats. (i) At a polynomial point (Kerr, m = 0, omega = -i n/4)
the minimal/dominant distinction of the recurrence degenerates
(Cook-Zalutskiy Sec. IV) and the argument as stated does not cover
the endpoint itself; the data (local exponent rising to 0.93 at
a_0 - a = 0.0017, cubic fit to 1.7%) are consistent with analyticity
through it, but the pinning of the death of 9_0 to exactly -9i/4
is the polynomial structure acting, which the vortex (no polynomial
solutions, P21b lemma) cannot show. (ii) If dF/d omega vanished at the
arrival the exponent would be 1/2, a genuine exceptional point on the
axis; none was seen in either system. The argument also explains the
re-emergence: a second-sheet root can cross back to the principal
sheet at another spin, again analytically, which is what 9_1 does at
a_1 = 0.40462 with the same rising-slope shape.
