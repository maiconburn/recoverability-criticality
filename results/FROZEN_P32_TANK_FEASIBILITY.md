# P32, is the tank experiment actually doable? Excitation and resolvability of the tower (freeze, 2026-09-12)

Frozen BEFORE any measurement of excitation amplitudes. This cycle
tests OUR OWN experimental proposal
(`EXPERIMENT_DESIGN_VORTEX_TANK.md`) before anyone builds anything.
The frequency-domain work (P21-P27) proved the tower modes EXIST. It
never asked two questions an experiment lives or dies by:

1. Are they EXCITED? A quasinormal mode with a tiny excitation factor
   is invisible no matter how long you record.
2. Are they RESOLVABLE? Our own P21c died because a matrix-pencil
   estimator could not separate the fundamental from the n = 1
   overtone in a realistic window.

## Instrument shakedown (before the freeze, recorded as such)

`dbt_td.evolve` at B = 10:
- m = -2 runs (16001 steps, 7 s) but m = -4 OVERFLOWS. Cause: the
  rotation term enters as W = B m / r^2 with |W| = B |m| at the
  horizon, so stability needs dt << 1/(B |m|), not just dt < drs. At
  B = 10, m = -4, dt = 0.05 gives dt |W| = 2. Fix: dt = cfl *
  min(drs, 1/max|W|), which makes strong-rotation runs 10-50x more
  expensive (still minutes on this machine).
- A blind Prony fit over t in [200, 750] returns junk: at B = 10 the
  tower fundamental has e-folding time B/0.25 = 39, so by t = 200 it
  has decayed 5 e-folds and by t = 750 it is 14 e-folds down. What is
  left is the branch-cut tail, not modes. The analysis window must be
  EARLY (the first few e-foldings after the pulse clears), exactly the
  trap that killed P21c.

Both are instrument facts, not predictions.

## Method (frozen)

Evolution: `dbt_td.evolve` with the stability fix, B = 10, m = -2, -3,
-4, -5, Gaussian initial data at x0 = 25, width 3 (generic, not tuned
to any mode), observer at r* = 60, drs = 0.02, cfl = 0.4, t_max = 400.
Two other initial-data settings (x0 = 40 width 6; x0 = 15 width 2) as
a robustness check.

Excitation measurement: linear least squares with the tower
frequencies FIXED at c_n/B from `p23_tower_cplx_m*.json` (the
symmetric-model recipe of P29/P30: the frequencies are predicted, so
only amplitudes are fitted, which is well conditioned), on the window
[t_start, t_start + 4 B / 0.25] with t_start the time the initial
pulse clears the observer. Excitation factor E_n = |A_n| / |A_0|.

Resolvability test: from the measured amplitudes build a synthetic
record at the design point of the note (c_s^2/C = 1.96 s^-1, 60 s,
100 Hz sampling), add the viscous damping of the note (0.1 s^-1 common
offset) and white noise at 1% and 5% of the peak surface amplitude,
then run a BLIND matrix pencil (`prony_modes`, orders 6 to 14) and
count the recovered counter-rotating modes.

## Predictions

P32.1 (excitation): for each m in {-2, -3, -4, -5} every tower mode
with n <= N(m) - 1 is excited by generic initial data with
E_n = |A_n|/|A_0| > 0.02, and the fitted amplitudes are stable to
within a factor 3 across the three initial-data settings.
KILL: any mode with E_n < 0.005 in all three settings (then that mode
is not a target for the experiment and the design note must drop it).

P32.2 (frequencies recovered): the fixed-frequency fit's residual is
below 10% of the signal r.m.s. in the window, i.e. the tower plus the
tail accounts for the ringdown.
KILL: residual above 30% (then the ringdown at B = 10 is not the tower
and P21-P23 do not describe the time domain).

P32.3 (blind resolvability at 1% noise): the blind pencil recovers
N(m) counter-rotating modes for m = -2 and m = -3 (N = 2 and 2), with
frequencies within 10% and the damping ratio gamma_1/gamma_0 within
30% of 3.
KILL: fewer than N(m) modes recovered for both m = -2 and m = -3 at
1% noise (then the protocol of the design note cannot count modes and
must be rewritten around fixed-frequency amplitude fitting instead of
blind counting).

P32.4 (the honest expectation, recorded): at |m| = 4, 5 the higher
overtones (n >= 2, damping ratios 5 and 7) will NOT be blindly
resolvable at 1% noise; the count will be recoverable only with the
frequencies fixed. If so, the design note's falsifier "a mode count
differing from N(m) by two or more" must be restated as a test on
amplitudes at predicted frequencies, not on a blind count.
No kill: this is the outcome that rewrites the protocol.

Instrument: `scripts/p32_tank_feasibility.py`; output
`results/p32_tank_feasibility.json`.
