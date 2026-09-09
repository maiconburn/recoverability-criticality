# A shallow-water draining-vortex experiment that tests the light-ring tower and diagnoses the core (design note, 2026-09-10)

Status: a design derived from P21-P27 (all preregistered and closed).
Internal document; no experiment has been proposed to anyone.

## What is being tested

1. The count law: at strong rotation the counter-rotating ringdown of
   a draining vortex has N(m) = floor(0.8008 |m| + 1/2) modes per
   azimuthal number (1, 2, 2, 3, 4 for |m| = 1..5), with damping rates
   in the ratio 1 : 3 : 5 : ... independent of |m|, frequencies from
   the elliptic tower |m| 2[K - E] = i pi (n + 1/2) (RESULTS_P23).
2. The core: an absorbing core (drain open, horizon inside the sink)
   gives that scale-free ladder; a reflecting core (drain closed)
   gives a spectrum that depends on the core radius, with an
   ultra-narrow trapped mode where the wall-to-light-ring cavity holds
   a Bohr-Sommerfeld level (RESULTS_P26, P27).
3. Absorption by the cut: in a drain-dominated flow the m = -1 first
   overtone disappears when C/D drops below 0.289 while the ringdown
   stays continuous (RESULTS_P21).

## Dictionary (surface flow v = (-D/r, C/r), depth h, c_s = sqrt(g h))

| quantity | expression |
|---|---|
| horizon radius | r_h = D / c_s |
| ergoregion radius | r_e = C / c_s |
| light ring of the counter-rotating tower | r_LR = 2 C / c_s |
| rotation parameter | B/A = C/D |
| scaled variables | rho = r c_s / C, c = omega C / c_s^2 |
| tower frequency, damping | f_n = Re c_n c_s^2 / (2 pi C), gamma_n = |Im c_n| c_s^2 / C |
| shallow-water condition at the light ring | k h = |m| h c_s / (2C) << 1 |

## Design point

h = 1.0 cm (c_s = 31.3 cm/s), C = 500 cm^2/s, D = 50 cm^2/s (C/D = 10).
Then r_h = 1.6 cm, r_e = 16 cm, r_LR = 32 cm, k h = 0.16 |m| / 5 at
|m| = 5 (0.16), drain flow 2 pi D h = 314 cm^3/s = 19 L/min, tank
radius >= 80 cm, c_s^2 / C = 1.96 s^-1. Torres et al. (2020) used
h = 5.55 cm, C = 151 cm^2/s, D ~ 0, 15 L/min, in a 3 m x 1.5 m tank:
the design point is a shallower, faster, drained version of an
existing apparatus.

Predictions at the design point (tower values; the finite-rotation
corrections at C/D = 10 are omega B = c + d/B with |d| ~ 0.3, i.e.
3 to 5%):

| m | n | c_n (tower) | f_n (Hz) | gamma_n (s^-1) | 1/gamma (s) |
|---|---|---|---|---|---|
| -2 | 0 | 0.4675 - 0.2536i | 0.146 | 0.50 | 2.0 |
| -2 | 1 | 0.0707 - 0.6887i | 0.022 | 1.35 | 0.74 |
| -3 | 0 | 0.7288 - 0.2517i | 0.227 | 0.49 | 2.0 |
| -3 | 1 | 0.4726 - 0.7233i | 0.147 | 1.42 | 0.71 |
| -4 | 0 | 0.9842 - 0.2510i | 0.307 | 0.49 | 2.0 |
| -4 | 1 | 0.7941 - 0.7351i | 0.248 | 1.44 | 0.69 |
| -4 | 2 | 0.4054 - 1.1652i | 0.126 | 2.28 | 0.44 |
| -5 | 0 | 1.2374 - 0.2506i | 0.386 | 0.49 | 2.0 |
| -5 | 1 | 1.0861 - 0.7405i | 0.339 | 1.45 | 0.69 |
| -5 | 2 | 0.7793 - 1.1961i | 0.243 | 2.34 | 0.43 |
| -5 | 3 | 0.3075 - 1.5934i | 0.096 | 3.12 | 0.32 |

The fundamental damping 0.49 s^-1 is the same for every m (the
m-independent ladder of P21h.3); the ratio gamma_1/gamma_0 = 2.9,
gamma_2/gamma_0 = 4.7, gamma_3/gamma_0 = 6.3 (the tower's 1 : 3 : 5 : 7
with the third-order correction (3/32)(n+1/2)^3/m^2 of P23).

## The core test (same tank, drain closed)

With D -> 0 the horizon disappears and the core reflects. For a core
of radius r_c the scaled wall sits at rho_c = r_c c_s / C; with
r_c = 3 cm, rho_c = 0.19. P27's rule (verified on 14/14 cases) gives,
for m = -4 with a node at the wall, one trapped mode at
c = 0.51 - 0.0001i (case B, exact 0.5146): f = 0.161 Hz with a
tunnelling damping of 2e-4 s^-1, i.e. a line whose width is set by
viscosity alone, absent with the drain open, and no 1 : 3 : 5 ladder.
Opening the drain must remove the narrow line and restore the ladder.
That is the operational meaning of "the core acts as a horizon".

## The absorption test (drain-dominated configuration)

C = 29 cm^2/s, D = 100 cm^2/s (C/D = 0.29, flow 63 L/min at h = 1 cm,
r_h = 3.2 cm): the m = -1 first overtone is at the edge of absorption;
raising C by 10% keeps it, lowering C by 10% removes it, and the
m = -1 ringdown amplitude changes continuously across the transition
(P21b.1: L2 distance linear in the offset, exponent 1.000). At the
transition the mode arrives at omega = (0 - 1.1616i) c_s^2/D in the
horizon units of P21 (A = D), i.e. a purely damped line of rate
1.16 c_s^2/D = 11 s^-1 at this D; the observable is the loss of the
n = 1 oscillatory component from the m = -1 ringdown, not a frequency.

## Systematics, in order of size

- Finite rotation (C/D = 10): 3 to 5% on frequencies, checked by the
  finite-B towers of P21 (omega B within 2% of c by B = 10 for n <= 2).
- Viscous bottom boundary layer: damping ~ sqrt(nu omega / 2) / h =
  0.1 s^-1 at h = 1 cm, 20% of the fundamental damping; the ratio test
  (1 : 3 : 5) is insensitive to a common additive offset only if it is
  subtracted; measure it on the co-rotating fundamental or on a
  non-rotating tank.
- Dispersion: k h = 0.16 at |m| = 5, 0.03 at |m| = 1: the tower is
  shallow-water; the capillary correction sigma k^2 / (rho g) = 2e-3
  is negligible.
- Core profile: the tower assumes an absorbing core; a partially
  reflecting sink (pipe larger than r_h with a lip) would show the
  P26 fingerprints (radius-dependent damping, narrow lines).
- Non-axisymmetry and free-surface deformation: keep the perturbation
  below 2% of h as in Torres et al.

## Protocol

Record the free surface (Fourier-transform profilometry or
chequerboard demodulation) for 60 s after the flow reaches steady
state; decompose in azimuthal m; for each m fit the radial-averaged
signal with a matrix-pencil (Prony) estimator to extract (f, gamma)
pairs; count the counter-rotating pairs per m and compare with N(m);
form the damping ratios; then close the drain and repeat.
Falsifiers: a counter-rotating mode count differing from N(m) by two
or more at any |m| <= 5 with the drain open; damping ratios outside
1 : 3 : 5 by more than 30% after the viscous subtraction; a narrow
line that survives opening the drain.
