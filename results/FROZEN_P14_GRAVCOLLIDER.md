# P14 — collider gravitacional (matéria escura ultraleve) — congelado
# antes de medir, 2026-08-30

Contexto: nuvens de bósons ultraleves (candidatos a matéria escura) em
torno de buracos negros ("átomos gravitacionais") evoluem por
superradiância e atravessam CRUZAMENTOS DE NÍVEIS durante inspirais de
binárias (programa "gravitational collider", Baumann–Chia–Porto). Medir
os parâmetros da nuvem (massa do bóson α = μM, números quânticos) a
partir do sinal de GW perto de um cruzamento é tarefa de estimação
espectral perto de degenerescência — nossa metrologia.

Modelo mínimo congelado: dois níveis da nuvem |a⟩,|b⟩ com energias
E_a(t), E_b(t) varridas linearmente pela frequência orbital Ω(t) da
binária (Landau–Zener): H(t) = [[−Δ(t)/2, η],[η, +Δ(t)/2]],
Δ(t) = c₁(Ω(t) − Ω_res), acoplamento η fixado pela perturbação de maré.
Observável: fase/frequência de GW carregando a "backreaction" da nuvem
(proxy congelado: população transferida P_LZ e sua derivada em relação
aos parâmetros). Parâmetros a estimar: (η, Ω_res) de um registro com
ruído branco na fase.

P14.1 (hierarquia no cruzamento): CRB de η com Ω_res livre escala como
gap⁻ᵖ com p ∈ [1.5, 2.5] quando o cruzamento é atravessado devagar
(regime adiabático, gap = 2η), medido variando η.
MORTE: fora da janela.

P14.2 (assinatura de velocidade): a informação total sobre η é
NÃO-MONOTÔNICA na taxa de varredura (máxima perto do regime
Landau–Zener crítico v ~ η², onde a transição é mais sensível), com
razão máx/assintótico > 3.
MORTE: monotônica ou razão ≤ 3.

P14.3 (o número de matéria escura): traduzindo para α = μM via
Ω_res ∝ μ·f(α): erro relativo de μ (massa do bóson) alcançável num
cruzamento limpo com SNR de fase = 100: σ(μ)/μ < 5%.
MORTE: > 20%.

## P14' (congelado 2026-08-30, ANTES de medir) — observável de fase de GW

Modelo: binária com chirp quadrupolar dΩ/dt = k·Ω^{11/3} + backreaction
−β·dP_b/dt; nuvem de dois níveis com Δ(t) = c·(Ω(t) − Ω_res), Ω_res ∝ μ
(massa do bóson); fase observada Φ(t) = 2∫Ω dt com ruído branco de fase
σ_φ = 0.1 rad por amostra, 2000 amostras, Ω varrendo 0.8→1.2 (Ω_res = 1).
Fiducial: k tal que a varredura local perto da ressonância é lenta
(v_eff ≈ 0.02·c), η = 0.05, c = 5, β = 0.01. Fisher 6×6 nos parâmetros
{Ω_res, η, β, k, Ω₀, φ₀}, com σ(μ)/μ = σ(Ω_res)/Ω_res marginalizado.

P14'.1 (o forecast honesto): a marginalização sobre os parâmetros da
binária degrada o σ(μ)/μ ingênuo (0.03%) por fator > 10, mas o resultado
fica < 5%.
MORTE: > 20% (cruzamento não mede μ na prática) ou < 0.1% (marginalização
não custa nada — indicaria erro).

P14'.2 (localização): ≥ 60% da informação de Fisher sobre Ω_res vem da
janela |Ω − Ω_res| < 5·η (a informação mora no cruzamento).
MORTE: < 40%.

P14'.3 (robustez à chirp mass): |corr(Ω_res, k)| < 0.9 no Fisher
marginalizado (a assinatura da nuvem não é absorvível pela taxa de chirp).
MORTE: ≥ 0.95.
