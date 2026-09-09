# P23, the escape count as light-ring anharmonicity, and the analytic arrival in Kerr as a predictor (freeze, 2026-09-09)

Frozen BEFORE any scaled-tower computation at |m| >= 8, before any WKB
beyond first order on the scaled potential, and before tracking any
Kerr sequence other than {2,0,9}, {2,-2,13}.

## Evidence in hand

Pure-vortex tower members c_n(m) (P21f, P21g, P21h) for |m| = 1..7,
the finite-B escape counts 1, 2, 2, 3, 4, 5 (|m| = 1..6) equal to the
number of members with Re c_n > 0, and the scaled count N(7) = 6.
Read against |m|/4 and (n + 1/2)^2 the real parts obey, to 3% of
|m|/4 for every member with n >= 1 and |m| >= 2,

    Re c_n(m) = |m|/4 - [k0 (n + 1/2)^2 + k1] / |m|,   k0 = 0.383, k1 = -0.033,

(fitted on n = 0 and n = 1 at |m| = 4..7 and checked on n = 2..5:
deviations 1 to 3%), while Im c_n(m) = -(2n + 1)/4 to 2% for
n <= N - 3 and drifts upward by 0.2 to 0.3 for the last two members
before the crossing. The leading terms are the light-ring values of
the scaled equation H'' + m^2 q(sigma) H = 0, q = (gamma + 1/sigma^2)^2
- 1/sigma^2 (gamma = c/|m|, m < 0): q = q_sigma = 0 at sigma = 2,
gamma = 1/4 gives Re c_0 = |m|/4, and the Schutz-Will step
Q_0 / sqrt(2 Q_0'') = i(n + 1/2) with Q'' = m^2/8 gives
c_n = |m|/4 - i(2n + 1)/4, m-independent damping (P21h.3). The
(n + 1/2)^2 / |m| term is the light-ring anharmonicity (second-order
WKB). With it the crossing Re c = 0 sits at n + 1/2 = 0.808 |m|
(times 1 + 0.07/m^2), so the escape count is

    N(m) = floor(0.808 |m| + 1/2)   (for |m| >= 2),

which reproduces 1, 2, 2, 3, 4, 5, 6 for |m| = 1..7 and DIFFERS from
the also-consistent reading N = |m| - 1 (|m| >= 3) from |m| = 9 on.

## Predictions

P23.1 (count law): the scaled tower (dbt_scaled.find_c, inner branch
+1, seeds from the law above, each root checked against variations of
the matching point rho_m and of the inner cutoff as in P21h) has
N(9) = 7 and N(10) = 8 members with Re c > 0. At |m| = 8 the law
puts the seventh member at Re c_6(8) = -0.02, on the crossing: N(8)
is 6 or 7 and Re c_6(8) lies in [-0.17, 0.13]. Every member with
n <= N - 2 has Re c_n within 0.15 of the law and Im c_n within 0.12
of -(2n + 1)/4 for n <= N - 3.
KILL: N(9) = 8 or N(10) = 9 (the |m| - 1 rule), or any member with
n <= N - 2 deviating from the law by more than 0.15 in Re c.

P23.1b (derivation gate): second-order Iyer-Will WKB on Q = m^2 q
about the complex extremum sigma_0(gamma), solved for complex gamma
at each n, reproduces Re c_n(m) within 0.15 for |m| >= 5 and
n <= N - 2, with the same count N(m) as the exact tower for
|m| = 5..10; expanded at gamma = 1/4 it yields the (n + 1/2)^2 / |m|
term with coefficient k0 = 0.38 +- 0.10 (the sign is the content:
Re c must DECREASE with n).
KILL: no such term at second order, or the wrong sign, or third-order
WKB needed to get within 0.15 at |m| = 7.

P23.2 (the analytic arrival law as a predictor, Kerr): for the
sequences {2, 0, 10_0}, {2, 0, 11_0}, {2, -2, 14_0} (Cook-Zalutskiy
Table II: endpoints 0.391144 / -2.50000i, 0.438874 / -2.75000i,
0.611751 / -3.61439i), a cubic in (a_0 - a) fitted ONLY to gate-passing
points with 0.01 <= Re(omega M) <= 0.04 (a_0 a free parameter of the
fit: Re = c_1 d + c_2 d^2 + c_3 d^3, d = a_0 - a) predicts a_0 within
1.5e-3 and the endpoint Im(omega M) (linear extrapolation of Im) within
3e-3 of the deep-instrument endpoint (caps to 4e6, P22 discipline);
a fold model Re^2 = s (a_0 - a) fitted to the same points misses a_0
by more than 3e-3 for every sequence.
KILL: cubic off by more than 3e-3 in a_0 for any of the three, or the
fold model within 1.5e-3 for any.

P23.3 (structure, recorded from the cached qnm tables, no new
measurement): the Schwarzschild overtones n = 0..6 of l = 2, m = 0
are damped modes at extremality (omega M at a = 0.9999: 0.425-0.072i,
0.403-0.218i, 0.358-0.374i, 0.296-0.549i, 0.226-0.750i, 0.163-0.975i,
0.114-1.212i), the n >= 8 ones die on the axis (Cook-Zalutskiy), and
the zero-damping family that collapses onto the origin is born from
the axis (the n_1 segments). Kerr therefore has three fates (survive
at finite damping, die on the axis, be born on the axis and collapse)
where the vortex has two (collapse, die). This is a comparison-table
entry, not a prediction.

Instruments: `dbt_scaled.py` (scaled solver), a new
`scripts/p23_tower_law.py` (towers at |m| = 8, 9, 10 and the WKB
comparison), `scripts/p23_kerr_extrap.py` (deep endpoints and the
blind cubic/fold extrapolation; the extrapolation is computed from
the far points BEFORE the endpoint is read).
