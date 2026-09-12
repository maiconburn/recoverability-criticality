# P31, label confusion on a real bridge, and where the labelled-versus-symmetric distinction does NOT pay: verdicts (2026-09-12)

Preregistration: `FROZEN_P31_KW51.md` (with the P31.5 addendum frozen
after the first run and before any sensitivity computation). Scripts:
`p31_kw51.py`, `p31b_sensitivity.py`. Data: KW51 tracked modes, Zenodo
10.5281/zenodo.3745914, `trackedmodes.zip`, md5
5cdb446519d1150228fab51b3a002239 verified on download, CC BY-NC-SA 4.0,
kept outside the repository in `~/fisica/prelab-data/kw51/`. Outputs:
`p31_kw51.json`, `p31b_sensitivity.json`.

## Summary

On 11328 hourly modal identifications of a steel railway bridge, the
close pair of modes 8 and 9 (3.904 and 4.063 Hz, gap 4.8%) carries
strongly ANTICORRELATED temperature residuals, corr = -0.747, against
a common-mode baseline of +0.543 and +0.935 for two separated control
pairs: the tracker is trading frequency between the two labels. The
consequence predicted by the theorem is measured: the residual
standard deviation of the SUM f_8 + f_9 is 1.90 times SMALLER than the
quadrature sum of the individual standard deviations, where for the
separated pairs the sum is 1.2 to 1.4 times WORSE than quadrature.
That is label confusion, in the field, in a data set nobody collected
for us.

And then the negative result, which is the more useful half. It does
NOT translate into better damage detection, and it cannot: a Hotelling
T^2 statistic built on the sample covariance is EXACTLY invariant under
invertible affine reparameterisation, verified here to 8e-12 by
mapping the labelled residuals through the Jacobian of (sum, product).
A detector that estimates the covariance already uses the
anticorrelation; renaming the coordinates gives it nothing. The
labelled-versus-symmetric distinction pays when the MODEL changes (as
in P29/P30, where the crossing overtone pair's two columns are replaced
by one cluster column, or by the confluent basis) or when the estimator
cannot use the full covariance. It does not pay for a reparameterisation
alone. This is the sharpest limit the principle has been given so far,
and it was found by trying.

## Verdict table

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P31.1 close pairs anticorrelated (corr <= -0.15), separated controls |corr| <= 0.15 | KILL: a close pair with corr >= 0 while both controls are near zero | 8-9: **-0.747**. 4-5: +0.237. Controls 2-3: +0.543, 12-13: +0.935 | the kill does not fire (the controls are far from zero), but the prediction as stated fails on three of four counts. What is true, and stronger: against a common-mode baseline of +0.54 to +0.94, the close pairs sit at +0.24 and -0.75, a shift of 0.7 to 1.7 in correlation exactly where the modes are close. The absolute threshold was the wrong statistic |
| P31.2 residual sd of the sum below quadrature by >= 1.15 for close pairs, controls in [0.9, 1.1] | KILL: below 1.05 for both close pairs, or above 1.15 for a control | 8-9: **1.901**. 4-5: 0.899. Controls: 0.805 and 0.719 | CONFIRMED for the 8-9 pair (a 1.9x variance gain in the symmetric coordinate); failed for 4-5 and for the control window, whose positive common-mode correlation makes the sum worse than quadrature, as it must |
| P31.3 symmetric control chart flags at least 5 points more post-retrofit hours at equal false-alarm rate | KILL: fewer, or agreement within 2 points | both charts: 1.14% pre, 100.00% during, 100.00% post. Difference 0.0 points | KILLED (tombstone 38). The retrofit shifts the higher frequencies by 1 to 2%, which is 10 to 20 residual standard deviations: the metric had no headroom |
| P31.4 blind PCA baseline on all 14 residuals | recorded, no kill | not computable: all 14 modes are simultaneously present in 116 hours, 1.0% of the record | VOID, and a fact worth recording about this benchmark |
| P31.5 minimum detectable shift at least 1.3x smaller in the symmetric parameterisation for the 8-9 pair | KILL: larger for 8-9, or the control differs by more than 1.3 | gain factor exactly 1.00 for every detected case (8-9 perturbing f_8: 1e-2 both; f_9: 5e-3 both; 4-5 perturbing f_4: 5e-3 both); 12-13 undetected up to 1% | KILLED (tombstone 39), and now understood: see the invariance below |

## Why P31.3 and P31.5 could not have worked

Hotelling's T^2 = (x - mu)^T S^-1 (x - mu) with S the sample covariance
is invariant under x -> A x for any invertible A: both mu and S
transform so that the quadratic form is unchanged. Verified on the
8-9 pair (2730 hours): mapping the labelled residuals through
A = [[1, 1], [mean f_9, mean f_8]], the Jacobian of (sum, product),
gives T^2 values identical to the labelled chart to a maximum relative
difference of 8.3e-12.

The chart actually built from the invariants differs from the labelled
one by up to 88% pointwise (correlation 0.897) for two reasons that
are both nuisance, not information: the product is not exactly linear
in the pair, and the invariants were regressed on temperature
separately rather than transformed after regression. Neither is a gain.

So the operational rule that comes out of this cycle:

- a symmetric REPARAMETERISATION buys nothing against any estimator
  that uses the full covariance;
- a symmetric MODEL, one that drops the ill-determined direction
  instead of renaming it, is what bought the 5 to 11 times better pair
  amplitude in P29 and the finite cluster coefficient in P30;
- the variance gain measured here (1.9x on the sum) is real and is the
  right diagnostic that a pair is confused, which is useful for
  deciding WHICH modes to drop from a model, but it is not by itself a
  better detector.

## Numbers for the record

| pair | kind | hours | corr of residuals | sd_a (Hz) | sd_b (Hz) | sd(sum) | quadrature | quadrature/sd(sum) |
|---|---|---|---|---|---|---|---|---|
| 4-5 | close (gap 5.6%) | 4598 | +0.237 | 0.01400 | 0.01380 | 0.02186 | 0.01966 | 0.899 |
| 8-9 | close (gap 4.8%) | 2730 | -0.747 | 0.01872 | 0.01451 | 0.01246 | 0.02368 | **1.901** |
| 2-3 | separated (53%) | 3394 | +0.543 | 0.00816 | 0.00862 | 0.01473 | 0.01186 | 0.805 |
| 12-13 | separated (19%) | 6217 | +0.935 | 0.05199 | 0.05113 | 0.10143 | 0.07292 | 0.719 |

Setup facts of the benchmark, useful to anyone using it: hourly
coverage per mode ranges from 27.4% (mode 8) to 96.5% (mode 6); the
published machine-learning analyses of this data set use the subset
3, 5, 6, 9, 10, 12, 13, 14, which drops both members of neither close
pair but drops mode 8, the one whose label is confused; the retrofit
shifts modes 6 and 10 to 14 upward by 1.4 to 2.6% and modes 1 to 5
and 9 slightly downward; deck temperature spans -3.0 to 37.9 C with
88% coverage.

Instrument lesson 17: before predicting that a reparameterisation
improves a statistic, check whether the statistic is invariant under
it. Affine invariance of quadratic-form detectors is elementary and it
made two of this cycle's five predictions unwinnable from the moment
they were written.
