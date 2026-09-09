# P25, symmetric versus labeled amplitude costs on real SXS ringdowns: verdicts (2026-09-10)

Preregistration: `FROZEN_P25_SXS_SYMMETRIC.md` (commit a70d99c). Scripts:
`p25_sxs_symmetric.py` (the original pipeline of `run_sxs_layer.py` with
the bootstrap draws kept), `p25_gate_synthetic_gap.py` (post-mortem
gate, not frozen). Data: `p25_sxs_symmetric.json`,
`p25_gate_synthetic_gap.json`.

## Summary

On the six SXS simulations across the (2,2,5)/(2,2,6) crossing, the
labeled difference D = A_5 - A_6 pays the inverse gap as predicted
(slope -1.10, corr -0.96), but the symmetric cluster moments
M_0 = A_5 + A_6 and M_1 = A_5 w_5 + A_6 w_6 are NOT flat (slopes -0.75
and -0.89, corr -0.82 and -0.86) and the contrast at the crossing is
sigma(A_5)/sigma(M_0) = 2.5, not > 10. P25.1 and P25.3 die as frozen.
A controlled gate on one simulation (SXS:BBH:1750, everything fixed,
only omega_6 moved to omega_5 + delta) shows the mechanism exactly as
the principle says: sigma(D) ~ delta^{-1.09}, sigma(A_5) ~ delta^{-1.00},
sigma(M_0) flat (slope -0.10, saturating at 0.93 for delta <= 0.02),
all matching the linear-algebra covariance (X^H X)^{-1} to 5%. The
real-data slope of the symmetric moments is therefore a confounder:
across six spins the conditioning of the whole overtone block
(damping rates and spacings of n = 4..7 in a 10-90 M window) changes
together with the pair gap, and six points spanning a factor 2.7 in
gap cannot separate the two. The freeze should have controlled for
it; it did not. Lesson 13 below.

## Verdict table

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P25.1 slopes of sigma(M_0), sigma(M_1) vs gap in [-0.3, 0.3] | KILL: below -0.6 | -0.753 (corr -0.822), -0.893 (corr -0.855) | KILLED |
| P25.2 slope of sigma(A_5 - A_6) = -1.0 +- 0.35 | KILL: above -0.5 | -1.103 (corr -0.962) | CONFIRMED |
| P25.3 sigma(A_5)/sigma(M_0) > 10 at the crossing | KILL: below 3 | 2.5 (sigma(D)/sigma(M_0) = 5.4) on SXS:BBH:1469 | KILLED |
| P25.4 pair waveform at t = 0, 20 M flat (expectation) | none | t = 0: same as M_0 (-0.75); t = 20 M: -3.3, dominated by the spin dependence of the damping factors e^{-20 Im omega}, uninformative as designed | VOID |

Per simulation (gap = |omega_5 - omega_6|, sigma in units of the
peak-normalised amplitude):

| sim | a_f | gap | sigma(A_5) | sigma(A_6) | sigma(M_0) | sigma(M_1) | sigma(D) | sigma(low n) |
|---|---|---|---|---|---|---|---|---|
| SXS:BBH:1469 | 0.8972 | 0.0667 | 1.63 | 1.98 | 0.660 | 0.654 | 3.57 | 2.1e-3 |
| SXS:BBH:0588 | 0.8931 | 0.0695 | 2.07 | 2.31 | 0.831 | 0.820 | 4.31 | 2.4e-3 |
| SXS:BBH:3569 | 0.8851 | 0.0836 | 1.63 | 1.54 | 0.707 | 0.684 | 3.09 | 2.4e-3 |
| SXS:BBH:0531 | 0.8699 | 0.1077 | 1.68 | 1.32 | 0.790 | 0.749 | 2.91 | 2.3e-3 |
| SXS:BBH:1979 | 0.8299 | 0.1402 | 1.09 | 0.694 | 0.481 | 0.429 | 1.76 | 1.7e-3 |
| SXS:BBH:1750 | 0.7500 | 0.1671 | 0.854 | 0.552 | 0.337 | 0.295 | 1.40 | 1.9e-3 |
| SXS:BBH:2525 (excluded, as before) | 0.6900 | 0.1793 | 2.88 | 2.09 | 0.895 | 0.767 | 4.96 | 4.5e-3 |

## The controlled gate

SXS:BBH:1750 (a_f = 0.75, true omega_5 = 0.4541 - 0.8782i,
omega_6 = 0.4594 - 1.0452i), omega_6 replaced by omega_5 + delta:

| delta | sigma(A_5) | sigma(M_0) (theory) | sigma(D) (theory) | cond(X) |
|---|---|---|---|---|
| 0.2 | 0.677 | 0.583 (0.616) | 0.903 (0.956) | 1.0e5 |
| 0.1 | 1.35 | 0.811 (0.852) | 2.41 (2.53) | 1.9e5 |
| 0.05 | 2.71 | 0.910 (0.953) | 5.37 (5.63) | 3.6e5 |
| 0.02 | 6.80 | 0.935 (0.977) | 13.7 (14.4) | 8.8e5 |
| 0.01 | 13.6 | 0.935 (0.977) | 27.4 (28.7) | 1.7e6 |
| 0.005 | 27.2 | 0.934 (0.976) | 54.6 (57.3) | 3.4e6 |

Slopes: sigma(A_5) -1.002, sigma(D) -1.093, sigma(M_0) -0.106 (theory
-0.103). With the confounder removed, the symmetric moment costs
nothing extra as the pair degenerates while the labeled amplitudes pay
exactly the inverse gap: the content of the principle, on a real
waveform, in the fit that the ringdown community uses.

## What stands

- The labeled cost on real SXS fits scales as the inverse gap
  (P25.2, and the -1.11 of README sec. 1.4).
- The symmetric moments are gap-independent when the gap is the only
  thing that changes (gate), by the covariance identity
  sigma^2(v) = v^H (X^H X)^{-1} v sigma_n^2, whose sum-direction
  element stays bounded as the two columns coalesce while the
  difference-direction element diverges as 1/delta^2.
- On the real set the six spins co-vary with the block's conditioning
  and the raw symmetric slope is -0.75: the prediction as frozen is
  false for that statistic, and no amount of reading the gate
  rescues it. A version that could be tested on real data would
  regress log sigma on log gap AND on the block conditioning (or use
  the (2,2,3)/(2,2,4) pair at the same spins as a control), which was
  not frozen and is not claimed.

Instrument lesson 13: a symmetric-versus-labeled prediction on real
data must freeze the CONTROLLED comparison (same waveform, same
nuisance conditioning) or a regression that includes the nuisance;
a raw slope over a handful of spins tests the confounder as much as
the principle. Same lesson as the radar line (physics-blind baseline
inside the freeze), now on the physics side.
