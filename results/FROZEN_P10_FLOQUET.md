# P10 — congelado ANTES de qualquer medição (pergunta do autor: "camadas
# que vibram na mesma frequência e se influenciam")

Data do congelamento: 2026-08-30. Sistema: qubit PT pós-selecionado com
drive periódico, H(t) = [[0, J], [J, -iγ/2]] + (A/2)·cos(Ω_d t)·σ_z,
γ = 1, Ω_d = 0.8. Propagador de um período U(T), quase-energias
λ_± = (i/T)·ln eig U(T), definidas mod Ω_d (as "camadas"/réplicas).

## P10.1 — EPs de camada (ressonância entre réplicas)
No sistema ESTÁTICO, gap real 2√(J²−1/16) = Ω_d ocorre em J* = 0.4717.
Previsão: com A > 0, surge estrutura de EP (colisão de quase-energias com
coalescência de autovetores) numa vizinhança de J*, ONDE O SISTEMA
ESTÁTICO NÃO TEM EP — camadas distintas se influenciando por ressonância.
MORTE: nenhuma quase-degenerescência com caráter de EP (gap de
quase-energia < 0.01 com colinearidade de autovetores > 0.99) encontrada
em J ∈ [0.35, 0.60], A ∈ (0, 0.6].

## P10.2 — a lei de custo é cega à camada
Perto do EP de Floquet, o CRB do splitting de quase-energia (amplitudes
livres, record estroboscópico c₁(nT)) diverge com o MESMO expoente da
tarefa análoga no EP estático medido na mesma janela de gaps.
MORTE: |expoente_Floquet − expoente_estático| > 0.5.

## P10.3 — o drive é o acoplamento entre camadas
A localização do quase-gap mínimo em J desloca-se continuamente de J*
quando A → 0⁺, e a largura da região de hibridização cresce
monotonicamente com A (papel de acoplamento efetivo entre réplicas).
MORTE: mínimo não conecta a J* no limite A→0, ou largura não-monótona
em A (fora de erro numérico).

## P10.4 (congelada 2026-08-30, APÓS morte de P10.1 e ANTES de medir)
Mecanismo aprendido com a morte: drive hermitiano (σ_z real) abre gap
entre réplicas (anticrossing, splitting ∝ A — P10.3 confirmou o fio).
Previsão afiada: com drive DISSIPATIVO, γ(t) = γ·(1 + A·cos Ω_d t)
(acoplamento anti-hermitiano entre réplicas), a mesma ressonância
J ≈ J* = 0.4717 produz COLISÃO: quasi-gap < 10⁻³ com colinearidade de
autovetores > 0.99 para algum A ∈ (0, 0.6], J ∈ [0.44, 0.50].
MORTE: nenhum ponto do plano satisfaz os dois critérios.
