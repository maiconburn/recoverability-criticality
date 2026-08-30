# P12 + P13 — vereditos (radar de teoria grande; congelados antes de medir)

## P12 — atravessabilidade ↔ Petz (ER=EPR operacional)

Trilha de instrumentação (toda registrada): v1 tinha a mensagem no lugar
errado (media preservação, não teleporte — pego por sanidade U=1); v2
corrigiu a inserção mas usava embed() com permutação BUGADA (pego por
teste unitário: gate caía no qubit errado — todos os resultados
anteriores void); v3 = aplicação tensorial com testes unitários PASS.

**P12.1 MORTA no modelo mínimo**: com o protocolo limpo (3+3 qubits,
Ising chutado 8 passos, acoplamento exp(igΣZZ) nos 2 pares carriers,
decodificação U* ou U^T), F(g) ≈ 0.25 com contraste ≤ 0.007 e
MI(REF:R0) ≤ 0.022 bits em g ∈ [−2, 2]. Leitura física: a janela de
atravessabilidade "sem decodificador" do GJW é fenômeno semiclássico de
N grande; em N pequeno o teleporte-por-tamanho EXIGE o decodificador
(Grover/YK) — consistente com o desenho do experimento de 7 qubits de
Landsman et al. P12.2/P12.3: void por premissa.

Aberto (degrau seguinte definido): implementar o decodificador YK
probabilístico (projeção de Bell) ou determinístico (Grover) e re-testar
a ponte Petz — a conexão conceitual (atravessar = canal de recuperação)
permanece intacta e testável.

## P13 — torre de anéis de fótons (ecos espaciais)

**P13.2 CONFIRMADA (o número)**: com 4 sub-anéis, banda 2–40 Gλ, 200
pontos, SNR=100/ponto: σ(γ)/γ = **0.29%** — o expoente de Lyapunov do
anel de fótons é mensurável com precisão sub-porcento neste modelo. É a
afirmação EHT-facing da linha.

**P13.1 parcial**: no regime profundo (γ = 1.2→3.0, gap 0.147→0.0009,
2.3 décadas):
- amplitude com γ fixo: expoente −0.86 (local final −0.98 → 1) ✓
- γ com amplitudes livres: −1.67 (dentro de 2 ± 0.5) ✓ CONFIRMADA
- amplitude do modo degenerante (a₄) com γ livre: **−2.40 estável**
  (locais −2.37..−2.44) — fora de 3 ± 0.5: MORTA como congelada. A
  previsão de 3 assumia par isolado; a torre multi-tom dá 2.4
  (regime de cluster, cf. Batenkov) — refinamento de escopo, não colapso.

Hierarquia qualitativa (1 → 1.7 → 2.4) presente e limpa através de
décadas de gap. Dados: p13_photon_ring.json, p13_deep.json, p13_a4.json;
p12_v3_{conj,T}.json.
