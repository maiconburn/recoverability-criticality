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
