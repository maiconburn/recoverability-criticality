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
