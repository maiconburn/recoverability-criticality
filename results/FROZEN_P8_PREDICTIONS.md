# P8: frozen predictions (preregistration, 2026-08-30; public since release v1.4)

Frozen BEFORE any external verification or contact. Standard repository
protocol: each prediction with a kill criterion.

## Context
EP-2 network proved in the static-patch tower of dS (ν ∈ ℤ; physical point
ν=1 ⇔ m² = 5/4·H²; boundary point ν=0 ⇔ m = 3/2·H = AHM logarithmic
operator). The metrology layer is ours; the log mechanics at ν=0 is prior
art (Arkani-Hamed-Maldacena 1503.08043, eq. 3.15 and footnote 9).

## P8.1: universal divergence of the estimation cost
Any spectator-mass forecast that includes BOTH towers (k_L/k_S)^{Δ±} with
free amplitudes will exhibit σ(ν̂) = C/(S·|ν−ν_c|) near ν_c ∈ {0, 1},
exponent −1.00 ± 0.05. Measured here: −1.002 (ν=0, C=2.0 exact in the
window r∈[0.05,0.6], 80 modes) and −1.022→−1.001 (ν=1, C=10.2).
KILL: exponent outside [−1.15, −0.85] in an independent reanalysis.

## P8.2: rescue through the logarithmic channel
Exactly at ν_c, the mass information survives only in the coefficient of
the log term (Jordan chain; exact coefficients: the ν=1 soft factor has
−ln x·x³ with coef −1 and ¼ln²x·x⁵). Estimator with the chain constraint:
σ_log = 2.7/S (our window), FINITE.
KILL: finite information at ν_c without using the log channel (in a model
with both amplitudes free), or a log channel with zero information.

## P8.3: bias of pipelines without the log
Fitting data generated at ν=1 (with the physical log present) using a
two power-law model WITHOUT the log produces a systematic bias in ν̂
(piling observed in MC: bias +0.3 → estimates collapse to ν≈1 from far
away; fine quantification pending).
KILL: a well-calibrated MC with no bias.

## P8.4: network
Every tower crossing at ν ∈ ℤ is an EP-2 (verified ν=1,2,3 × 5 points,
rank-1 + Jordan ~1e-12). Prediction: no diabolical crossing exists in the
static-patch scalar tower.
KILL: a crossing with rank deficiency 2.

## Novelty status (audited this session)
- Known: log/Jordan at ν=0 (AHM 2015); EPs in Kerr-dS/SdS/RN-dS QNMs
  (2503.21276, 2512.06903, 2608.16521, 2601.00704); integer Bessel logs.
- Not found in abstracts nor in the full texts checked (AHM 1503.08043;
  Chen-Wang 0911.3380; Moradinezhad Dizgah et al. 1801.07265): the ν∈ℤ
  NETWORK as proven EP-2, the cost law σ = C/(S·d) at the critical points,
  the irresolvability window, the rescue through the log channel, the ln²
  as chain fingerprint.
- Pending: a broader full-text sweep (QSF/collider follow-ups 2016–2026)
  before any public claim.

## Amendment A1 (2026-08-30, BEFORE any external test)

P8.3 as written was ill-posed: exactly at ν_c the likelihood in ν is flat
(that is the content of P8.1), so "bias in ν̂" is not the right observable.
Corrected operationalization (the original text above remains for audit):

**P8.3':** data generated at ν=1 with the physical log term present reject
the two power-law model WITHOUT the log by goodness of fit. Measured:
χ²/dof = 12.3 (noise 1e-3), 1.1×10³ (1e-4), 1.1×10⁵ (1e-5), fiducial
window r∈[0.05,0.6], 80 modes, while the model with the log channel gives
χ²/dof = 1.00 and recovers the chain coefficient without bias
(C = −0.3500 ± 0.0001 at noise 1e-5, truth −0.35).
KILL: χ²/dof of the no-log model compatible with 1 on data with the
physical log, or recovered C with bias > 3σ.

## P8-F2 (frozen 2026-08-30, BEFORE measuring): the log in the two-scale object

Lesson from the earlier phases: single-k is analytic in ν and does not see
the log; the log lives in the TWO-scale structure. Frozen object: in
quasi-dS (H = e^{−ε₁N}, m²/H² crossing 5/4 at N*), the FIXED-TIME spectrum
y(k) = k³|σ_k(N_ref)|², N_ref = N* + 6, for a grid of k whose horizon
exits sweep the crossing. In static dS with ν=1, y(k) has
(π²/4)y = k + [−ln k + c]k³ + ¼k⁵ln²k (our exact result).

P8-F2.1 (survival): the fit of y(k) in the basis {k, k³, k³ln k, k⁵, k⁵ln k}
improves over the no-log basis with Δχ²/dof > 4, and the coefficient of
k³ln k has the sign of the static case (negative), with attenuated
amplitude A ≡ |c_log/c_log^{static}| ∈ (0.05, 1].
KILL: no improvement (the log does not survive the sweep) or A ≤ 0.05.

P8-F2.2 (localization): repeating with m² such that ν(N_exit of the k band)
stays at 1±0.15 without crossing 1: |c_log| drops to < 0.3 of the value at
the crossing.
KILL: log equally present far from the crossing (it would be a fit artifact).

P8-F2.3 (attenuation by the sweep): A(ε₁) decreases monotonically over
ε₁ ∈ {0.002, 0.005, 0.01}.
KILL: non-monotonic beyond the fit error.

## P8-F3 (frozen 2026-08-31, BEFORE any measurement): the log channel in the INTERACTING squeezed limit

Instrument: CosmoFlow PiSigma (validated to 3.8e-4 against the exact dS
spectrum, results/p18_cosmoflow_validation.json; 1.1 s per bispectrum
call). Single-exchange collider configuration: quadratic mixing
rho = 0.1 H plus one cubic vertex kappa2 (dot-pi^2 sigma), all other
cubics zero. Shape-normalized squeezed data S(k_L) at fixed late N_ref,
k_S = 1, k_L over >= 1.5 decades.

INSTRUMENT GATE (before the physics runs): in STATIC dS at nu = 1
(m^2 = 5H^2/4), the squeezed tower collides at relative order
(k_L/k_S)^2 and the fit basis {x^{1/2}, x^{5/2}, x^{5/2} ln x} must
beat the log-less basis by dchi2/dof > 4 with a stable log coefficient
(this is the known degenerate-dimension statement; if CosmoFlow cannot
see it, the tool cannot test F3 and the cycle stops there).

P8-F3.1 (control, no crossing): quasi-dS with epsilon_1 = 0.005 and the
k band exiting with nu(N_exit) fixed near 0.7 (no crossing of 1): the
log term adds nothing (dchi2/dof < 1).
KILL: log improvement without a crossing (fit artifact).

P8-F3.2 (the survival question): same epsilon_1, mass chosen so
nu(N_exit) crosses 1 inside the k band: the log channel survives with
dchi2/dof > 4 and amplitude ratio A = |c_log / c_log^static| in
(0.05, 1], sign matching the static case.
KILL: no improvement, or A <= 0.05. Declared risk: P8-F2 killed the
free-sector version of this claim (adiabatic laundering); if the
interacting channel also launders, the honest verdict is "tree-level
cosmological clock fully excluded", which is a result, not a failure.

P8-F3.3 (sweep attenuation): A(epsilon_1) decreases monotonically over
epsilon_1 in {0.002, 0.005, 0.01}.
KILL: non-monotonic beyond fit error.

### Amendment F3-A1 (2026-08-31, before any physics run; gate iterations documented)

The gate basis frozen above was derived incorrectly: {x^{1/2}, x^{5/2}}
are the soft exponents of the sigma two-point factor, not of the
shape-normalized bispectrum. For S = (k1 k2 k3)^2 B with k_S = 1, the
nu = 1 tower is {x^{-1/2}, x^{3/2}} (branches x^{1/2 -/+ nu}), the
degenerate collision sits at x^{3/2}, and the gate basis becomes
{x^{-1/2}, x^{3/2}, x^{3/2} ln x}. Two instrument fixes recorded at the
same time: fits minimize RELATIVE residuals (weighted least squares),
and the coupling-linearity subgate runs in the perturbative regime
(rho: 0.05 -> 0.10 with kappa2: 0.005 -> 0.010, expected B ratio 4);
the first attempt at rho = 0.2 landed in the strong-mixing regime where
the transport resummation legitimately breaks single-exchange scaling.
Gate v1 also lacked CosmoFlow's own adiabatic i-epsilon prescription
(couplings must ramp on about one e-fold AFTER the initial conditions);
v2 fixed that and the raw S(k_L) became smooth and monotonic.

### Amendment F3-A2 (2026-08-31, before the deciding run; LAST instrument amendment, declared)

The v3 gate metric (dchi2/dof > 4) was specified for noisy data; the
gate data is deterministic, so chi2 is uncalibrated and the threshold
meaningless (v3 measured: no-log relative chi2/dof 4.1e-3, log 1.4e-4,
improvement factor 28, c_log negative as the static analysis predicts).
Replacement criterion, frozen BEFORE the deciding run and final (no
further gate amendments; if this fails the cycle stops):
LOCALIZATION AT THE DEGENERACY. Improvement factor
R(nu) = chi2_nolog/chi2_log on the same kL grid and basis
{x^{1/2-nu}, x^{3/2}, x^{3/2} ln x} (collision exists only at nu = 1):
GATE PASSES iff R(nu=1) / R(nu=0.85) > 10 and c_log at nu=1 keeps its
negative sign. Secondary check (reported, not gating): coupling
linearity ratio at rho 0.025 -> 0.05, kappa2 0.0025 -> 0.005.
