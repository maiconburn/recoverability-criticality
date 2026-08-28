# Capacidade de Stahl v2 — a lei fechada (2026-08-28)

## Resultado central

**α_ρ(λ) agora é previsão de zero parâmetros ajustados**, computável sem nenhuma medição de escada QNM:

> **α_ρ(λ) = taxa de decaimento do funcional linear δρ_lin(N) = D_ρ[δb_N]**,
> onde δb_N = erro do Padé restrito de b (só teoria de aproximação) e D_ρ = resposta linear de ρ no EP (um solve barato por N no background exato).

### Validação nos 5 λ já medidos (modelo construído sem usar as taxas)

| λ | α_lin (previsto) | α_ρ (medido) | z |
|---|---|---|---|
| −0.100 | 1.027 | 1.026 ± 0.093 | 0.0 |
| −0.050 | 1.172 | 1.173 ± 0.084 | 0.0 |
| +0.020 | 1.358 | 1.360 ± 0.121 | 0.0 |
| +0.050 | 1.062 | 1.063 ± 0.087 | 0.0 |
| +0.080 | 0.872 | 0.851 ± 0.130 | +0.2 |

Regressão: slope 1.040, **R² = 0.9988** (gate K1-v2 exigia ≥ 0.9).

### Teste pré-registrado em λ virgens (congelado ANTES de medir)

| λ | congelado | medido | z |
|---|---|---|---|
| 0.035 | 1.1596 | 1.1595 ± 0.077 | −0.00 |
| 0.065 | 0.9239 | 0.9244 ± 0.073 | +0.01 |

## A estrutura por trás (o conteúdo físico)

1. **Perfil de Green empírico**: α_pt(z) = taxa pontual de |δb_N(z)| — cresce monotônico da borda (≈0.47) ao horizonte (≈3.1). É a função de Green do conjunto de Stahl medida diretamente, sem mapeamento conforme.
2. **Profundidade do observável**: α_lin coincide com α_pt(z*) em **z* ≈ 0.30–0.40 para todos os λ** — o canal crítico do EP "lê" a geometria no meio do bulk. A "profundidade informacional do observável" (turno 110) virou um número medível: z*.
3. **Por que o proxy v1 morreu**: a distância a um branch point ignora o perfil completo da Green e a localização do kernel. A taxa não é propriedade da singularidade sozinha — é a Green NO PONTO onde o observável mora.

## Bônus da rodada

- **Halving universal estendido: 7/7 backgrounds** (1.000, 1.000, 1.000, 1.001, 1.004, 1.001, 1.029).
- Trajetória do EP refinada com os pontos novos: q²_c suave em λ (−18.27 → −17.83 → −17.34 → −17.02 → −16.79 → −16.15).
- Splitting de canais: 1.24–1.56, persiste em toda a família.

## Consequência para o P4

A competição "singularidade de B vs singularidade de 𝒥" (fase 1) fica **subsumida**: o preditor exato não passa por distância-a-singularidade nenhuma — passa pelo perfil de Green + kernel. A pergunta viva do P4 vira: **a CMI de fronteira prevê z*?** (i.e., a profundidade do kernel é derivável de informação de emaranhamento?). Essa é a formulação correta para a fase 2.

## Reprodução

`results/v2_linear.json` (5 λ), `results/v2_frozen_fresh.json` (congelamento), `results/v2_fresh_test.json` (teste virgem). Método: seção B/C dos scripts desta rodada (resposta linear via ShootingSolver no EP; EPs novos por continuação em λ com seeds de Puiseux).
