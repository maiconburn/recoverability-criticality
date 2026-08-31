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

## Vereditos (2026-08-31, `p17_theorem_check.json`)

| check | previsão congelada | medido (últimos slopes) | veredito |
|---|---|---|---|
| C1 σ(controle), EP-2 | slope 0, σ → const | 0.0000; σ → 0.77958 | CONFIRMADO |
| C2 σ(gap), vínculo de Green | −1.00 | −1.0000 | CONFIRMADO |
| C3 σ(gap), amplitudes livres | −2.00 | −2.0000 | CONFIRMADO |
| C4 σ(controle), EP-3 | slope 0 | −0.0000 | CONFIRMADO |
| C4 σ(gap), EP-3 | −2.00 (= −(N−1)) | −2.0000 | CONFIRMADO |

Precisão de 4 casas em todos — como deve ser para um enunciado exato.
Escopo do C3: verdade antissimétrica (A₁ = −A₂, tipo Green), como
congelado no cabeçalho do script; verdade simétrica cai no degrau −1
(a escada de conhecimento de amplitudes depende da configuração da
fonte — refinamento aberto, não afeta o teorema).

Nota de instrumento: a primeira rodada usou μ puramente imaginário
(modo sem parte oscilante); com essa fase, o canal de Green é puramente
imaginário e Re[A·g] com A real projeta fora o canal ρ inteiro —
matriz de Fisher exatamente singular, σ espúrio ∝ 1/θ da inversão de
resíduos 1e-60. Terceira aparição do colapso de posto por fase/simetria
(P16.2 espelho, aqui fase); guarda de resíduo de inversão adicionada e
fases genéricas (μ = 0.7 − i) usadas na rodada final.

Consequências no programa: P14-LZ, o desenho da LEP3 e P16.2 são o
mesmo fato — expoente crítico 0 do parâmetro de controle.

## A escada completa (2026-08-31, mesma sessão)

Os três degraus {p−1, 2p−2, 2p−1} derivam de um único objeto: normas de
linha da inversa de Vandermonde. Tangentes do modelo na base de
monômios t^k e^{−iμt}: direção de amplitude do nó j = coluna
(δ_j^k/k!); direção de frequência = A_j × coluna deslocada uma ordem.
Com Gram genérica positiva-definida nos monômios,
CRB(parâmetro) ≍ ‖linha correspondente de V⁻¹‖, e o expoente é a ordem
dominante em s dessa linha:

- Tarefa A (amplitudes, frequências conhecidas): Vandermonde SIMPLES
  p×p ⇒ linhas ~ s^{−(p−1)}.
- Tarefas B e C (tudo livre): sistema CONFLUENTE 2p×2p (nós duplos — a
  mesma estrutura confluente do EP) ⇒ linhas de amplitude ~ s^{−(2p−1)},
  linhas de frequência ~ s^{−(2p−2)} (o fator A_j·t da coluna de
  frequência custa exatamente um grau).

Verificação simbólica exata (sympy, `p17b_ladder_symbolic.py`):
p=2 → {−1, −2, −3}; p=3 → {−2, −4, −5}. Seis de seis, ordens inteiras
exatas. Bate com todo o histórico numérico do programa: hierarquia
EP-2 medida {1.03, 2.12, 3.12}, P15.1 em EP-3 {−2.01, −3.98, −5.01},
C2/C3 deste documento.

Prior art (verificado na API do arXiv): os degraus 2p−2 e 2p−1 são os
teoremas de super-resolução de Batenkov–Goldman–Yomdin
(arXiv:1904.09186) e o condicionamento de matrizes de Fourier com nós
aglomerados de Batenkov–Demanet–Goldman–Yomdin (arXiv:1809.00658) —
citados no congelamento do P15. Nosso: a identificação EP ⇄ cluster
confluente, o degrau A, o expoente 0 do controle, e a unificação dos
três degraus numa única matriz.

Coluna vertebral analítica do programa (hierarquia CRB) COMPLETA:
expoente 0 (controle, teorema), p−1 / 2p−2 / 2p−1 (Vandermonde),
N−1 (Jacobiano simétrico). A lei de custo de RECONSTRUÇÃO
(ε ~ e^{−αN}/√d, halving no EP) é lei separada e segue com sua própria
validação EGB — não coberta por este documento.
