# P1 — varredura de acoplamento: resultado (2026-08-28)

Protocolo: previsões congeladas em `sweep_predictions.json` e `p4_predictions.json` ANTES das medições (λ=−0.1 vista antes do congelamento P4 — flagged). 5 acoplamentos com EP real: λ ∈ {−0.10, −0.05, 0.02, 0.05, 0.08}.

## O que confirmou (estrutural — as alegações da teoria)

1. **Halving universal no EP**: 2α_EP/α_ρ = {1.00, 1.00, 1.00, 1.00, 1.03} nos cinco backgrounds. A lei do turno 112 não é acidente do λ=0.08 — é universal na família. Este é o resultado central da varredura.
2. **Splitting de canais persiste**: α_ρ/α_sup ∈ [1.24, 1.49] (média 1.38), nunca →1. O refinamento de kernel (turno 110) sobrevive ao gate K2 — a teoria NÃO se reduz a Stahl em norma sup.
3. **Espectroscopia nova**: trajetória do EP espelhado q²_c(λ) = −5.71 → −5.45 → −18.27 → −17.34 → −16.15 (não-monótona!), ω_c(λ) = −2.82i → −5.67i. Inédito na literatura.
4. **Extinção do EP**: para λ ≥ 0.12 a colisão espelho não existe em q² real até q²=−40 — o EP se extingue ou migra pro plano complexo. Transição qualitativa nova na família EGB.

## O que falhou (o proxy — critério K1 pré-registrado DISPAROU)

O proxy analítico "α ∝ função de Green do branch point mais próximo" **não prevê α(λ) quantitativamente**:

- Regressão dN/dec medido vs previsto: **R² = 0.40** (gate exigia ≥ 0.9); slope 0.68±0.49.
- Regressão α medido vs previsto: R² = 0.52; deriva sistemática monótona em λ (medido/previsto: 1.42→1.00).

Leitura: a distância a UM branch point não basta — a taxa real vê os 4 branch points + zeros complexos + peso de kernel do canal (capacidade de Stahl verdadeira). O caminho "α de zero parâmetros" continua aberto, mas exige a teoria de capacidade completa (modelo v2, novo congelamento, novos λ de teste — ex. 0.03, 0.065, −0.075).

## P4 fase-1 (arbitragem preliminar)

Estrutura analítica derivada: sob o kernel de Abel, 𝒥 herda singularidades de B **mais os zeros complexos de b** (z=±i, fixos em λ) → curvas α_B e α_CMI separam em λ=0.02. Medido: 1.360±0.121 → z(métrica)=+1.8, z(CMI)=+3.3. **Direção: desfavorece a camada CMI** — mas como o proxy-base falhou K1, o veredito final do P4 espera a baseline de capacidade correta.

## Tabela

| λ | α_ρ medido | dN/dec medido | dN/dec previsto | halving | split |
|---|---|---|---|---|---|
| −0.100 | 1.026±0.093 | 1.208±0.036 | 1.600 | 1.000 | 1.35 |
| −0.050 | 1.173±0.084 | 1.011±0.006 | 1.323 | 1.000 | 1.44 |
| +0.020 | 1.360±0.121 | 0.817±0.003 | 1.008 | 1.000 | 1.24 |
| +0.050 | 1.063±0.087 | 1.135±0.013 | 1.202 | 1.004 | 1.40 |
| +0.080 | 0.851±0.130 | 1.450±0.019 | 1.353 | 1.029 | 1.49 |

Reprodução: `scripts/sweep_predictions.py` (congela) → `scripts/run_sweep.py` (~15 min) → `scripts/analyze_sweep.py`. Dados: `results/sweep.json`, `results/sweep_fits.json`.
