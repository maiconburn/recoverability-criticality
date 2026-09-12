# P31, label confusion in bridge monitoring: pair invariants against labelled frequencies on the KW51 data (freeze, 2026-09-12)

Frozen AFTER inspecting the data set's structure, coverage, mode
separations, temperature correlations and retrofit shifts (all listed
below as the setup), and BEFORE computing any residual correlation,
variance ratio or control chart. The predictions concern quantities not
visible in the setup.

## Data

Maes and Lombaert, "Monitoring data for railway bridge KW51 in Leuven,
Belgium, before, during, and after retrofitting", Zenodo
10.5281/zenodo.3745914, file `trackedmodes.zip` (md5
5cdb446519d1150228fab51b3a002239, verified), CC BY-NC-SA 4.0,
non-commercial use with citation. Local copy:
`~/fisica/prelab-data/kw51/trackedmodes/trackedmodes.mat` (not
committed). 11328 hourly records from 2018-10-01 to 2020-01-15:
`f` (11328 x 14 natural frequencies, Hz), `xi` (damping ratios),
`m` (11328 x 14 x 12 complex mode shapes), `env` (11328 x 11
environmental channels, deck temperature `tBD31A` in [-3.0, 37.9] C,
88.0% coverage). Retrofitting 2019-05-15 to 2019-09-27: 5424 hours
before, 3241 during, 2663 after.

## Setup established by inspection (not predictions)

| mode | mean f (Hz) | coverage | corr(f, T) | retrofit shift |
|---|---|---|---|---|
| 4 | 2.4376 | 50.3% | -0.310 | -1.18% |
| 5 | 2.5662 | 87.9% | -0.644 | -0.34% |
| 8 | 3.9041 | 27.4% | -0.062 | +0.85% |
| 9 | 4.0628 | 92.9% | -0.738 | -0.78% |
| 2 | 1.2331 | 34.4% | -0.428 | -1.13% |
| 3 | 1.8844 | 95.0% | -0.553 | -0.58% |
| 12 | 5.3572 | 67.8% | +0.051 | +2.06% |
| 13 | 6.3520 | 85.8% | -0.192 | +1.45% |

The two CLOSE pairs are 4-5 (mean gap 0.1367 Hz, 5.6% relative,
minimum over time 0.0679 Hz, both present 5114 hours) and 8-9 (mean
gap 0.1856 Hz, 4.8%, minimum 0.1213 Hz, both present 3094 hours).
Within each close pair the two members respond very differently to
temperature (-0.310 against -0.644; -0.062 against -0.738), so the gap
breathes with the season. The SEPARATED control pairs are 2-3 (gap
0.651 Hz, 53%) and 12-13 (0.992 Hz, 19%). No pair's gap reaches zero,
so this is close approach and label confusion, not a crossing: the
draft freeze's crossing-count metric is withdrawn.

## Predictions

Temperature correction, fixed here: for each frequency, a piecewise
linear regression on deck temperature with a knot at 2.5 C, fitted on
the PRE-retrofit hours only, applied to all hours; residual = observed
minus predicted. Only hours with both pair members and temperature
present are used.

P31.1 (the mechanism is label confusion): the temperature residuals of
the two members of each CLOSE pair are NEGATIVELY correlated,
corr <= -0.15 for 4-5 and for 8-9, while each SEPARATED control pair
has |corr| <= 0.15.
KILL: a close pair with corr >= 0 while both control pairs are also
near zero, i.e. no excess anticorrelation where the modes are close.

P31.2 (the gain): for each close pair the residual standard deviation
of the SUM s = f_a + f_b is smaller than the quadrature sum
sqrt(sd_a^2 + sd_b^2) by a factor of at least 1.15, while for the
separated control pairs the same ratio lies in [0.9, 1.1].
KILL: ratio below 1.05 for both close pairs, or above 1.15 for a
control pair.

P31.3 (detection of the retrofit): a Hotelling T^2 chart with the
threshold set to a 1% false-alarm rate on the pre-retrofit hours,
built on the four temperature residuals of the two close pairs, is
compared in two parameterisations: LABELLED (f_4, f_5, f_8, f_9) and
SYMMETRIC (f_4 + f_5, f_4 f_5, f_8 + f_9, f_8 f_9). The symmetric
chart flags a larger fraction of POST-retrofit hours than the labelled
chart, by at least 5 percentage points, at equal pre-retrofit false
alarm rate.
KILL: the symmetric chart flags fewer post-retrofit hours, or the two
agree to within 2 points.

P31.4 (blind baseline, lesson 13, recorded with no kill): the same
chart built on the first three principal components of all 14
temperature-corrected residuals, the standard physics-blind method. If
it matches or beats both parameterisations, the labelled-versus-
symmetric distinction adds nothing operational here and that is the
result.

Instrument: `scripts/p31_kw51.py`; output `results/p31_kw51.json`.
Data are NOT committed (licence, and `prelab-data/` is outside the
repository).
