# Teste pré-lab #1 — pipeline IBM de duas tarefas · referência congelada (simulador)

**Data:** 2026-08-28 · **Stack:** Qiskit 2.5.2 + Aer, ruído tipo-Heron (depol 3e-4/3e-3, readout 1–2%), 4096 shots/ponto · **Física:** qubit não-hermitiano H = [[−iγ, J],[J,0]] com γ = 0.3072/µs (ancorado nos dados reais do Murch), realizado por dilatação Sz.-Nagy (sistema+ancilla, pós-seleção ancilla=|0⟩).

## As duas tarefas, mesmo orçamento

- **Task A (espectral):** populações pós-selecionadas em 8 tempos → fit (J, γ) → par de autovalores; incerteza por bootstrap binomial dos counts.
- **Task B (recuperabilidade FÍSICA):** mapa de Petz do canal pós-selecionado implementado como SEGUNDO circuito dilatado (recovery em hardware, não estimação offline); fidelidade média sobre os 6 estados cardeais com dupla pós-seleção.

## Referência QM-padrão (congelada em `ibm_sim_reference.json`)

| r = J/J_EP | σ espectral | F Petz |
|---|---|---|
| 0.20 | 0.0022 | 0.841 |
| 0.80 | **0.0100** | 0.816 |
| 1.00 (EP) | 0.0062 | 0.817 |
| 1.20 | 0.0074 | 0.817 |
| 4.00 | 0.0035 | 0.955 |

- **Task A sente o EP**: σ espectral sobe ~4× na aproximação (pico no flanco r≈0.8–1.2 — mesma morfologia dos dados reais do teste #2).
- **Task B não sente**: F_Petz plana (0.81–0.82) através de r = 0.8→1.2; sem mergulho em r=1. Variação lenta com J vem só da contração global (monótona).
- **Critério para a QPU (pré-registrado):** travamento da ontologia exigiria feature em F_Petz co-localizada com o pico de σ espectral (mergulho ≥ 3σ_shot em r∈[0.9,1.1] ausente na referência). QM padrão = curvas acima dentro de barras.

## Estado e próximos passos

- Pipeline pronto e validado fim-a-fim com ruído realista; custo estimado de QPU: 9 valores de r × (8 tempos + 6 estados) × 4096 shots ≈ **bem dentro dos 10 min/mês do IBM Open Plan**.
- **Bloqueio único para rodar em hardware real: token IBM Quantum** (conta gratuita em quantum.ibm.com → API token). Com o token: trocar `AerSimulator` por `QiskitRuntimeService.backend(...)` — 10 linhas.
- Refinamentos antes da QPU (opcionais): grade r mais fina em [0.9, 1.1]; barras de erro de F_Petz; mitigação de readout.

Reprodução: `ibm_pipeline.py` (~2 min no Aer), `fig_ibm_reference.png`.
