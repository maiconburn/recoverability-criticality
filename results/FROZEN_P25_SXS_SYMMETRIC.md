# P25, the principle on real ringdowns: symmetric questions are free, labeled ones pay (freeze, 2026-09-10)

Frozen BEFORE any symmetric-combination statistic is computed on the
SXS fits.

## Evidence in hand

`run_sxs_layer.py` (README sec. 1.4, `results/sxs_layer.json`): on six
public SXS simulations spanning the (2,2,5)/(2,2,6) avoided crossing
(remnant spins 0.75 to 0.897, minimum gap 0.0667 at a* = 0.8975), a
linear least-squares fit of the (2,2) ringdown to eight Kerr
overtones with FIXED frequencies (qnm package) and injected white
noise (1e-4 of the peak, 40 bootstrap draws, seed 20260828) gives
individual-amplitude uncertainties sigma(A_5), sigma(A_6) that scale
as gap^{-1.11} (corr 0.959), while the low overtones stay flat.

## The prediction

The principle (`PRINCIPLE_LABELS_PAY.md`): the pair's contribution to
the waveform, A_5 e^{-i omega_5 t} + A_6 e^{-i omega_6 t}, is a
symmetric function of the pair; its cluster moments
M_0 = A_5 + A_6 and M_1 = A_5 omega_5 + A_6 omega_6 are analytic
through the crossing and must be estimated with a cost independent of
the gap; the labeled antisymmetric combination
D = (A_5 - A_6) pays the inverse gap.

P25.1 (symmetric, free): on the same six simulations, same seed, same
noise draws, the log-log slope of sigma(M_0) and of sigma(M_1) against
gap_56 lies in [-0.30, 0.30] (both), i.e. exponent 0 within the
scatter of six points.
KILL: slope below -0.60 for either.

P25.2 (labeled, pays): the slope of sigma(A_5 - A_6) against gap_56 is
-1.0 +- 0.35.
KILL: slope above -0.5.

P25.3 (contrast at the crossing): on the simulation nearest a* the
ratio sigma(A_5)/sigma(M_0) exceeds 10.
KILL: ratio below 3.

P25.4 (recorded expectation, no separate kill): the reconstruction
error of the pair's waveform at t = 0 and at t = 20 M (the physical
response) scales like the symmetric moments, flat in the gap.

Instrument: `scripts/p25_sxs_symmetric.py`, a copy of the original
pipeline that stores the bootstrap amplitude draws and evaluates the
combinations; nothing in the fit changes. Outlier policy as before:
SXS:BBH:2525 excluded if it is among the picks (flagged in the
output).
