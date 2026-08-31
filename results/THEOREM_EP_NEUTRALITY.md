# Teorema da neutralidade do parâmetro de controle no EP (2026-08-31)

Motivação: três medições independentes deram custo CHAPADO para estimar o
parâmetro de controle no EP — P14-LZ (σ(μ)/μ = 0.03%), o desenho da LEP3
(todas as configs sobre a linha do EP), P16.2 (p = −0.07 em 1.5 décadas
de gap). Aqui a explicação analítica, com verificação numérica de alta
precisão (script `p17_theorem_check.py`, previsões declaradas ANTES de
rodar — seção "Verificações").

## Enunciado

Seja H(θ) família analítica de matrizes N×N com EP de ordem N em θ = 0,
e sejam os dados y(t) = Re[A·g(t; θ)] + ruído branco, com A ∈ ℂ nuisance
e g uma função SIMÉTRICA analítica do espectro {ω_j(θ)} — o que inclui
todo canal de resposta linear: a função de Green escalar é a diferença
dividida de ordem N−1 de e^{−iωt} sobre o espectro,

  g(t; θ) = Σ_j e^{−iω_j t} / Π_{k≠j}(ω_j − ω_k) = Δ^{N−1}[e^{−iω·t}],

simétrica por construção e INTEIRA nos invariantes. Então a informação
de Fisher marginalizada para θ é analítica em θ = 0 e, sob as condições
de genericidade abaixo, σ(θ̂) → constante positiva finita no EP:
**o expoente crítico do parâmetro de controle é exatamente 0.**

## Prova (EP-2; o caso geral é idêntico com e₁…e_N)

1. (Simetria ⇒ analiticidade.) Autovalores ω± = μ ± √ρ com μ = tr H/2,
   ρ = μ² − det H, ambos analíticos em θ. Função simétrica analítica dos
   autovalores é função analítica dos polinômios simétricos elementares
   (teorema clássico), logo g(t; θ) = ĝ(t; μ(θ), ρ(θ)) é analítica em θ
   ATRAVÉS do EP. Exemplo explícito (canal de Green):
   ĝ = −i e^{−iμt} · sin(√ρ t)/√ρ = −i e^{−iμt} (t − ρt³/6 + ρ²t⁵/120 − …),
   série par em √ρ ⇒ inteira em ρ. A raiz quadrada do unfolding
   simplesmente não aparece.

2. (Fisher analítica.) As colunas do design J são ∂y/∂θ e as 2 colunas
   de amplitude — todas analíticas em θ. I(θ) = JᵀJ/σ² analítica;
   a marginalizada I_eff = I_θθ − I_θA I_AA⁻¹ I_Aθ (complemento de
   Schur) é analítica onde I_AA é invertível.

3. (Genericidade.) (i) transversalidade: ρ'(0) ≠ 0 (o controle de fato
   desdobra o EP); (ii) a direção ∂g/∂θ|₀ ∉ span das colunas de
   amplitude — para o canal de Green, ∂ĝ/∂ρ|₀ ∝ t³e^{−iμt}, que é
   linearmente independente de e^{−iμt} e t e^{−iμt}: vale; (iii) I_AA
   invertível no espaço de nuisance de posto correto (lição P16.2: com
   par espelho o posto cai para 2 — reparametrizar antes).
   Sob (i)–(iii), I_eff(0) > 0 e σ(θ̂) é finita e contínua. ∎

## Corolário A — a escada de Jacobianos (de onde vêm os expoentes)

Toda a divergência espectral é contabilidade de mudança de variável em
cima de uma Fisher analítica. CRB transforma como I_η = I_ρ·(dρ/dη)²:

- gap s = 2√ρ: σ(ŝ) = σ(ρ̂)·|ds/dρ| ∝ s⁻¹ — expoente 1.
  (Kerr medido: custo de extração ∝ gap^−1.11.)
- EP-N: coeficiente simétrico c ∝ s^N ⇒ σ(ŝ) ∝ s^{−(N−1)} — o PRIMEIRO
  degrau {p−1} da escada P15 {p−1, 2p−2, 2p−1}, agora derivado.
- Quantidades rotuladas (autovalor individual, resíduo, autovetor) não
  são simétricas ⇒ pagam o custo crítico. Físico: nenhum aparelho mede
  rótulo; aparelhos medem resposta (simétrica). O custo crítico é
  propriedade da PERGUNTA, não do sinal.

## Corolário B — degrau de amplitudes livres (heurístico, verificação C3)

Com amplitudes POR MODO livres (observador agnóstico, sem o vínculo de
Green), as funções-base e^{−iω₁t}, e^{−iω₂t} degeneram linearmente em s
e a marginalização da direção quase-nula custa um Jacobiano extra:
previsão σ(ŝ) ∝ s⁻² — o segundo expoente da hierarquia medida
(task 2 = 2.12). A hierarquia de tarefas é uma escada de CONHECIMENTO
sobre amplitudes: vínculo de Green ⇒ s⁻¹; amplitudes livres ⇒ s⁻².

## Fronteira de validade (honesta)

- Movimento AO LONGO da variedade do EP (ρ ≡ 0): o canal só informa via
  μ(θ); anisotropia de custo ali é variação mundana de I_μμ — consistente
  com o veredito de P15.4 (anisotropia da LEP3 dominada por escala γ).
- Falha de genericidade (iii) exige redução de posto do nuisance antes
  da marginalização (P16.2 v1 vs v2).
- Ruído não-branco ou amostragem que mate ∂ĝ/∂ρ|₀ muda constantes, não
  o expoente 0 (a analiticidade é estrutural).

## Verificações numéricas (previsões declaradas antes de rodar)

Modelo EP-2: ω± = (a − i)θ_μ-drift + … concretamente μ = −i + 0.3θ,
ρ = θ; canal de Green amortecido, t ∈ [0, 4], 200 pontos, mpmath 50 dps.
- C1: σ(θ̂) marginalizada em θ = 10⁻¹…10⁻⁸: slope log-log local → 0
  (|slope| < 0.05 em θ ≤ 10⁻⁴) e σ → constante positiva.
- C2: parametrização direta em s (nuisance μ, A): slope → −1.00 ± 0.05.
- C3: modelo de amplitudes livres por modo (8 parâmetros reais):
  slope de σ(ŝ) → −2.00 ± 0.15 (corolário B).
- C4: EP-3 (μ = −i, ω_j = μ + ε_j s, s = θ^{1/3}, canal = diferença
  dividida de 2ª ordem): σ(θ̂) slope → 0; σ(ŝ) slope → −2.00 ± 0.15
  (= −(N−1)).
MORTE do teorema: C1 ou C4-controle com slope fora de ±0.05 (a
analiticidade é exata — não há margem). C2/C3/C4-gap fora das faixas
mata o corolário correspondente, não o teorema.

## Vereditos

(preenchido após a rodada — ver seção homônima ao fim)
