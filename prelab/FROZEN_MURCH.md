# Previsões congeladas — teste #2 (dados públicos murchlab, nonlinear-qubit)

Congelado 2026-08-28, ANTES de qualquer fit nos CSVs. Dataset: tomografia Rabi
do qubit ef pós-selecionado (linhagem Naghiloo), 10 amplitudes de drive com
razão r = J/J_EP ∈ {0.14, 0.42, 0.70, 1.00, 1.39, 2.09, 6.95, 13.9} — inclui
o ponto NO EP (r = 1.0000).

## P_A — amplificação espectral no EP (lei L1, ambas as leituras preveem)

A incerteza (bootstrap) da estimação do PAR de autovalores de H_eff a partir
do registro tem pico em r = 1, escalando ~1/gap; no ponto r = 1 o registro é
melhor descrito pela forma secular de bloco de Jordan (A + B·t)e^{−γt} do que
por senoide amortecida (ΔBIC > 10).

## P_B — o contraste (discriminador honesto em dados ruidosos)

O erro de RECUPERAÇÃO DO ESTADO INICIAL a partir do mesmo registro truncado é
SUAVE através de r = 1 (sem pico no EP): QM padrão. A leitura de travamento
da ontologia exigiria os dois erros com pico juntos no EP.

## P_C — armadilha de Fisher (documentação, não discrimina)

Com ruído de shot fixo, as taxas vs N de AMBAS as tarefas seguem ~N^{−1/2}
(envelope de Fisher) — travamento aritmético, sem conteúdo. Registrado para
mostrar por que o teste L2 decisivo exige o desenho P6 (registro quântico,
truncamento em modos), não truncamento temporal de dados ruidosos.

## Critérios

- P_A confirma se: pico de incerteza em r=1 com contraste ≥3× vs r=0.42/2.09,
  e ΔBIC secular > 10 no ponto r=1.
- P_B confirma QM padrão se: razão (erro de estado em r=1)/(média vizinhos)
  ∈ [0.7, 1.5] enquanto a razão espectral equivalente > 3.
- Qualquer pico conjunto dos dois erros no EP: assinatura anômala → escalar
  imediatamente (bug hunt primeiro, depois seria o primeiro indício real da
  ontologia em dados de hardware).
