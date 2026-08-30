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
