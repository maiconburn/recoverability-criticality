# P15, the hierarchy at order N (frozen before; synthetic confirmed)

## P15.1 CONFIRMED: the cluster ladder {p−1, 2p−2, 2p−1}

Synthetic EP-3 (cubic Puiseux pattern, 60-digit arithmetic with a
conditioning gate: the v1 in double precision was a pinv floor below
g=0.03, a known house artifact):

| task | predicted (p=3) | final local exponents |
|---|---|---|
| amplitudes, fixed frequencies | 2 | −2.05 → −2.01 |
| worst frequency direction, everything free | 4 | −3.70 → −3.98 |
| amplitude, everything free | 5 | −5.05 → −5.01 |

With the p=2 case already measured in the program (1, 2, 3), the
hierarchy is **{p−1, 2p−2, 2p−1} in the order p of the degeneracy**:
the cost law gains generality in N.

## P15.3 CONFIRMED: coexistence with the response gain
Response of the splitting to the physical parameter: exponent 0.3333
(= 1/3 exact). The "EP-N sensing debate" resolves as in the EP-2: the
response gain ε^{1/N} is real AND the spectral costs of the ladder are
real: they are different TASKS on the same system.

## P15.2, real data: in progress
Cataloged sources: NV EP-3 (Nat. Nanotech 19, 160) and trapped-ion
LEP3 (figshare). Preregistration in FROZEN_P15_EPN.md; window ±0.75.

## P15.2, ion data (LEP3): VOID by design, with a bonus

Public dataset analyzed (figshare 10.6084/m9.figshare.30343429,
CC BY 4.0; 120 bootstrap samples of (α, γ) fits per configuration):
reverse engineering of the configurations shows that ALL of them obey
γ = 4ω/|1 − 2α| (6/6 exact pairs): the experiment sits ON the LEP3
line and sweeps the POSITION along it, never the distance to the EP.
Without a gap sweep, the ladder exponent is not testable: **VOID by
the frozen criterion**, and the P15.2 preregistration remains open for
any laboratory with a transverse sweep (the public prediction:
{2, 4, 5} ± 0.75).

Bonus: the bootstrap σ's vary ~5× along the line (σ_γ: 0.05 → 0.26),
measuring the ANISOTROPY of the estimation cost along an EP-3 line: an
observable our theory does not yet predict; noted as an open question.

Final state of the P15 line: ladder theory at order N CONFIRMED on
high-precision synthetic ({p−1, 2p−2, 2p−1}; locals −2.01/−3.98/−5.01);
response ε^{1/3} exact; the available public data do not test the
ladder because of the experimental design. Data: p15_ep3_v2.json,
p15_lep3_data.json.

## P15.4, Petermann hypothesis: KILLED by the frozen control

corr[ln(σ/γ), ln κ_V] = −0.27 (weak, opposite sign to the prediction);
the frozen scale control fired (pure γ correlates 0.525 > κ_V).
Verdict: CONFOUNDED-BY-SCALE. The anisotropy along the LEP3 line is
dominated, at least in part, by mundane experimental physics (larger
γ = fewer oscillations in the measurement window = worse fit) and by a
systematic difference between the α < ½ and α > ½ branches that local
κ_V does not capture. REFINED open question: separating the confounder
would require the raw records (not the aggregated bootstraps) or data
with window ∝ 1/γ. The "second law" (geometric parallel cost) remains
without a live candidate. Data: p15_4.json.
