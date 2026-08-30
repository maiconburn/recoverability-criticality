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
