# P30, confluent cluster fitting of a crossing overtone pair (method note, 2026-09-10)

Not a frozen prediction: a method check on the six SXS waveforms of
P25/P29 (`p30_cluster_fit.py`, `p30_cluster_fit.json`). Three models on
identical data, noise (1e-4 of the peak, 40 draws, seed 20260828) and
window (10 to 90 M after the peak):
L, eight labeled overtones; S, the pair replaced by its mean column
u = (e_5 + e_6)/2; C, the pair replaced by the confluent basis
{u, t u} (the Jordan-block pair of the exceptional point).

| sim | gap | sigma(A_5) | M_0/S measured | VIF = 1/sqrt(1 - rho^2) | rho (partial) | sigma(C_0) | sigma(C_1) | pair-waveform error L / C / S (t <= 20 M) |
|---|---|---|---|---|---|---|---|---|
| 1469 | 0.0667 | 1.63 | 9.0 | 8.5 | 0.9930 | 0.638 | 0.113 | 1.6 / 1.8 / 12 |
| 0588 | 0.0695 | 2.07 | 10.7 | 8.3 | 0.9926 | 0.819 | 0.148 | 1.9 / 6.2 / 111 |
| 3569 | 0.0836 | 1.63 | 7.8 | 8.1 | 0.9924 | 0.720 | 0.137 | 1.7 / 33 / 386 |
| 0531 | 0.1077 | 1.68 | 8.4 | 7.8 | 0.9917 | 0.847 | 0.185 | 1.8 / 3200 / 24500 |
| 1979 | 0.1402 | 1.09 | 8.0 | 7.0 | 0.9899 | 0.545 | 0.168 | 1.1 / 123 / 792 |
| 1750 | 0.1671 | 0.85 | 5.2 | 5.6 | 0.9840 | 0.377 | 0.164 | 0.73 / 4.2 / 25 |

Slopes against gap: sigma(A_5) -0.78, sigma(C_0) -0.58, sigma(C_1)
+0.33, sigma(S) -0.23.

## What it says

- The inflation factor of P29 (M_0/S = 5 to 11) is the variance
  inflation factor of adding the difference column to the symmetric
  model: rho, the partial correlation of the sum and difference
  columns after projecting out the other six overtones, is 0.984 to
  0.993, and 1/sqrt(1 - rho^2) reproduces the measured ratio to the
  bootstrap noise of 40 draws. The difference column is, to leading
  order in the gap, t times the sum column: the confluent
  (Jordan-block) partner, nearly collinear with it over a window
  dominated by damping.
- The confluent coefficient C_1 (the finite combination
  (A_5 - A_6)(omega_5 - omega_6)/2 of the ladder's amplitude rung) has
  a small, gap-independent uncertainty (0.11 to 0.19, slope +0.3),
  while the labeled A_5 diverges as gap^{-0.8}: the ladder's content
  on real waveforms.
- The confluent basis represents the pair only where
  gap x T_eff <~ 0.5: at the two crossing simulations the C fit
  reproduces the pair's waveform as well as the labeled fit (1.8 vs
  1.6, 6.2 vs 1.9); away from the crossing it does not (errors up to
  3200), because there the pair is resolved and two overtones are the
  right model. The recipe is therefore regime-dependent: near a
  crossing (gap x T_eff small) fit the cluster {u, t u}; away from it
  fit the labels. The crossover is set by the gap in units of the
  effective window, not by the gap alone.
