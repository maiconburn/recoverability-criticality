# P6 dry-run — resultado

**Data:** 2026-08-28 · **Modelo:** qubit de trilho duplo + banho estruturado Szegő (J ∝ √(1−(ω/W)²)(1−qω/W)), EP de 2ª ordem na segunda folha · **Pergunta:** a taxa de recuperabilidade quântica (mapa de Petz) e a taxa de reconstrução espectral, medidas do MESMO registro truncado em N modos detectores, travam juntas (ontologia de recoverability) ou são invariantes independentes (física padrão)?

## Veredito do dry-run

**Na mecânica quântica padrão (que a simulação realiza por construção), as duas taxas NÃO travam.** São dois invariantes analíticos distintos do mesmo sistema, previstos a priori e confirmados:

- **α_spec = [α_chain(q) − 2·ln ρ_B]/2** por N (Szegő corrigido por Green no ponto do ressonante) — ex.: S-B previsto 1.15, medido **1.145 ± 0.001**.
- **α_Petz = 2·ln ρ_B** por N (profundidade de Bernstein do polo da emissão) — ex.: S-A previsto 0.314, medido **0.288–0.301**.

| Config (q, W) | razão α_Petz/α_spec medida | previsão padrão | ontologia |
|---|---|---|---|
| S-A (0.9, 2) | 0.99 → 0.75 | ≈1 **por acidente numérico** (0.314 vs 0.310) | 1 |
| S-B (0.5, 2) | **0.22–0.30** | 0.27 | 1 |
| S-C (0.5, 1.4) | **0.62–0.72** | ~0.65 | 1 |

**K2 (no EP):** a taxa espectral **halva** (0.54 / 0.34 / 0.53 — Puiseux, como no EGB); a taxa de Petz **não halva** (0.98 / 0.98 / 0.97). A informação de estado não vê o ponto crítico espectral; a informação de parâmetro vê.

## O que isso estabelece

1. **O protocolo funciona e tem poder de matar pré-registrado.** As duas hipóteses (razão=1+halving duplo vs razões {0.27, 0.65}+halving só espectral) separam por >3× com barras de erro <5%.
2. **A armadilha do acidente foi real e foi pega**: em (q=0.9, W=2) os dois invariantes coincidem numericamente (razão 0.99!) — um teste de botão único teria "confirmado" a ontologia. A réplica de botão (exigência do árbitro) desfaz: a razão se move a 0.22 com q e 0.65 com W.
3. **A leitura deflacionária das validações EGB fica reforçada**: o halving espectral no EP reproduziu-se aqui (0.53) pelo mesmo mecanismo de Puiseux, enquanto a recuperabilidade quântica ignora o EP — custo de reconstrução espectral e custo de recuperação de estado são moedas distintas na física conhecida.
4. **A ontologia agora é uma previsão contra a QM padrão**: para sobreviver, precisa que o experimento real (qubit supercondutor classe Naghiloo, filtro de Purcell estruturado) mostre travamento onde a simulação da QM padrão mostra não-travamento — ou seja, física nova de verdade. Critérios K1/K2 congelados aplicam-se aos dados de laboratório como estão.

## Status da hipótese original ("buraco negro torna matéria macro quântica")

Não refutada — mas o descendente testável dela ("quanticidade e custo de informação são a mesma moeda") acaba de perder o refúgio teórico: dentro da física conhecida as moedas são distintas. O que resta é a aposta experimental, agora com protocolo, números e critérios de morte prontos.

## Gates e limitações

- Emissão analítica vs evolução temporal: concordância 5e-5 (limitada pela cauda t^{−3/2} de van Hove no heralding — produção usa a forma analítica).
- Puiseux ✓ (expoentes ~0.5 nas escadas); raízes com |F| < 1e-13; EPs com gap de colisão < 2e-8, achados por continuação (homotopia) da âncora verificada.
- Números "congelados" da spec do agente de design (g_EP=0.232342 etc.) **não reproduziram** e foram recomputados (FASE-0 real): S-A (0.286476, −0.312671, λ=0.06456−0.31521i); S-B (0.290717, −0.175705); S-C (0.314417, −0.221155).
- Pendentes para v2 (não mudam o veredito do dry-run): perna de canal aprendido, 2ª família de detector, réplica ruidosa σ=1e-8, auditoria M→2M, e o refinamento da janela de S-B no EP (SE 0.04).

Reprodução: `p6/run_p6.py` (~9 min), `p6/plot_p6.py`; dados em `p6/results_p6.json`; protocolo em `p6/SPEC.md`.
