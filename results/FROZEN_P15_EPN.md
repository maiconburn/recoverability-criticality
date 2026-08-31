# P15 — hierarquia de custo em EP de ordem N (congelado 2026-08-31,
# ANTES de qualquer sintético ou dado real)

Derivação congelada: perto de um EP-N, N frequências formam um CLUSTER de
largura g. A estimação a partir do record é um problema de Prony com
cluster de tamanho p = N. Estrutura prevista (generaliza a hierarquia
EP-2 medida no programa):

| tarefa | expoente previsto | caso p=2 (medido) | caso p=3 (previsto) |
|---|---|---|---|
| amplitudes, frequências fixas | p − 1 | 1 ✓ | **2** |
| frequências (splitting), amplitudes livres | 2p − 2 | 2 ✓ | **4** |
| amplitude, tudo livre | 2p − 1 (Batenkov) | 3 ✓ | **5** |

## P15.1 (sintético EP-3)
Cluster de 3 exponenciais com padrão Puiseux de EP-3
(λ_k = λ₀ + g·e^{2πik/3}·(fator), k=0,1,2), record com ruído branco,
janela fixa: expoentes CRB medidos em {2, 4, 5} ± 0.6 varrendo g por ≥ 2
décadas.
MORTE: qualquer um fora da janela.

## P15.2 (dados reais de EP-3)
Fontes catalogadas: NV EP-3 (Nat. Nanotech 19, 160, Source Data) e íons
aprisionados LEP3 (figshare 10.6084/m9.figshare.30343429). Previsão: nos
dados que permitirem reconstruir ao menos UMA tarefa da tabela, o
expoente medido fica a ±0.75 do previsto.
MORTE: expoente disponível fora da janela.
VOID declarável: se os Source Data só contiverem agregados sem records —
reportar "não testável com dados públicos" e manter P15.2 como
pré-registro aberto para laboratórios.

## P15.3 (consistência de resposta)
No mesmo sintético, a RESPOSTA do splitting ao parâmetro físico segue
ε^{1/3} (o ganho alegado pela literatura de sensores EP-3) — coexistindo
com os custos da tabela: o "debate do sensing" em ordem N é resolvido
pela separação de tarefas, como no EP-2.
MORTE: resposta não-consistente com 1/3 (±0.1) no regime pequeno-ε.

## P15.4 (congelado 2026-08-31, ANTES de calcular) — anisotropia ao longo da linha de EP

Hipótese: o custo de estimação NO EP, ao longo da linha de LEP3, é
controlado pela não-ortogonalidade local dos autovetores (fator de
Petermann). Medida operacional congelada: κ_V(α) = número de condição da
matriz de autovetores do LH do experimento, avaliado num offset relativo
fixo δ=10⁻³ da linha (γ = γ_LEP3(α)·(1+δ), ω=1) — comparável entre α's.
Observável: σ_γ/γ̄ dos bootstraps públicos (normalizado por escala; σ_γ
cru reportado como secundário).

Previsão: corr[ln(σ_γ/γ̄), ln κ_V] > 0.8 nas ≥9 configurações utilizáveis,
com lei de potência σ/γ ∝ κ_V^q, q ∈ (0, 1.5].
MORTE: corr < 0.5.
Controle congelado: se σ_γ/γ̄ correlacionar melhor com γ̄ puro do que com
κ_V (|corr_γ| > |corr_κ| + 0.1), a hipótese Petermann NÃO é suportada
mesmo com corr alta — reportar como confundida por escala.
