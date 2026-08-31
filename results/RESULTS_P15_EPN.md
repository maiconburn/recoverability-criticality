# P15 — a hierarquia em ordem N (congelada antes; sintético confirmado)

## P15.1 CONFIRMADA — a escada do cluster {p−1, 2p−2, 2p−1}

EP-3 sintético (padrão de Puiseux cúbico, aritmética de 60 dígitos com
gate de condicionamento — a v1 em double era piso de pinv abaixo de
g=0.03, artefato conhecido da casa):

| tarefa | previsto (p=3) | expoentes locais finais |
|---|---|---|
| amplitudes, frequências fixas | 2 | −2.05 → −2.01 |
| pior direção de frequência, tudo livre | 4 | −3.70 → −3.98 |
| amplitude, tudo livre | 5 | −5.05 → −5.01 |

Com o caso p=2 já medido no programa (1, 2, 3), a hierarquia é
**{p−1, 2p−2, 2p−1} na ordem p da degenerescência** — a lei de custo
ganha generalidade em N.

## P15.3 CONFIRMADA — coexistência com o ganho de resposta
Resposta do splitting ao parâmetro físico: expoente 0.3333 (= 1/3 exato).
O "debate do sensing EP-N" se resolve como no EP-2: o ganho de resposta
ε^{1/N} é real E os custos espectrais da escada são reais — são TAREFAS
diferentes sobre o mesmo sistema.

## P15.2 — dados reais: em andamento
Fontes catalogadas: NV EP-3 (Nat. Nanotech 19, 160) e íons aprisionados
LEP3 (figshare). Pré-registro em FROZEN_P15_EPN.md; janela ±0.75.

## P15.2 — dados de íons (LEP3): VOID por desenho, com um brinde

Dataset público analisado (figshare 10.6084/m9.figshare.30343429,
CC BY 4.0; 120 amostras de bootstrap de fits (α, γ) por configuração):
engenharia reversa das configurações mostra que TODAS obedecem
γ = 4ω/|1 − 2α| (6/6 pares exatos) — o experimento senta SOBRE a linha
de LEP3 e varre a POSIÇÃO ao longo dela, nunca a distância ao EP. Sem
varredura de gap, o expoente da escada não é testável: **VOID pelo
critério congelado**, e o pré-registro P15.2 permanece aberto para
qualquer laboratório com varredura transversal (a previsão pública:
{2, 4, 5} ± 0.75).

Brinde: os σ de bootstrap variam ~5× ao longo da linha
(σ_γ: 0.05 → 0.26), medindo a ANISOTROPIA do custo de estimação ao longo
de uma linha de EP-3 — observável que nossa teoria ainda não prevê;
anotado como questão aberta.

Estado final da linha P15: teoria da escada em ordem N CONFIRMADA em
sintético de alta precisão ({p−1, 2p−2, 2p−1}; locais −2.01/−3.98/−5.01);
resposta ε^{1/3} exata; dados públicos disponíveis não testam a escada
por desenho experimental. Dados: p15_ep3_v2.json, p15_lep3_data.json.

## P15.4 — hipótese Petermann: MORTA pelo controle congelado

corr[ln(σ/γ), ln κ_V] = −0.27 (fraca, sinal oposto ao previsto);
controle de escala congelado disparou (γ puro correlaciona 0.525 > κ_V).
Veredito: CONFOUNDED-BY-SCALE. A anisotropia ao longo da linha de LEP3 é
dominada, ao menos em parte, por física experimental mundana (γ maior =
menos oscilações na janela de medição = fit pior) e por uma diferença
sistemática entre os ramos α < ½ e α > ½ que κ_V local não captura.
Questão aberta REFINADA: separar o confundidor exigiria os records crus
(não os bootstraps agregados) ou dados com janela ∝ 1/γ. A "segunda lei"
(custo paralelo geométrico) segue sem candidato vivo. Dados: p15_4.json.
