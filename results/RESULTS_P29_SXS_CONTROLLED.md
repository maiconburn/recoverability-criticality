# P29, the controlled symmetric-versus-labeled comparison on real ringdowns: verdicts (2026-09-10)

Preregistration: `FROZEN_P29_SXS_CONTROLLED.md` (commit b27d478).
Script `p29_sxs_controlled.py`, data `p29_sxs_controlled.json`. Same
six SXS fits as P25 plus a seven-column reference fit in which the
pair columns e_5, e_6 are replaced by their mean (amplitude S): the
symmetric model, carrying the spin-dependent conditioning of the
other overtones but no degenerate pair.

| sim | a_f | gap | sigma(S) | sigma(M_0) | sigma(D) | sigma(A_5) | M_0/S | D/S | A_5/S |
|---|---|---|---|---|---|---|---|---|---|
| SXS:BBH:1469 | 0.8972 | 0.0667 | 0.0731 | 0.660 | 3.57 | 1.63 | 9.0 | 48.8 | 22.3 |
| SXS:BBH:0588 | 0.8931 | 0.0695 | 0.0779 | 0.831 | 4.31 | 2.07 | 10.7 | 55.3 | 26.6 |
| SXS:BBH:3569 | 0.8851 | 0.0836 | 0.0907 | 0.707 | 3.09 | 1.63 | 7.8 | 34.1 | 18.0 |
| SXS:BBH:0531 | 0.8699 | 0.1077 | 0.0943 | 0.790 | 2.91 | 1.68 | 8.4 | 30.9 | 17.8 |
| SXS:BBH:1979 | 0.8299 | 0.1402 | 0.0600 | 0.481 | 1.76 | 1.09 | 8.0 | 29.4 | 18.1 |
| SXS:BBH:1750 | 0.7500 | 0.1671 | 0.0654 | 0.337 | 1.40 | 0.854 | 5.2 | 21.4 | 13.1 |

Slopes against gap (log-log, six sims): sigma(S) -0.23 (corr -0.50,
the confounder, weak), M_0/S -0.52 (corr -0.81), D/S -0.87 (corr
-0.94), A_5/S -0.55 (corr -0.86).

## Verdict table

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P29.1 sigma(M_0)/sigma(S) in [0.7, 1.5] on every sim, slope in [-0.3, 0.3] | KILL: ratio > 3 anywhere, or slope < -0.6 | ratios 5.2 to 10.7; slope -0.52 | KILLED (by the ratio clause) |
| P29.2 sigma(D)/sigma(S) slope -1.0 +- 0.4, ratio > 3 at the crossing | KILL: slope > -0.5 or ratio < 1.5 | slope -0.87, ratio 48.8 | CONFIRMED |
| P29.3 sigma(A_5)/sigma(S) slope -1.0 +- 0.4 | KILL: slope > -0.5 | slope -0.55 | passes its kill, misses the window |

## What it says

The principle's statement is about Fisher information: the symmetric
moment of a degenerating pair keeps a FINITE cost at the crossing
(no divergence), which the controlled gate of P25 showed (flat in
delta at 0.93). What P29 adds is the size of that finite cost in a
model that also carries the labeled degree of freedom: five to eleven
times the cost of the same moment in the model that never introduced
the labels, and mildly rising toward the crossing (slope -0.5). The
difference column (e_5 - e_6)/2, nearly a t e^{-i omega t} shape,
correlates with the neighbouring overtones and drags the sum
coefficient with it. So "ask the symmetric question" does not mean
"fit the labels and add them up"; it means "fit the symmetric model":
on these waveforms the seven-column fit determines the pair's total
amplitude 5 to 11 times better than the eight-column fit does, and
the labeled difference 20 to 55 times worse than that. For ringdown
analyses near an avoided crossing the recipe is to replace the two
overtone columns by their cluster columns (mean, and if needed the
first moment) rather than to fit them separately, a change of model,
not of post-processing.

Tombstone 34 (P29.1). The kill clause was well placed: the freeze
asked for equality with the symmetric model and the data say a
constant factor of order the number of neighbouring modes; the
factor's gap-dependence (-0.5) is the residual the principle does not
explain and is recorded as open.
