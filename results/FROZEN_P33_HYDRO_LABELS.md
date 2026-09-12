# P33, where the gradient expansion stops is where the labels stop, not where the physics stops (freeze, 2026-09-12)

Frozen BEFORE any computation in the complex momentum plane for this
cycle.

AMENDED 2026-09-12, before any measurement of a frozen prediction, for
an instrument-calibration error in the first draft. The draft quoted
q^2_c = -16.147205102, omega_c = -5.6738278 i from `RESULTS.md`; those
belong to the EP at the top of the studied Gauss-Bonnet range
(lambda_GB ~ 0.105), not to lambda_GB = 0. Locating the mirror EP with
this solver at lambda_GB = 0 (fine march along the spacelike axis,
mirror symmetry held to 1e-13, rho falling 9.731 -> 0.0396 between
q^2 = 0 and -5.00) gives

    lambda_GB = 0:  q^2_c = -5.0130 +- 0.001,  omega_c = -3.5342 i

in the solver's own units (omega and q in units of pi T, where the
q^2 = 0 fundamental is 3.119452 - 2.746676 i). Every circle radius
below is set from this value; the predictions themselves are unchanged
in form. EP locations for other couplings, for the record:
lambda = 0.05 -> q^2_c = -17.50, omega_c = -4.533 i;
lambda = 0.08 -> -16.25, -5.126 i.

## The claim

Grozdanov, Kovtun, Starinets and Tadic (PRL 122, 251601, 2019) showed
that the radius of convergence of the hydrodynamic gradient expansion
is set by critical points of the spectral curve: places in the complex
momentum plane where two quasinormal modes collide. A collision with
eigenvector coalescence is an exceptional point. This repository's
theorem says the symmetric functions of a colliding pair are analytic
through such a point while the individual (labeled) eigenvalues are
not. Put together:

    at the collision the symmetric invariant has a simple ZERO,
    the labeled eigenvalues have a square-root BRANCH POINT.

A zero costs a Taylor series nothing; a branch point caps its radius of
convergence. So the mode-by-mode dispersion relation stops converging
strictly before the pair's symmetric description does, and the
breakdown of the expansion is a breakdown of the labelling, not of the
physics.

Scope, stated plainly: the system here is the scalar (transverse
tensor) channel of the 5D planar Einstein black brane, lambda_GB = 0,
where the mirror EP-2 sits at q^2_c = -5.0130, omega_c = -3.5342 i
(measured here; see the amendment). That channel has no conserved-charge
(hydrodynamic) mode, so this is the same mathematical structure as the
hydrodynamic series but for a pair of non-hydrodynamic modes. The
sound and shear channels are not computed here and no claim is made
about their numbers.

## Objects

At q^2 = 0 the pair is the fundamental and its mirror,
omega_+ = 3.119452 - 2.746676 i and omega_- = -3.119452 - 2.746676 i, so
mu(0) = -2.746676 i and rho(0) = 9.730978 with
omega_+- = mu(q^2) +- sqrt(rho(q^2)) (`shooting.pair_invariants`).
Along the real spacelike axis rho decreases and vanishes at q^2_c.

## Predictions

P33.1 (monodromy): tracking the pair once around a circle of radius
0.5 centred on q^2_c (120 points, `ShootingSolver.pair` continuation)
exchanges the labels and preserves the invariants:
|omega_+(end) - omega_-(start)| < 1e-5 and
|omega_-(end) - omega_+(start)| < 1e-5, while
|mu(end) - mu(start)| < 1e-6 and |rho(end) - rho(start)| < 1e-6, and
the labels genuinely move, |omega_+(end) - omega_+(start)| > 0.5.
Same at radius 1.0.
KILL: no exchange at either radius (the collision would not be a
square-root branch point), or an invariant shifting by more than 1e-4.

P33.2 (zero versus branch point, and the two radii): rho has a simple
zero at q^2_c, |rho(q^2_c)| < 1e-7 with |drho/dq^2| > 0.05. Taylor
coefficients about q^2 = 0 from Cauchy integrals on circles of radius
3.5 and 4.5 (both inside |q^2_c| = 5.013; 128 points, the pair tracked
around the circle) give radius estimates from the decay of
|a_n|^(-1/n) over n = 6..14: R_omega = 5.0 +- 0.6 (the EP is the
nearest singularity of the labelled mode) and R_rho > 1.2 R_omega.
KILL: R_rho < 1.05 R_omega, or R_omega outside [4.0, 6.5], or rho not
vanishing at q^2_c.

P33.3 (usefulness): at a test momentum q^2_t chosen strictly between
the two measured radii (specifically q^2_t = -(R_omega + R_rho)/2, on
the spacelike axis), the order-12 truncated series about q^2 = 0
reproduces rho to better than 5% relative error while the series for
omega_+ errs by more than 30%.
KILL: the rho series errs by more than 15%, or the omega_+ series is
accurate to better than 15%.

P33.4 (the cost ladder, re-verification, recorded without a kill): with
relative noise eta injected into the Wronskian, the error in omega_+-
at distance d from the EP scales as sqrt(eta) for d below the noise
scale while the error in mu and rho scales as eta (exponents 1/2 and 1,
the first rung of the P15/P17 ladder). Recorded as a check that the
holographic instrument reproduces the known ladder, not as a new claim.

Instrument: `src/recoverability_ep/shooting.py` (unchanged),
`scripts/p33_hydro_labels.py`; output `results/p33_hydro_labels.json`.
