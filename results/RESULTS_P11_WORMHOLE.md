# P11 — dupletos de buraco de minhoca: morte instrutiva por má modelagem

Previsões congeladas em FROZEN_P11_WORMHOLE.md; duas rodadas:
- v1 (shooting bilateral): VOID por instrumento (raízes com Im ω > 0,
  não-físicas; crescimento exponencial nas regiões proibidas engoliu a
  integração). Distinção instrumento≠física mantida.
- v2 (matriz de transferência analítica da barreira sech², r/t validados
  contra integração numérica a 10⁻¹⁰; modos todos físicos):
  **P11.1 MORTA como formulada** — o "splitting" medido CRESCE e satura
  (0.046→0.098 para L=6→16), consistente com espaçamento de torre de
  cavidade (~π/2L_eff), não com dupleto exponencial.

Diagnóstico: erro de modelagem no congelamento. O dupleto
simétrico/antissimétrico com splitting e^{-κL} pertence ao poço duplo
LIGADO; o buraco de minhoca é uma cavidade ABERTA entre duas barreiras,
cuja assinatura é a TORRE de modos de cavidade (os "ecos") sob o modo de
barreira — estrutura multi-modo, não dupleto fino. P11.2/P11.3: void por
premissa.

O que a morte ensina (candidata a P11' — NÃO congelada ainda): a
detectabilidade de buraco de minhoca é a tarefa de detectar modos de
cavidade de amplitude pequena sob o ringdown de barreira — "amplitudes
com frequências livres" da hierarquia, aplicada a uma torre. Exige
modelagem honesta da excitação (amplitudes relativas dos modos de
cavidade) antes de congelar de novo.

Dados: results/p11_wormhole.json (v1, void), p11_wormhole_v2.json.
Scripts: p11_wormhole.py, p11_wormhole_v2.py.

## P11' — vereditos finais (excitação simulada; três lições de modelagem)

Simulação de onda 1+1D honesta (pulso gaussiano, contornos absorventes,
referência = barreira única). Lição 3: o U0 = 0.15 congelado é
SUB-CRÍTICO (barreira quase transparente, sem trem de ecos) — regime
físico documentado: U0 = 0.5.

| Previsão | Veredito | Números (U0=0.5) |
|---|---|---|
| P11'.1 trem de ecos, Δt = 2L ± 15% | morta em U0=0.15; **CONFIRMADA L≥12 no regime físico** | Δt = 26.1/34.0/42.0/50.0 vs 2L = 24/32/40/48 (erros 4–9%; offset +2 ≈ travessia das barreiras) |
| P11'.2 SNR_min cresce com L | **MORTA** | SNR_template(L) PLANO (0.74–0.76): refletividade fixa ⇒ energia de eco constante; L controla resolvibilidade, não detectabilidade |
| P11'.3 template ≥ 10× melhor | **MORTA** | razão 4.5→5.9× (cresce com L, direção certa, magnitude menor) |

Detectores: autocorrelação crua e de envelope falham (colam na borda da
janela); peak-finding com altura ≥ 25% do máximo e distância ≥ L/2
funciona. Dados: results/p11_prime{,_echo,_u05}.json.

Estado da linha: pausada com saldo = trem validado + razão template/
agnóstico ~5× quantificada com amplitudes físicas. Herdeiras no radar:
torre ESPACIAL de anéis de fótons (lente/EHT) e atravessabilidade↔Petz
(ER=EPR) — ver memória do programa.
