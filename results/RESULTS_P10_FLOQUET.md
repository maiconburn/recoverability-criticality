# P10 — camadas de frequência e a lei de custo (pergunta do autor, ciclo completo)

Origem: pergunta leiga do autor, 2026-08-30: "e se o mundo quântico tivesse
camadas ou frequência? tipo esquemas que vibram na mesma frequência e um
influencia o outro". Tradução: réplicas de Floquet (camadas) + ressonância.
Previsões congeladas ANTES de cada medição (FROZEN_P10_FLOQUET.md, commits
com timestamp separados).

Sistema: qubit PT pós-selecionado, γ=1, drive Ω_d=0.8; réplicas de
quase-energia = as "camadas".

## Vereditos

| Previsão | Veredito | Número |
|---|---|---|
| P10.1: drive hermitiano (σ_z) cria EP na ressonância de réplicas | **MORTA** | anticrossing: quasi-gap ∝ A (Rabi entre camadas), colinearidade ~0.55 |
| P10.2: lei de custo cega à camada | **CONFIRMADA** | expoente −1.531 (Floquet) vs −1.398 (estático), diff 0.134 ≤ 0.5 |
| P10.3: drive = fio entre camadas, mínimo → J* quando A→0 | **CONFIRMADA exata** | J_min(A→0) = 0.47170 = J* (5 casas); gap ∝ A monotônico |
| P10.4 (afiada pela morte de P10.1): drive DISSIPATIVO (γ(t)) colide as camadas | **CONFIRMADA** | dois EPs de Floquet: (J=0.4842769, A=0.100226) e (J=0.4466490, A=0.202121), gap ~7–9×10⁻¹⁰, colinearidade 1.000000 |

## A física em uma frase

Camadas de frequência ressonantes se acoplam pelo drive; acoplamento
hermitiano ABRE o gap entre elas (anticrossing), acoplamento dissipativo
as faz COLIDIR (EP de Floquet) — e no EP de camadas vale a mesma lei de
custo do EP estático.

## Calibração de novidade (não auditada em full-text)

EPs de Floquet em sistemas não-hermitianos são conhecidos na literatura
de fotônica/PT. O conteúdo potencialmente novo aqui: (i) a extensão da
lei de custo de estimação ao EP de réplicas (cegueira à camada, medida);
(ii) o contraste hermitiano-abre / dissipativo-colide na MESMA
ressonância de réplicas deste sistema mínimo, com ciclo pré-registrado.
Auditoria de literatura pendente antes de qualquer claim externo.

Nota de processo: P10.4 foi declarada "KILLED" pelo refinador fraco
(coordinate descent, gap 5.6e-3) e confirmada pelo refinador correto
(Nelder-Mead, gap 7e-10) — os critérios congelados nunca mudaram; a
busca sim. Scripts: p10_floquet.py, p10_dissipative.py; dados:
p10_floquet.json, p10_dissipative.json, p10_costlaw.json.
