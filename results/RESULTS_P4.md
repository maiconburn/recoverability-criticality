# P4 fase 2 — o kernel medido, a hipótese CMI refutada, e as duas selas (2026-08-28)

## O que foi feito

Kernel de sensibilidade K_λ(z) do canal crítico medido diretamente (bumps polinomiais de Bernstein, resposta linear no EP) nos 7 backgrounds; dicionário de emaranhamento z_t(ℓ) (faixa RT) por background; hipótese congelada H_CMI: z̄_K(λ) = z_t(κ/|q_c|) com κ único calibrado na âncora.

## Resultado 1 — o kernel mora no horizonte

K(z) é **dominado pelo horizonte** (centroide 0.74–0.90, pico típico z≈0.96), oscilante com nós (fase complexa do modo). O endereço efetivo z*≈0.35 da v2 NÃO é onde o kernel mora — é uma **sela**: competição entre o kernel (cresce para o horizonte) e o erro de aproximação (decai para o horizonte).

## Resultado 2 — H_CMI refutada

| λ | z̄_K medido | z_t(κ/\|q_c\|) previsto | resíduo |
|---|---|---|---|
| −0.100 | 0.878 | 0.965 | −0.087 |
| −0.050 | 0.865 | 0.967 | −0.102 |
| +0.020 | 0.868 | 0.792 | +0.076 |
| +0.035 | 0.899 | 0.796 | +0.103 |
| +0.050 | 0.893 | 0.801 | +0.092 |
| +0.065 | 0.737 | 0.806 | −0.070 |
| +0.080 | 0.813 | 0.813 | 0 (calibração) |

Estrutura de sinal sistemática e oposta por ramo: a previsão cai com |q_c| (alavanca de 1.8×), o medido é plano. **A escala do kernel não vem do comprimento de blindagem de emaranhamento da fronteira — vem da estrutura do modo no horizonte (plana em λ).** A rota "CMI prevê o endereço" morre na sua forma natural.

## Resultado 3 — as duas selas (descoberta)

O produto |K(z)|·|δb_N(z)| tem **dois máximos** (bump do horizonte e bump da borda); o domínio troca em N≈9. Previsão derivada: taxa em janelas partidas deve cair de íngreme para rasa. Verificado nos dados já medidos (λ=0.08):

> α(N∈[4,8]) = **1.460** · α(N∈[10,15]) = **0.677**

O "α_ρ = 0.851" das rodadas anteriores era a média de janela de um **crossover entre dois endereços informacionais**. A lei v2 continua exata (ela computa o funcional completo); sua leitura correta: um observável pode ter **múltiplas profundidades informacionais, com dominância dependente do orçamento N** — refinamento genuíno e testável do conceito do turno 110.

## Balanço do P4

- **Metade "aproximação"** da lei (perfil de Green do conjunto de Stahl): derivável de teoria clássica; o objeto 𝒥/Abel da conversa mapeia aqui — sem conteúdo informacional além do relabel.
- **Metade "kernel"**: física de modo no horizonte; NÃO derivável da escala de emaranhamento testada. 
- Consequência: "informação como fonte" não sobrevive no setor holográfico testado. O último reduto experimental da ontologia segue sendo o laboratório (P6), com protocolo pronto.

## Reprodução

`results/p4_kernels.json` (kernels), `results/p4_predictions.json` (fase 1), scripts desta rodada. Dicionário z_t: integral RT com b(z) exato; JM correction O(λ) documentada como refinamento pendente (não muda a estrutura de sinal do veredito).
