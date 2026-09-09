# P20, Rayleigh's curse at the exceptional point: verdicts (2026-09-09)

Preregistration: `FROZEN_P20_RAYLEIGH_EP.md` (commit 79f4a44, before any
run). Script: `scripts/p20_rayleigh_ep.py`. Data: `p20_rayleigh_ep.json`.
Slopes are local log-log slopes of sigma against epsilon (last decade,
epsilon = 1e-5 -> 1e-6); the gap slope in s is 2*slope_eps - 1.

## Summary

The control-neutrality theorem survives the change from additive noise
to photon counting and to the quantum Fisher information of classical
light. Tsang's constant-Fisher super-resolution is reproduced exactly in
the time domain (eigenmode-incoherent excitation, fixed variance), and
it is shown to require a source whose statistics depend on
s = sqrt(epsilon): any source analytic in the physical unfolding
parameter has dark-mode populations vanishing to EVEN order (measured
2.0000), so the counting Fisher information for epsilon stays finite and
the gap keeps its s^-1 cost. Rayleigh's curse is unbeatable at an EP
with physical sources; the only loophole is a non-analytic one.

| prediction | frozen | measured (last decade) | verdict |
|---|---|---|---|
| P20.1 S1 coherent, sigma(eps) slope, M1/M2/M3 | 0 | 0.0000 / 0.0000 / 0.0000 | CONFIRMED |
| P20.1 S1 gap slope in s, M1/M2/M3 | -1.00 +- 0.05 | -1.0000 (all three) | CONFIRMED |
| P20.1 S1 marginalized over (x, y), M3 | 0 | 0.0000 | CONFIRMED |
| P20.2 S2 eigenmode-incoherent, sigma(eps) slope, M1/M3 | +0.50 +- 0.05 | +0.5000 / +0.5000 | CONFIRMED (Tsang, time domain) |
| P20.2 S2 gap slope in s, M1/M3 | 0.00 +- 0.05 | 0.0000 / 0.0000 | CONFIRMED |
| P20.2 S2 direct detection M2 | 0 / -1 | Fisher identically zero | VOID (see below) |
| P20.3 S3 (1,1),(1,2),(2,2): sigma(eps) / gap, M1 M2 M3 | 0 / -1 | 0.0000 / -1.0000 in all nine | CONFIRMED |
| P20.3 S3 (2,1): sigma(eps) / gap, M1 M2 | 0 / -1 | 0.0000 / -1.0000 | CONFIRMED |
| P20.3 S3 (2,1): M3 (QFI) | 0 / -1 | 0.0003 / -0.9994 at eps 1e-4; last decade floor-limited | CONFIRMED on valid decades |
| P20.3 S3 (2,1): population zero order | 2.00 +- 0.05 | 2.0000 | CONFIRMED (even-order zero) |
| P20.4 S4 gamma = 0.5 / 0.9 / 0.99, M1 and M3 | +0.5 / 0 | +0.5000, +0.4999, +0.4984 (M1); +0.5000, +0.4998, +0.4979 (M3) | CONFIRMED |
| P20.4 S4 gamma = 1.0, M1 and M3 | 0 / -1 | 0.0000 / -1.0000 | CONFIRMED |

Gates: Gaussian QFI reproduces the single-mode thermal result at n = 0.1
and n = 3 (rel. err. 2e-41), the squeezed-vacuum result F = 2 (exact),
and a two-mode thermal state with epsilon-dependent populations and a
rotating mode basis against a brute-force Fock-space QFI (rel. err.
8e-8). Regularization gate: halving n_bg leaves every slope unchanged to
1e-4 except the last decade of S3 (2,1) M3, which moves from -0.34 to
-0.23: that decade is declared floor-limited (total population 2.5e-13
against a 4e-12 regularization floor) and excluded, as the freeze
required.

## The candidate theorem, now with evidence

Let n_k(epsilon) be the population of any fixed detection mode. For a
source whose second-order statistics are analytic in epsilon and
positive semidefinite, n_k is a nonnegative analytic function. A
nonnegative analytic function that vanishes at a point vanishes to even
order. Therefore either n_k(0) > 0, or n_k = c epsilon^2 + O(epsilon^3),
and the counting Fisher (dn_k)^2 / n_k = 4 c epsilon^2 / (c epsilon^2)
= 4c is finite. The control parameter keeps exponent 0 and the gap keeps
exponent 1 under photon counting, and (P20.3 M3) under the quantum
Fisher information of classical Gaussian light. Measured: configuration
(2,1), where the observer sits on the Jordan direction and the noise
port does not, has total population vanishing with slope exactly 2.0000
and Fisher exponent 0.0000.

Tsang's mechanism needs a population LINEAR in epsilon. In the
eigenmode-incoherent source S2 the dark mode carries V s^2/2 = 2V epsilon:
linear, because the source variance is held fixed while the eigenmode
amplitudes of any finite physical source would scale as 1/s. Holding the
variance fixed is a statement about s, not about epsilon: the source is
non-analytic in the physical parameter. That is the loophole, and it is
the only one found: partial coherence (P20.4) does not close it (the
curse resurges only at gamma = 1 exactly, with a crossover scale that
shrinks with 1 - gamma), in agreement with Tsang and Nair (Optica 6,
400, 2019) and against Larson and Saleh (Optica 5, 1382, 2018).

Consequence for EP sensing: no measurement of classical light, coherent
or incoherent, mode-resolved or direct, beats the s^-1 cost of the gap
or the exponent 0 of the unfolding parameter at an exceptional point,
unless the excitation itself is engineered to follow the eigenvectors
with a variance independent of their collapse. This complements
Lau-Clerk (coherent drive) and Wiersig-Rotter (scattering QFI, finite
enhancement) with the incoherent case, and identifies the exact
loophole.

## P20.2 M2: void, with the reason

The frozen expectation "direct detection of the incoherent pair pays the
curse (0 / -1)" was wrong for a reason visible after the fact: with a
REAL unfolding parameter the two eigenfrequencies mu +- sqrt(epsilon)
have identical decay rates, and an incoherent sum has no interference
term, so the time-resolved intensity I(t) = 2V e^{-2 Im(mu) t} is
independent of epsilon at every order. The Fisher information is
identically zero (measured sigma ~ 1e28, slope ~ 1 = the central-
difference roundoff signature). Direct intensity detection of an
eigenmode-incoherent pair is blind to a real splitting; all the
information sits in the mode structure, which is what M1 and M3 read.
Recorded in the graveyard as a frozen expectation that died of a
modeling oversight.

## Instrument lesson (fourth of its kind)

The first run reported QFI slopes of 0 / -1 for S2, contradicting the
classical M1 Fisher (+0.5 / 0), which a QFI can never undercut. The
Gaussian-state covariance builder was adding the vacuum identity to the
DERIVATIVE covariance as well as to the covariance itself. The
single-mode gates in the freeze did not catch it because they built
their matrices by hand. A two-mode gate against a brute-force Fock-space
QFI (populations and mode rotation both epsilon-dependent) now runs
before any physics and would have caught the bug at once. House rule
reinforced: every gate must exercise the same code path the physics
uses, in the same dimensionality.
