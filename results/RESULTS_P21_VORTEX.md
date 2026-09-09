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

## P21f: the escaping modes are the pure-vortex resonances (verdict 2026-09-09)

Preregistration `FROZEN_P21F_VORTEX_SCALED.md` (commit 68d7dd9), with
the derivation: in the DBT equation set r = B rho, omega = c/B and let
B -> infinity; the drain terms drop and the equation becomes the
B-free pure-vortex problem H'' + [(c - m/rho^2)^2 - (m^2 - 1/4)/rho^2] H = 0,
outgoing at infinity, one WKB branch rho^{1/2} e^{-+ i|m|/rho} at
rho -> 0. Solver `src/recoverability_ep/dbt_scaled.py` (direct
integration along a rotated ray, Wronskian matching); the physical
inner branch is rho^{1/2} e^{+i|m|/rho} (the other branch fails the
anchor). Script `scripts/p21f_scaled_vortex.py`, data
`results/p21f_scaled_vortex.json`.

Gate: the m = -2, n = 0 anchor from the B = 100 track (0.4698 - 0.2549i
after the 1/B extrapolation) is reproduced at 0.46670 - 0.25362i,
0.6%: PASSED.

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P21f.1 scaled eigenvalues reproduce the finite-B limits within 3% | as stated | m=-1 n=0: 0.1800-0.2634i vs 0.1813-0.2610i (0.9%); m=-2 n=0: 0.6%; m=-2 n=1: 0.0721-0.6872i vs 0.0616-0.6940i (1.8%); m=-3 n=0: 0.7292-0.2512i vs 0.7347-0.2547i (0.9%); m=-3 n=1: 0.5%; m=-4 n=0: 0.9842-0.2515i vs 0.9927-0.2542i (0.9%); m=-4 n=1: 1.0%; m=-4 n=2: 0.4099-1.1623i vs 0.4029-1.1742i (1.1%). Eight of eight within 2% | CONFIRMED |
| P21f.2 scaled resonance count (Re c > 0, Im c > -2) = floor((|m|+2)/2) for |m| = 1..4, predicting 3, 4 for |m| = 5, 6 | as stated | counts 1, 2, 2, 3, 4, 4: agrees through |m| = 4 and at |m| = 6, but |m| = 5 has FOUR resonances (1.237-0.250i, 1.089-0.740i, 0.779-1.203i, 0.296-1.586i; each a consistent minimum of the Wronskian landscape under changes of matching point and inner cutoff) | KILLED as frozen; the mismatch at |m| = 5 is the subject of P21g |
| P21f.3 first-order Schutz-Will WKB on the scaled potential within 15% (Re) / 20% (spacing) at |m| >= 3, kill above 30% at |m| = 4 | as stated | m=-4 n=0: WKB 1.062-0.215i vs exact 0.984-0.252i (Re 8%, Im 15%) but for the tower the first-order eikonal misses badly (m=-4: n=1 WKB 1.317-0.357i vs 0.792-0.734i); m=-2 n=0 Re 23%, m=-1 n=0 Re 53% | KILLED (the eikonal limit needs |m| far larger than 4; the tower spacing is not the light-ring Lyapunov exponent at these m) |

Reading. The physics of the escaping family is settled: they are the
resonances of the pure vortex, the light-ring family that a vortex
with negligible drain shows, and the drain creates the absorbed family
together with its branch-cut arrivals. What is NOT settled is the
counting: the pure vortex has (at least) one more resonance at |m| = 5
than the finite-B floor rule allows. Either four B = 0 overtones
escape at m = -5 (the floor rule dies), or the extra scaled resonance
is a mode with no B = 0 ancestor, born from the branch cut at finite
rotation (the reverse of absorption). `FROZEN_P21G_VORTEX_M5_EMERGENT.md`
decides.

## P21g: m = -5, four escape and nothing is born (verdict 2026-09-09)

Preregistration `FROZEN_P21G_VORTEX_M5_EMERGENT.md` (commit 83864b9).

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P21g.1 finite-B escape count at m = -5: 3 (R2) or 4 (R1) | as stated | n = 0, 1, 2 escape (omega B at B = 10: 1.23-0.25i, 1.08-0.74i, 0.78-1.19i against the scaled 1.237-0.250i, 1.089-0.740i, 0.779-1.203i); n = 3 ALSO escapes: the kmax-600 tracker holds it to B = 4.8 (omega B = 0.307-1.598i) and longer fractions bridge it at B = 5.5, 6.5, 7.5 (kmax 3000-6000, two inversions), 10 (three inversions) and 20 (five inversions), all with omega B = 0.31-1.59i against the scaled c_3 = 0.296-1.586i; n = 4 arrives linearly (Re 0.010 at B = 3.44, slope -0.0134, Im -1.33 finite, B_c ~ 4.2) | four escape: reading R1 |
| P21g.2 a mode born from the cut near c_3/B | as stated | the root near c_3/B at B = 10 and 20 IS the n = 3 overtone (continuous trajectory from B = 0) | R2 KILLED |
| P21g.3 universality of birth | conditional on R2 | void | VOID |

Escape counts 1, 2, 2, 3, 4 for |m| = 1..5: the floor rule of P21e is
dead at |m| = 5 (it was confirmed only for |m| <= 4, as its freeze
stated). The finite-B count equals the number of pure-vortex tower
members with Re c > 0 (the member following the last escaping one has
Re c < 0: m = -4, -0.203 - 1.512i), which is frozen as the rule in
`FROZEN_P21H_VORTEX_ESCAPE_RULE.md` with m = -6 as the test.

## P21h: the escape rule Re c_n(m) > 0 (verdict 2026-09-09)

Preregistration `FROZEN_P21H_VORTEX_ESCAPE_RULE.md` (commit 8463c66).
Run: m = -6, robust tracker with a tightened jump guard (0.08 of
|omega|, initial step 0.005; the default guard let the n = 2 track hop
at B = 0.18 in a spectrum whose overtones are 0.75 apart at |omega| ~ 3),
plus a long-fraction bridge (kmax 3000 / 6000) for the near-axis n = 4.

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P21h.1 m = -6: five escaping modes n = 0..4 with omega B -> the scaled tower; n = 5 absorbed | as stated | n = 0..3 escape with omega B at B = 10 (or the last converged point) 1.486-0.249i, 1.361-0.741i, 1.109-1.209i, 0.724-1.637i against the scaled 1.490-0.251i, 1.362-0.746i, 1.105-1.205i, 0.741-1.638i; n = 4 escapes: bridged at B = 3.5, 4.5, 6, 8 with kmax 6000 (omega B = 0.216-1.994i, 0.207-2.002i, 0.201-2.007i, 0.197-2.011i) against the scaled c_4 = 0.190-2.045i; at B = 10 the fraction no longer converges at kmax 6000 (Re/|omega| ~ 0.09). n = 5 had no B = 0 seed from the eikonal guesses: its absorption is untested | CONFIRMED on the testable part (five escape); "n = 5 absorbed" untested |
| P21h.2 m = -7 scaled tower count | reported as prediction | six members with Re c > 0: 1.741-0.250i, 1.633-0.742i, 1.427-1.225i, 1.075-1.697i, 0.606-2.031i, 0.143-2.419i, so N(7) = 6 | prediction for a future m = -7 finite-B run |
| P21h.3 fixed-n damping varies by < 15% across m | as stated | n = 0: -0.25..-0.26; n = 1: -0.69..-0.75; n = 2: -1.16..-1.22; n = 3: -1.59..-1.70; n = 4: -2.03..-2.04 (all < 10%) | CONFIRMED |

Escape counts 1, 2, 2, 3, 4, 5 for |m| = 1..6, equal to the number of
pure-vortex tower members with Re c > 0 in every case tested. The
member that follows the last escaping one has Re c < 0 where computed
(m = -4). The rule stands; its derivation (why the Re c = 0 crossing of
the pure-vortex tower decides absorption) is the next theory target,
together with the astrophysical question of whether the same
mechanism governs which Kerr overtones survive extreme rotation.

Instrument lesson 7: for |m| >= 6 the B = 0 overtones are close enough
(0.75 apart at |omega| ~ 3) that a 25% relative jump guard lets the
tracker hop; use 8% with a 0.005 initial step. Near-axis modes with
Re(omega)/|omega| below ~0.1 need kmax ~ 6000 at 30 digits; classify
them where the fraction converges.

## Why the rule holds: a topological argument (theory addendum, 2026-09-09)

Three facts, two of them measured in this cycle and one derived:

1. Each counter-rotating overtone is a continuous curve omega_n(B) on
   the principal sheet, ordered by damping at B = 0, that can end only
   by reaching the branch cut on the negative imaginary axis (the DBT
   has no polynomial modes, so no quasinormal mode can sit on the axis;
   P21b lemma) or by surviving to B -> infinity.
2. Any mode that survives to B -> infinity must approach a point of the
   scaled pure-vortex spectrum, omega ~ c_k(m)/B, because the DBT
   equation at r = B rho, omega = c/B tends to the B-free pure-vortex
   equation (P21f derivation, verified at <= 2% on eight modes).
3. The pure-vortex tower members with Re c_k < 0 have their limit
   point on the far side of the cut from where every B = 0 overtone
   starts (Re omega > 0). A curve confined to the principal sheet
   cannot cross the axis at Im omega < 0.

Hence an overtone whose damping-ordered partner in the pure-vortex
tower has Re c < 0 cannot reach its only admissible large-B
destination and must end at the cut at a finite B_c: it is absorbed.
An overtone whose partner has Re c > 0 has a reachable destination and
collapses onto it. The rule "escape iff Re c_n(m) > 0" is the
statement that the label continuity of (1) pairs overtone n with tower
member n; that pairing is what the m = -6 bridge checked member by
member. What is NOT derived here: why the pure-vortex tower's real
parts decrease with n and cross zero where they do (a property of the
scaled potential (c - m/rho^2)^2 - (m^2 - 1/4)/rho^2 that the
first-order eikonal misses, P21f.3), and whether the same argument,
with the polynomial modes of Kerr replacing "no mode on the axis",
governs which Kerr overtones survive extreme rotation.

## P21h.2: the m = -7 finite-B run (verdict 2026-09-09, evening)

Prediction (frozen in `FROZEN_P21H_VORTEX_ESCAPE_RULE.md`): N(7) = 6
escaping overtones, i.e. n = 0..5 collapse onto the pure-vortex tower
and n = 6 is absorbed. Run: robust tracker (jump guard 0.08, initial
step 0.005, all seven B = 0 seeds found: 3.4866-0.3534i, 3.4333-1.0659i,
3.3287-1.7962i, 3.1775-2.5566i, 2.9891-3.3593i, 2.7779-4.2133i,
2.5621-5.1205i), plus deep continued-fraction probes near the axis
(`p23_m7_bridge.py`, `p23_m7_n6_track.py`; kmax 2000 to 12000 at
40 digits with the residual guard relaxed to 1e-9).

| n | fate | evidence | tower c_n (complex-ray solver) |
|---|---|---|---|
| 0 | escapes | omega B = 1.7367-0.2494i at B = 10 | 1.7410-0.2503i |
| 1 | escapes | 1.6299-0.7426i at B = 10 | 1.6339-0.7430i |
| 2 | escapes | 1.4146-1.2188i at B = 10 | 1.4272-1.2261i |
| 3 | escapes | 1.0877-1.6666i at B = 10 | 1.0784-1.6968i |
| 4 | escapes | 0.6580-2.0425i at B = 3.32 (tracker halts there, Re/|omega| = 0.3, kmax 600) | 0.6203-2.0574i |
| 5 | escapes (the borderline case: Re c_5 = 0.07) | deep secant continuation to B = 3.06 (Re omega 0.0785 -> 0.0354, omega B 0.1569-2.370i -> 0.1083-2.405i, 16000/32000 terms agree to 1e-5), then kmax-independent roots at B = 6 (omega B = 0.0799-2.424i, 32000/64000 to 7e-4) and B = 8 (0.0753-2.427i); a Muller-only search had reported the mode absent at B = 3.0-4.0 (P24, killed) | 0.0696-2.4303i |
| 6 | absorbed | deep re-track: Re(omega) = 0.4214, 0.3072, 0.2060, 0.1602, 0.1278 at B = 0.575, 0.625, 0.675, 0.700, 0.719 (slopes -2.3, -2.0, -1.8, -1.7), B_c = 0.79 by linear extrapolation; the kmax-600 tracker's later points (Re ~ 0.07-0.11 at B = 1.3-1.9, Im ~ -3.4) are not reproduced by deep fractions: truncation artifacts of the lesson-6 kind | -0.6405-2.7176i (Re < 0) |

Verdict P21h.2: CONFIRMED. N(7) = 6: n = 0..5 escape onto the tower
(n = 5 reaching the member with the smallest positive real part yet
tested, slowly, as 1/B), n = 6 is absorbed linearly at B_c = 0.795.
Counts 1, 2, 2, 3, 4, 5, 6 for |m| = 1..7 are now all measured at
finite B, and the law N(m) = floor(0.8008 |m| + 1/2) of P23 has
no exception in the measured range.

Instrument lesson 10 (scaled solver): the real-axis inner integration
of `dbt_scaled.wronskian` carries the physical branch as the
subdominant solution (by exp(2 |Im c| rho_m) at the matching point),
which made the deep tower members cutoff-sensitive and, at |m| >= 8,
unusable. `wronskian_cplx` integrates the inner solution along
rho = r e^{-i theta}, where that branch is dominant; the arc back to the
real axis needs the first-derivative term of the non-constant
d rho / dt. Results are invariant to theta, rho_min and rho_m to five
decimals. The P21f-h towers are superseded by `p23_tower_cplx_m*.json`
(counts unchanged for |m| <= 7; deep members move by up to 0.07).

Instrument lesson 12 (Muller false negatives near the axis): see
`RESULTS_P24_VORTEX_MULTIPLET.md`; near-axis roots are to be followed
by secant continuation, never declared absent from Muller searches.

Instrument lesson 11 (deep fractions): `find_qnm`'s residual guard
(1e-18) was set for kmax ~ 600 at 30 digits; with thousands of terms
the residual floor is ~1e-10 and the guard rejects converged roots as
stalled. For kmax >= 2000 use 40 digits and resid_max = 1e-9, and
gate consecutive kmax values at 1e-3 rather than 1e-5 near the axis,
where the fraction converges slowly in kmax.
