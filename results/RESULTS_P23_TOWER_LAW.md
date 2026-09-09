# P23, the escape count derived: light-ring anharmonicity of the pure vortex; the analytic arrival law as a predictor in Kerr (verdicts 2026-09-09)

Preregistration: `FROZEN_P23_TOWER_LAW.md` (commit e6a055e). Scripts:
`p23_tower_law.py` (exact scaled towers at |m| = 8, 9, 10 and the
Iyer-Will comparison), `p23_action_wkb.py` (uniform first-order WKB
with the exact barrier action), `p23_kerr_extrap.py` and
`p23_kerr_extrap_fit.py` (Kerr blind extrapolation). Data:
`p23_tower_law_m-8.json`, `..._m-9.json`, `..._m-10.json`,
`p23_tower_law.json`, `p23_action_wkb.json`, `p23_kerr_extrap.json`.

## Summary

The number of counter-rotating overtones of the draining vortex that
escape absorption by the branch cut, measured as 1, 2, 2, 3, 4, 5 for
|m| = 1..6 (P21d-h) and 6, 7, 8 for |m| = 8, 9, 10 (this cycle), is derived. The
escaping modes are the light-ring resonances of the pure vortex
(P21f), and their real parts obey

    Re c_n(m) = |m|/4 - (3/8) (n + 1/2)^2 / |m| + O(1/|m|),

where |m|/4 is the light-ring frequency and the second term is the
anharmonicity of the light-ring barrier: the barrier action of the
scaled equation expands as J(gamma) = 2 pi h + 3 pi h^2 + O(h^3) in
h = 1/4 - gamma (the coefficient 3 pi verified to 2e-6), and the
Bohr-Sommerfeld condition |m| J(gamma_n) = i pi (n + 1/2) gives the
formula. With the full action the crossing Re c = 0 happens at
n + 1/2 = kappa |m| with kappa = 0.8008 (quadratic
truncation: sqrt(2/3) = 0.8165; the empirical fit of P21: 0.808), so

    N(m) = floor(kappa |m| + 1/2),

about four fifths of |m|, NOT |m| - 1. The uniform WKB tower
reproduces every exact tower member for |m| = 2..7 within 0.075 and
the count for every |m| tested. In Kerr, the analytic arrival law of
P22 works as a blind predictor: a cubic fitted to points with
0.01 <= Re(omega M) <= 0.04 predicts the death spin of {2,0,10_0},
{2,0,11_0}, {2,-2,14_0} to 6e-5, 4.5e-4, 5.8e-5 while the
fold model misses by 5e-3 to 7e-3.

## Verdict table

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P23.1 counts N(9) = 7, N(10) = 8; N(8) in {6, 7} with Re c_6(8) in [-0.17, 0.13]; members within 0.15 of the law | KILL: N(9) = 8 or N(10) = 9, or a member off by > 0.15 | N(8) = 6, N(9) = 7, N(10) = 8 (complex-ray solver, every member verified at two ray angles and two matching points); Re c_6(8) = -0.0604 (frozen window [-0.17, 0.13]); largest deviation from the law for n <= N-2: 2: 0.001, 3: 0.000, 4: 0.001, 5: 0.002, 6: 0.003, 7: 0.005, 8: 0.005, 9: 0.006, 10: 0.007; Im c_n within 0.12 of -(2n+1)/4 for n <= N-3 EXCEPT |m| = 10, n = 5 (Im -2.5949, off by 0.155): the damping clause of the prediction misses there by 0.035 (the -(2n+1)/4 law is the leading order; the anharmonic correction to Im grows as alpha^3/m^2 and is not in the frozen law) | CONFIRMED on the counts and on Re c_n (the |m| - 1 reading dies at |m| = 9 and 10); the damping sub-clause misses at one member |
| P23.1b second-order WKB reproduces the (n+1/2)^2/|m| term with k0 = 0.38 +- 0.10, right sign, members within 0.15 for |m| >= 5 | KILL: no such term, wrong sign, or third order needed | barrier action J = 2 pi h + 3 pi h^2: k0 = 3/8 = 0.375 exactly at this order (empirical 0.383); uniform first-order WKB with the full action reproduces the exact tower within 0.075 for |m| = 2..7 (n = 0..N-1) and gives the exact counts 2, 2, 3, 4, 5, 6; the Iyer-Will barrier-top expansion, typed from memory, produced the WRONG sign for the (n+1/2)^2 term at |m| = 20, 40 and failed to converge for n >= 1 at |m| <= 10: discarded as an unverified implementation (recorded in `p23_tower_law_wkb.log`); the derivation stands on the exact action, whose h^2 coefficient is the same second-order anharmonic content | CONFIRMED (the term is the light-ring anharmonicity; derived, not fitted) |
| P23.2 cubic from Re in [0.01, 0.04] predicts a_0 within 1.5e-3 and Im within 3e-3; fold misses by > 3e-3 | KILL: cubic off > 3e-3, or fold within 1.5e-3 | {2,0,10_0}: cubic 0.39144 vs deep 0.39138 (err +5.6e-5; Cook-Zalutskiy 0.391144), fold 0.38578 (err -5.6e-3), Im -2.4979 vs -2.4996 (1.7e-3); {2,0,11_0}: cubic 0.43844 vs deep 0.43888 (err -4.5e-4; C-Z 0.438874), fold 0.43181 (err -7.1e-3), Im -2.7466 vs -2.7497 (3.0e-3, at the edge of the window); {2,-2,14_0}: cubic 0.61211 vs deep 0.61206 (err +5.8e-5; C-Z 0.611751), fold 0.60695 (err -5.1e-3), Im -3.6147 vs -3.6145 (1.4e-4) | CONFIRMED (a_0 to 5e-4 or better from data a full 0.01 to 0.04 away in Re; the fold model fails on all three) |
| P23.3 Kerr has three fates, the vortex two | recorded | l = 2, m = 0, n = 0..6 are damped modes at a = 0.9999 (cached qnm tables); n >= 8 die on the axis; the collapsing family is born on the axis (P22) | recorded |

## The derivation

Scaled equation (P21f), m < 0, |m| written for -m:

    H'' + Q H = 0,   Q = (c + |m|/rho^2)^2 - (m^2 - 1/4)/rho^2
                       = m^2 [ (gamma + 1/rho^2)^2 - (1 - 1/(4 m^2))/rho^2 ],   gamma = c/|m|.

For real gamma < 1/4 the bracket q(rho; gamma) is negative on
(rho_-, rho_+) with rho_+- = [1 -+ sqrt(1 - 4 gamma)]/(2 gamma): a
barrier between the vortex core (rho < rho_-, oscillatory, where the
admissible solution rho^{1/2} e^{+i|m|/rho} carries flux inward, the
analogue of the horizon condition) and the outer region (outgoing
e^{i c rho}). The barrier top is the light ring, rho = 2 at
gamma = 1/4, where q = q_rho = 0 and q_rho_rho = 1/8. The exact action

    J(gamma) = int_{rho_-}^{rho_+} sqrt(-q) d rho
             = sqrt(gamma) (rho_+ - rho_-)^2 int_0^1 sqrt(t(1-t)) sqrt(gamma rho^2 + rho + 1) / rho^2 dt

(rho = rho_- + t (rho_+ - rho_-)) is analytic in gamma near 1/4 and
expands as J = 2 pi h + 3 pi h^2 + O(h^3), h = 1/4 - gamma: the
2 pi h is the parabolic barrier (pi q_gamma h / sqrt(q_rho_rho / 2)
with q_gamma = 1), the 3 pi h^2 its first anharmonic correction,
computed numerically to (J - 2 pi h)/h^2 -> 2.999998 pi. The
Bohr-Sommerfeld (Gamow) condition for the barrier resonances,

    |m| J(gamma_n) = i pi (n + 1/2),

solved order by order in 1/|m| gives, with alpha = n + 1/2,

    h = i alpha/(2|m|) + 3 alpha^2/(8 m^2) + ...,
    c_n = |m| gamma_n = |m|/4 - i alpha/2 - (3/8) alpha^2/|m| + ...

The first two terms are the Schutz-Will light-ring tower (P21h.3:
damping -(2n+1)/4 independent of m); the third is the anharmonic
shift that drives Re c_n through zero. The crossing at the full
action: on gamma = i y the condition needs Re J(i y) = 0, which
holds at y* = -0.3511, giving alpha* = |m| Im J(i y*)/pi =
kappa |m|. The count of escaping modes is the number of n with
n + 1/2 < kappa |m|, kappa = 0.8008: N(m) = 1, 2, 2, 3, 4, 5, 6, 6, 7, 8,
9, 10 for |m| = 1..12. The action-WKB tower itself (the condition
solved with the full action for each n) gives the same counts and,
for |m| = 8, 9, 10, the members

| n | |m| = 8 | |m| = 9 | |m| = 10 |
|---|---|---|---|
| 0 | 1.988-0.250i | 2.240-0.250i | 2.491-0.250i |
| 1 | 1.894-0.745i | 2.156-0.746i | 2.416-0.747i |
| 2 | 1.706-1.227i | 1.989-1.232i | 2.265-1.235i |
| 3 | 1.420-1.687i | 1.735-1.700i | 2.038-1.710i |
| 4 | 1.034-2.115i | 1.395-2.143i | 1.732-2.164i |
| 5 | 0.543-2.502i | 0.963-2.555i | 1.346-2.592i |
| 6 | -0.062-2.838i | 0.435-2.926i | 0.877-2.988i |
| 7 | -0.789-3.116i | -0.196-3.250i | 0.319-3.346i |
| 8 | | -0.937-3.521i | -0.333-3.660i |

(at |m| = 8 the seventh member sits 0.06 below the axis, inside the
WKB error of 0.075 seen at |m| = 7: the exact tower decides N(8)).

Three remarks. (0) The frozen law's k0 = 0.383 was fitted to the
real-axis towers; with the corrected deep members the exact Re c_n
follow the 3/8 law to <= 0.007 for n <= N - 2 at every |m| tested
(table below). (i) The rule "escape iff Re c_n > 0" (P21h) plus this
formula makes the escape count a property of the light ring of the
pure vortex alone: the finite-B overtone n escapes if and only if the
n-th light-ring resonance of the B -> infinity problem has not yet
been pushed across the imaginary axis by its own anharmonic shift.
(ii) The O(1/|m|) constant of the empirical fit (k1 = -0.033) is of
the size of the (m^2 - 1/4) versus m^2 difference and of the next
WKB order; it is not needed for any count except at borderline
values of kappa |m| + 1/2, where the exact tower decides (|m| = 8).

## Towers at |m| = 2..10 and the instrument change

The real-axis scaled solver of P21f-h (inner solution integrated
outward from rho_min on the real axis) failed at |m| >= 8: the inner
condition selects the branch rho^{1/2} exp(+i|m|/rho), which on the
real axis has the same modulus as the other branch near rho = 0 and is
SUBDOMINANT by exp(2 |Im c| rho_m) at the matching point, so
integration error is amplified and the deep members become
cutoff-sensitive (the P21h "0.04 sensitivity" was this; at |m| = 8 the
re-solves from perturbed settings hopped to neighbouring members or
diverged). The fix (`dbt_scaled.wronskian_cplx`, this cycle) integrates
the inner solution along the ray rho = r e^{-i theta}, on which the
physical branch has modulus exp(-|m| sin(theta)/r) and is the GROWING
one in the direction of integration, then along the arc back to the
real matching point (the arc's first-derivative term from the
non-constant d rho/dt was the last defect found; with it the roots are
invariant to theta = 0.3..0.8, rho_min = 0.01..0.02 and rho_m = 0.7..1.0
to five decimals). Low members are unchanged (m = -4, n = 0:
0.98416 -> 0.98420); deep members move by up to 0.07
(m = -7, n = 5: 0.1425-2.4185i -> 0.0696-2.4303i, which the action-WKB
had put at 0.0681-2.4245i). No count for |m| <= 7 changes.


Complex-ray solver (`dbt_scaled.wronskian_cplx`), every root verified at theta = 0.5 / 0.8 and rho_m = 1.0 / 0.7 (spread <= 2e-7). Columns: exact c_n; action-WKB (full barrier action); the frozen empirical law |m|/4 - [0.383 (n+1/2)^2 - 0.033]/|m|; old real-axis value where one existed (P21f-h).

| m | n | exact c_n | action-WKB | dev | law Re | old real-axis |
|---|---|---|---|---|---|---|
| -2 | 0 | 0.4675-0.2536i | 0.4530-0.2471i | 0.0159 | +0.469 | 0.4667-0.2536i |
| -2 | 1 | 0.0707-0.6887i | 0.0638-0.6692i | 0.0206 | +0.086 | 0.0721-0.6872i |
| -2 | 2 | -0.8207-0.9135i | -0.8107-0.8805i | 0.0345 | -0.680 |  |
| -3 | 0 | 0.7288-0.2517i | 0.7187-0.2487i | 0.0105 | +0.729 | 0.7292-0.2512i |
| -3 | 1 | 0.4726-0.7233i | 0.4648-0.7145i | 0.0117 | +0.474 | 0.4731-0.7253i |
| -3 | 2 | -0.0623-1.0977i | -0.0652-1.0833i | 0.0147 | -0.037 |  |
| -3 | 3 | -0.9385-1.3148i | -0.9336-1.2951i | 0.0203 | -0.803 |  |
| -4 | 0 | 0.9842-0.2510i | 0.9765-0.2493i | 0.0078 | +0.984 | 0.9842-0.2515i |
| -4 | 1 | 0.7941-0.7351i | 0.7875-0.7301i | 0.0083 | +0.793 | 0.7921-0.7340i |
| -4 | 2 | 0.4054-1.1652i | 0.4008-1.1570i | 0.0094 | +0.410 | 0.4099-1.1623i |
| -4 | 3 | -0.2030-1.5037i | -0.2045-1.4925i | 0.0113 | -0.165 |  |
| -4 | 4 | -1.0736-1.7185i | -1.0707-1.7045i | 0.0143 | -0.931 |  |
| -5 | 0 | 1.2374-0.2506i | 1.2312-0.2495i | 0.0063 | +1.237 | 1.2372-0.2502i |
| -5 | 1 | 1.0861-0.7405i | 1.0804-0.7373i | 0.0065 | +1.084 | 1.0885-0.7399i |
| -5 | 2 | 0.7793-1.1961i | 0.7747-1.1908i | 0.0070 | +0.778 | 0.7785-1.2031i |
| -5 | 3 | 0.3075-1.5934i | 0.3046-1.5861i | 0.0079 | +0.318 | 0.2963-1.5861i |
| -5 | 4 | -0.3472-1.9087i | -0.3480-1.8995i | 0.0092 | -0.295 |  |
| -5 | 5 | -1.2152-2.1226i | -1.2132-2.1116i | 0.0111 | -1.061 |  |
| -6 | 0 | 1.4895-0.2504i | 1.4844-0.2497i | 0.0052 | +1.490 | 1.4899-0.2506i |
| -6 | 1 | 1.3638-0.7434i | 1.3589-0.7412i | 0.0054 | +1.362 | 1.3622-0.7457i |
| -6 | 2 | 1.1099-1.2127i | 1.1057-1.2090i | 0.0056 | +1.107 | 1.1047-1.2051i |
| -6 | 3 | 0.7229-1.6419i | 0.7195-1.6367i | 0.0061 | +0.724 | 0.7414-1.6375i |
| -6 | 4 | 0.1934-2.0142i | 0.1913-2.0077i | 0.0068 | +0.213 | 0.1899-2.0450i |
| -6 | 5 | -0.4933-2.3133i | -0.4938-2.3055i | 0.0078 | -0.425 |  |
| -6 | 6 | -1.3599-2.5267i | -1.3584-2.5177i | 0.0091 | -1.191 |  |
| -7 | 0 | 1.7410-0.2503i | 1.7366-0.2498i | 0.0045 | +1.741 | 1.7407-0.2504i |
| -7 | 1 | 1.6334-0.7452i | 1.6292-0.7435i | 0.0046 | +1.632 | 1.6333-0.7423i |
| -7 | 2 | 1.4167-1.2227i | 1.4129-1.2199i | 0.0047 | +1.413 | 1.4274-1.2249i |
| -7 | 3 | 1.0879-1.6709i | 1.0846-1.6671i | 0.0050 | +1.084 | 1.0752-1.6969i |
| -7 | 4 | 0.6416-2.0775i | 0.6391-2.0727i | 0.0054 | +0.647 | 0.6060-2.0305i |
| -7 | 5 | 0.0696-2.4303i | 0.0681-2.4245i | 0.0060 | +0.100 | 0.1425-2.4185i |
| -7 | 6 | -0.6405-2.7176i | -0.6408-2.7109i | 0.0067 | -0.557 |  |
| -8 | 0 | 1.9922-0.2502i | 1.9883-0.2498i | 0.0039 | +1.992 |  |
| -8 | 1 | 1.8981-0.7463i | 1.8943-0.7450i | 0.0040 | +1.896 |  |
| -8 | 2 | 1.7090-1.2291i | 1.7055-1.2270i | 0.0041 | +1.705 |  |
| -8 | 3 | 1.4229-1.6896i | 1.4198-1.6867i | 0.0043 | +1.418 |  |
| -8 | 4 | 1.0364-2.1185i | 1.0338-2.1147i | 0.0045 | +1.035 |  |
| -8 | 5 | 0.5444-2.5062i | 0.5425-2.5017i | 0.0049 | +0.556 |  |
| -8 | 6 | -0.0604-2.8435i | -0.0615-2.8383i | 0.0054 | -0.019 |  |
| -8 | 7 | -0.7885-3.1218i | -0.7886-3.1158i | 0.0059 | -0.689 |  |
| -9 | 0 | 2.2430-0.2502i | 2.2396-0.2499i | 0.0035 | +2.243 |  |
| -9 | 1 | 2.1595-0.7471i | 2.1561-0.7461i | 0.0035 | +2.158 |  |
| -9 | 2 | 1.9917-1.2335i | 1.9885-1.2319i | 0.0036 | +1.988 |  |
| -9 | 3 | 1.7383-1.7024i | 1.7354-1.7000i | 0.0037 | +1.732 |  |
| -9 | 4 | 1.3971-2.1463i | 1.3945-2.1434i | 0.0039 | +1.392 |  |
| -9 | 5 | 0.9646-2.5580i | 0.9625-2.5545i | 0.0041 | +0.966 |  |
| -9 | 6 | 0.4362-2.9299i | 0.4347-2.9257i | 0.0045 | +0.456 |  |
| -9 | 7 | -0.1947-3.2547i | -0.1956-3.2500i | 0.0048 | -0.140 |  |
| -9 | 8 | -0.9369-3.5259i | -0.9370-3.5206i | 0.0053 | -0.821 |  |
| -10 | 0 | 2.4937-0.2502i | 2.4906-0.2499i | 0.0031 | +2.494 |  |
| -10 | 1 | 2.4186-0.7476i | 2.4155-0.7468i | 0.0032 | +2.417 |  |
| -10 | 2 | 2.2678-1.2367i | 2.2648-1.2353i | 0.0032 | +2.264 |  |
| -10 | 3 | 2.0403-1.7115i | 2.0376-1.7096i | 0.0033 | +2.034 |  |
| -10 | 4 | 1.7346-2.1662i | 1.7322-2.1638i | 0.0034 | +1.728 |  |
| -10 | 5 | 1.3484-2.5949i | 1.3463-2.5920i | 0.0036 | +1.345 |  |
| -10 | 6 | 0.8783-2.9915i | 0.8766-2.9881i | 0.0038 | +0.885 |  |
| -10 | 7 | 0.3201-3.3500i | 0.3189-3.3461i | 0.0041 | +0.349 |  |
| -10 | 8 | -0.3321-3.6645i | -0.3327-3.6601i | 0.0044 | -0.264 |  |
| -10 | 9 | -1.0857-3.9299i | -1.0858-3.9251i | 0.0048 | -0.953 |  |

Counts N(m) (members with Re c > 0): |m| = 2: 2, |m| = 3: 2, |m| = 4: 3, |m| = 5: 4, |m| = 6: 5, |m| = 7: 6, |m| = 8: 6, |m| = 9: 7, |m| = 10: 8. Largest deviation of Re c_n from the frozen law for n <= N - 2: 2: 0.001, 3: 0.000, 4: 0.001, 5: 0.002, 6: 0.003, 7: 0.005, 8: 0.005, 9: 0.006, 10: 0.007.

## Beyond the freeze: |m| = 12 and 15 (recorded after the freeze)

kappa |m| + 1/2 = 10.11 and 12.51; the law predicts N = 10 and 12, the
second a borderline case. Action-WKB tower and the exact members near
the crossing (complex-ray solver, ray angles 0.4 / 0.5 / 0.8 agreeing
to 1e-5; the rho_m = 0.7 setting no longer converges at these |m|):

| m | n | action-WKB | exact |
|---|---|---|---|
| -12 | 7 | 1.2025-3.4709i | 1.2040-3.4737i |
| -12 | 8 | 0.6748-3.8424i | 0.6760-3.8454i |
| -12 | 9 | 0.0710-4.1791i | 0.0719-4.1825i |
| -12 | 10 | -0.6134-4.4774i | -0.6130-4.4811i |
| -15 | 10 | 0.9137-4.7584i | 0.9146-4.7608i |
| -15 | 11 | 0.3255-5.1024i | 0.3263-5.1051i |
| -15 | 12 | -0.3260-5.4166i | -0.3255-5.4194i |

N(12) = 10 and N(15) = 12 (`p23_tower_ext.json`), the action-WKB
within 0.004 of the exact members even at the crossing. The count law
now stands at |m| = 1..10, 12, 15; the only reading that survives is
kappa = 0.8008 from the light-ring action.

## Kerr: the blind extrapolation

Blind fits use only the deep-converged points with
0.01 <= Re(omega M) <= 0.04 (window densified to a spacing of 0.0025
in spin); the deep endpoint is the linear extrapolation of the last
two deep-converged points below Re = 0.01 (caps to 4e6), computed
after the fits were written to disk.

| sequence | window | cubic a_0 (c_1, c_2, c_3; rms) | fold a_0 (rms) | deep a_0 | Cook-Zalutskiy | cubic / fold error vs deep | Im at a_0: cubic / deep / C-Z |
|---|---|---|---|---|---|---|---|
| {2,0,10_0} | 14 pts, a in [0.3500, 0.3825], Re in [0.0129, 0.0395] | 0.39144 (1.645, -23.6, 166; 1.6e-5) | 0.38578 (8.7e-6) | 0.39138 (last Re 0.0039) | 0.391144 | +5.6e-5 / -5.6e-3 | -2.4979 / -2.4996 / -2.5 |
| {2,0,11_0} | 13 pts, a in [0.4000, 0.4300], Re in [0.0116, 0.0385] | 0.43844 (1.510, -16.7, 90; 3.5e-6) | 0.43181 (2.2e-5) | 0.43888 (last Re 0.0033) | 0.438874 | -4.5e-4 / -7.1e-3 | -2.7466 / -2.7496 / -2.75 |
| {2,-2,14_0} | 11 pts, a in [0.5800, 0.6050], Re in [0.0121, 0.0384] | 0.61211 (1.909, -30.9, 272; 1.3e-5) | 0.60695 (1.9e-5) | 0.61206 (last Re 0.0056) | 0.611751 | +5.8e-5 / -5.1e-3 | -3.6147 / -3.6145 / -3.61439 |

The fold model fits the window points about as well as the cubic
(rms 1e-5 to 2e-5 on both: the window alone cannot tell the shapes
apart) but extrapolates to a death spin 5e-3 to 7e-3 too early in
all three cases; the cubic lands within 5e-4 of the deep endpoint
and within 5e-4 of Cook-Zalutskiy's value. The coefficients repeat
the P22 pattern (c_1 = 1.5 to 1.9, c_2/c_1 = -11 to -16 per unit
spin). Note the instrument change recorded before any endpoint was
read: the 48000-cap gate of the main P22 run fails at
Re(omega M) = 0.03 to 0.07 for these overtones (n >= 10), so the
tracks used the deep caps throughout (`p23_kerr_extrap.py`, patched
before the fits), and the window had to be densified
(`p23_kerr_extrap_fit.py`) because a 0.01 spin step leaves only 2-3
points inside it.

## What the laboratory can test, and why the 2020 Nottingham data cannot yet

At strong rotation (B/A >> 1) the draining vortex rings, in the
counter-rotating sector, with N(m) = floor(0.8008 |m| + 1/2) modes per
azimuthal number, with damping rates (2n + 1)/(4 B) independent of m
and frequencies [|m|/4 - (3/8)(n + 1/2)^2/|m|]/B (B = C/c_s in units of
the sound-horizon radius; in physical units multiply by c_s^2/C). For
the m = -2 sector this is two modes (n = 0, 1) with damping ratio
1 : 3 and frequencies 0.467 c_s^2/C and 0.071 c_s^2/C, the second nearly
non-propagating. A measurement of the number of counter-rotating
ringdown modes at high rotation, or of their damping ratio 1 : 3 : 5,
tests the light-ring picture directly.

Torres, Patrick, Richartz and Weinfurtner (PRL 125, 011301, 2020)
measured exactly the pure-vortex counter-rotating spectrum (circulation
C = 151 cm^2/s, drain D = 0, the first 25 counter-rotating modes,
one peak frequency per m, no damping rates). Their data are NOT a test
of this tower: with water depth h = 5.55 cm the light ring of the
non-dispersive model sits at r = 2 C / c_s = 4.1 cm (c_s = sqrt(g h) =
74 cm/s), where k h = |m| h / r = 1.35 |m| >> 1 for every m, i.e. deep
water, and the frequencies are set by the gravity-capillary dispersion
they modelled (their light-ring frequencies grow at about 0.17 Hz per
unit |m|, against 1.43 Hz per unit |m| for the shallow-water tower).
The non-dispersive regime needs k h << 1 at the light ring, i.e.
h << 2 C / (|m| c_s); with C = 1000 cm^2/s and h = 2 cm one gets
r = 45 cm and k h = 0.044 |m|, shallow for |m| <= 5, in a tank of the
Nottingham size. One caveat on the inner boundary: the tower's inner condition
(flux into the core, the horizon condition of the draining bathtub
pushed to rho -> 0 in the B/A -> infinity limit) requires a drain; a
vortex whose core reflects rather than absorbs would ring with a
different counter-rotating spectrum, so the experiment needs the
surface drain that Torres et al. found negligible in their flow.
That is the experiment the tower predicts: N(m) =
1, 2, 2, 3, 4 counter-rotating modes for |m| = 1..5 with damping
rates in the ratio 1 : 3 : 5 : ... and the fundamental at
f_0 = |m| c_s^2 / (8 pi C) (0.62 |m| Hz for those parameters).

## Theory addendum (2026-09-10): the action in closed form and the analytic tower

The symbolic expansion of the barrier action about the light ring
(`p23_action_series.py`, x-series to order 10, turning points as
series in h, the smooth part of the integrand integrated in the
angle variable) gives

    J(h)/(pi h) = 2 + 3 h + (15/2) h^2 + (175/8) h^3 + (2205/32) h^4 + ...,

which is, term by term, 2 * 2F1(1/2, 3/2; 2; 4h). With
2F1(1/2, 3/2; 2; z) = (4/(pi z)) [K - E] at parameter z, this is the
identity

    J(gamma) = 2 [ K(k) - E(k) ],   k^2 = 1 - 4 gamma,

verified against the quadrature to 1e-31 at real and complex gamma.
The pure-vortex tower is therefore the solution set of a closed
transcendental equation in complete elliptic integrals,

    |m| * 2 [ K(k_n) - E(k_n) ] = i pi (n + 1/2),   k_n^2 = 1 - 4 c_n / |m|,

whose roots reproduce the exact members within the first-order WKB
accuracy (m = -7, n = 5: 0.0681 - 2.4245i against 0.0696 - 2.4303i;
m = -10, n = 7: 0.3189 - 3.3461i against 0.3201 - 3.3500i). Inverting
the series order by order,

    c_n(m) = |m|/4 - i a/2 - (3/8) a^2/|m| + (3i/32) a^3/m^2
             - (5/256) a^4/|m|^3 + (9i/2048) a^5/m^4 + ...,   a = n + 1/2,

(plus an O(1/|m|) constant k_1 = +0.031 from the (m^2 - 1/4) term
and the next WKB order, fitted on the n = 0 members). The third term
is the anharmonic shift that decides the count; the fourth explains
the damping drift that the P23.1 freeze had recorded as a miss: at
m = -10, n = 5 it gives Im c = -2.75 + 0.156 = -2.594 against the
exact -2.5949, and across the towers the imaginary parts of all
members with Re c > 0 at |m| >= 5 are reproduced to 0.003. The real
parts of the last member before the crossing are 0.02 to 0.07 below
the truncated series (the expansion parameter a/|m| is 0.8 there);
the elliptic form has no such limitation.

The crossing constant is the root of Re[K(k) - E(k)] = 0 on the line
k^2 = 1 - 4 i y:

    y* = -0.35114692526,   kappa = (2/pi) Im[K - E](k*) = 0.80080533966,

against 0.8165 from the a^2 truncation and 0.8031 from the a^4
truncation. The escape count of the draining vortex is thus

    N(m) = floor( 0.80080533966 |m| + 1/2 ),

with every case measured (|m| = 1..10, 12, 15; finite-B for |m| <= 7)
in agreement.

## The O(1/|m|) constant k_1 (addendum, 2026-09-10; `results/p23_k1_split.json`)

The exact towers exceed the leading elliptic condition by
|m| (c_exact - c_WKB1) = +0.0306, +0.0310, +0.0311, +0.0311 at n = 0
for |m| = 4, 6, 8, 10 (imaginary part -0.007 -> -0.003): k_1 = 0.031.
Two contributions separate cleanly:

- First-order WKB with the EXACT potential, (m^2 - 1/4)/rho^2 instead
  of m^2/rho^2 (turning points in closed form,
  rho_+- = [sqrt(m^2 - 1/4) -+ sqrt(m^2 - 1/4 - 4 c |m|)] / (2c)),
  shifts the tower by -0.0625/|m| = -1/(16 |m|), the same at every
  |m| and n to four digits.
- The remainder, the genuine second-order WKB correction, is
  +0.0931, +0.0935, +0.0936, +0.0936 per |m| at n = 0 (|m| = 4..10),
  extrapolating in 1/m^2 to 0.09370, i.e. 3/32 = 0.09375 to 5e-5, with
  a weak n-dependence (0.0917 at n = 2, |m| = 10) that vanishes as |m|
  grows.

So k_1 = -1/16 + 3/32 = 1/32 = 0.03125 (measured 0.0311), and the
analytic tower reads

    c_n(m) = |m|/4 - i a/2 - (3/8) a^2/|m| + 1/(32 |m|) + (3i/32) a^3/m^2 + ...

The value 3/32 for the second-order term is a numerical identification
(four digits, one free constant), not a derivation; the Dunham
second-order integral for this potential is the open item.

Large-|m| check of the 3/32 (`p23_k1_large_m.py`, `p23_k1_large_m.json`):
second-order part 0.09370, 0.09372, 0.09374 at |m| = 15, 20, 30 (n = 0),
the deficit to 3/32 falling as 1/m^2 (0.011, 0.012, 0.009 in units of
1/m^2); |m| = 40 is beyond the complex-ray solver. k_1 = 1/32 stands
at 1e-5.
