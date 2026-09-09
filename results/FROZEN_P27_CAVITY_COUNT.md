# P27, the trapped-mode count of a reflecting vortex core (freeze, 2026-09-10)

Frozen BEFORE any exact computation of the six new cases below.

## The rule

For a reflecting core at rho_c, the counter-rotating modes with
0 < Re c < |m|/4 that are trapped between the wall and the light-ring
barrier satisfy the Bohr-Sommerfeld condition of the cavity
[rho_c, rho_-(c)], rho_-(c) = [1 - sqrt(1 - 4c/|m|)] / (2c/|m|):

    Phi(c) = int_{rho_c}^{rho_-(c)} sqrt(Q(rho; c)) d rho = pi (n + delta),
    delta = 3/4 (Dirichlet, node at the wall), 1/4 (Neumann),

Q = (c + |m|/rho^2)^2 - (m^2 - 1/4)/rho^2. Their damping is the
tunnelling rate through the barrier, exp(-2 |m| J) in order of
magnitude, i.e. far below the light-ring ladder.

## Retrodiction (the eight P26 cases, computed before this freeze)

| |m| | wall | rho_c | BS levels in (0, |m|/4) | exact (P26) |
|---|---|---|---|---|
| 2 | Dirichlet | 0.3 / 0.5 / 1.0 | none | none |
| 2 | Neumann | 0.5 | none | none |
| 4 | Dirichlet | 0.3 | one, c = 0.616 | 0.6408 - 0.0006i |
| 4 | Dirichlet | 0.5 / 1.0 | none | none |
| 4 | Neumann | 0.5 | one, c = 0.794 | 0.7470 - 0.0031i |

8/8 counts, positions to 4-6%.

## Predictions for six new cases (exact solver `p26_vortex_core.py` run AFTER this freeze)

| case | |m| | wall | rho_c | predicted count | predicted c |
|---|---|---|---|---|---|
| A | 2 | Dirichlet | 0.15 | 0 | (borderline: Phi_max/pi = 3.69 against the n = 3 level at 3.75) |
| B | 4 | Dirichlet | 0.2 | 1 | 0.487 |
| C | 4 | Neumann | 0.2 | 0 | |
| D | 6 | Dirichlet | 0.5 | 1 | 1.013 |
| E | 6 | Dirichlet | 0.3 | 1 | 0.208 |
| F | 6 | Neumann | 0.5 | 0 | |

P27.1: the exact counts of trapped modes (Im c > -0.05, 0 < Re c < |m|/4)
equal the predicted counts in at least five of the six cases, and
every predicted position is within 8% (relative, in Re c) of an exact
trapped mode.
KILL: two or more counts wrong, or a position off by more than 15%.

P27.2 (the damping): every trapped mode found has |Im c| < 0.02 (the
tunnelling suppression), and among the trapped modes the one with
the larger barrier action (smaller Re c) is the narrower.
KILL: a trapped mode with |Im c| > 0.05.

Case A is flagged as borderline in the freeze itself: if it fails the
count while the others pass, P27.1 still passes by its "five of six"
clause, and the borderline is recorded as such.
