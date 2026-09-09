# P26, does the vortex core absorb or reflect? A ringdown diagnostic (freeze, 2026-09-10)

Frozen BEFORE any computation with a reflecting inner boundary.

## Context

The pure-vortex tower (P21f-P23) is the counter-rotating spectrum of
H'' + Q H = 0, Q = (c + |m|/rho^2)^2 - (m^2 - 1/4)/rho^2, with the
outgoing condition at infinity and the ABSORBING condition at the
core, rho^{1/2} exp(+i|m|/rho) as rho -> 0 (the draining-bathtub
horizon pushed to the origin). Its members obey
|m| 2[K(k) - E(k)] = i pi (n + 1/2) with damping -(2n+1)/4 and count
N(m) = floor(0.8008 |m| + 1/2). Torres et al. (2020) describe their
draining-free "Unruh vortex" core as horizon-like (perturbations deep
inside cannot propagate out). A core that reflects instead would
turn the region between the core radius rho_c and the light-ring
barrier (rho = 2 at Re c = |m|/4) into a leaky cavity. The
counter-rotating ringdown then carries a diagnostic of the core.

Units: rho = r c_s / C; a core of radius r_c has rho_c = r_c c_s / C
(Torres et al.: C = 151 cm^2/s, c_s = 74 cm/s, a 2 cm sink gives
rho_c ~ 1).

## Predictions

P26.1 (absorbing core is scale-free): with the absorbing condition the
spectrum does not depend on any core radius (there is none); this is
the tower already measured. Recorded as the reference, not a
prediction.

P26.2 (reflecting core, hard wall H(rho_c) = 0, rho_c = 0.3, 0.5, 1.0,
m = -2 and m = -4): the counter-rotating spectrum with Re c in
(0, |m|/4) contains, besides light-ring-like members, at least one
TRAPPED mode per rho_c with |Im c| < 0.08 (damping at least three
times smaller than the tower's fundamental 0.25) and Re c below the
light-ring frequency |m|/4; the number of such trapped modes grows as
rho_c decreases (longer cavity). The tower's damping ladder
-(2n+1)/4 is not present: no set of three modes with damping ratio
1 : 3 : 5 within 15%.
KILL: no mode with |Im c| < 0.08 for any rho_c, or the 1 : 3 : 5
ladder surviving within 15% at rho_c = 0.5.

P26.3 (the diagnostic): the two boundary conditions differ by a
factor > 3 in the damping of the least-damped counter-rotating mode
at m = -2 (absorbing: 0.254; reflecting at rho_c = 0.5: < 0.08), so a
measured Q factor of the m = -2 counter-rotating ringdown at strong
rotation decides between them.
KILL: as P26.2.

P26.4 (Neumann wall, H'(rho_c) = 0, rho_c = 0.5, m = -2): same
qualitative answer as Dirichlet (trapped modes, no ladder); the
trapped frequencies differ from the Dirichlet ones by less than the
cavity spacing.
KILL: no trapped mode.

Instrument: `dbt_scaled.wronskian_cplx` with the inner leg replaced
by a wall condition at rho_c (start with H = 0, H' = 1 for Dirichlet;
H = 1, H' = 0 for Neumann; integrate outward on the real axis to
rho_m, no ray needed because the wall fixes the solution up to
normalisation), root search by local secant from a grid of seeds in
Re c in (0.02, |m|/4 + 0.3), Im c in (-2, -0.005), each root verified
at two matching points. Script `scripts/p26_vortex_core.py`.
