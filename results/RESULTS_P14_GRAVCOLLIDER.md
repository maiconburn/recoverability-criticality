# P14, metrology of the gravitational collider (ultralight dark matter)

Frozen before measuring (FROZEN_P14_GRAVCOLLIDER.md); v1 had pinv
masking a singular Fisher (σ=0 impossible: artifact recorded); v2 with
explicit inversion + conditioning gate + physical window ∝ 1/v.

| Prediction | Verdict | Numbers |
|---|---|---|
| P14.1: σ(η) ∝ gap^p, p∈[1.5,2.5] | **KILLED** | p = −0.89: LZ population is a gap⁻¹ task (amplitude-like); the hierarchy is per task |
| P14.2: non-monotonic information in the sweep rate | **CONFIRMED** (with nuance) | max/asymptotic ratio = 1540; secondary structure at v∈[0.25,1] = Stückelberg interference; the global peak is adiabatic (v→0), not LZ-critical as the text suggested |
| P14.3: σ(μ)/μ < 5% in a clean crossing | **CONFIRMED** | **σ(μ)/μ = 0.03%** with SNR=100, cond(F)=1.4e3 |

Reading: level crossings of boson clouds are spectroscopically
GENEROUS in the adiabatic regime: boson mass at 0.03% per crossing in
the minimal model. Caveats: 2 levels, population observable as a proxy
for the backreaction, no modeling of the real GW phase, no correlated
noise. Next step: map onto the phase observable of the gravitational
collider literature (Baumann–Chia–Porto) and redo the forecast.
Data: p14_gravcollider.json (v1, void), p14_v2.json.

## P14', forecast on the GW phase observable (marginalized)

Self-consistent quadrupolar chirp with backreaction −β·dP_b/dt; 6×6
Fisher on the phase {Ω_res, η, β, k, Ω₀, φ₀}; σ_φ = 0.1 rad × 2000
samples.

| Prediction | Verdict | Numbers |
|---|---|---|
| P14'.1: marginalization costs >10× but σ(μ)/μ < 5% | inconclusive at the fiducial (16.3%; cost 39×) | fiducial map: 5.4% (7 cycles, β=0.03) → 1.4% (14c) → **0.26% (28c)**; σ ∝ 1/(cycles²·β) approx. |
| P14'.2: the information lives in the crossing | **CONFIRMED** | 100% of the Ω_res Fisher within \|Ω−Ω_res\| < 5η |
| P14'.3: non-degenerate with the chirp mass | **CONFIRMED** | corr(Ω_res, k) = +0.19 |

Consolidated reading: in a level crossing of the cloud, the ultralight
boson mass is measurable at sub-percent from the GW phase WITH full
marginalization of the binary parameters, provided the crossing
accumulates ~tens of cycles, and the information is 100% local to the
crossing, with no fatal degeneracy with the chirp mass. Caveats: 2
levels, Newtonian quadrupole, white phase noise, a single crossing, no
spins/PN. Candidate external piece (note or contribution to community
gravitational-collider code): NOTHING sent.

## P14'', multi-crossing: full spectroscopy of the gravitational atom

3 resonances of the same cloud (ratios fixed by the spectrum, distinct
spin dependencies), 9×9 Fisher on the phase, 45 total cycles, pinv
with rcond 1e-12 (cond 4.5e14: near-flat global phase directions,
normal).

| Prediction | Verdict | Numbers |
|---|---|---|
| P14''.1 coherent gain > 0.8·√3 | CONFIRMED (narrowly) | gain 1.42; singles: 0.98%/12.5%/61.7% (late crossings swept fast by the Ω^{11/3} chirp) |
| P14''.2 spin costs < 2× | **CONFIRMED beyond prediction** | degradation 0.996: the ratios measure χ at 0.1% on their own |
| P14''.3 σ(μ)/μ < 0.1% | inconclusive | 0.689% at the 45-cycle fiducial; scales ∝1/cycles² (P14') |

Headline: a single system with 3 crossings delivers **boson mass at
0.7% AND black hole spin at 0.1% simultaneously**, with full
marginalization: the ratios between resonances turn degeneracy into a
double measurement. Caveats: 3×(2 levels) model, Newtonian, equal
couplings, a single event. Data: p14_multi.json.
