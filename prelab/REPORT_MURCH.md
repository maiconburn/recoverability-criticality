# Teste pré-lab #2 — dados reais do transmon (murchlab) · resultado

**Data:** 2026-08-28 · **Fonte:** github.com/murchlab/Nonlinear-quantum-evolution-... (público, linhagem Naghiloo) · **Dataset usado:** `pf_pe_pg_july2nd.pkl` — varredura de 101 amplitudes de drive × 50 tempos, 18000 médias/ponto, observável P_f/(P_e+P_f) do qubit ef pós-selecionado (livre de convenção de fase) · **Previsões congeladas:** `FROZEN_MURCH.md`

## Setup extraído dos dados

- Modelo: H = [[−iγ, J],[J, 0]] pós-selecionado; γ global = **0.3072 rad/µs** (platô), J por amplitude.
- **EP localizado nos dados: amp\* ≈ 4.5×10⁻⁴, J\* = 0.1517 ≈ γ/2 = 0.1536** ✓, gap mínimo 0.049. Transição PT limpa (oscilante → sobreamortecido).

## Veredito (bootstrap, 30 réplicas/ponto, janela confiável amp ∈ [1.2e-4, 3.3e-3])

| Grandeza | no EP | mediana longe | razão |
|---|---|---|---|
| σ espectral (par de autovalores) | 0.0281 | 0.0087 | **3.2×** (e cresce ainda mais adentrando a fase quebrada) |
| σ recuperação de estado (n₀) | 0.0069 | 0.0285 | **0.24×** |

**As duas incertezas se movem em direções OPOSTAS através do EP**: o custo de estimar o espectro sobe aproximando/entrando na fase PT-quebrada; o custo de recuperar o estado inicial do MESMO registro desce. Em hardware quântico real:

- **P_A ✓** (lei L1, amplificação espectral perto do EP — consistente com tudo que medimos em EGB e no dry-run);
- **P_B ✓ com força extra** (QM padrão): não só ausência de pico conjunto — **anti-correlação** dos dois custos através do EP. A leitura de travamento da ontologia ("mesma moeda") é inconsistente com estes dados na forma forte.
- **P_C** (armadilha de Fisher) registrado: taxas vs N em dados ruidosos não discriminam; por isso este teste é de contraste-em-d, e o teste N-a-N decisivo continua sendo o desenho P6.

## Caveats honestos

- σ's são de bootstrap sobre refits do modelo — dependem do modelo H_eff 2-níveis; extremos de amplitude excluídos (amp < 1.2e-4: J não identificável; amp > 3.3e-3: regime não-linear do paper, resíduos sobem).
- "Recuperação de estado" = estimação de n₀ (estilo pretty-good), não o mapa de Petz físico; para o L2 pleno, ver desenho P6/IBM.
- Tomografia completa (CSVs x/±y) não foi usada nesta versão: convenções de sinal não documentadas (temp_tools.py ausente do repo) derrubaram os fits de coerência; populações bastaram para o contraste.

## Próximos da fila (ordem 2 → 1 → 3)

1. **#1 IBM**: pipeline de duas tarefas no simulador Qiskit (dilatação de Dogra + Petz de Biswas-Mandayam), congelar referência QM-padrão, depois 10 min de QPU do tier gratuito.
2. **#3 Kerr**: escada SXS em torno do avoided crossing (2,2,5)-(2,2,6) em a\*=0.8975 (549 simulações públicas; a mais próxima a d=2.6×10⁻⁴).

Reprodução: `analyze_sweepJ.py` (~2 min), `sweepJ_results.json`, `fig_murch_contrast.png`.
