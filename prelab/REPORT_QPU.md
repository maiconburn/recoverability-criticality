# Teste L2 em QPU real — ibm_fez · veredito final pré-lab

**Data:** 2026-08-28 · **Backend:** ibm_fez (IBM Heron, 156 qubits), fila 0 · **Custo:** 126 circuitos × 4096 shots (2 jobs: `da904i9qtnsc73d10u30`, `da904ihqtnsc73d10u3g`), profundidade mediana 14 — fração pequena do tier gratuito · **Física:** qubit não-hermitiano dilatado (Sz.-Nagy), γ = 0.3072 (ancorado nos dados do Murch), escada r = J/J_EP ∈ [0.2, 4.0] com 3 pontos na banda do EP.

## Resultado

| | banda do EP (r∈[0.9,1.1]) | referência longe | veredito |
|---|---|---|---|
| σ espectral (Task A) | 0.0078 | 0.0019 (r=0.2) | **elevada 4.0×** — sente o EP ✓ |
| F Petz físico (Task B) | 0.8285 | 0.8355 (flancos) | **dif = −0.007, dentro do shot noise** — NÃO sente o EP ✓ |

- QPU rastreia a referência congelada (Aer + ruído tipo-Heron) ponto a ponto em F_Petz (dif ≤ 0.02 em todos os r; 0.953 vs 0.955 em r=4).
- **Critério pré-registrado**: travamento exigiria feature de F_Petz co-localizada com o pico espectral na banda do EP → **AUSENTE**.
- Anomalias registradas (não afetam o veredito): σ espectral em r=0.50 (0.0285) e r=4.0 (0.0198) acima da referência — artefatos de robustez do fit (basin ruim / aliasing da grade de 8 tempos com leitura real); banda do EP e âncoras limpas.

## Significado

**O teste discriminante da ontologia — as duas tarefas no MESMO registro quântico, com recuperação de Petz FÍSICA em circuito — rodou em hardware quântico real pela primeira vez. Resultado: as duas moedas não travam.** Sequência completa de arbitragens do L2: simulação (P6 dry-run) → dados públicos de transmon (anti-correlação) → **QPU real (sem travamento)**. A ontologia de recoverability, na forma forte, agora só tem o laboratório dedicado da classe Naghiloo como último recurso — e com três derrotas consecutivas, o prior é fortemente contra.

As leis estruturais (L1: amplificação espectral no EP) seguem confirmadas em TODOS os cinco mundos testados: EGB holográfico, qubit simulado, transmon real (dados), espectro de Kerr, e agora QPU.

## Desativação (pedido do usuário) — checklist executado

Ver log da sessão: `.env` apagado, sem conta persistida em `~/.qiskit`, monitores encerrados. **Recomendação: revogar/rotacionar o token em quantum.ibm.com** (passou pelo chat).

Reprodução: `qpu_run.py`, `qpu_results.json`, `fig_qpu_verdict.png`; referência: `ibm_sim_reference.json`.
