# P20, Rayleigh's curse at the exceptional point: frozen predictions (preregistration, 2026-09-09)

Frozen BEFORE any measurement. Each prediction carries a kill criterion.

## Context and motivation

The control-neutrality theorem (`THEOREM_EP_NEUTRALITY.md`) was proven
for additive white Gaussian noise: the Fisher information for the
control parameter that unfolds an EP is analytic, so its critical
exponent is exactly zero, and the gap costs sigma(s) ~ s^-1 (Rayleigh's
curse in spectral form). Tsang, Nair and Lu (PRX 6, 031033, 2016) showed
that for two INCOHERENT point sources the curse can be beaten by
spatial-mode demultiplexing (SPADE): photon counting in a mode that is
dark at coincidence gives a Fisher information for the separation d that
stays constant as d -> 0, because the dark-mode population is ~ d^2 and
Poisson/thermal counting statistics carry a 1/population factor. The
subsequent coherence debate (Larson-Saleh, Optica 2018; Tsang-Nair,
Optica 2019; Kurdzialek, Quantum 2022) settled that SPADE survives
partial coherence once losses are accounted for.

An arXiv scan on 2026-09-08/09 found no paper connecting this mechanism
to exceptional points ("exceptional point" AND "mode demultiplexing",
"non-Hermitian" AND superresolution, "exceptional point" AND incoherent
AND Fisher: zero hits). The question here: can mode-resolved photon
counting beat the gap curse at an EP, and does it change the exponent
zero of the control parameter?

## Frozen analytic expectation (the candidate theorem)

Let epsilon be the physical unfolding parameter (rho = s^2/4 ~ epsilon,
transversal). For ANY source whose second-order statistics are analytic
in epsilon and positive semidefinite, the population n_k(epsilon) of any
fixed detection mode is a nonnegative analytic function of epsilon.
A nonnegative analytic function that vanishes at epsilon = 0 vanishes to
EVEN order, so either n_k(0) > 0 or n_k ~ epsilon^2 (or higher even
order). In both cases the counting Fisher information for epsilon,
(dn/depsilon)^2 / n, is finite at the EP. Consequences:

- exponent of the control parameter under photon counting: 0 (unchanged);
- exponent of the gap: 1 (the curse is unbeatable at an EP);
- Tsang's super-resolution needs a population linear in epsilon, i.e. a
  source whose statistics depend on s = sqrt(epsilon): non-analytic in
  the physical parameter. This is exactly "two independent excitations
  of the two eigenmodes with fixed variance", which near an EP requires a
  source coupling to the Jordan direction that scales as sqrt(epsilon).

If this holds, the theorem extends from additive noise to any counting
statistics and to the quantum Fisher information of classical
(Gaussian, zero-mean) light, and the only loophole is a non-analytic
source. If it fails, the failure is the discovery.

## Instrument (frozen)

EP-2 toy with generic phase: mu = 0.7 - 1i, unfolding rho = epsilon,
gap s = 2 sqrt(epsilon), eigenfrequencies omega_pm = mu pm sqrt(epsilon).
Time window t in [0, 6], 600 samples (damping e^-6 at the end of the
window). epsilon from 1e-1 down to 1e-6, one point per decade, local
log-log slopes of sigma between consecutive decades; the "measured" value
is the last slope (epsilon = 1e-5 -> 1e-6). Derivatives by central
differences in mpmath (40 digits; step 1e-12 relative).

Source classes:

- S1, coherent fixed source: g(t) = e^{-i mu t}[x cos(st/2) + (2y/s) sin(st/2)],
  x = 1, y = 0.8 e^{0.4i}, mean photon number N = 100.
- S2, eigenmode-incoherent (Tsang-type, NON-analytic normalization):
  field = E+ e^{-i omega+ t} + E- e^{-i omega- t} with E+, E- independent
  zero-mean complex Gaussian, variance V = 1 each, fixed as s -> 0.
- S3, port-incoherent (analytic): H(epsilon) = mu I + [[0, 1], [epsilon, 0]]
  (EP-2 at epsilon = 0, nilpotent N = [[0,1],[0,0]], transversal). White
  noise of unit variance injected in bare port j, observed at bare port k,
  field g_kj(t) = <k| e^{-iHt} |j>. All four (k, j).
- S4, partially coherent eigenmode amplitudes, fixed V (same
  non-analytic normalization as S2): <E+ E-*> = gamma V with
  gamma in {0.5, 0.9, 0.99, 1.0}.

Measurements:

- M1, mode-resolved counting in a FIXED basis: Gram-Schmidt of
  {v0, v1, dv0, dv1, d2v0, d2v1} evaluated at epsilon = 0, where
  v0 = e^{-i mu t}, v1 = t e^{-i mu t}; a seventh "rest" bucket collects
  the remaining population. Coherent light: Poisson per mode,
  Fisher = sum (dn_k)^2 / n_k. Thermal light: independent-thermal model
  per mode, Fisher = sum (dn_k)^2 / (n_k (n_k + 1)) (documented as the
  classical Fisher of that measurement model).
- M2, direct time-resolved intensity: Fisher = sum_t (dI_t)^2 / I_t
  (coherent) or / (I_t (I_t + 1)) (thermal), with a 1e-9 relative floor.
- M3, quantum Fisher information: coherent state, F = 4 N |d g|^2 in the
  unnormalized mode vector; zero-mean Gaussian light, the closed-form
  Gaussian QFI in the 4-mode support {v0, v1, dv0, dv1} at the evaluation
  point, with a thermal regularization floor n_bg = 1e-12 in every mode
  (declared; insensitivity gate: halving n_bg must not move any slope by
  more than 0.02). GATE before physics: the Gaussian QFI implementation
  must reproduce, to 1e-6 relative, the single-mode thermal result
  F = 1/(n(n+1)) at n in {0.1, 3} and the squeezed-vacuum result F = 2.

## Predictions

P20.1 (S1, coherent; M1, M2, M3): slope of sigma(epsilon) -> 0
(|slope| < 0.05); slope of sigma(s) -> -1.00 +- 0.05.
KILL: any of the three measurements outside the windows.

P20.2 (S2, eigenmode-incoherent, fixed V; M1 and M3): slope of
sigma(epsilon) -> +0.50 +- 0.05 (error on the control parameter SHRINKS
at the EP); slope of sigma(s) -> 0.00 +- 0.05 (Tsang's constant Fisher,
time-domain form). M2 direct detection on the SAME state: sigma(epsilon)
slope 0, sigma(s) slope -1 (the curse under direct detection).
KILL of the INSTRUMENT (not of the physics): failure to reproduce these
established results means the pipeline is broken; fix before anything
else is read.

P20.3 (S3, port-incoherent analytic, all four configurations; M1, M3):
slope of sigma(epsilon) -> 0 (|slope| < 0.05) and slope of sigma(s)
-> -1.00 +- 0.05 in every configuration. In configuration (k, j) = (2, 1)
the total detected population vanishes at the EP with local slope
2.00 +- 0.05 in epsilon (even-order zero).
KILL of the candidate theorem: any configuration with sigma(s) slope
above -0.5, or a population vanishing with slope 1.00 +- 0.2.

P20.4 (S4, fixed V, partial coherence): for gamma in {0.5, 0.9, 0.99}
slopes as P20.2 (+0.5 / 0); for gamma = 1.0 exactly, slopes as P20.1
(0 / -1).
KILL of the reading "the loophole is the normalization, not the
coherence": some gamma < 1 with sigma(s) slope below -0.5.

## Declared risks

- The independent-thermal counting model in M1 ignores cross-mode
  correlations of the thermal state; M3 (QFI) is the authoritative
  quantum bound, M1 is the practical measurement.
- The regularization floor n_bg could fake a slope if populations reach
  it: the insensitivity gate above is mandatory.
- Rank collapse by phase (third-time lesson): generic phases in mu and y
  are frozen above; an inversion-residual guard is mandatory.
