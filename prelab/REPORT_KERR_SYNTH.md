# Teste pré-lab #3 (camada sintética) — lei de custo crítico no espectro de Kerr

**Data:** 2026-08-28 · **Fonte:** frequências QNM de Kerr tabuladas (pacote `qnm`, Teukolsky exato) · **Alvo:** avoided crossing (2,2,5)×(2,2,6) em a* = 0.8975 (gap mín. 0.067; EP verdadeiro em spin complexo a ≈ 0.897+0.010i, Lo et al.)

## Desenho

Ringdowns sintéticos com 8 overtones (amplitudes fixas conhecidas, fases congeladas por seed), ruído σ=1e-4, extração linear de amplitudes com frequências de Kerr fixas; bootstrap 60×; escada de 10 spins através do crossing.

## Resultado

| a | d=\|a−a*\| | gap(5,6) | σ(A5,A6) | σ(A0,A1) |
|---|---|---|---|---|
| 0.700 | 0.198 | 0.178 | 1.46 | 0.0040 |
| 0.880 | 0.018 | 0.093 | 2.74 | 0.0048 |
| **0.8975** | **0** | **0.067** | **3.60** | 0.0048 |
| 0.920 | 0.023 | 0.126 | 1.63 | 0.0043 |
| 0.950 | 0.053 | 0.240 | 0.73 | 0.0040 |

- **Pico exatamente no crossing**, simétrico, com **saturação** no valor imposto pelo gap finito (EP em spin complexo) — a forma "amplificação 1/gap com corte" prevista pelas leis L1.
- **corr(log σ_par, −log gap) = 0.912** ao longo de toda a escada.
- Canal-especificidade: modos baixos (A0, A1) planos (razão de custo até **749×**).

## Leitura

A lei de custo crítico validada em EGB/qubit transfere para o espectro de um buraco negro astrofísico real (Kerr): extrair o par de overtones perto do avoided crossing custa ordens de magnitude mais informação, com o teto ditado pela distância do EP complexo. Consequência observacional: remanescentes com spin ~0.90 (GW190521-like) são exatamente os piores para overtone-fitting do par 5-6 — testável na camada SXS/GWOSC (próxima: ondas NR reais, 549 sims mapeadas).

Reprodução: bloco em `kerr_synthetic.json` (script no histórico da sessão; ~30 s).
