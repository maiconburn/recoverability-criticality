# P21f, the escaping modes are the pure-vortex resonances (freeze, 2026-09-09)

Frozen BEFORE solving the scaled problem. Motivation: P21d/P21e found
that 1, 2, 2, 3 counter-rotating modes (|m| = 1..4) escape absorption by
the branch cut and collapse onto the origin as omega ~ c_n(m)/B, with
scaled limits omega B at B = 10 (kmax-gated):

    m = -1: c_0 = 0.186 - 0.262i (B = 82)
    m = -2: c_0 = 0.470 - 0.256i (B = 100), c_1 = 0.071 - 0.688i
    m = -3: c_0 = 0.727 - 0.251i, c_1 = 0.472 - 0.721i
    m = -4: c_0 = 0.982 - 0.250i, c_1 = 0.793 - 0.733i, c_2 = 0.406 - 1.165i

## Derivation (done before any numerics on the scaled problem)

In the DBT wave equation H_{r*r*} + [(omega - B m/r^2)^2 - V] H = 0 set
r = B rho, omega = c/B and let B -> infinity at fixed rho, c. Then
r* = r + O(ln r) -> B rho, (1 - 1/r^2) -> 1, the 1/r^4 part of V is
O(1/B^2) and drops, and the equation becomes B-independent:

    H_{rho rho} + [ (c - m/rho^2)^2 - (m^2 - 1/4)/rho^2 ] H = 0,   rho > 0,

which is the DBT equation with the drain removed (A = 0): the pure
vortex. Outgoing condition at rho -> infinity: H ~ e^{i c rho}. Inner
condition: for 1 << r << B the solution is WKB, H ~ r exp(-+ i B m / r)
= rho exp(-+ i m / rho), and the horizon-ingoing wave selects one
branch; in the scaled problem the inner condition is that branch at
rho -> 0. The eigenvalues c_n(m) of this problem are the large-B limits
of the escaping modes; the absorbed modes have no pure-vortex limit
(they need the horizon) and are the ones that meet the cut.

Consequence for the laboratory: the escaping family IS the light-ring
family that Torres, Patrick, Richartz and Weinfurtner (2020) measured
in a vortex with negligible drain (their omega_* - i Lambda (n + 1/2)
approximation is the eikonal limit of the scaled equation), and the
drain (A, i.e. finite B/A) is what creates the absorbed family and its
branch-cut arrivals. In physical units omega_phys = c_n(m) c_s^2 / C.

## Predictions

P21f.1 (the limit is the pure vortex): the scaled problem, solved by
direct integration (outgoing asymptotic series at large rho, WKB inner
branch at small rho, matching in the complex plane), reproduces the
table above to within 3% in |c| for every entry, once the B = 10
entries are corrected by the measured 1/B trend (the m = -2, n = 0
entry at B = 100 is the cleanest anchor: 0.470 - 0.256i, tolerance 1%).
KILL: any entry off by more than 5% after the 1/B correction.

P21f.2 (the escape rule is a counting of pure-vortex resonances): the
number of eigenvalues c of the scaled problem with Re c > 0 and
Im c > -2 (the counter-rotating light-ring tower with damping below the
first absorbed mode) equals floor((|m| + 2)/2) for |m| = 1, 2, 3, 4 and
predicts 3 and 4 for |m| = 5 and 6.
KILL: a count different from 1, 2, 2, 3 for |m| = 1..4.

P21f.3 (eikonal structure): the light ring of the scaled potential
Q(rho) = (c - m/rho^2)^2 - (m^2 - 1/4)/rho^2 gives, in the WKB
(Schutz-Will) approximation, c_n ~ c_LR - i (n + 1/2) lambda_LR with
Re c_0 within 15% of the exact value for |m| >= 3 and the level spacing
Im(c_{n+1} - c_n) within 20% of the exact one.
KILL: WKB off by more than 30% at |m| = 4.

## Instrument (frozen)

`src/recoverability_ep/dbt_scaled.py`: integrate the scaled equation
from rho_max ~ 40/|c| inward with the outgoing series
e^{i c rho} (1 + z_1/rho + ...) along a ray rotated into the complex
rho plane when needed, and from rho_min ~ 0.05 outward with the WKB
branch rho^{1/2 (1 +- ...)} exp(-+ i m/rho) (both branches tried; the
one continuous with the finite-B data is the physical one and is
reported), matching the Wronskian at rho ~ 1; roots by Muller. Gate:
the B = 100 anchor above to 1% before any prediction is read.
