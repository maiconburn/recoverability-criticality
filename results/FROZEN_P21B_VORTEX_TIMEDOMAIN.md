# P21b, time-domain continuity through the cut (addendum freeze, 2026-09-09)

Frozen BEFORE any time-domain run at rotation B > 0 (the only run so far
is the B = 0 gate of the new solver `src/recoverability_ep/dbt_td.py`,
which recovers the fundamental 0.40703 - 0.34099i against the
continued-fraction value 0.406833 - 0.341236i).

## Lemma (no purely imaginary quasinormal modes in the DBT)

Cook and Zalutskiy (PRD 94, 104074, 2016) showed for Kerr that a mode
with purely imaginary frequency can be a quasinormal mode only if its
Frobenius series terminates (a polynomial mode). In the CLY four-term
recurrence for the DBT, termination at order K requires
a_{K+1} = a_{K+2} = a_{K+3} = 0 with a_K != 0, which by the recurrence at
k = K + 2 forces delta_{K+2} a_K = 0; but
delta_k = 4k^2 - 4k - 3 = (2k + 1)(2k - 3) never vanishes at integer k.
Hence, by the same argument, the DBT has no polynomial modes and no
purely imaginary quasinormal modes for any (m, B). A counter-rotating
overtone that reaches Re(omega) = 0 at B_c cannot remain a quasinormal
mode there: it leaves the principal sheet exactly at B_c. This sharpens
P21.1 and explains why Cardoso-Lemos-Yoshida could not follow the modes.

## The prediction: the response is continuous, the label is not

By the control-neutrality theorem the physical response is an analytic
function of the parameters through any spectral singularity. Therefore
the time-domain ringdown signal s(t; B) of a fixed counter-rotating
initial datum must vary SMOOTHLY through B_c even though a quasinormal
mode disappears from the principal sheet there: the absorbed mode's
contribution turns continuously into a branch-cut (second-sheet pole)
contribution.

P21b.1 (continuity). For m = -1 and the first arrival B_c(n = 1) found
by P21, with signals at B_c +- delta, delta in {0.005, 0.01, 0.02, 0.04}:
the relative L2 distance ||s(B_c + delta) - s(B_c - delta)|| / ||s(B_c)||
over the window t in [t_arrival + 5, t_arrival + 40] scales with
exponent 1.0 +- 0.25 in delta.
KILL: exponent < 0.5 (a jump: the absorption is visible in the
response), which would contradict the theorem in this system.

P21b.2 (the ghost). A matrix-pencil decomposition of s(t; B) on the
same window returns, on BOTH sides of B_c, a damped component within
0.1 of omega(B_c) = -i y_c with amplitude continuous through B_c
(ratio of amplitudes at B_c + 0.01 and B_c - 0.01 within [0.5, 2]).
KILL: the component absent or its amplitude dropping by more than
a factor 2 across B_c.

P21b.3 (the mode really leaves). The same decomposition at
B = B_c - 0.04 returns the counter-rotating n = 1 frequency within 0.02
of the continued-fraction value, i.e. the time-domain instrument sees
the mode where the frequency-domain instrument says it exists (mutual
gate).
KILL: disagreement above 0.05.

## Instrument (frozen)

Method of lines in the tortoise coordinate, RK4, fourth-order centred
Laplacian, Sommerfeld boundaries; domain r* in [-60, 300], dr* = 0.05,
observer at r* = 20, Gaussian initial datum centred at r* = 12 with
width 1.0 and carrier frequency 0.3 (counter-rotating branch selected by
the sign convention of the field); window chosen after the direct pulse
has passed the observer. Matrix-pencil order 6. Convergence gate:
halving dr* changes the extracted frequencies by less than 1e-3.
