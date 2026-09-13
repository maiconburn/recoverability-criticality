# Prior-art audit before any submission (2026-09-13)

Purpose: decide, claim by claim, what in this repository is new, what is
a rediscovery, and what must be cited, BEFORE a paper carries the
author's name. Method: thirteen full texts read (pdftotext, keyword
scan, then the relevant passages), the LaTeX source of one paper
downloaded to avoid transcribing an equation from a PDF, one symbolic
computation to compare a published expansion with ours, and twelve
targeted web searches. Everything below is checkable from the files
named.

## Headline verdicts

| claim | status | prior art | what survives |
|---|---|---|---|
| Counter-rotating overtones of the draining bathtub are absorbed by the branch cut, linearly, at finite rotation; no purely imaginary mode exists (P21) | NEW as far as this audit finds | Cardoso, Lemos and Yoshida 2004 wrote "we haven't been able to track some overtone modes with negative m for very high rotation since ... the real part of these modes eventually change sign. It is extremely difficult, using the method employed here, to compute modes having Re[omega] ~ 0" and, assuming the frequencies asymptote to zero, "a WKB analysis shows that omega ~ k/B, where k is some m-dependent constant". Dolan, Oliveira and Crispino 2012 note the branch cut on the negative imaginary axis for the tails and that "in the limit of very large C the imaginary part of the least-damped counter-rotating mode asymptotes to zero" | the mechanism (arrival at the cut, exponent 1.000), the lemma (CLY recurrence has no polynomial solutions), the continuity of the response through the absorption, the escape rule Re c_n > 0, and the constants k = c_n(m) that CLY left unnamed |
| The 1/|m| series of the light-ring tower: Re c_n = |m|/4 - (3/8)(n+1/2)^2/|m| + 1/(32|m|), Im c_n = -(n+1/2)/2 + ... (P23, "derived") | REDISCOVERY | Dolan, Oliveira and Crispino, PRD 85, 044031 (2012), Eq. (51): the geodesic expansion of the DBT quasinormal frequency to O(m^-3) (computed to O(m^-9)) for general overtone, with counter-rotating light-ring parameters. Its C -> infinity limit, taken symbolically here from the LaTeX source, is EXACTLY our series through every term we derived, and contains three terms we never derived: -7iN/(128 m^2), -17N^2/(512 m^3), -9/(4096 m^3). At |m| = 10 it beats our series on every member (see table) | nothing at the level of the series. The 3/32 "derivation" (Dunham contour) is a consistency check of a 2012 result |
| The barrier action in closed form, J = 2[K(k) - E(k)], k^2 = 1 - 4c/|m|; the tower as roots of |m| 2[K - E] = i pi (n + 1/2) | NEW as far as this audit finds (zero occurrences of "elliptic" in the thirteen texts; Dolan-Oliveira 2013 use K and Pi for the scattering angle, not for the action) | Dolan et al. 2012 (the asymptotic series it resums); Patrick, Coutant, Richartz and Weinfurtner 2018 and Torres, Coutant, Dolan and Weinfurtner 2018 (WKB actions for the vortex, numerically) | the resummation: the series is asymptotic (Dolan et al. say so, "suggesting that Eq. (51) is in fact an asymptotic series") and fails at the crossing where n + 1/2 ~ 0.8 |m|; the elliptic form does not |
| The count law N(m) = floor(0.8008 |m| + 1/2), kappa the root of Re[K - E] = 0 (P23) | NEW as far as this audit finds, with a caveat | nobody counts; but the O(m^-3) series of Dolan et al. gets the same counts for |m| <= 20 (table below), because the crossing sits where its error is still smaller than the spacing. The quadratic truncation sqrt(2/3) = 0.8165 fails at |m| = 8, 13, 18, 19 | a closed-form constant and the statement "four fifths of |m|, not |m| - 1"; the exact counts at |m| = 12, 15 measured |
| The escaping modes are the light-ring resonances of the pure vortex; damping ladder 1 : 3 : 5 (P21f) | leading order KNOWN | Dolan et al. 2012 Eq. (37): omega = Omega m - i Lambda (n + 1/2), with Lambda^- -> c^2/(2C) as C -> infinity, i.e. our -(2n+1)/4 | the identification of the SURVIVORS with this tower, and the exact scaled towers to |m| = 15 |
| Reflecting versus absorbing core: trapped Bohr-Sommerfeld modes, tunnelling dampings, loss of the ladder (P26, P27) | LARGELY KNOWN | Torres, Patrick and Gregory, PRD 106, 045026 (2022): effective boundary with reflectivity K, "bound states located between the effective vortex core and the angular momentum barrier", Breit-Wigner lines, WKB estimates; Patrick et al. 2018: Bohr-Sommerfeld S_d = pi(n + 1/2) with tunnelling damping T = exp(-S); Vieira and Destounis, PRD 112, 064086 (2025): Dirichlet or Neumann at the core of a horizonless vortex, bound spectra; Solidoro, Patrick, Gregory, Weinfurtner PRL 2025 (partially reflecting wall) | only the specific count rule in the scaled limit (14/14) and the barrier-top resonance; a section, not a headline |
| Tank feasibility: Q_0 = |m|/2 invariant, blind counting fails, fixed-frequency cluster fitting (P32) | NEW as an audit of our own design | Torres et al. PRL 125, 011301 (2020) (deep-water experiment, C/D ~ 16); Smaniotto et al. 2025 (helium vortex, overtones excited) | the invariant Q and the protocol; useful to experimenters |
| Control-neutrality theorem, Vandermonde ladder, Fisher exponents (theorem paper) | the mathematics is classical (Kato; symmetric functions; Vandermonde conditioning); the estimation-theory exponents are new as far as this audit finds | already cited: Morikawa-Ogawa-Hirose 2026, Ould El Hadj-Dolan 2026, Rossi-Oshita-Gualtieri-Berti 2026, Wiersig-Rotter 2026, Batenkov et al. MISSING and mandatory: Yang, Berti and Franchini, PRL 135, 201401 (2025), the paper that identified EPs in the Kerr spectrum and states that near an EP "the two modes are just different covers of the same complex function on a Riemann surface"; Panosso Macedo, Katagiri, Kubota and Motohashi, PRD 113, 043053 (2026), whose abstract says "the EP frequency, given by the average of the resonant modes, emerges as the physically relevant observable in the near-EP regime", whose Eq. (4) has excitation factors B = B_EP[1 +- b/delta]/2 (our Corollary B), and who show the two-mode fit is unstable | the exponents 0 and {p-1, 2p-2, 2p-1}, the SXS measurement of the labelled cost, the confluent-basis fit. The paper must be positioned as the metrology layer of a statement that four groups made qualitatively in 2025-2026 |
| The cosmological EP (P8 paper): de Sitter tower degeneracies at integer nu are EP-2, never higher; Gamma-function structure; metrology cost | not contradicted by anything found, but thin | de Sitter QNMs omega = -i(3/2 -+ nu + 2n)H are standard (Lopez-Ortega 2006; Jafferis et al. 2015; Sun 2021); the nu = 0 logarithm is Arkani-Hamed-Maldacena; Warnick 2024 treats the dS spectrum's instability with explicit modes and co-modes | an explicit exactness statement plus a negative forecast. The repository itself killed the paper's original motivation (the "cosmological clock", tombstones in GRAVEYARD). Recommendation: do not submit standalone; fold into the theorem paper as one worked example |

## The decisive computation (P23 against Dolan et al. 2012)

Eq. (51) of Dolan, Oliveira and Crispino (LaTeX source arXiv:1105.1795,
label `freqex`), with the counter-rotating light-ring parameters of
their Eqs. (bc), (rc), (lc), l_c^- = -2C - 2 sqrt(D^2 + C^2),
r_c^- = [sqrt(D^2 + C^2) |b_c^- - C|]^{1/2}, m -> -|m|, N = n + 1/2,
c = 1, and then C -> infinity at fixed D, in our scaled units
c = omega C / c_s^2 (sympy, this audit):

    c_n = |m|/4 - iN/2 + (1/32 - 3N^2/8)/|m| + (3iN^3/32 - 7iN/128)/m^2
          + (-5N^4/256 - 17N^2/512 - 9/4096)/|m|^3 + O(m^-4).

Our P23 series: |m|/4 - iN/2 - (3/8)N^2/|m| + 1/(32|m|) + (3i/32)N^3/m^2
- (5/256)N^4/|m|^3. Difference: -7iN/(128 m^2) + (-17N^2/512 - 9/4096)/|m|^3,
i.e. terms we never derived. Against the exact |m| = 10 tower
(complex-ray solver, `p23_tower_cplx_m-10.json`):

| n | exact | Dolan (C -> oo), |diff| | ours, |diff| |
|---|---|---|---|
| 0 | 2.49374 - 0.25016i | 0.0000 | 0.0003 |
| 1 | 2.41857 - 0.74765i | 0.0000 | 0.0008 |
| 2 | 2.26777 - 1.23667i | 0.0001 | 0.0013 |
| 3 | 2.04032 - 1.71147i | 0.0003 | 0.0017 |
| 4 | 1.73463 - 2.16622i | 0.0009 | 0.0020 |
| 5 | 1.34838 - 2.59493i | 0.0026 | 0.0027 |
| 6 | 0.87834 - 2.99154i | 0.0062 | 0.0056 |
| 7 | 0.32013 - 3.34999i | 0.0132 | 0.0127 |
| 8 | -0.33206 - 3.66447i | 0.0259 | 0.0258 |
| 9 | -1.08574 - 3.92989i | 0.0475 | 0.0482 |

Both series are asymptotic and fail together as n + 1/2 -> 0.8|m|.

Counts, exact (complex-ray, |m| <= 10; 12 and 15 in `p23_tower_ext.json`)
against the three formulas:

| |m| | exact | floor(0.8008|m| + 1/2) | sqrt(2/3) truncation | Dolan O(m^-3) at C -> oo |
|---|---|---|---|---|
| 2..7 | 2, 2, 3, 4, 5, 6 | same | same | same |
| 8 | 6 | 6 | 7 | 6 |
| 9, 10 | 7, 8 | 7, 8 | 7, 8 | 7, 8 |
| 13 | - | 10 | 11 | 10 |
| 18, 19 | - | 14, 15 | 15, 16 | 14, 15 |

## Citations to add before anything is submitted

Vortex paper: Dolan, Oliveira, Crispino PRD 85, 044031 (2012) [the
series]; Cardoso, Lemos, Yoshida PRD 70, 124032 (2004) [the untracked
modes, omega ~ k/B]; Berti, Cardoso, Lemos PRD 70, 124006 (2004);
Dolan, Oliveira PRD 87, 124038 (2013) [scattering, Regge poles];
Torres, Coutant, Dolan, Weinfurtner JFM 857, 291 (2018) [light rings
at arbitrary depth]; Patrick, Coutant, Richartz, Weinfurtner PRL 121,
061101 (2018) [Bohr-Sommerfeld quasibound states]; Torres, Patrick,
Richartz, Weinfurtner PRL 125, 011301 (2020) [the experiment]; Torres,
Patrick, Gregory PRD 106, 045026 (2022) [reflecting effective core];
Solidoro, Patrick, Gregory, Weinfurtner PRL (2025) [partially
reflecting wall]; Vieira, Destounis PRD 112, 064086 (2025)
[horizonless vortex, Dirichlet/Neumann core]; Smaniotto et al. (2025,
helium vortex, overtones); Yu and Wu arXiv:2605.03730 (2026, total
transmission modes with vorticity); Matyjasek, Benda, Stafinska
arXiv:2408.16116 (2024, nine-digit DBT modes); Cook and Zalutskiy PRD
94, 104074 (2016) [polynomial-mode criterion used in the lemma];
Lepe and Saavedra (2005) [low-frequency approximation, superseded].

Theorem paper: add Yang, Berti, Franchini PRL 135, 201401 (2025) and
Panosso Macedo, Katagiri, Kubota, Motohashi PRD 113, 043053 (2026),
and Lo, Sabani, Cardoso PRD 111, 124002 (2025) [Kerr excitation
factors]; Takahashi, Motohashi, Takahashi PRD 112, 064006 (2025)
[resonance in coupled systems].

## Recommendation

1. Vortex paper: WRITE IT, with Dolan et al. 2012 in the abstract's
   second sentence. Title the contribution as the strong-circulation
   limit and its two non-perturbative facts (absorption by the cut;
   the elliptic resummation and the count), not as a derivation of the
   series. Referees will be from the Sheffield, Nottingham, Belem and
   UFABC groups; every one of them knows Eq. (51).
2. Theorem paper: add the two 2025-2026 citations and one paragraph
   placing Panosso Macedo et al.'s "average is the observable" as the
   qualitative statement whose exponent we compute. Then it is
   submittable as a short paper.
3. P8 paper: do not submit standalone.
4. Principle synthesis: internal only.

Record in `RESULTS_P23_TOWER_LAW.md`: the series is the C -> infinity
limit of a 2012 result (addendum below the 3/32 section). This is a
downgrade of novelty, not a tombstone: nothing measured was wrong.
