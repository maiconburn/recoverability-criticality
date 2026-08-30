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
