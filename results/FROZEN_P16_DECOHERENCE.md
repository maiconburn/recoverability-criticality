# P16 — decoerência como quarta tarefa: previsões congeladas (pré-registro, 2026-08-31)

Congeladas ANTES de qualquer medida. Protocolo padrão: cada previsão com
critério de morte.

## Contexto e motivação

A conjectura fundadora (lápide 1: "curvatura forte pode suprimir
decoerência?") está morta na forma original: Danielson–Satishchandran–Wald
provaram que todo horizonte de Killing decoere superposições
(arXiv:2205.06279, arXiv:2301.00026 — títulos verificados na API do arXiv
em 2026-08-31). Reburial refinado e testável: a taxa de decoerência não é
suprimida pela curvatura — ela HERDA a estrutura crítica espectral do
fundo. Decoerência = quarta tarefa na hierarquia de expoentes.

Sonda: qubit em dephasing puro acoplado ao campo no fundo EGB; o que a
sonda vê é a função de Green do par fundamental de QNMs. Estrutura exata
do canal: r(t) = Im[(e^{−iω₁t} − e^{−iω₂t})/(ω₁ − ω₂)] — oscilador
amortecido; no EP espelho vira o canal secular t·e^{−γt} (bloco de
Jordan), o mesmo canal log/polinomial de P8.

## Instrumento (congelado)

Família fundamental, λ = 0.105, EP espelho ancorado em q² ≈ −34.386
(par-semente [0.02−7.1641i, −0.02−7.1641i], kernel_compare). Shooting com
continuação sequencial; refino do EP por zoom em |ω₁−ω₂|; varredura
log-espaçada de δ = q² − q²_c nos dois lados. Ruído sintético congelado:
branco, σ = 1e-3 do máximo do sinal, rng seed 16. Grade t ∈ [0, 4/γ_EP],
400 pontos.

## P16.1 — resgate pelo canal secular (gêmeo aberto do P8.2)

Fit do sinal ruidoso com M_sec = Re[(a + bt)e^{−iwt}] vs
M_nosec = Re[A₁e^{−iω₁t} + A₂e^{−iω₂t}] com AMPLITUDES LIMITADAS
(|A| ≤ 10·max|r|; lição do P8-F2 v1: sem o limite, amplitudes ±1/gap
divergentes compensam o secular e o teste é cego — armadilha conhecida,
neutralizada no congelamento).
PREVISÃO: Δχ²/dof(nosec − sec) > 4 em gap/γ_EP ≤ 0.01 e < 1 em
gap/γ_EP ≥ 0.5 (localização no EP, como P8-F2.2).
MORTE: sem rejeição no EP, ou rejeição igual longe do EP (artefato).

## P16.2 — expoente da tarefa de estimação por decoerência

CRB para δq² estimado do sinal r(t) com as 2 amplitudes complexas livres
(nuisance, marginalizadas). Derivação congelada: tarefa de splitting tem
expoente 2 no gap (hierarquia {1,2,3} do EP-2); o unfolding √ dá
Jacobiano |dδω/dδq²| ∝ gap⁻¹; composição: σ(δq²) ∝ gap^(−1.0).
PREVISÃO: expoente p ∈ [0.6, 1.5] no fit log-log de σ(δq²) vs gap
(lado subamortecido).
MORTE: p fora da faixa (nova classe — informativo, mas mata ESTA
previsão). Portões de condicionamento: inversão explícita, cond(I)
reportado, mpmath se cond > 1e12 (regra da casa pós-P14/P15).

## P16.3 — proteção pós-EP com kink de raiz quadrada (a nova)

No lado sobreamortecido, um dos canais fica MAIS longevo:
Γ_slow(δ) = γ_EP − B·|δ|^h. O fantasma digno da conjectura fundadora:
atravessar o ponto crítico protege parcialmente a coerência de um canal.
PREVISÃO: h ∈ [0.4, 0.6] (kink de raiz quadrada, dΓ/dδ → −∞ no EP);
lado subamortecido com Γ_slow plano (|slope|/γ_EP < 0.05 na mesma
janela); splitting dos dois lados com expoente 0.5 ± 0.1.
MORTE: sem proteção (Γ_slow ≥ γ_EP), ou expoente fora de [0.4, 0.6].

## Risco de sobreposição (declarado antes de medir)

P16.2 pode reduzir-se a confirmação da hierarquia já medida em outro
observável (valor: universalidade entre classes de observável, não
descoberta). P16.3 é a afirmação nova. Se TUDO se reduzir a reanálise de
ringdown já publicada por nós, veredito honesto = "confirmação
cross-observável", não descoberta.
