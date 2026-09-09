# P29, the controlled symmetric-versus-labeled comparison on the SXS fits (freeze, 2026-09-10)

Frozen BEFORE computing the seven-column reference fits. Written to
apply lesson 13 of P25: the confounder (the conditioning of the whole
overtone block, which changes with spin) is carried by a reference
fit that has no pair degeneracy.

## Construction

Same six simulations, seed, noise, window and eight-column design as
`run_sxs_layer.py` / `p25_sxs_symmetric.py`. Reference fit: the
seven-column design in which the two pair columns e_5, e_6 are
replaced by their mean (e_5 + e_6)/2, with amplitude S; it has the
same low and high overtones (the confounder) and no degenerate pair.
Its bootstrap uncertainty sigma(S) is the symmetric cost with the
confounder in place.

## Predictions

P29.1 (symmetric is free, controlled): the ratio
sigma(M_0)/sigma(S) lies in [0.7, 1.5] on every one of the six
simulations, and its log-log slope against gap_56 lies in
[-0.3, 0.3].
KILL: a ratio above 3 on any simulation, or slope below -0.6.

P29.2 (labeled pays, controlled): the ratio sigma(D)/sigma(S) has a
log-log slope against gap_56 of -1.0 +- 0.4 and exceeds 3 on the
simulation nearest the crossing.
KILL: slope above -0.5, or ratio below 1.5 at the crossing.

P29.3 (the individual amplitudes): sigma(A_5)/sigma(S) has slope
-1.0 +- 0.4 (the -1.11 of README sec. 1.4 was measured against gap
alone, uncontrolled).
KILL: slope above -0.5.

Outlier policy as before (SXS:BBH:2525 excluded). Script
`scripts/p29_sxs_controlled.py`; output `results/p29_sxs_controlled.json`.
