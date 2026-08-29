# Cross-family test of the critical-cost law (deep family, λ=0.120) — QUARANTINED FINDING

Status: measured in one session (2026-08-30); same-day quarantine rule
applies — reported as data + candidate reading, NOT as a claim.

## Setup
Anchor: the wall-classified deep-family mirror EP at λ = 0.120
(q²_c = −32.285, ω_c = −9.730063i, anchor gap 3.1×10⁻⁶). Constrained-Padé
reconstruction ladder, full validation driver adapted
(`scripts/run_validation_deep.py`, forest guard |Δq²| < 0.5), per-level EP
relocation. Data: `results/validation_deep.json`, `results/deep_ladder_final.json`.

## What is solid
- **The exponential structure transfers**: α(d) = 0.805 constant across
  three decades of distance (d ∈ [3.2×10⁻⁴, 10⁻¹]), like the fundamental
  family.
- Anchor floor ~3×10⁻⁶ saturates d = 10⁻⁴ and the N = 15 EP point — bounded
  and understood.

## What did NOT reproduce
- **Rate halving at the EP**: α_off/α_EP ≈ 0.7–1.1 measured (prediction 2),
  using the clean odd-N subsequence (5, 7, 11, 13).
- Strong parity systematic: even-N reconstructions give ε(EP) ~ O(1)
  (0.85/0.42/0.88 at N = 8/10/12) even with relocation |shift| ≤ 0.09,
  while odd-N decays five decades. Unexplained; contaminates any strong
  conclusion. N = 3, 6, 9, 14 lost to relocation failures (forest guard or
  no EP).

## Candidate readings (to be arbitrated later)
1. **Isolation condition**: the halving derivation assumes an ISOLATED
   EP-2; the deep EP sits in the dense near-degenerate forest (E3), which
   can contaminate the Puiseux structure. Halving would then be a property
   of isolated EPs — a scope refinement of the law, testable by measuring
   halving vs distance-to-nearest-neighbor structure.
2. Family-specific law (halving only for the fundamental pair) — weaker
   prior, would require understanding why.
3. Measurement artifact tied to the parity systematic — must be excluded
   first before any physics reading.

## Next stress tests (not run)
- Diagnose the even-N pathology (pair identity at the reconstructed EP).
- Repeat at a second deep-family point (λ = 0.117 needle) and at a
  fundamental-family EP with an artificially crowded neighborhood.

## Adendo (mesma sessão) — paridade diagnosticada; anti-halving persiste

Remedição dos N pares com gate espelho e seed correto
(`results/even_fix.json`): N=6 → 4.9e-3 e N=10 → 6.4e-5 LIMPAM (artefato de
bacia do secante confirmado); N=8 converge para um par espelho DIFERENTE em
ω = ±0.226 − 8.91i — um VIZINHO da floresta, contaminação direta observada;
N=12 sem par espelho perto de −9.73i. Série limpa (N=5,6,7,10,11):
α_EP ≈ 1.24. Com α_off = 0.80: **razão α_off/α_EP ≈ 0.65 — anti-halving**
(no EP converge MAIS RÁPIDO; a fundamental halva, razão 2). Segue
quarentenado; leitura líder continua a condição de isolamento, agora com o
vizinho de N=8 como evidência direta de contaminação. Teste discriminador
lançado: mesmo protocolo no ponto λ=0.117 (agulha mais estreita ⇒ mais
contaminada ⇒ razão ainda menor, se a leitura 1 estiver certa).

## Segundo ponto (λ=0.117) — replica o não-halving

Âncora espelhada genuína (gap 4.1×10⁻⁵, ω=−10.2945i, espelho a 1.5×10⁻⁶),
todos os 13 níveis limpos (sem patologia de paridade aqui):
α_off ≈ 0.74 (d=10⁻¹, N=6→15, 3 décadas); α_EP ≈ 0.89 (N=6→10, antes do
piso de âncora ~1.1×10⁻⁴ que domina N≥11). **Razão ≈ 0.83 — sem halving**,
consistente com λ=0.120 (0.65). Duas medições independentes na região da
floresta: o fator-2 do EP NÃO aparece no estrato fundo; razão fica em
0.65–0.9. A leitura de isolamento segue líder; discriminador restante
(não executado): halving num EP fundamental com vizinhança artificialmente
povoada — separa física (isolamento) de artefato de medida.
Dados: results/validation_deep_0.117.json.

## CORREÇÃO (mesma sessão, análise canal-separada) — "não-halving" é VOID; teste INDETERMINADO

Separando os canais dos pares salvos (μ = média, ρ = ((ω₁−ω₂)/2)²):
1. **As razões 0.65–0.83 mediam o canal μ**, não o canal crítico: |δμ| decai
   com α_μ = 1.15 (λ=0.120) e domina o pair_error dos níveis limpos. O
   halving da lei é uma afirmação sobre o canal ρ (2α_EP/α_ρ), como na
   validação original — meu teste simplificado media a coisa errada.
2. **O canal ρ está sob o piso da âncora**: |δρ| ≈ 8×10⁻¹² plano de N=5 a
   15 — exatamente (gap_âncora)² = (3.1×10⁻⁶)². δρ verdadeiro é menor que o
   mensurável já em N=5. Não há evidência de não-halving nem de halving:
   **INDETERMINADO por piso**. Medir exigiria âncora com gap ≲ 10⁻⁸.
3. A hipótese de isolamento morreu por dado independente e fica morta:
   Δω ao vizinho mais próximo é MENOR nos fundamentais que halvam (0.55,
   0.62) do que nos fundos (2.71, 1.09) — o discriminador proposto está
   invertido nos dados.

Estado final desta linha: transferência da estrutura exponencial (α_off
constante em 3 décadas) CONFIRMADA nos dois pontos fundos; halving no
estrato fundo: ABERTO (limitado por instrumento, não decidido). O ciclo
claim→refutação→correção desta seção (não-halving → void em horas) é mais
um caso da regra de quarentena funcionando.

## Kernel do estrato fundo — cota de desacoplamento (fecho da linha)

Bumps de Bernstein em três regimes de ε (1e-6, 1e-3, 1e-9), gates de espelho
e identidade (`scripts/kernel_compare.py`, `results/kernel_compare_*.json`):
- Fundamental (λ=0.105): kernel horizonte-dominado reproduzido
  (K = 50–483 em z ≥ 0.5, centroide 0.752 — bate com P4). Ferramenta
  validada.
- Fundo (λ=0.120): TODA resposta ρ mensurável fica no piso da âncora
  (δρ ~ 1e-11) em qualquer ε do regime linear; os picos aparentes
  (z=0.5/0.875 no run sem gate) não reproduzem entre ε's — artefatos de
  identidade. Resultado à prova de piso: **K_fundo < 10⁻² em todo z
  acessível ⇒ o canal crítico fundo é ≥4 ordens menos acoplado ao dado
  métrico interior que o fundamental.**

Estado final da linha nesta máquina: (i) estrutura exponencial transfere
(α_off constante, 2 pontos); (ii) halving: indeterminado por piso;
(iii) canal ρ fundo metricamente desacoplado (cota); (iv) hipótese de
isolamento morta; (v) endereço do canal fundo: não-resolvível com o solver
atual (exigiria piso ≲ 1e-16). Medições futuras exigem instrumento com
precisão de ρ além de rtol 1e-10.
