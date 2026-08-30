# P12 + P13 — congelados antes de medir (radar de teoria grande, 2026-08-30)

## P12 — atravessabilidade ↔ recuperabilidade (ER=EPR operacional)

Modelo mínimo Yoshida–Kitaev do wormhole atravessável: 3+3 qubits,
pares de Bell (TFD em β=0), scrambler U determinístico (Ising chutado,
semente fixa: h_x=1.05, h_z=0.5, J=1, 6 passos), mensagem no qubit 1 da
esquerda, acoplamento exp(i g Σ Z_L Z_R), leitura no qubit espelho da
direita. Varredura g ∈ [−1.5, 1.5].

P12.1 (reproduzir GJW no mínimo): F_teleporte(g) tem janela: máx em
g* ≠ 0 com F(g*) − F(0) > 0.15.
MORTE: sem pico deslocado ou contraste ≤ 0.15.

P12.2 (a ponte ER=EPR↔Petz): a fidelidade do canal recuperado por Petz
(canal mensagem→qubit direito, referência maximamente mista) rastreia a
atravessabilidade: corr[F_tel(g), F_Petz(g)] > 0.9 na varredura, e o g
que maximiza uma maximiza a outra (|Δg*| < 0.2).
MORTE: corr < 0.5 ou picos discordantes.

P12.3 (no-locking na nova arena): o custo espectral de ESTIMAR g das
estatísticas de saída (CRB de g) NÃO trava na janela: variação de σ_g
dentro de fator 2 através do pico de F.
MORTE: dip/pico de σ_g alinhado ao pico de F além de fator 2.

## P13 — torre de anéis de fótons (ecos espaciais; lente/EHT)

Modelo mínimo da assinatura universal de sub-anéis: visibilidade
V(u) = Σ_{n=1..4} a·w^n · cos(2π d_n u + φ_n), diâmetros
d_n = d_∞(1 + c·e^{−γn}), w = e^{−γ} (Lyapunov), d_∞=40 μas, c=0.3,
φ_n = 0, banda u ∈ [2, 40] Gλ, ruído branco por amostra.

P13.1 (hierarquia espacial): CRB de γ com amplitudes livres escala como
gap⁻² e amplitudes com γ livre como gap⁻³, onde gap ≡ separação efetiva
dos harmônicos da torre (varrida via γ ∈ [0.3, 1.2]); expoentes ±0.5.
MORTE: fora das janelas.

P13.2 (número EHT-like): com SNR=100 por ponto e 200 pontos na banda,
σ(γ)/γ < 10% para γ = ln(e^π)≈π/… medir para γ=1.0 e reportar o número
(previsão: < 10%).
MORTE: σ(γ)/γ > 30%.

## P12'' (congelado 2026-08-30, após morte de P12.1, ANTES de medir)
Protocolo Hayden–Preskill/Yoshida–Kitaev probabilístico completo, 8
qubits: Bell(REF,M) ⊗ Bell(L1,R1) ⊗ Bell(L2,R2) ⊗ Bell(M2,Mt); U
(Ising chutado, 8 passos, semente fixa) em (M,L1,L2); U* em (M2,R1,R2)
com espelhamento de índices; projeção de Bell pós-selecionada nos pares
de saída (L1,R1) e (L2,R2); leitura: F = ⟨φ+|ρ(REF,Mt)|φ+⟩.

P12''.1 (o decodificador funciona): F pós-selecionada > 0.8, com
probabilidade de sucesso da pós-seleção em [1/32, 1/4] (referência
não-scrambled U=1: F = 0.25).
MORTE: F ≤ 0.5.

P12''.2 (a ponte Petz): a fidelidade do decodificador YK rastreia a
recuperabilidade de Petz do canal M→lado-R (sem decodificação):
F_YK ≥ 0.9·F_Petz (YK é quase-ótimo) e ambos caem juntos quando o
scrambling é enfraquecido (varredura de passos do U: 1, 2, 4, 8):
corr(F_YK, F_Petz) > 0.9 na varredura.
MORTE: corr < 0.5 ou F_YK < 0.5·F_Petz em algum ponto.

## Emenda P12''-A1 (2026-08-30, ANTES do re-teste; texto original mantido)
P12''.2 comparava F_YK com o Petz do canal SEM pós-seleção — que é
proibido de ter informação por no-signaling (e os dados obedeceram:
F_Petz = 0.2500 exato, independente do scrambling — verificação acidental
do teorema). Reformulação: F_Petz do canal CONDICIONADO ao sucesso da
projeção de Bell (M → Mt | sucesso), que é o objeto que o decodificador
YK aproxima. Critérios mantidos: corr(F_YK, F_Petz_cond) > 0.9 na
varredura de scrambling e F_YK ≥ 0.5·F_Petz_cond.
Também: varredura de passos ∈ {2,3,4,5,6,8,12} para caracterizar o
revival do scrambler pequeno (P12''.1 avaliada no MÁXIMO da varredura,
não em 8 fixo — emenda de operacionalização, morte se F_max ≤ 0.5).
