# P11 — congelado antes de medir (pergunta do autor: buracos de minhoca;
# "alguma forma de experimentar nossas ideias?")

Data: 2026-08-30. Modelo mínimo da literatura de ecos: barreira dupla
simétrica V(x) = (V0/2)[sech²(x−L/2) + sech²(x+L/2)] na coordenada
tortoise (duas "gargantas" separadas por L); V0 = 0.3, largura unitária.
QNMs por shooting em ω complexo com condições outgoing nas duas pontas
(Wronskian). O par fundamental vira DUPLETO simétrico/antissimétrico.

## P11.1 — splitting exponencial
δω(L) ≡ |ω₊ − ω₋| decai exponencialmente com a separação: ln δω linear em
L (R² > 0.98) na faixa L ∈ [6, 16].
MORTE: curvatura sistemática (power law ou saturação).

## P11.2 — hierarquia no dupleto (o custo de ver um buraco de minhoca)
CRB de estimar o splitting (amplitudes livres) do ringdown de duração
finita escala como δω^(−2±0.5), e amplitude com frequências livres como
δω^(−3±0.5) — mesma hierarquia do programa, agora dizendo: o SNR
necessário para DISTINGUIR buraco de minhoca de buraco negro por
espectroscopia agnóstica cresce exponencialmente com L (via δω(L)).
MORTE: expoentes fora das janelas.

## P11.3 — template vence agnóstico exponencialmente
Com frequências fixadas por template (busca modelada, estilo LVK), o
custo cai para δω^(−1±0.5); razão de SNR exigido
(agnóstico/template) > 10 no maior L da varredura.
MORTE: razão < 10, ou expoente template fora da janela.

## P11' (congelado 2026-08-30, após morte de P11.1, ANTES de medir)
Excitação especificada: equação de onda 1+1D, ∂²ψ/∂t² = ∂²ψ/∂x² − V(x)ψ,
mesma V de barreira dupla (U0=0.15, gargantas em ±L/2); condição inicial
pulso gaussiano ψ(x,0)=exp[−(x−x_s)²/2σ²], σ=2, x_s=−(L/2+15), ∂ψ/∂t(0)
tal que o pulso viaja para +x; observador em x_o=+(L/2+20); contornos
absorventes. Referência "buraco negro": barreira ÚNICA em x=+L/2, mesma
excitação e observador.

P11'.1 (ecos): o sinal do wormhole exibe trem de ecos com atraso entre
ecos Δt = 2L ± 15% (tempo de ida-e-volta da cavidade).
MORTE: sem trem, ou atraso fora da janela.

P11'.2 (detectabilidade): definindo D(SNR) a estatística de distinção
wormhole-vs-BH via Fisher no sinal completo (janela pós-prompt), o SNR
mínimo para 5σ cresce MONOTONICAMENTE com L na faixa L ∈ [8, 24] e a
razão SNR_min(L=24)/SNR_min(L=8) > 3.
MORTE: não-monotônico ou razão ≤ 3.

P11'.3 (template vence): busca com template completo do wormhole (forma
conhecida, só amplitude global livre) exige SNR ≥ 10× menor que a
detecção agnóstica de "energia extra pós-prompt" (janela cega) no maior L.
MORTE: razão < 10.
