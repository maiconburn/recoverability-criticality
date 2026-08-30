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

Auditoria (arXiv API, 25 papers, 2026-08-30): EPs de Floquet são bem
estabelecidos (fotônica, Lindblad com drive periódico 2011.02054/2306.12322,
acoplamento dissipativo de Floquet 2504.13616, FEPs múltiplos 2509.02556).
NÃO encontrados: (i) o contraste explícito hermitiano-abre vs
dissipativo-colide na mesma ressonância de réplicas; (ii) QUALQUER análise
de Fisher/Cramér-Rao/custo de estimação em EP de Floquet — a camada de
metrologia permanece não-reivindicada também aqui. Full-text não varrido;
calibrar claims de mecanismo como "não encontrado em abstracts".

Nota de processo: P10.4 foi declarada "KILLED" pelo refinador fraco
(coordinate descent, gap 5.6e-3) e confirmada pelo refinador correto
(Nelder-Mead, gap 7e-10) — os critérios congelados nunca mudaram; a
busca sim. Scripts: p10_floquet.py, p10_dissipative.py; dados:
p10_floquet.json, p10_dissipative.json, p10_costlaw.json.

## Adendo — a cunha de EPs (mapa completo)

Duas linhas de EPs genuínos no plano (J, A), 23 pontos com gap ~10⁻⁹
(Nelder-Mead sobre log-gap, NSTEP=600):
- ramo inferior: J_EP(A) = 0.4655→0.3987 para A = 0.05→0.60 (dJ/dA ≈ −0.121)
- ramo superior: J_EP(A) = 0.4843→0.5483 para A = 0.10→0.60 (dJ/dA ≈ +0.128)
Ambos extrapolam para J* = 0.4717 em A→0: a ressonância estática de
réplicas é o VÉRTICE da cunha, e o drive dissipativo a abre em duas
linhas de EPs com uma banda PT-quebrada de Floquet entre elas — o
análogo dinâmico exato do par de EPs estáticos que flanqueia a banda
overdamped. Dados: results/p10_ep_line.json, p10_ep_line2.json.
