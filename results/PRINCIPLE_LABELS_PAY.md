# The response is analytic, the labels pay: a principle for information near spectral singularities (synthesis, 2026-09-10)

Status: a synthesis of results already recorded in this repository
(each with its preregistration, kill criteria and verdict). Nothing
here is new measurement; the point is the single statement the
measurements support, its proof sketch, its exponents, its
predictions, and its limits. Not submitted anywhere.

## The statement

Let a linear system have a spectrum {omega_k} with excitation
amplitudes {A_k}, both depending analytically on a control parameter
epsilon, and let the spectrum have a singularity at epsilon = 0: an
exceptional point (two or more eigenvalues coalescing with their
eigenvectors), a branch cut of the resolvent (a mode reaching a
continuum), a polynomial point (an algebraically special solution), or
a confluence (two power laws merging into a logarithm). Then:

1. Every physically observable response, and every quantity that is a
   symmetric function of the spectrum, is analytic in epsilon through
   the singularity. Its Fisher information about epsilon is finite;
   the critical exponent of the cost of estimating the control
   parameter is exactly zero.

2. Every labeled quantity, an individual eigenvalue, an individual
   amplitude, "which mode is which", pays a critical cost with an
   exponent fixed by the Jacobian of the map from symmetric to labeled
   variables: for an EP of order p, the Cramer-Rao ladder
   {p - 1, 2p - 2, 2p - 1} (frequency gap, amplitudes with a Green's
   function constraint, free antisymmetric amplitudes), i.e. the row
   norms of the inverse Vandermonde (simple for the gap, confluent for
   the amplitudes).

3. At a branch cut the mode does not stop: its trajectory continues
   analytically onto the second sheet (implicit function theorem for
   the analytically continued spectral function), so its real part
   vanishes linearly in the control parameter, never as a square root;
   the response stays continuous because the pole's contribution
   passes into the cut integral.

4. With a source analytic in epsilon, positivity plus analyticity make
   a dark-mode population vanish to even order, so photon counting and
   the quantum Fisher information of classical light are finite at the
   EP: Rayleigh's curse cannot be beaten by an EP. Super-resolution
   claims need a source non-analytic in epsilon (the fixed-variance
   source of Tsang, which depends on sqrt(epsilon)).

In one sentence: the singularity belongs to the bookkeeping, not to
the physics; the cost is a property of the question asked, not of the
signal.

## The mathematics in three lines

- Response channels are divided differences of e^{-i omega t} over the
  spectrum: symmetric functions, hence analytic in the elementary
  symmetric polynomials e_j(omega), which are the coefficients of the
  characteristic polynomial and analytic in epsilon. (Theorem,
  `THEOREM_EP_NEUTRALITY.md`; verified 5/5 at 60 digits,
  `p17_theorem_check.py`.)
- Individual eigenvalues are algebraic functions of the e_j with a
  branch point at the EP; the Fisher matrix in labeled coordinates is
  J^T F J with J the Vandermonde (confluent Vandermonde for
  amplitudes), whose inverse row norms scale as gap^{-(p-1)},
  gap^{-(2p-2)}, gap^{-(2p-1)}. (Exact symbolic, `p17b_ladder_symbolic.py`,
  6/6 for p = 2, 3; prior art for the amplitude rungs: Batenkov,
  Goldman, Yomdin.)
- The spectral function F(omega, epsilon) of a Leaver-type problem is
  built from the minimal solution of a recurrence whose tail carries a
  square root of omega; the sign choice makes F single-valued on the
  cut plane, and its continuation across the cut is the same
  expression with the other sign, analytic. Roots of F are analytic in
  epsilon wherever dF/d omega is nonzero. (`RESULTS_P22_KERR_NIA.md`,
  theory addendum.)

## Eight instances, each preregistered

| instance | system | labeled cost (measured) | response cost (measured) | record |
|---|---|---|---|---|
| 1 | EP-2 of a damped pair, exact model | gap exponent -1; antisymmetric amplitudes -2; EP-N gap -(N-1) | control parameter: exponent 0.000 (5/5 exact checks) | `THEOREM_EP_NEUTRALITY.md`, `RESULTS_P15_EPN.md` |
| 2 | Kerr overtone pair (2,2,5)/(2,2,6) on six SXS waveforms | extraction cost of the pair ~ gap^{-1.11} (corr 0.96) through the avoided crossing at a = 0.8975 | | `README.md` sec. 1.4 |
| 3 | superconducting qubit, real cloud QPU (ibm_fez) and Murch-lab data | spectral-estimation cost enhanced ~4x near the EP | Petz state-recovery fidelity flat | `README.md` sec. 1.5 |
| 4 | photon counting / QFI at an EP (P20) | Tsang's +0.5 / 0 reproduced only with a source non-analytic in epsilon | finite Fisher, dark population vanishes to even order (4-digit agreement) | `RESULTS_P20_RAYLEIGH_EP.md` |
| 5 | cosmological collider, nu = 1 confluence (P8-F4') | the "Jordan log channel" is the confluent limit of two powers, not an extra channel (F4'.1 killed, F4'.2 confirmed) | | `RESULTS_P8_PHASE1.md` |
| 6 | Kerr-de Sitter excitation factors (Rossi, Oshita, Berti 2026) | rank-2 Riesz cluster P +- = P/2 +- D/s explains the enhancement and opposite phases; cluster moments finite | | `RESULTS_P15_EPN.md` addendum |
| 7 | draining vortex, counter-rotating overtones (P21-P24) | absorption by the branch cut linear in rotation (exponents 1.000, 1.004, 1.002); no purely imaginary mode (lemma); survivors collapse onto the branch point as c_n/B; escape rule Re c_n > 0; tower |m| 2[K(k) - E(k)] = i pi (n + 1/2), k^2 = 1 - 4 c/|m|; count N(m) = floor(0.8008 |m| + 1/2), measured 1, 2, 2, 3, 4, 5, 6 | time-domain ringdown continuous through the absorption, exponent 1.000 | `RESULTS_P21_VORTEX.md`, `RESULTS_P23_TOWER_LAW.md`, `RESULTS_P24_VORTEX_MULTIPLET.md` |
| 8 | Kerr overtones reaching the negative imaginary axis (P22, P23.2) | arrival linear at the endpoint (local exponent -> 1, cubic law), death spins to 2e-4 of Cook-Zalutskiy, pinned to -i n/4 where a polynomial mode exists; re-emergence; a cubic from Re in [0.01, 0.04] predicts death spins blind to 5e-4 while a fold model misses by 5e-3 | (continuity not measured in Kerr) | `RESULTS_P22_KERR_NIA.md`, `RESULTS_P23_TOWER_LAW.md` |

Twenty-seven predictions died along the way (`GRAVEYARD.md`); the
statement above survived every one of its own kill criteria.

## What it predicts that can be checked by others

- Any EP-based sensor: no critical gain for estimating the parameter
  that unfolds the EP; the gain, where real, is in the linear-response
  prefactor. (Independent of, and consistent with, the Langbein /
  Lau-Clerk / Wiersig discussion; our addition is the exact exponent
  structure and the reason.)
- Black-hole spectroscopy: the cost of separating two overtones near
  an avoided crossing scales as the inverse gap; fitting the waveform
  (symmetric) does not pay it, fitting the labeled overtones does.
- Kerr: the death spins of the {2, 0, n_0} and {2, -2, n_0} sequences
  follow an analytic (cubic) law in the spin from data a full 0.01 to
  0.04 away in Re(omega M); anyone with the public `qnm` package can
  reproduce the numbers in `p23_kerr_extrap.json`.
- The rotating draining vortex (shallow water, k h << 1 at the light
  ring): N(m) = 1, 2, 2, 3, 4 counter-rotating ringdown modes for
  |m| = 1..5 at strong rotation, damping rates in the ratio
  1 : 3 : 5, fundamental frequency |m| c_s^2 / (8 pi C); at moderate
  rotation the m = -1 first overtone is absorbed at B/A = 0.289 with a
  continuous ringdown. Existing data (Torres et al. 2020) are in the
  deep-water regime and do not test this; the shallow regime needs
  h << 2C/(|m| c_s), and the tower assumes an absorbing core (a
  drain), which their surface flow lacked.
- Any analogue with a branch cut and no polynomial modes: modes reach
  the cut linearly and nothing is born from it; with polynomial modes
  (Kerr) sequences can end and begin on the axis.

## Limits, honestly

- Linear response only; strong-field or nonlinear ringdown is outside.
- The source must be analytic in the control parameter; Tsang's
  non-analytic source is a real loophole and is where super-resolution
  lives.
- The Kerr side lacks the continuity measurement (time-domain
  Teukolsky) and a count law: the analogue of "which overtones survive
  extreme rotation" is Cook-Zalutskiy's multiplet bookkeeping plus the
  ZDM/DM bifurcation, not yet derived from an action.
- The O(1/|m|) constant of the vortex tower (k_1 = +0.031) is fitted,
  not derived.
- Applications outside physics (identifiability in machine learning
  under permutation symmetry is the one honest analogue) are
  untested; one applied line (radar sensor management) was tried and
  died against a physics-blind baseline.
