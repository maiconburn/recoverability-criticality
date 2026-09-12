# P33, where the gradient expansion stops is where the labels stop: verdicts (2026-09-12)

Preregistration: `FROZEN_P33_HYDRO_LABELS.md` (amended before any
measurement to correct the EP location, which the draft had taken from
a different Gauss-Bonnet coupling). Scripts: `p33_hydro_labels.py`
(monodromy, Cauchy coefficients), `p33b_invariant_tracking.py`
(invariant tracker, corrected radius estimators),
`p33c_beyond_ep.py` (continuation past the EP, the P33.3 test),
`p33d_noise_scaling.py` (cost ladder). Data: the JSON files of the same
names. System: scalar channel of the 5D planar Einstein black brane,
lambda_GB = 0, in the solver's units (omega, q in units of pi T).

## Summary

The mirror pair of the fundamental scalar mode collides at
q^2_c = -5.0123755, omega_c = -3.5387430 i. There the symmetric
invariant rho = ((omega_+ - omega_-)/2)^2 has a simple ZERO
(rho = 8.7e-17, drho/dq^2 = 3.205) while the labelled eigenvalues have
a square-root BRANCH POINT: a loop around the EP exchanges them to
thirteen decimal places, 1.6e-13, while mu and rho return to
themselves to 5e-14 and 2.8e-13. A zero costs a Taylor series nothing
and a branch point caps its radius, so the two descriptions stop
converging at different momenta:

    labelled mode:        R_omega = 5.100 +- 0.038   (= |q^2_c| to 1.8%)
    symmetric invariant:  R_rho   = 7.559            (1.48 x further)

and at a momentum between them, q^2 = -6.3475, the order-12 series
about q^2 = 0 reproduces rho to 2.9% while the series for the labelled
mode errs by 233%. The breakdown of the mode-by-mode expansion is a
breakdown of the labelling, not of the physics: the pair is perfectly
well described 48% further out in momentum if one asks the symmetric
question. This is the repository's theorem in the arena where the
radius of convergence of hydrodynamics is defined (Grozdanov, Kovtun,
Starinets and Tadic, PRL 122, 251601, 2019), for a pair of
non-hydrodynamic modes; the sound and shear channels are not computed
here.

## Verdict table

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P33.1 monodromy: labels exchange to 1e-5, invariants return to 1e-6, labels move by more than 0.5, at radii 0.5 and 1.0 | KILL: no exchange at either radius, or an invariant shifting by more than 1e-4 | radius 0.5: swap error 1.64e-13, label motion 2.415, mu shift 5.3e-14, rho shift 2.8e-13. Radius 1.0: the label tracker runs away (to omega ~ -4148, an instrument failure), while the invariant tracker returns mu to 7.4e-14 and rho to 3.0e-13 | CONFIRMED at radius 0.5 with eight orders of margin; at radius 1.0 only the invariant half is measurable with this tracker |
| P33.2a rho has a simple zero at q^2_c: |rho| < 1e-7, |drho/dq^2| > 0.05 | KILL: rho not vanishing | rho = 8.65e-17, drho/dq^2 = 3.2049 | CONFIRMED |
| P33.2b radii from |a_n|^(-1/n) over n = 6..14: R_omega = 5.0 +- 0.6 and R_rho > 1.2 R_omega | KILL: R_rho < 1.05 R_omega, or R_omega outside [4.0, 6.5] | with the frozen estimator R_omega = 6.84 and R_rho = 7.16, ratio 1.047: BOTH kill clauses fire | KILLED by the estimator I specified (tombstone 37) |
| the same claim with a correct estimator (recorded after the freeze, clearly labelled) | not frozen | corrected ratio test (the n^(-3/2) prefactor of a square-root branch point removed) plateaus at R_omega = 5.100 +- 0.038 over n = 7..11, and the |a_n| = C n^(-3/2) R^(-n) fit gives 5.055, against |q^2_c| = 5.01238: agreement to 1.8%. For rho the raw ratio test plateaus (no such prefactor) at R_rho = 7.559. Ratio 1.482 | the claim holds; the frozen test of it did not |
| P33.3 at a momentum between the two radii the order-12 series reproduces rho to better than 5% while the labelled series errs by more than 30% | KILL: rho worse than 15%, or the labelled series better than 15% | at q^2 = -6.3475: rho true -5.9100655 against series -6.0834677, error 2.93%; labelled mode true -1.7784570 i against series -3.2929 - 4.2990 i, error 233% | CONFIRMED |
| P33.4 noise scaling: labelled error ~ sqrt(eta), invariant error ~ eta | recorded, no kill | both errors are linear in eta below saturation; what separates them is the amplification |d omega|/|d rho| = 2.8, 56, 365 at half-splittings 0.797, 0.0358, 0.00367, tracking 1/(2s) = 1.3, 28, 272 to within a factor 2. Above saturation the labelled error pins at the splitting and the invariant error at the splitting squared | the ladder's first rung CONFIRMED in the form 1/gap amplification; the frozen sqrt(eta) wording was wrong and is corrected below |

## The collision, seen from three sides

Along the spacelike axis, approaching (label tracker, mirror symmetry
held to 1e-13 throughout):

| q^2 | omega_+ | rho |
|---|---|---|
| 0 | 3.1194516 - 2.7466757 i | 9.7309782 |
| -2.00 | 2.5663313 - 2.9268544 i | 6.5860560 |
| -4.00 | 1.6500889 - 3.2459552 i | 2.7227930 |
| -4.75 | 0.8935542 - 3.4486482 i | 0.7984390 |
| -5.00 | 0.1989184 - 3.5342215 i | 0.0395690 |
| -5.0123755 (EP) | 0 - 3.5387430 i (double) | 8.7e-17 |

Past the collision both roots are purely imaginary and separate
(`p33c_beyond_ep.py`, each root continued independently, |Re omega| <
1e-6 enforced):

| q^2 | omega (upper) | omega (lower) | mu | rho |
|---|---|---|---|---|
| -5.4975 | -2.4230562 i | -5.0561196 i | -3.7395879 i | -1.7332558 |
| -5.9975 | -2.0017806 i | -5.9953113 i | -3.9985459 i | -3.9870719 |
| -6.4975 | -1.6932378 i | -6.9193405 i | -4.3062892 i | -6.8280374 |
| -6.9975 | -1.4406680 i | -7.8615525 i | -4.6511102 i | -10.3069396 |
| -7.4975 | -1.2228741 i | -8.8252103 i | -5.0240422 i | -14.4488790 |

## Three trackers, and why two of them fail

This is the methodological product of the cycle, and it is the theorem
telling you how to compute.

1. Label tracking (nearest match on omega_+, omega_-) works up to the
   EP and fails past it: at q^2 = -5.75 on the real axis the mirror
   symmetry breaks to 3e-3 and the tracker jumps; on the radius-1.0
   monodromy circle it ran to omega ~ -4148 - 45 i and took 1535 s.
   Reason: past the EP the labels are not continuous functions of q^2.
   It is the ONLY tracker that can see monodromy.
2. Invariant tracking (extrapolate mu and rho, seed mu +- sqrt(rho))
   keeps the invariants to 1e-13 on the radius-1.0 circle but CANNOT
   see monodromy, because the principal square root re-assigns the
   labels at every step; and it too runs away far past the EP, where
   the seed built from a principal root does not resemble the true
   pair of purely imaginary roots.
3. Independent continuation of each root on the imaginary axis, past
   the EP, with |Re omega| < 1e-6 enforced: works, 59 points from
   -5.03 to -7.65.
   Lesson: match the tracker to the local structure. Labels for
   monodromy, invariants for analytic continuation in a neighbourhood,
   separate real-axis roots in the overdamped regime.

## Noise scaling (P33.4)

Additive noise eta on the Wronskian (relative to |W| ~ 4e1 away from the roots), median over 12
seeds, at three distances d from the EP (half-splitting s = sqrt(3.205 d)):

| d | s (half-splitting) | eta | |d omega| | |d rho| | |d omega| / |d rho| | 1/(2s) |
|---|---|---|---|---|---|---|
| 1e-06 | 0.00183 | 1e-08 | 3.928e-05 | 1.075e-07 | 365.4 | 272.6 |
| 1e-06 | 0.00183 | 1e-07 | 2.978e-04 | 7.572e-07 | 393.3 | 272.6 |
| 1e-06 | 0.00183 | 1e-06 | 1.646e-03 | 2.620e-06 | 628.3 | 272.6 |
| 1e-04 | 0.01791 | 1e-08 | 7.274e-07 | 1.293e-08 | 56.2 | 27.9 |
| 1e-04 | 0.01791 | 1e-07 | 6.401e-06 | 1.636e-07 | 39.1 | 27.9 |
| 1e-04 | 0.01791 | 1e-06 | 9.085e-05 | 2.246e-06 | 40.5 | 27.9 |
| 5e-02 | 0.39829 | 1e-08 | 9.094e-08 | 3.239e-08 | 2.8 | 1.3 |
| 5e-02 | 0.39829 | 1e-07 | 8.127e-07 | 3.417e-07 | 2.4 | 1.3 |
| 5e-02 | 0.39829 | 1e-06 | 7.860e-06 | 3.670e-06 | 2.1 | 1.3 |
| 5e-02 | 0.39829 | 1e-05 | 2.118e-04 | 8.930e-05 | 2.4 | 1.3 |
| 5e-02 | 0.39829 | 1e-04 | 2.068e-03 | 9.342e-04 | 2.2 | 1.3 |
| 5e-02 | 0.39829 | 1e-03 | 1.609e-02 | 5.644e-03 | 2.9 | 1.3 |

Amplification of the labelled error over the invariant error, against the inverse gap:

| d | half-splitting s | measured median |d omega|/|d rho| | 1/(2s) | ratio |
|---|---|---|---|---|
| 1e-06 | 0.00183 | 393.3 | 272.6 | 1.44 |
| 1e-04 | 0.01791 | 40.5 | 27.9 | 1.45 |
| 5e-02 | 0.39829 | 2.4 | 1.3 | 1.89 |

Saturation: once eta is large enough that the labelled error reaches the
splitting, it stops growing (|d omega| pinned at 1.77e-2 for eta = 1e-5 to 1e-2 at
d = 1e-4) and the invariant error pins at s^2 = rho itself (3.20e-4 against
rho = 3.21e-4): the pair is then simply unresolved, and both descriptions lose it
together. Below saturation both errors are LINEAR in eta (slopes 0.99 and 0.97 at
d = 1e-4, 1.11 and 1.10 at d = 0.05); what separates them is not a different power
of eta but the constant 1/gap by which the labelled question amplifies the same
underlying error. That is the first rung of the ladder (P15/P17) as it appears in
this instrument, and it is NOT the sqrt(eta)-versus-eta split written into the
freeze: recorded as a correction of the frozen wording, which had no kill clause.

## Instrument lesson 16

Never estimate a radius of convergence from |a_n|^(-1/n) at modest n.
It converges like R times C^(-1/n), so with coefficients to n = 14 and
C of order 4 it overshoots by 35% (6.84 against the true 5.01), enough
to kill a correct prediction. Use the ratio test with the algebraic
prefactor of the expected singularity removed (a_n/a_(n+1) = R(1 +
p/n), p = 3/2 for a square-root branch point), or fit
|a_n| = C n^(-p) R^(-n) with p free, and report the plateau and its
spread. The Cauchy coefficients themselves were sound: the circles of
radius 3.5 and 4.5 agreed to all printed digits, which is the right
consistency check.
