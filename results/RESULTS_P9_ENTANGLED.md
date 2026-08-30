# P9 — sonda emaranhada vs a lei de custo no EP (resultado de um dia; calibrado)

Pergunta: uma ancilla emaranhada compra de volta parte do custo gap^-p
perto de um ponto excepcional?

Setup: canal PT pós-selecionado K(t)=exp(-iH_eff t), H_eff=[[0,J],[J,-iγ/2]],
EP em J=γ/4. Três estratégias com orçamento de shots fixo (ruído por
quantidade medida ∝ √N_quantidades): A = sonda |0⟩ (coluna 0 de K);
B = sonda (|00⟩+|11⟩)/√2 com ancilla ociosa (K inteiro num setting);
C = sondas |0⟩ e |+⟩ (K inteiro, dois settings, sem emaranhamento).
CRB marginalizado para splitting (amplitudes livres) e amplitude
(frequências livres). Script: scripts/entangled_probe_ep.py; dados:
results/entangled_probe_ep.json.

Resultado:
- Expoentes (janela gap 0.07–0.87): A: −1.26 / −2.62; B: −1.08 / −2.46;
  C: idêntico a B por construção do modelo de ruído.
- No ponto mais crítico: ganho de prefator ≈ 1.4× de A para B/C, em ambas
  as tarefas.

Leitura: **o emaranhamento não altera o escalonamento** gap^-p; entrega o
mesmo que a diversidade clássica de settings (B ≡ C), com vantagem apenas
operacional (uma preparação). Consistente com os limites fundamentais de
sensing não-Hermitiano (arXiv:1805.11760), agora na linguagem de tarefas
do programa.

Caveats/aberto: (i) modelo de ruído aditivo por quadratura não captura
medidas coletivas/conjuntas — vantagem quântica por MEDIDA fica em aberto;
(ii) janela de gap finita distorce expoentes (~0.2); (iii) sem execução em
hardware — não se justifica para um prefator 1.4× explicado
classicamente.
