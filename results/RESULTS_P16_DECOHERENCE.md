# P16 — decoerência como quarta tarefa: vereditos (2026-08-31)

Pré-registro: `FROZEN_P16_DECOHERENCE.md` (commitado antes de qualquer
medida). Instrumento: par fundamental de QNMs em λ = 0.105, EP espelho
ancorado do `shooting_ep_hunt.json` (q²_c = −34.385584, ω_EP = −7.164147i,
gap 1.3e-4), continuação com gates de espelho e salto de identidade.
Dados: `p16_decoherence.json`; scripts `p16_decoherence.py` (trajetória e
P16.3) e `p16_fix.py` (instrumento v2 de P16.1/P16.2).

## P16.3 — proteção pós-EP: CONFIRMADA (todas as janelas congeladas)

| medida | congelado | medido |
|---|---|---|
| expoente do splitting (lado sub) | 0.5 ± 0.1 | 0.495 |
| expoente do splitting (lado sobre) | 0.5 ± 0.1 | 0.501 |
| proteção Γ_slow < γ_EP em todo ponto | sim | sim (todos) |
| expoente do kink h | [0.4, 0.6] | 0.493 |
| lado sub plano, slope norm. | < 0.05 | 0.018 |

Atravessando o acoplamento crítico, um canal fica MAIS longevo:
Γ_slow = γ_EP − B·|δ|^0.49, proteção máxima 3.1% na janela medida
(δ até 0.0215; a continuação para no gate de salto de identidade).
Assimetria do kink em δ pareado (0.0215): lado sobreamortecido perde
0.223 em Γ_slow contra 0.010 do lado subamortecido — 22×. O fantasma
digno da conjectura fundadora (lápide 1): não "curvatura suprime
decoerência", mas "cruzar a criticalidade espectral protege parcialmente
um canal, com kink de raiz quadrada". Leitura de canal: Γ_slow é o polo
mais lento do banho visto pela sonda em dephasing puro; a proteção é
afirmação sobre o espectro, herdada pelo envelope de coerência tardio.

## P16.1 — resgate pelo canal secular: MORTA

Com o instrumento correto (v2), χ²/dof ≈ 1 para os DOIS modelos em todos
os pontos, inclusive no EP (sec 387.8 vs nosec 385.5, dof 392): nenhuma
rejeição. O canal secular t·e^{−γt} é mimetizado ao nível de ruído 1e-3
por duas exponenciais livres numa janela finita (aproximação tipo Prony)
— a armadilha não era o compensador de Petermann (neutralizado pelo
bound), era identificabilidade da própria classe de observável. Contraste
instrutivo com P8.2: o canal log em VARIÁVEL DE ESCALA (décadas em k) é
detectável a χ²/dof 1e5; o canal secular em TEMPO com janela ~4/γ não é.
Detectabilidade do canal de Jordan depende da classe do observável — é
por isso que assinaturas seculares de EP em ringdown temporal são duras.

## P16.2 — expoente da tarefa de estimação: MORTA (informativa)

σ(δq²) ≈ 3.2e-3 CHAPADO em 1.5 décadas de gap: p = −0.066 (subconjunto
sub-resolvido gap·T < 0.5: −0.029), contra previsão congelada 1.0 e
faixa de morte fora de [0.6, 1.5]. Leitura: o ganho de resposta do
unfolding √ (dω/dδq² ∝ gap⁻¹) cancela EXATAMENTE o custo espectral de
resolução — estimar o parâmetro de CONTROLE (distância ao EP no espaço
de acoplamento) é neutro ao EP. Terceira aparição independente do
padrão: P14-LZ (σ(μ)/μ chapado), desenho da LEP3 (configs na linha do
EP funcionam), agora aqui. Candidato a enunciado geral: em EP-2, custo
de estimação diverge para parâmetros ESPECTRAIS, não para o parâmetro
de controle que desdobra o EP.

## Notas de instrumento (trilha honesta)

v1 tinha três defeitos, todos apanhados pelas red flags da casa antes de
qualquer veredito: (1) refino de EP por grade caiu em basin errado
(gap 1e-9 espúrio por colapso de identidade) — substituído pela âncora
já refinada do shooting_ep_hunt + gates; (2) CRB via matriz de Gram em
dupla precisão (cond 1e24 = cond(J)², σ mascarado — padrão pinv) —
refeito por SVD de J; (3) bound de amplitude do modelo secular clipava o
parâmetro verdadeiro (b_true 19.6 vs bound 10) — corrigido; e a
degenerescência exata posto-2 das colunas de amplitude (simetria de
espelho: Im E₂ = −Im E₁) exigiu reparametrizar o nuisance para 2 graus
reais. Nenhum veredito muda entre v1 e v2 exceto a validade do
instrumento de P16.2.

## Saldo

Uma confirmação nova (P16.3, a proteção pós-EP), duas lápides (P16.1,
P16.2 — nº 16 e 17 do cemitério), e dois subprodutos conceituais: a
dependência de classe de observável na detectabilidade do canal de
Jordan, e a neutralidade ao EP da estimação do parâmetro de controle
(padrão agora visto 3×, candidato a teorema — PROVADO no mesmo dia: ver `THEOREM_EP_NEUTRALITY.md`, expoente 0 exato).
