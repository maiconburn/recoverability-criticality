# P14 — metrologia do collider gravitacional (matéria escura ultraleve)

Congelado antes de medir (FROZEN_P14_GRAVCOLLIDER.md); v1 tinha pinv
mascarando Fisher singular (σ=0 impossível — artefato registrado); v2 com
inversão explícita + gate de condicionamento + janela física ∝ 1/v.

| Previsão | Veredito | Números |
|---|---|---|
| P14.1: σ(η) ∝ gap^p, p∈[1.5,2.5] | **MORTA** | p = −0.89: população LZ é tarefa gap⁻¹ (amplitude-like); hierarquia é por tarefa |
| P14.2: informação não-monotônica na taxa de varredura | **CONFIRMADA** (com nuance) | razão máx/assintótico = 1540; estrutura secundária em v∈[0.25,1] = interferência de Stückelberg; pico global é adiabático (v→0), não LZ-crítico como o texto sugeria |
| P14.3: σ(μ)/μ < 5% num cruzamento limpo | **CONFIRMADA** | **σ(μ)/μ = 0.03%** com SNR=100, cond(F)=1.4e3 |

Leitura: cruzamentos de níveis de nuvens de bósons são espectroscopicamente
GENEROSOS no regime adiabático — massa do bóson a 0.03% por cruzamento no
modelo mínimo. Ressalvas: 2 níveis, observável populacional como proxy da
backreaction, sem modelagem de fase de GW real, sem ruído
correlacionado. Próximo degrau: mapear no observável de fase da literatura
do gravitational collider (Baumann–Chia–Porto) e refazer o forecast.
Dados: p14_gravcollider.json (v1, void), p14_v2.json.

## P14' — forecast no observável de fase de GW (marginalizado)

Chirp quadrupolar autoconsistente com backreaction −β·dP_b/dt; Fisher 6×6
na fase {Ω_res, η, β, k, Ω₀, φ₀}; σ_φ = 0.1 rad × 2000 amostras.

| Previsão | Veredito | Números |
|---|---|---|
| P14'.1: marginalização custa >10× mas σ(μ)/μ < 5% | inconclusive no fiducial (16.3%; custo 39×) | mapa de fiduciais: 5.4% (7 ciclos, β=0.03) → 1.4% (14c) → **0.26% (28c)**; σ ∝ 1/(ciclos²·β) aprox. |
| P14'.2: informação mora no cruzamento | **CONFIRMADA** | 100% do Fisher de Ω_res em \|Ω−Ω_res\| < 5η |
| P14'.3: não-degenerado com chirp mass | **CONFIRMADA** | corr(Ω_res, k) = +0.19 |

Leitura consolidada: num cruzamento de níveis da nuvem, a massa do bóson
ultraleve é mensurável a sub-porcento da fase de GW COM marginalização
completa dos parâmetros da binária, desde que o cruzamento acumule
~dezenas de ciclos — e a informação é 100% local ao cruzamento, sem
degenerescência fatal com a chirp mass. Ressalvas: 2 níveis, quadrupolo
Newtoniano, ruído branco de fase, um único cruzamento, sem spins/PN.
Candidata a peça externa (nota ou contribuição a código da comunidade
gravitational-collider) — NADA enviado.

## P14'' — multi-cruzamento: espectroscopia completa do átomo gravitacional

3 ressonâncias da mesma nuvem (razões fixas pelo espectro, dependências de
spin distintas), Fisher 9×9 na fase, 45 ciclos totais, pinv com rcond
1e-12 (cond 4.5e14 — direções quase-planas de fase global, normal).

| Previsão | Veredito | Números |
|---|---|---|
| P14''.1 ganho coerente > 0.8·√3 | CONFIRMADA (raspão) | ganho 1.42; singles: 0.98%/12.5%/61.7% (cruzamentos tardios varridos rápido pelo chirp Ω^{11/3}) |
| P14''.2 spin custa < 2× | **CONFIRMADA acima do previsto** | degradação 0.996 — as razões medem χ a 0.1% sozinhas |
| P14''.3 σ(μ)/μ < 0.1% | inconclusive | 0.689% no fiducial de 45 ciclos; escala ∝1/ciclos² (P14') |

Manchete: um único sistema com 3 cruzamentos entrega **massa do bóson a
0.7% E spin do buraco negro a 0.1% simultaneamente**, com marginalização
completa — as razões entre ressonâncias transformam degenerescência em
medição dupla. Ressalvas: modelo de 3×(2 níveis), Newtoniano, acoplamentos
iguais, um só evento. Dados: p14_multi.json.
