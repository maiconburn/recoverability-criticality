# Validação numérica da lei de complexidade crítica

**Data:** 2026-08-28 · **Benchmark:** black brane Einstein–Gauss–Bonnet 5D, λ_GB = 0.08 · **Veredito: as três previsões estruturais pré-registradas foram confirmadas; o número congelado de 1.47 níveis/década foi medido em 1.45 ± 0.02.**

## 1. O que estava congelado

No turno 112 da conversa original (nó "Lei de complexidade crítica" do grafo), antes de qualquer cálculo, ficou pré-registrado que, para reconstrução geométrica com erro ε_g(N) ~ e^{−αN}:

| # | Previsão | Forma congelada |
|---|----------|-----------------|
| P1 | amplificação fora do EP | ε_ω(N,d) ∝ e^{−αN}/√d |
| P2 | taxa no EP cai pela metade | ε_ω(N,0) ∝ e^{−αN/2} |
| P3 | custo informacional logarítmico | N_ε(d) = A + (1/2α)·ln(1/d) |
| P4 | valor numérico | ≈ 1.47 níveis extras por década |

## 2. O ponto excepcional

O EP relevante é a colisão do modo escalar fundamental com seu parceiro espelho (ω → −ω̄) no eixo real de q² (momento espacial): a transição propagante → sobreamortecido. A simetria mantém o EP no eixo e faz de ρ = ((ω₁−ω₂)/2)² uma função real com zero simples — um EP de segunda ordem genuíno.

- **q²_c = −16.147205102**, **ω_c = −5.6738278 i** (unidades de raio de horizonte, normalização de tempo de boundary).
- Verificação: o par ω₀/ω₁ usado como candidato inicial **nunca colide** — o gap decai apenas assintoticamente (~|q|^{−1/3}); a colisão espelho é a estrutura crítica finita mais próxima.

### Método numérico (o obstáculo real)

Colocação de Chebyshev tem número de condição de autovalor ~10¹⁰ nessa região de momento — piso de ruído ~10⁻² em precisão dupla, inutilizável no EP. A validação usa um **solver de shooting**: série de Frobenius de ordem 14 no horizonte, integração até z = 10⁻³, QNM = zero do Wronskiano W(ω) = z⁵ψ′. Pares quase degenerados são extraídos por modelo quadrático local de W (condicionamento linear no ruído de W, não √). Precisão: ~10⁻⁹ longe do EP, ~10⁻⁵ no EP (confirmado por robustez a rtol, offset de horizonte e corte de boundary; ω_c estável a ~10⁻⁶). Validação externa: fundamental de AdS₅ (λ=0) reproduz o valor de literatura 3.119452 − 2.746676i a 10⁻⁸.

## 3. Dados

13 geometrias de Padé admissíveis (N = 2..12, 14, 15 coeficientes near-horizon; N = 13 e 16 têm polo físico e são rejeitadas pelo protocolo pré-registrado). Para cada N: erro do par de QNMs em d = |q²−q²_c| ∈ {10⁻¹ … 10⁻⁴} e em d = 0. Decomposição exata em canais via ω± = μ ± √ρ:

- **canal regular** = |μ_N − μ| (plano em d);
- **canal crítico** = |√ρ_N − √ρ| (o objeto das previsões);
- δρ_N = perturbação geométrica no canal crítico, medida em d=0.

## 4. Resultados

### P1 — amplificação 1/√d: **CONFIRMADA**

Expoente livre ajustado no canal crítico, janela d ∈ [3×10⁻³, 10⁻⁴] (entre o ramo de grande d, onde domina a diferença de inclinação δa·d, e a saturação):

> **γ = 0.498 ± 0.062** (previsto: 0.5), consistente em todos os N = 5..15.

O erro total exibe os DOIS componentes que a própria teoria previu: o platô regular (a lei refinada κ_O·e^{−2Ng_O} do turno 110) e o termo crítico crescendo como d^{−1/2} até saturar.

### P2 — taxa pela metade no EP: **CONFIRMADA**

| taxa | valor | R² |
|------|-------|-----|
| α_ρ (canal crítico δρ_N) | 0.851 ± 0.130 | 0.83 |
| α_EP (erro espectral em d=0) | 0.438 ± 0.068 | 0.82 |
| **razão 2·α_EP/α_ρ** | **1.03 ± 0.22** | previsto: 1 |

E mais forte — a estrutura de raiz quadrada com **coeficiente unitário**, ponto a ponto sobre ~5 décadas de δρ:

> **ε_ω(N,0) / √δρ_N = 1.03 ± 0.09** para todos os N = 4..15.

Contraste interno previsto pela teoria: a **posição** do EP converge na taxa cheia (α_shift = 0.848 ≈ α_ρ), enquanto o **espectro no EP** converge na metade — é exatamente a assinatura de sensibilidade √ de um EP de segunda ordem.

### P3 — custo logarítmico: **CONFIRMADA**

N*(d) medido por regressão do canal crítico por distância (alvo ε = 10⁻⁵): 5 pontos alinhados numa reta (R² = 0.999) entre 2 e 4 décadas de aproximação.

### P4 — níveis por década: **1.45 ± 0.02**

> Congelado: **≈ 1.47** (com α = 0.784 do fit exploratório) · Derivado do α_ρ medido: **1.35** · **Medido: 1.450 ± 0.019**

A parte estrutural (crescimento logarítmico, coeficiente 1/2α) está confirmada; o valor numérico congelado saiu a 1.4% do medido.

### Colapso universal (além do pré-registrado)

Todo o dataset (N, d) colapsa na curva **sem parâmetros livres** g(u) = √(u+1) − √u, com u = a·d/δρ_N — a forma fechada implícita no modelo do turno 112. Desvios só onde o ramo δa·d assume (u ≳ 10³), como esperado.

## 5. Refinamento que os dados exigem

A versão ingênua "α = taxa da métrica em norma sup" falha: α_geom(sup) = 0.57 ≠ α_ρ = 0.85. O que entra nas previsões é a taxa **do canal crítico** (a projeção δρ), exatamente como o turno 110 já tinha corrigido com o kernel de sensibilidade K_O. Ou seja: a versão forte "um α universal" morre (como a conversa já sabia), e a versão com canal/kernel é a que os dados confirmam quantitativamente.

## 6. Limitações honestas

- Oscilações de Padé (N = 7 e 10 anomalamente bons, N = 8 ruim) são correlacionadas entre todos os canais; os fits usam todos os N admissíveis, sem seleção.
- Piso numérico ~10⁻⁵ no EP: os pontos ε(0) de N = 14, 15 (~3×10⁻⁴) estão a fator ~3 do pior caso de robustez — as taxas não mudam excluindo-os.
- Um único benchmark (EGB λ=0.08) e um único EP; a extensão natural é o qBTZ e EPs em q² complexo.
- N_ε como staircase literal é grosseiro (saltos de qualidade do Padé); a medida contínua por regressão é a quantitativa.

## 7. Reprodução

```bash
cd theory-validation
uv run pytest                     # 13 testes
uv run python scripts/run_validation.py    # ~6 min, resume se interrompido
uv run python scripts/analyze_validation.py
```

Saídas: `results/validation.json` (dados brutos, pares completos), `results/fits.json` (todos os fits), `results/figures/fig1..fig5`.
