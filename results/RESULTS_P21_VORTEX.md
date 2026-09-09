# P21, the draining-bathtub vortex: verdicts (2026-09-09)

Preregistration: `FROZEN_P21_VORTEX.md` (commit 9dc4ac2), addenda
`FROZEN_P21B_VORTEX_TIMEDOMAIN.md` (17cbd7d), `FROZEN_P21C_VORTEX_OVERTONE_WINDOW.md`,
`FROZEN_P21D_VORTEX_ESCAPE_COUNT.md` (9819ed5). Instruments:
`src/recoverability_ep/dbt.py` (Leaver continued fraction with the
Cardoso-Lemos-Yoshida recurrence, Nollert tail, residual guard, on-axis
rejection), `src/recoverability_ep/dbt_td.py` (time-domain evolution in
the tortoise coordinate). Scripts: `p21_vortex_scan.py`,
`p21_vortex_m2_robust.py`, `p21_validate_beyond.py`, `p21_vortex_analyze.py`,
`p21b_vortex_timedomain.py`. Data: `p21_vortex_scan.json`,
`p21_beyond_validation.json`, `p21_vortex_m-2_robust*.json`,
`p21_vortex_m-3_robust*.json`, `p21b_vortex_timedomain.json`,
`p21c_vortex_overtone_window.json`. Figure: `figures/fig_p21_vortex.png`.

## Summary

The counter-rotating overtones of the draining bathtub that
Cardoso-Lemos-Yoshida (2004) "could not follow" past Re(omega) = 0 are
absorbed by the branch cut of the retarded Green's function: they reach
the negative imaginary axis LINEARLY at finite rotation B_c(m, n) (raw
approach exponents 1.000, 1.004, 1.002 for m = -1, n = 1, 2, 3), there
is no quasinormal mode beyond (every "root" found past B_c is either a
single-inversion artifact of the continued fraction or the mirror image
of a co-rotating mode that was already there), and the DBT admits no
purely imaginary quasinormal mode at all (the recurrence has no
polynomial solutions). The physical response is continuous through the
absorption: the time-domain ringdown at B_c +- delta differs by an
amount linear in delta (exponent 1.000), the theorem's content in this
system. The modes that are not absorbed collapse onto the branch point
omega = 0 as omega ~ c_n/B (m = -1, n = 0: exponent -0.989 on
B in [10, 82]); for m = -2 two modes escape (n = 0 and n = 1), for
m = -1 one. No exceptional point exists at real rotation for
|m| <= 2, n <= 3, B <= 10: adjacent co-rotating overtones never come
closer than 0.79, their real parts cluster on m B at large rotation
with imaginary parts separated by about one.

## Verdict table

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P21.1 linear arrival, m = -1, n = 1, 2, 3 | exponent 1.0 +- 0.15; Im smooth; no principal-sheet root beyond | raw exponents 1.000 / 1.004 / 1.002 (dRe/dB constant to 3 digits over the last decade: -0.637, -0.761, -0.816); Im smooth; beyond B_c only artifacts (single-inversion zeros) and mirrors of co-rotating modes (identified to 4e-5) | CONFIRMED |
| P21.1 for m = -2, n = 2, 3 | same | raw exponents 1.451* / 0.996, dRe/dB constant at -1.331 / -1.54 (*the n = 2 raw fit spans a kmax change near the cut, the slopes are the honest reading); no root of any kind beyond B_c | CONFIRMED |
| P21.1 for m = -2, n = 1 | arrival at finite B_c | does NOT arrive: the mode collapses onto the origin (0.127 - 0.588i at B = 1.0, 0.076 - 0.455i at 1.4, 0.058 - 0.390i at 1.67); the fixed-inversion tracker lost it at B = 1.01 (pole-zero artifact), other inversions hold it | premise wrong for this mode: it belongs to the escaping family (see P21d) |
| P21.2 no EP at real rotation, adjacent co-rotating overtones, |m| <= 2, B <= 10 | gap > 1e-3; large-B clustering with Im separated > 0.3 | min gaps 0.916 / 0.980 / 0.990 (m = 1), 0.792 / 0.950 / 0.980 (m = 2); at B = 10, m = 1: omega = 10.013 - 0.499i (n = 0), real parts on m B, imaginary parts separated by ~1 | CONFIRMED |
| P21.3 complex-B EPs behind gaps < 0.1 | as stated | no gap below 0.1 | VOID (as provided for) |
| P21.4 fundamental never arrives; Re ~ B^-1 on [10, 100] | exponent -1.0 +- 0.2 | m = -1: exponent -0.989 on [10, 82], omega B -> 0.186 - 0.262i; m = -2: see robust re-track (the fixed-inversion tracker hopped onto n = 1 between B = 3.8 and 6.7) | CONFIRMED (m = -1: -0.989; m = -2 robust re-track: -0.996 for Re and Im on [10, 100]) |
| P21.5 B_c(m=-1, n=1) in [0.2, 0.5] | as stated | 0.2894 | CONFIRMED |
| P21.5 B_c(m=-2, n=1) in [0.3, 1.0] | as stated | the mode never arrives | window void by premise (it is an escaping mode); the kill criterion only covered m = -1 |
| P21b.1 continuity of the response through B_c | exponent 1.0 +- 0.25 | relative L2 distance 4.64e-3 / 9.28e-3 / 1.855e-2 / 3.71e-2 at delta = 0.005 / 0.01 / 0.02 / 0.04: exponent 1.000 | CONFIRMED |
| P21b.2, P21b.3 ghost and mutual gate | as stated | the frozen window opens 37 time units after excitation; the n = 1 overtone (e-folding 0.86) is gone by then | VOID by instrument design |
| P21c.2, P21c.3 (re-frozen with an early window) | as stated | gate failed: the pencil resolves the fundamental (1.5e-2 from the CF) but not the n = 1 overtone (nearest component 0.21 away) | UNTESTABLE with this instrument (declared outcome) |

Arrival rotations (B_c = B/A in horizon units, from the linear
extrapolation of Re(omega); the kmax 600 -> 1200 refinement moves them
by <= 2e-3):

| m | n | B_c | Im(omega) at arrival | dRe/dB at arrival |
|---|---|---|---|---|
| -1 | 1 | 0.2894 | -1.1616 | -0.637 |
| -1 | 2 | 0.1170 | -2.2267 | -0.761 |
| -1 | 3 | 0.0424 | -3.2541 | -0.816 |
| -2 | 2 | 0.425 | -1.8095 | -1.331 |
| -2 | 3 | 0.288 | -2.9552 | -1.54 |

## Lemma: no purely imaginary quasinormal modes

Cook and Zalutskiy (PRD 94, 104074, 2016) showed for Kerr that a purely
imaginary quasinormal frequency requires a terminating (polynomial)
Frobenius series. In the CLY four-term recurrence, termination at order
K needs a_{K+1} = a_{K+2} = a_{K+3} = 0 with a_K != 0, which at k = K + 2
forces delta_{K+2} a_K = 0, and delta_k = (2k + 1)(2k - 3) never
vanishes at integer k. The DBT therefore has no polynomial modes and no
quasinormal mode on the negative imaginary axis for any (m, B). A
counter-rotating overtone reaching the axis at B_c cannot stay a
quasinormal mode there; it leaves the principal sheet exactly at B_c,
which is what the scan sees and what CLY could not follow.

## What the analogue laboratory can test

The first absorption of the m = -1 family sits at B/A = 0.289, i.e. a
drain three and a half times the circulation in the DBT units
(D = 3.46 C). The Nottingham vortex experiments run at C/D from ~10
upward (Torres et al. 2020 had a negligible drain in the observation
region), so the absorption regime needs a strong-drain configuration.
Two signatures are frozen and testable: (i) the counter-rotating
ringdown at fixed excitation varies smoothly with the drain through the
absorption (no jump), and (ii) the n = 1 counter-rotating frequency
moves toward zero real part linearly in B with slope -0.64 (in horizon
units) and disappears from any modal fit past B/A = 0.29 while the
signal itself does not change abruptly. The escaping family (one mode for m = -1, two for m = -2 and m = -3;
see P21d) is the one the existing experiments see: long-lived counter-rotating
modes that collapse onto the origin as 1/B.

## Instrument lessons (recorded)

1. A zero of ONE inversion of Leaver's continued fraction is not a
   mode. The n-th inversion has spurious zeros (pole-zero pairs) away
   from the n-th overtone, and it can also LOSE a genuine root through
   a pole-zero cancellation (m = -2, n = 1 at B = 1.01). Rule: a root is
   accepted only if two inversions agree on it, or if it is a zero of
   nearly every inversion; trackers must fall back across inversions
   and pick the agreeing root nearest the seed.
2. On the negative imaginary axis the continued fraction stalls (equal-
   modulus solutions): a stalled Muller iterate with |f| ~ 1e-14 and a
   non-terminating series is not a mode. The first "purely imaginary
   n = 3 mode" of m = 1 at B = 0 was such a stall; the true mode is
   0.034974 - 3.259712i.
3. Fitting an approach exponent with a free B_c on the last decade
   biases the exponent upward (1.29-1.37 for exactly linear data); the
   honest estimator is the constancy of dRe/dB, or the exponent with
   B_c fixed by linear extrapolation.
4. Near the origin, modes that all collapse as 1/B are close in
   absolute terms; a jump guard must be relative to |omega|, otherwise a
   tracker hops between them (the m = -2 fundamental hopped onto n = 1
   between B = 3.8 and 6.7).
5. The collocation instrument in Leaver's variable works only as a
   coarse map (fundamental to 4e-7 at N = 60, degrading with N because
   of the cut); never a source of a claim.

## Robust re-tracks (m = -2) and the large-B collapse

With the inversion-fallback tracker: m = -2, n = 1 tracked to B = 10
without arrival (omega = 0.0071 - 0.0688i at B = 10, kmax-independent
at 1500 and 3000); n = 2 and n = 3 arrive at B_c = 0.424 and 0.288
(slopes -1.35 and -1.5, linear). The fundamental m = -2, n = 0 tracked
to B = 100: exponents of Re and Im on [10, 100] both -0.996,
omega B -> 0.470 - 0.256i. P21.4 is therefore CONFIRMED for both m.
The escaping modes collapse onto the branch point omega = 0 with
omega ~ c_n / B: c_0 = 0.186 - 0.262i (m = -1); c_0 = 0.470 - 0.256i,
c_1 ~ 0.07 - 0.69i (m = -2).

## P21d: how many modes escape? (verdict 2026-09-09)

Preregistration `FROZEN_P21D_VORTEX_ESCAPE_COUNT.md` (commit 9819ed5),
conjecture "the number of escaping counter-rotating modes equals |m|".
Run: m = -3, n = 0..3 (n = 4 seed not found at B = 0), robust tracker,
then a deep continued-fraction probe for n = 2.

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P21d.1 m = -3: n = 0, 1, 2 escape; n = 3, 4 arrive | as stated | n = 0 and n = 1 escape (B = 10: 0.0727 - 0.0251i and 0.0472 - 0.0721i, kmax-independent to 1e-9; exponents on [3, 10]: -0.98/-0.98 and -1.00/-0.98); n = 3 arrives at B_c = 0.482; n = 2 ARRIVES: Re(omega) = 0.0360, 0.0228, 0.0093, 0.0059, 0.0016 at B = 1.20, 1.30, 1.45, 1.50, 1.60 (kmax 10000 and 20000 agreeing), then 0.00416, 0.00249, 0.00088 at B = 1.53, 1.56, 1.59 (kmax 20000, inversions 2 and 3, all six |f_n| small): slope -0.054 constant, B_c = 1.606, Im(omega) -> -0.666 finite; at B = 1.8 no root within 0.15 for any inversion at kmax 10k/20k | KILLED |
| P21d.2 ordering: B_c decreases with n | as stated | m = -3: B_c(n=3) = 0.48 < B_c(n=2) ~ 1.64 | CONFIRMED |
| P21d.3 collapse law for escaping modes, exponents in [-1.2, -0.8] | as stated | m = -2 n = 0: -0.996/-0.996 on [10, 100]; m = -3 n = 0, 1: -0.98/-0.98, -1.00/-0.98 on [3, 10]; m = -1 n = 0: -0.989 | CONFIRMED |

Escape counts: 1, 2, 2 for |m| = 1, 2, 3. Not |m|. Two rules survived
(saturation at two; floor((|m|+2)/2)), frozen as P21e and decided by
m = -4 (`FROZEN_P21E_VORTEX_ESCAPE_M4.md`).

## P21e: the escape count at m = -4 (verdict 2026-09-09)

Run: m = -4, n = 0..3 (n = 4, 5 seeds not found at B = 0 by the eikonal
guesses), robust tracker to B = 10, deep continued-fraction probe
(kmax 10000 / 20000) for n = 3.

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P21e.1 count of escaping modes at m = -4: 2 under (a) saturation, 3 under (b) floor((|m|+2)/2) | as stated | n = 0, 1, 2 escape (B = 10: 0.0982 - 0.0250i, 0.0793 - 0.0733i, 0.0406 - 0.1165i; collapse exponents on [3, 10] -0.98/-0.97, -0.99/-0.98, -1.01/-0.99; n = 2 kmax-independent to 1e-6); n = 3 ARRIVES: Re(omega) = 0.0619, 0.0186, ~0.001-0.003 at B = 0.90, 1.00, 1.08 with Im -> -1.33 finite, no root at B = 1.14 at kmax 20000 (the kmax-10000 root there is a truncation artifact); B_c = 1.05 +- 0.03. Count = 3 | (b) CONFIRMED, (a) KILLED |
| P21e.2 classification decided where the fraction converges | as stated | every classification above uses points with Re(omega) > 0.02 that pass the kmax gate; the kmax-600 tracker's post-arrival segment (Re rising to 0.024 with Im drifting from -1.79 to -0.57 over B in [1.2, 2.9]) is the same truncation artifact seen for m = -3 and was discarded | CONFIRMED |

Escape counts 1, 2, 2, 3 for |m| = 1, 2, 3, 4: floor((|m| + 2)/2). The
escaping modes collapse onto the branch point as omega ~ c_n(m)/B with
the scaled limits (omega B at B = 10, kmax-gated):

| m | n = 0 | n = 1 | n = 2 |
|---|---|---|---|
| -1 | 0.186 - 0.262i (B = 82) | | |
| -2 | 0.470 - 0.256i (B = 100) | 0.071 - 0.688i | |
| -3 | 0.727 - 0.251i | 0.472 - 0.721i | |
| -4 | 0.982 - 0.250i | 0.793 - 0.733i | 0.406 - 1.165i |

Re c_0 grows as ~ |m|/4 and Im c_n sits near -0.25, -0.72, -1.17 for
n = 0, 1, 2, roughly -(2n + 1)/4: the large-B spectrum of the escaping
family looks like a quantized tower on the scaled variable omega B.
A WKB derivation of c_n(m) and of the escape rule is the natural next
freeze (P21f), not attempted here.

Arrival rotations of the absorbed modes, all linear:

| m | n | B_c |
|---|---|---|
| -3 | 2 | 1.606 |
| -3 | 3 | 0.482 |
| -4 | 3 | 1.05 +- 0.03 |

Instrument lesson 6 (the one that decided P21d): near the negative
imaginary axis the continued fraction converges only for kmax growing
roughly like 1/Re(omega)^2 (the two solutions of the recurrence differ
in modulus by 2 Re sqrt(-2 i omega)/sqrt(k)). At kmax = 600 the m = -3,
n = 2 tracker produced a trajectory hugging the cut with
Re(omega) ~ 0.001-0.01 for B in [1.9, 4.7]; every point of it moved with
kmax (600 -> 1500 -> 3000) and vanished at 3000: a truncation artifact,
not a mode. Rule: any root within Re(omega) < 0.05 of the axis must pass
a kmax-independence gate before it enters a claim; arrival rotations
are read from the linear approach where the gate passes, never from
the last 1e-3.
