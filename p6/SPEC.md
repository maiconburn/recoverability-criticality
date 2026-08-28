# P6 — Especificação Final Congelada: Travamento de Taxas (Petz vs. Espectral) em um Qubit Dissipativo com EP de 2ª Ordem

**Versão:** 2.0-FINAL (pós-arbitragem) · **Data de congelamento:** 2026-08-28 · **Unidades:** Γ = 1, ħ = 1.
**Status:** especificação implementável; o dry run in-silico REALIZA o desfecho da física padrão (prova de validade do protocolo, não teste da ontologia). O teste da ontologia é a rodada de laboratório (circuito supercondutor classe Naghiloo com filtro de Purcell estruturado implementando J(ω)). Todo número desta especificação é congelado ANTES de qualquer desmascaramento; campos marcados `[FASE-0]` são obrigatoriamente computados e congelados pelo dry run endurecido antes da rodada discriminante.

---

## 0. Sumário dos números congelados

| Grandeza | Valor congelado |
|---|---|
| Configurações (q, W) | S-A = (0.9, 2) âncora · S-B = (0.5, 2) escada-q · S-C = (0.5, 1) primária/polo fundo |
| EP em S-A | g_EP = 0.232342, δ_EP = −0.054897, λ_EP = −0.00423 − 0.17402 i |
| Constante de Puiseux (S-A) | C = 0.0302; expoente medido 0.5003 ± 0.01 |
| EP em S-B, S-C | `[FASE-0]` (método da colisão, Seç. 1.4) |
| α_spec previsto (por N) | ln(1/q + √(1/q² − 1)) = **0.46715** (q = 0.9) · **1.31696** (q = 0.5) |
| α_Petz previsto (por N) | 2 ln\|x + √(x² − 1)\|, x = λ_res/W: **0.174** (S-A; medido 0.169) · S-B ≈ 0.17 `[FASE-0]` · S-C ∈ [0.40, 0.50] `[FASE-0]`, gate ≥ 0.40 |
| Razões padrão α_Petz/α_spec | S-A: 0.372 · S-B: ≈ 0.13 · S-C: ≈ 0.34 (exatos em `[FASE-0]`) |
| Separações (certificado ≥ 2×) | S-A: 2.7× · S-B: ≈ 7.6× · S-C: ≈ 2.9× |
| Previsão da ontologia | razão = 1.00 ± 0.2 em todo d e TODA configuração; halving no EP nas DUAS taxas |
| Escada de distâncias | d ∈ {0.3, 0.1, 0.03, 0.01, 0.003} ∪ {0}, d = (g − g_EP)/g_EP, δ = δ_EP fixo |
| Grade de truncamento | N ∈ {4, 6, …, 60} (par); janelas comuns: S-A [8, 36], S-B [8, 20], S-C [8, 30] |
| Numéricos | M = 1200 (auditoria 2400), T = 150, NREF = 200 (auditoria 400), σ_ruído = 1e−8, seed = 20260828 |

---

## 1. Modelo (matrizes explícitas, valores numéricos)

### 1.1 Sistema e Hamiltoniano total

Qubit de trilho duplo (uma excitação em duas cavidades a, b). Base lógica: |a⟩ ≡ |1_a 0_b⟩, |b⟩ ≡ |0_a 1_b⟩. A cavidade **a** acopla a UMA banda fotônica estruturada (a torre infinita); **b** é sem perdas.

Bloco do sistema:

```
H_S = [ δ   g ]
      [ g   0 ]        (base {|a⟩, |b⟩})
```

Setor de uma excitação do Hamiltoniano hermitiano total, dimensão M + 2, base {|a⟩, |b⟩, |m⟩, m = 1..M}:

```
H_tot = δ |a⟩⟨a| + g (|a⟩⟨b| + |b⟩⟨a|) + Σ_m ω_m |m⟩⟨m| + Σ_m g_m (|a⟩⟨m| + |m⟩⟨a|)
```

A conservação da excitação torna a evolução heralded exatamente linear (classe Naghiloo linear; sem não-linearidade de pós-seleção). A física não-hermitiana vive no Hamiltoniano efetivo dependente de energia H_eff(z) = [[δ + Σ(z), g], [g, 0]]. No limite Markoviano W ≫ Γ o modelo reduz ao canônico H_eff = [[0, g], [g, −iγ]] com γ = Γ/2, EP em g = Γ/4, δ = −Γq/4 (cancela o desvio de Lamb).

### 1.2 Banho (a torre infinita) e formas fechadas

Densidade espectral em [−W, W], nula fora:

```
J(ω) = (Γ / 2π) · sqrt(1 − (ω/W)²) · (1 − q·ω/W)
```

Congelado: Γ = 1; q ∈ {0.9, 0.5}; W ∈ {2, 1} conforme a configuração. μ₀ = ∫J dω = ΓW/4. Baths semicírculo puro ou Lorentziano são EXCLUÍDOS (classes Bernstein–Szegő/pseudomodo terminam finitamente — modo de falha verificado).

Autoenergia em forma fechada (u = z/W, R(u) = sqrt(u − 1)·sqrt(u + 1), ramos principais de CADA sqrt separadamente — nunca sqrt(u² − 1)):

```
Σ_I (z) = (Γ/2) · [ (u − R(u))·(1 − q·u) + q/2 ]      (folha física)
Σ_II(z) = (Γ/2) · [ (u + R(u))·(1 − q·u) + q/2 ]      (segunda folha, troca de ramo)
```

Verificações obrigatórias: Im Σ_I(ω + i0) = −πJ(ω) na banda; Σ_I(z) → μ₀/z = ΓW/(4z) para |z| → ∞; Σ_I(0) = −iΓ/2 + Γq/4.

A cadeia de Jacobi (Lanczos/Mori) da medida J tem coeficientes convergindo GEOMETRICAMENTE à cadeia de Chebyshev livre (a_n → 0, b_n → W/2) na taxa exata (zero da função de Szegő em ω = W/q fora da banda):

```
α_chain(q) = 2·ln(1/q + sqrt(1/q² − 1))   [por sítio]
           = 0.93430 (q = 0.9) · 2.63392 (q = 0.5)     (verificado a 4 dígitos no dry run)
```

### 1.3 Discretização (congelada)

Nós e pesos de Gauss–Chebyshev-U, m = 1..M, M = 1200 (auditoria: 2400):

```
x_m = cos(mπ/(M+1));  λ_m = (2/(M+1))·sin²(mπ/(M+1));  ω_m = W·x_m
w_ref(ω) = (2/(πW²))·sqrt(W² − ω²)         (medida de referência normalizada)
Δ_m = λ_m / w_ref(ω_m)                     (peso de quadratura em dω)
g_m = sqrt( J(ω_m) · Δ_m )
```

### 1.4 Ponto excepcional: localização e escada

O EP (2ª ordem) resolve, na segunda folha, F(z) = (z − δ − Σ_II(z))·z − g² = 0 junto com dF/dz = 0. MÉTODO CONGELADO (o Newton 4D ingênuo em (F, F′) trava — modo de falha verificado): Newton 2D na função de colisão analítica s(g, δ) = (z₁ − z₂)², com o par de raízes rastreado por continuação (homotopia desde a semente Markoviana g = Γ/4, δ = −Γq/4, deformando W: ∞ → W_alvo em 20 passos logarítmicos).

Congelado (S-A, dry run): **g_EP = 0.232342, δ_EP = −0.054897, λ_EP = −0.00423 − 0.17402 i** (unidades de Γ). Ordem 2 verificada: |λ₊ − λ₋| = |C|·d^0.5003±0.01 sobre d ∈ [0.003, 0.3], C = 0.0302. `[FASE-0]`: os mesmos quatro números para S-B e S-C, com os mesmos gates (resíduo de colisão |z₁ − z₂| < 1e−6; expoente de Puiseux 0.50 ± 0.05).

Parâmetro de distância: **d = (g − g_EP)/g_EP** ao longo do eixo g, com δ = δ_EP fixo. Escada: d ∈ {0.3, 0.1, 0.03, 0.01, 0.003} ∪ {0}.

Autovalores de referência λ_±(d) (a "verdade"): raízes de F com Σ_II em forma fechada, Newton em mpmath (dps = 50), com verificação cruzada contra a cadeia exata de NREF = 200 sítios + cauda transparente (concordância < 1e−12 — gate).

---

## 2. Definição de N (idêntica para as duas tarefas)

### 2.1 A cabeça de dados única

**N = número de modos detectores retidos** (inteiro par, N ∈ {4, 6, …, 60}). Modos detectores da FAMÍLIA 1 (congelada): polinômios ortonormais da medida semicírculo de referência — na grade,

```
ũ_k[m] = sqrt(λ_m) · U_k(x_m),   k = 0..N−1     (U_k = Chebyshev de 2ª espécie)
```

Estes vetores são EXATAMENTE ortonormais para k < M (quadratura de Gauss). São uma "autobase do detector" fixa, agnóstica ao modelo.

Amplitudes espectrais emitidas (Seç. 3, passos 1–2): γ^(i)[m], i ∈ {a, b}. A cabeça de dados no truncamento N é a matriz N × 2:

```
(A_N)_{k,i} = Σ_m ũ_k[m] · γ^(i)[m]
```

**AMBAS as tarefas recebem exatamente A_N (2N números complexos) e NADA mais.** A tarefa Petz constrói o canal a partir de A_N; a tarefa espectral consome A_N via o mapa triangular abaixo. Mesmo array em memória, mesmo hash SHA-256 registrado no log de cada ponto.

### 2.2 As três faces e o mapa triangular publicado

(i) **Momentos do registro.** R_j^(i) = ∫ ω^j sqrt(w_ref(ω)) γ^(i)(ω) dω, j = 0..N−1. Bijeção triangular exata com as projeções (expansão do monômio em U_k):

```
ω^j = W^j · 2^{−j} · Σ_{m=0}^{⌊j/2⌋} [ C(j,m) − C(j,m−1) ] · U_{j−2m}(ω/W),  C(j,−1) := 0
⇒ (P_N)_{j,k} = W^j 2^{−j} (C(j,m) − C(j,m−1)) para k = j − 2m; 0 caso contrário
R^(i) = P_N · A_N[:, i]
```

P_N é triangular inferior, invertível; **não há fatoriais** (a variante com 1/k! imporia um envelope fatorial comum às duas tarefas — EXCLUÍDA, ver Seç. 5).

(ii) **Modos de ambiente:** as próprias N projeções (A_N). Face operacional congelada.

(iii) **Geometria reconstruída:** n_J = ⌊N/2⌋ sítios de Jacobi do banho, obtidos pelo estimador da Seç. 4 (2·n_J parâmetros reais ≤ conteúdo da cabeça).

**Resolução da falha fatal do árbitro (descompasso 2N−1 vs. N):** a convenção antiga entregava 2N−1 momentos ao lado espectral e N modos ao lado Petz — fator ~2 oculto na razão. AGORA: uma única cabeça A_N para ambas. Conversão declarada e publicada: **α(por sítio) = 2·α(por N)**; todas as taxas desta especificação são POR N. Consequência nos números: α_spec(por N) = α_chain/2 = ln(1/q + √(1/q²−1)) = 0.46715 (q=0.9) / 1.31696 (q=0.5); as razões padrão antigas (0.18/0.065, por sítio) tornam-se 0.372/0.13 (por N).

**Gate D1 (invariância de convenção):** reajustar todas as taxas com eixo n_J em vez de N deve multiplicar ambas por exatamente 2 e deixar TODAS as razões idênticas ao float64; qualquer desvio voida a rodada.

**Redundância declarada:** vale a identidade exata R_j^(a) = R_{j+1}^(b)/g (pois γ^(a)/γ^(b) = ω/g ponto a ponto). Ou seja, a coluna a adiciona exatamente UM nível de momento da coluna b. O estimador espectral pode usar as duas colunas no objetivo (Seç. 4.3); é PROIBIDO qualquer dado além de A_N. A identidade é usada como gate de consistência C1: max_j |R_j^(a) − R_{j+1}^(b)/g| < 1e−10 (réplica exata).

### 2.3 Janelas de ajuste congeladas (por configuração)

| Config | Janela comum (razão K1) | Sub-janelas (estabilidade) | Petz estendida (secundária) |
|---|---|---|---|
| S-A | N ∈ [8, 36] | [8, 22] / [22, 36] | [8, 60] |
| S-B | N ∈ [8, 20] | [8, 14] / [14, 20] | [8, 60] |
| S-C | N ∈ [8, 30] | [8, 18] / [18, 30] | — (já ≥ 4.3 décadas) |

K1 primário em S-A e S-C; S-B é ponto de escada/certificado (janela comum curta pelo piso espectral). Décadas de decaimento Petz na janela: S-A ≈ 2.1 (estendida ≈ 3.9), S-C ≈ 4.3 (satisfaz a exigência ≥ 4 décadas do árbitro na configuração primária).

**Regra de piso (simétrica):** um ponto (N, tarefa) só entra no ajuste se eps > 100 × piso numérico da tarefa (piso_Petz = 1e−12; piso_spec = auditado por mpmath, Seç. 6.4-h). Ponto excluído de uma tarefa é excluído da estatística de RAZÃO para ambas (nunca do ajuste individual da outra — reportar ambos).

### 2.4 Réplica ruidosa

Ruído gaussiano iid complexo por entrada retida de A_N: Re e Im ~ N(0, σ²), σ = 1e−8, gerador `numpy.random.default_rng(20260828)`. Sorteado UMA vez por (config, d) para as 60 projeções máximas; as cabeças A_N são prefixos do mesmo sorteio; a MESMA realização é entregue às duas tarefas. Janela ruidosa: truncada no maior N com eps_exato > 100σ_propagado; exclusões simétricas na razão.

### 2.5 Segunda família de detector e cláusula de gradação

**Família 2 (robustez de base, correção 7b):** peso plano w_B = 1/(2W) em [−W, W] (Legendre). Construção na grade: v_k[m] = sqrt(Δ_m · w_B(ω_m)) · P̃_k(ω_m/W) com P̃_k Legendre ortonormal, seguido de QR com reortogonalização completa. Exigência: RAZÕES de taxas invariantes em 10% entre famílias 1 e 2 (as taxas individuais podem mudar de prefator; as previsões de Bernstein/Szegő dão o MESMO expoente para qualquer peso Szegő na mesma banda).

**Relatividade de gradação (correção 8):** α_Petz é relativo à base detectora. Uma base adaptada ao canal (SVD) trivializa a tarefa em N = 2 (o canal complementar tem posto 2) e é EXCLUÍDA. Os critérios de morte aplicam-se à família 1 congelada; os proponentes da ontologia endossam esta base ou nomeiam a sua, com números, ANTES do desmascaramento. Silêncio = endosso. Não existe rota de escape pós-hoc "gradação errada".

---

## 3. Procedimento Petz passo a passo

### 3.1 Emissão (uma vez por (config, d))

1. Montar H_tot (Seç. 1.1, 1.3), dimensão M + 2. `numpy.linalg.eigh` → (E, V).
2. Evoluir as duas colunas de base: ψ^(i)(T) = V·exp(−iE T)·V†·e_i, i ∈ {a, b}, **T = 150**. Gate G10: amplitude residual no sistema ‖P_S ψ(T)‖ < 5e−12 (S-A: e^{−0.174·150} ≈ 4.6e−12; S-C: ≈ 1e−15).
3. Remover fases livres → amplitudes espectrais emitidas independentes de T:

```
γ^(i)[m] = exp(+i ω_m T) · ⟨m|ψ^(i)(T)⟩
```

Forma analítica (para verificação e para a perna aprendida): γ^(i)[m] = g_m · G_{a,i}(ω_m + i0), com G(ω) = inv([[ω − δ − Σ_I(ω+i0), −g], [−g, ω]]), i.e. γ^(a) = g_m·ω_m/D, γ^(b) = g_m·g/D, D(ω) = (ω − δ − Σ_I(ω+i0))·ω − g².

### 3.2 O canal truncado

A_N (Seç. 2.1) é N × 2 com A_N†A_N ≤ I (automático: A_N = Π_N·V_emissão). Canal quântico legítimo E_N: estado do qubit → (bloco mantido C^N) ⊕ (flag 1-dim |⊥⟩):

```
Kraus: E_0 = A_N;   E_i = sqrt(k_i)·|⊥⟩⟨v_i|,  i = 1, 2
onde B = I₂ − A_N†A_N = Σ_i k_i |v_i⟩⟨v_i|  (autodecomposição 2×2)
```

O déficit de informação de E_N em N finito é o objeto de estudo — NÃO é um piso de ruído.

### 3.3 Mapa de Petz exato

Estado de referência congelado σ_ref = I/2 (prior de ignorância; Petz = mapa pretty-good/retrodição). S = E_N(I/2) = diag(S_kept, s_flag), S_kept = A_N A_N†/2 (N×N, posto ≤ 2, pseudo-inversa no suporte com corte 1e−13·máx autovalor), s_flag = Tr(B)/2.

```
Kraus da recuperação: R_0 = (1/√2)·A_N†·S_kept^{−1/2}   (bloco mantido)
                      R_i = (1/√2)·sqrt(k_i/s_flag)·|v_i⟩⟨⊥|
```

### 3.4 Fidelidade — forma fechada congelada

Fidelidade de entrelaçamento F_e(R_N ∘ E_N) = (1/4)·Σ_{m,n} |Tr(R_m E_n)|² (termos cruzados mantido/flag anulam-se identicamente — verificado). Com s₁, s₂ = autovalores de A_N†A_N (2×2!), k_i = 1 − s_i, s_flag = (2 − s₁ − s₂)/2, obtém-se a forma fechada exata:

```
F_e(N) = (1/8) · [ 2·(√s₁ + √s₂)² + (k₁² + k₂²)/s_flag ]
F̄(N) = (2·F_e + 1)/3          (fórmula exata de qubit; sem Monte Carlo)
```

Verificações: s₁ = s₂ = 1 ⇒ F̄ = 1; s₁ = s₂ = 0 ⇒ F̄ = 1/2. Cross-checks obrigatórios (uma vez por config): (a) fórmula geral de Kraus reproduz a forma fechada a < 1e−12; (b) MC Haar de 200 estados (seed 7) concorda com F̄ a < 1e−3.

### 3.5 Métrica de erro e ajuste

```
eps_Petz(N) = F̄_complete − F̄(N),   F̄_complete = F̄ com todos os M modos (gate G9: ≥ 0.999;
              valor S-A d = 0.3 congelado: 0.99993)
```

α_Petz = −inclinação de ln eps_Petz vs N na janela congelada. **Modelo composto (correção 2):** ajustar `eps = C_e·e^{−αN}` E `eps = C_e·e^{−αN} + C_a·N^{−p}` (componente algébrica de van Hove da borda de banda), p livre em [2, 4]. Gates: dominância exponencial C_a·N^{−p} < 0.1·C_e·e^{−αN} em todo N da janela (senão encolher a janela pelo topo e reportar); deslocamento de α entre os dois modelos < 5%; R² ≥ 0.98; reportar BIC de ambos e do puro power-law. CIs de 95%: bootstrap de resíduos (2000 réplicas) + jackknife de sub-janelas.

Previsão analítica congelada (lei de Bernstein): **α_Petz = 2·ln|x + sqrt(x²−1)|, x = λ_res/W** (elipse de Bernstein do polo de ressonância da amplitude emitida). S-A: 0.1738 (medido 0.169, dentro de 3%). S-C: alvo ≥ 0.40; se `[FASE-0]` der α_Petz(S-C) < 0.40, ativar o fallback congelado W = 0.8 (mesmos gates).

### 3.6 Perna de canal aprendido (correção 6 — limite da assimetria de informação lateral)

A perna primária conhece E_N exatamente. A perna secundária NÃO: constrói a recuperação a partir do canal RECONSTRUÍDO da mesma cabeça. Com θ̂_N do ajuste espectral (Seç. 4, mesmo N): Ĵ, Σ̂_I, D̂ ⇒ γ̂^(i)[m] = sqrt(Ĵ(ω_m)·Δ_m)·(ω_m ou g)/D̂(ω_m + i0) ⇒ Â_N ⇒ Kraus R̂ pelas fórmulas 3.3 com Â_N. Fidelidade da composição mista R̂_N ∘ E_N (canal verdadeiro, recuperação aprendida), fórmula geral:

```
F_e = (1/8)·| Tr(Â† Ŝ_kept^{−1/2} A) |² + (1/8)·Σ_{ij} (k̂_i k_j / ŝ_flag)·|⟨v_j|v̂_i⟩|²
```

Reportar α_Petz^known e α_Petz^learned nas mesmas janelas. **Uma alegação de travamento só conta se sobreviver na perna aprendida.**

### 3.7 Ponto d = 0 (perna do EP)

Mesmo pipeline em g = g_EP. O pulso de bloco de Jordan (A + Bt)·e^{−iλ_EP t} produz projeções ∝ (a + b·k)·ρ^{−k}; ver o modelo-curva K2 na Seç. 6.3.

---

## 4. Procedimento espectral passo a passo

### 4.1 Entrada

A MESMA A_N (e a mesma réplica ruidosa). Conhecidos do estimador: g, δ, W, Γ e a classe analítica de J (classe Szegő com fator polinomial) — NÃO os valores de q nem os coeficientes da cadeia. Estimando: o par de autovalores (λ₊, λ₋) na segunda folha.

### 4.2 Estimador congelado: casamento de momentos restrito à classe

Parâmetros (todos reais): θ = (μ₀; a_0..a_{n_J−1}; b_1..b_{n_J−1}), **n_J = ⌊N/2⌋** (2·n_J parâmetros ≤ 4N dados reais — sobredeterminado). Modelo direto:

```
Σ_θ(z) = μ₀ / (z − a_0 − b_1²/(z − a_1 − ... − b_{n_J−1}²/(z − a_{n_J−1} − t(z))))
cauda transparente:  t_I(z) = (z − sqrt(z−W)·sqrt(z+W))/2      [folha física]
                     t_II(z) = (z + sqrt(z−W)·sqrt(z+W))/2      [segunda folha]
na banda: t_I(ω + i0) = (ω − i·sqrt(W² − ω²))/2
```

(a cauda transparente = condição de onda de saída, análogo exato da condição de horizonte ingoing do protocolo EGB; é ela que dá segunda folha à reconstrução racional). Na grade:

```
J_θ(ω_m) = −Im Σ_θ(ω_m + i0)/π          (guarda: passo rejeitado se min J_θ < 0)
D_θ(ω_m) = (ω_m − δ − Σ_θ(ω_m+i0))·ω_m − g²
γ_θ^(a)[m] = sqrt(J_θ(ω_m)·Δ_m)·ω_m/D_θ ;  γ_θ^(b)[m] = sqrt(J_θ(ω_m)·Δ_m)·g/D_θ
A_N^model(θ)_{k,i} = Σ_m ũ_k[m]·γ_θ^(i)[m]
```

Objetivo (Levenberg–Marquardt, `scipy.optimize.least_squares`, xtol = ftol = 1e−14):

```
r(θ) = vec[ Re, Im ]( A_N^model(θ) − A_N^data )     (as duas colunas; 4N resíduos reais)
```

Casar A_N ou R_N é equivalente (P_N triangular invertível — a face é a mesma informação); congela-se o casamento direto de A_N. Inicialização por CONTINUAÇÃO EM N: θ̂(N) parte de θ̂(N−2) preenchido com (a = 0, b = W/2); N inicial = 4 parte da cadeia Markoviana. Aceitação (réplica exata): ‖r(θ̂)‖_∞ < 1e−10. Dois reinícios aleatórios (perturbação 1%) devem reconvergir ao mesmo θ̂ (< 1e−8) — gate contra mínimos locais.

**Por que este estimador e nenhum outro (carga estrutural):** qualquer rota que reconstrua γ(ω) ponto a ponto a partir da cabeça truncada (inversão autoconsistente de J, ou Lanczos direto da medida de emissão |γ_b|²) herda a taxa de BERNSTEIN do polo — e forçaria travamento parcial por construção. O casamento restrito à classe compara dados e modelo ATRAVÉS do mesmo fator de polo, cancelando-o; o erro remanescente é o da cauda da cadeia (invariante de Szegő puro). Estas rotas proibidas são controles negativos obrigatórios (Seç. 5.4).

### 4.3 Autovalores

```
F_N(z) = (z − δ − Σ_θ̂^{II}(z))·z − g² = 0,   Σ^{II} = fração continuada 4.2 com t_II
```

Newton com sementes de Puiseux λ_EP ± Ĉ√d MAIS grade de 8 sementes no círculo de raio 2|Ĉ|√d em torno de λ_EP (o salto de raiz para o pseudo-corte da reconstrução é o risco dominante — observado e corrigido no dry run). Auditorias por raiz reportada: |F_N(λ̂)| < 1e−10; distinção de par |λ̂₊ − λ̂₋| > 1e−8 (fora do EP); consistência de continuação em d e em N.

### 4.4 Métricas de erro (congeladas)

```
eps_spec(N, d) = ( |λ̂₊ − λ₊(d)| + |λ̂₋ − λ₋(d)| ) / 2       [unidades de Γ]
```

referências λ_±(d) da Seç. 1.4 (forma fechada + mpmath, 1e−14). Em d = 0 (modelo quadrático local): ẑ_c = raiz de F_N′ (Newton, semente λ_EP); splitting espúrio s̃ = sqrt(|F_N(ẑ_c)| / |F_N″(ẑ_c)/2|);

```
eps_spec(N, 0) = |ẑ_c − λ_EP| + s̃/2
```

**Controle e_param (correção 7a):** registrar junto, para todo (N, d),

```
e_param(N) = max( |μ̂₀ − μ₀|/μ₀, max_j |â_j − a_j|, max_j |b̂_j − b_j| )
```

contra a cadeia exata de referência — separa halving de Puiseux genuíno de patologia do localizador de raízes: a previsão padrão é e_param ~ e^{−(α_chain/2)·N} SEM halving em d = 0, enquanto eps_spec halva.

α_spec = −inclinação de ln eps_spec vs N, mesmas janelas, mesmo modelo composto, mesmos gates e CIs da Seç. 3.5. Réplica em q = 0.5: pontos com eps < 1e−12 exigem confirmação mpmath (Seç. 6.4-h).

### 4.5 Precisão estendida

Ajustes em float64; gate de piso G8: para 3 valores de N preregistrados por configuração (os 3 mais fundos da janela), recomputar resíduo, F_N e autovalores em mpmath (dps = 50) no θ̂ ajustado; desvio relativo de eps_spec < 10%.

---

## 5. Botão de desacoplamento e por que travamento NÃO é tautológico aqui

### 5.1 Os dois invariantes analíticos independentes

- **α_spec** é fixado pela convergência Szegő/Jacobi da MEDIDA do banho — posição do zero da função de Szegő, ω = W/q. Botão: **q**. Valor por N: ln(1/q + √(1/q²−1)). Independente de W e de Γ.
- **α_Petz** é fixado pelo parâmetro de elipse de Bernstein do POLO de ressonância da amplitude emitida — profundidade |Im λ_res|/W. Botão: **Γ/W**. Independente de q (em ordem dominante; o EP desloca-se fracamente com q — quantificado em `[FASE-0]`).

### 5.2 Escadas bilaterais congeladas (correção 5)

| Escada | Configurações | Previsão padrão |
|---|---|---|
| Escada-q (Γ/W fixo = 0.5) | S-A → S-B | α_spec: 0.467 → 1.317 (**2.82×**); α_Petz pinado (< 10%) |
| Escada-Γ/W (q fixo = 0.5) | S-B → S-C | α_Petz: ≈ 0.17 → ≈ 0.45 (**≈ 2.7×**); α_spec pinado (< 3%) |

**Certificado preregistrado (Fase 0, antes de qualquer desmascaramento):** separação padrão α_spec/α_Petz ≥ 2× em TODA configuração usada (valores: S-A 2.7×, S-B ≈ 7.6×, S-C ≈ 2.9×) E cada taxa movida ≥ 2× por seu botão enquanto a outra fica pinada. Nota: a quarta célula (q = 0.9, W = 1) tem razão padrão ≈ 1 por acidente numérico e é EXCLUÍDA como configuração de teste — travamento observado só conta replicado nas TRÊS configurações certificadas.

### 5.3 Por que não é tautologia

1. **Cabeça única, funcionais distintos:** ambos os estimadores consomem exatamente A_N; eps_Petz é função apenas dos autovalores do Gram 2×2 A_N†A_N (Seç. 3.4); eps_spec é função do ajuste de cadeia na classe. Nenhuma estatística suficiente compartilhada além da cabeça preregistrada.
2. **Física padrão prevê taxas DIFERENTES, com botões independentes** — dois invariantes de duas singularidades diferentes do mesmo modelo. O certificado ≥ 2× é a prova quantitativa de que travar não está embutido.
3. **Mesmo canal físico, sem setores desacoplados:** o estado desconhecido e a informação espectral viajam pela MESMA emissão do MESMO sistema acoplado (evita o strawman de setores disjuntos que matou a proposta rival P3).
4. **Nulos totalmente numéricos** (nada de "c ∈ [1,2] a medir" — falha da rival P2); referências externas exatas, sem autorreferência de warm-start.

### 5.4 Desenhos rejeitados (tautologias e contaminações documentadas — controles negativos obrigatórios no código)

- Estimação de momentos com ruído fixo: todo estimador regular atinge o piso à MESMA taxa (envelope de Fisher) — travamento aritmético; demonstrado (saturação em N ≈ 6). EXCLUÍDO.
- Níveis de Taylor com 1/k!: envelope fatorial comum força decaimento superexponencial compartilhado. EXCLUÍDO.
- Banho de dois band-gaps na cavidade b: pontos de ramo internos contaminam ambos os registros (arrasta α_Petz para ≈ 0.09 com curvatura algébrica). EXCLUÍDO.
- Base detectora adaptada (SVD do canal): trivializa Petz em N = 2. EXCLUÍDA (Seç. 2.5).
- Extração de polos agnóstica (matrix-pencil/Prony sobre momentos hermitianos): platô no valor da distância ao corte (≈ 0.65) — controle negativo reproduzível.
- Inversão pontual de J ou Lanczos da medida de emissão: trava no invariante de Bernstein — controle negativo NOVO obrigatório (demonstra por que 4.2 é como é).

### 5.5 Assimetrias declaradas (não escondidas)

O lado Petz conhece o canal; o lado espectral conhece (g, δ, W, classe). Intrínseco à comparação estado-vs-parâmetro; LIMITADO pela perna de canal aprendido (3.6), que remove o conhecimento exato do canal. Métricas congeladas: eps_Petz = déficit de F̄; eps_spec = distância média de autovalores em Γ. Por transparência reporta-se também a razão com a métrica de amplitude sqrt(eps_Petz); a decisão usa SÓ as métricas congeladas (a escolha de métrica é parte do preregistro — sem escape pós-hoc de convenção).

---

## 6. Previsões congeladas (ontologia vs. física padrão) e critérios de morte

### 6.1 Física padrão (computada e congelada pelo dry run; o dry run É mecânica quântica padrão)

- **S1 (espectral fora do EP):** eps_spec(N, d) = (C₀/√d)·e^{−α_spec·N}, α_spec = 0.46715 (q = 0.9) / 1.31696 (q = 0.5) por N, independente de d na escada. Prefator 1/√d: expoente p_d = 0.50 ± 0.07 na regressão ln eps_spec (N fixo = 16) vs ln d — `[FASE-0]` fim-a-fim com rastreamento endurecido (a verificação anterior foi contaminada por salto de raiz; refazer é OBRIGATÓRIO antes do congelamento final). Custo de informação: N* = const + (1/(2·0.467))·ln(1/d) por alvo de erro fixo (q = 0.9) — a lei EGB transportada.
- **S2 (espectral NO EP):** eps_spec ~ e^{−α_spec·N/2} — halving APENAS espectral; alvo `[FASE-0]`: α_spec(0)/α_spec(0.3) ∈ [0.45, 0.55]; e_param SEM halving simultâneo (Seç. 4.4).
- **S3 (Petz):** eps_Petz(N) = C·e^{−α_Petz·N}, α_Petz = 0.174 (S-A; medido 0.169, R² 0.993) / ≈ 0.17 (S-B) / ∈ [0.40, 0.50] (S-C) `[FASE-0]`. SEM prefator 1/√d: p_d = 0.00 ± 0.05 (regressão em N fixo = 20). No EP: sem halving assintótico; curva padrão congelada eps(N) = (A + B·N)²·e^{−α₀·N} com α₀ TRAVADO no valor fora-do-EP (só A, B livres) — inclinação local deriva PARA CIMA com N.
- **S4 (razões):** α_Petz/α_spec = 0.372 (S-A) / ≈ 0.13 (S-B) / ≈ 0.34 (S-C) — fortemente ≠ 1 e dependente de botão.
- **S5 (canal aprendido):** α_Petz^learned = α_Petz^known dentro de 10% (o aprendizado da cadeia converge mais rápido que o déficit de Bernstein nas configurações certificadas) — `[FASE-0]`; se falhar, a perna aprendida vira apenas-diagnóstico e isso é registrado antes do desmascaramento.

### 6.2 Ontologia (geometria de recuperabilidade)

- **O1:** α_Petz/α_spec = 1.00 ± pequeno em TODO d e nas TRÊS configurações certificadas (por N, na cabeça congelada).
- **O2:** AMBAS as taxas halvam no EP: α(0)/α(0.3) = 0.50, exponencial limpa, sem deriva de janela, nas duas tarefas.
- **O3:** o prefator 1/√d aparece TAMBÉM em eps_Petz (p_d = 0.50), e o custo de informação Petz ganha o mesmo termo (1/2α)·ln(1/d).

### 6.3 K2 endurecido (correção 3): curva-padrão no EP, lado Petz

Em d = 0, configuração primária S-C (secundária: S-A janela estendida), ajustar DOIS modelos de 2 parâmetros:

```
M_std: eps(N) = (A + B·N)² · e^{−α₀·N}     (α₀ = α̂_Petz fora do EP, TRAVADO)
M_ont: eps(N) = C · e^{−α₀·N/2}
```

Estatística: ΔBIC = BIC(M_std) − BIC(M_ont).
- **RETIRAR a ontologia (lado EP-Petz)** se ΔBIC < −10 E as inclinações das duas sub-janelas derivarem para cima (consistente com M_std), com halving espectral S2 presente.
- **CANDIDATO** somente se ΔBIC > +10 E o ajuste livre der α_Petz(0)/α_Petz(0.3) ∈ [0.40, 0.60] com R² ≥ 0.98 E sub-janelas concordando em 10%.
- Qualquer outro desfecho: VOID (inconclusivo; recondicionar — nunca conta como confirmação nem retirada).

### 6.4 Critérios de morte e gates

**K1 (travamento de taxas — primário).** Para cada configuração e cada d da escada: ρ̂ = α̂_Petz/α̂_spec na janela comum, CI de 95% (bootstrap de resíduos 2000× + jackknife de sub-janelas).

- **RETIRAR a ontologia** se |ln ρ̂| > ln(1.25) em ≥ 3 dos 5 pontos d, com CIs excluindo ρ = 1, em qualquer configuração certificada (i.e., os dados concordam com as razões padrão congeladas 0.372/0.13/0.34 e não com 1).
- **CANDIDATO a lei nova** somente se TODAS: ρ̂ ∈ [0.8, 1.25] com CI excluindo a razão padrão em ≥ 4 de 5 pontos d; nas TRÊS configurações S-A, S-B, S-C (réplica de botão obrigatória — travamento em um só botão = coincidência/artefato); sobrevivendo na perna de canal aprendido; razões invariantes em 10% na família 2 de detector.

**K2:** regra da Seç. 6.3. Petz sem halving com halving espectral presente ⇒ ontologia retirada.

**K3 (gates de validade — falha VOIDA a rodada, não retira a ontologia):**
- (a) Exponencialidade composta: dominância ≥ 10:1 do termo exponencial na janela, deslocamento de α < 5% entre modelos, R² ≥ 0.98, BICs reportados (substitui o exp-vs-power nu).
- (b) Certificado de desacoplamento: separações ≥ 2× em toda configuração; escadas 5.2 com taxa movida ≥ 2× e taxa pinada (< 3% espectral, < 10% Petz).
- (c) Puiseux 0.50 ± 0.05 nas duas configurações q; prefatores p_d conforme S1/S3.
- (d) Qualidade do EP: resíduo de colisão < 1e−6; |F| < 1e−10; par rastreado por continuação.
- (e) Discretização: todas as α deslocam < 3% sob M → 2M e NREF → 2NREF.
- (f) Réplica ruidosa: taxas concordam < 5% na sub-janela válida.
- (g) Auditoria de raízes: 100% das raízes com |F| < 1e−10, distinção de par, continuação consistente.
- (h) Pisos: G8 mpmath (< 10% nos 3 N fundos); regra dos 100× (Seç. 2.3), exclusões simétricas na razão.
- (i) Robustez de base: razões famílias 1↔2 em 10%.
- (j) e_param: taxa α_chain/2 por N em 5%, inclusive d = 0 (sem halving).
- (k) Gates de construção: G10 heralding < 5e−12; G9 F̄_complete ≥ 0.999; C1 identidade de registro < 1e−10; D1 invariância de convenção exata; cross-checks 3.4.

### 6.5 Lista FASE-0 (computar e congelar ANTES do desmascaramento da rodada discriminante)

1. EPs de S-B e S-C (g_EP, δ_EP, λ_EP, C, expoente de Puiseux) pelo método 1.4.
2. Tabela T0: α_Petz (known + learned, famílias 1 e 2) e α_spec, nas 3 configurações, com CIs — na convenção por-N.
3. α_Petz(S-C) ≥ 0.40 (senão fallback W = 0.8 e repetir 1–2).
4. Certificado bilateral 5.2; razões padrão exatas S4.
5. Verificação fim-a-fim do 1/√d espectral e do halving espectral no EP (S2), com rastreamento endurecido, nas duas configurações q.
6. Parâmetros (A, B) da curva-padrão K2 em S-C e S-A.
7. Controles negativos 5.4 reproduzidos; todos os gates K3 verdes.
Registro: JSON com hashes SHA-256 de todas as cabeças A_N, seeds, versões, e os números acima — arquivado antes de qualquer dado de laboratório.

---

## 7. Plano de implementação (funções, laços, runtime estimado)

### 7.1 Módulos (numpy + scipy.optimize.least_squares + mpmath)

```
p6/
  bath.py     J(w,Gamma,W,q); nodes_weights(M,W)->(x,lam,omega,Delta); couplings->g_m;
              Sigma_closed(z,sheet,Gamma,W,q)  [formas 1.2, vetorizada + variante mp]
  model.py    H_total(g,delta,omega,g_m); evolve_columns(H,T)->psi_a,psi_b;
              strip_phases->gamma[M,2]; gamma_analytic (3.1, verificação)
  modes.py    cheb_modes(N)->Utilde[M,N]; legendre_modes(N); P_matrix(N,W);
              project(gamma,Utilde)->A_N (+ SHA-256); add_noise(A,sigma,rng)
  petz.py     gram_eigs(A_N)->(s1,s2); F_bar_closed(s1,s2); F_bar_complete;
              kraus_general(A_N) [cross-check]; haar_mc(200,seed=7);
              learned_leg(theta_hat,...)->F_bar_mixed (3.6); eps_petz_curve
  fitspec.py  cf_sigma(theta,z,sheet,W); forward_A(theta,...); residual(theta);
              fit_chain(A_N,theta_init)->theta_hat  [LM, continuação em N, guarda J>=0,
              2 reinícios]; roots_pair(theta_hat,seeds)->(l+,l-)+auditorias;
              ep_local(theta_hat)->(z_c,split); e_param(theta_hat,ref)
  refs.py     find_EP(config) [homotopia W + Newton 2D em s(g,delta)=(z1-z2)^2];
              lambda_ref(d) [Sigma_II fechada + mp dps=50]; ref_chain(NREF=200,mp);
              puiseux_fit(escada)
  controls.py prony_hermitiano (platô ~0.65); lanczos_emissao (trava Bernstein);
              inversao_pontual (trava Bernstein); ruido_fixo_fisher (tautologia)
  analysis.py fit_exp / fit_composite / bic / bootstrap_jackknife_ci;
              k1_verdict / k2_verdict / gates_report / tabelas / D1_invariance
  phase0.py   executa e congela a lista 6.5 (JSON assinado)
  run_all.py  laço mestre + logs por ponto (hash, seeds, gates)
```

### 7.2 Laços mestres

```
FASE 0: for cfg in [S-A,S-B,S-C]: find_EP; puiseux; T0; certificado; curva K2; gates
FASE 1: for cfg in [S-A,S-B,S-C]:
          for d in [0.3,0.1,0.03,0.01,0.003,0]:
            eigh(H_tot) 1x; 2 evoluções; F_bar_complete
            for N in range(4,61,2):
              A_N (mesmo array/hash p/ ambas) [+ réplica ruidosa]
              Petz: known + learned + família 2      -> eps_Petz(N)
              Espectral: fit_chain -> raízes/EP-local -> eps_spec(N), e_param(N)
          ajustes (composto), razões, K1; d=0: K2
        auditorias: M->2M (pontos escolhidos), NREF->2NREF, G8 mp, controles negativos
```

### 7.3 Runtime (laptop, 1 núcleo, float64, M = 1200; medidas do protótipo escalonadas)

| Bloco | Custo |
|---|---|
| Fase 0 completa (3 EPs + certificados + curvas) | ~20 min |
| eigh 1202² + 2 evoluções, por (cfg × d) = 18× | ~3 s cada, ~1 min |
| Petz forma fechada, 29 N por ponto (Gram 2×2) | < 1 s |
| Espectral LM com continuação, 29 N por ponto | ~5–20 s |
| Grade completa 3 cfg × 6 d, todas as pernas | ~30–60 min |
| Réplica ruidosa + família 2 + learned (reusa evoluções) | +15 min |
| Auditoria M = 2400 (eigh ~20 s) em pontos escolhidos | +15 min |
| G8/referências mpmath (dps = 50) | ~10 min |
| **Total** | **~1.5–2.5 h, < 1.5 GB RAM** |

### 7.4 Riscos conhecidos (endurecimentos obrigatórios, observados nos protótipos)

1. Salto de raiz de Newton para o pseudo-corte → grade de sementes + |F| < 1e−10 + continuação.
2. Localizador de EP como sistema 4D trava → SEMPRE a forma de colisão 2D com homotopia em W.
3. Ramos: computar sqrt(z−W)·sqrt(z+W), NUNCA sqrt(z²−W²).
4. LM em n_J grande: continuação em N + guarda J_θ ≥ 0 + 2 reinícios; falha de reconvergência = ponto VOID.
5. Pseudo-inversa de S_kept: corte 1e−13·máx; posto deve ser 2 (gate).
6. Deconvolução funcional/pontual de γ truncado no lado espectral: PROIBIDA (Seç. 5.4).
7. Banhos Bernstein–Szegő (torre finita): excluídos pela classe de J.

### 7.5 Mapa correções-do-árbitro → seções

| Correção | Onde |
|---|---|
| 1. Cabeça única + mapa triangular + recomputação + invariância | 2.1–2.3, D1, 6.4-k |
| 2. Polo fundo (α_Petz ≥ 0.4) / ≥ 4 décadas / modelo composto | S-C, 2.3, 3.5, 6.4-a |
| 3. Curva-padrão K2 preregistrada | 6.3 |
| 4. 1/√d + halving espectral fim-a-fim endurecidos | 6.1-S1/S2, 6.5-5, 4.3 |
| 5. Desacoplamento bilateral (escada Γ/W) | 5.2, 6.4-b |
| 6. Perna de canal aprendido | 3.6, K1 |
| 7. Controles e_param + segunda base | 4.4, 2.5, 6.4-i/j |
| 8. Relatividade de gradação vinculada | 2.5, 6.5 |
| 9. Pisos numéricos e gates simétricos | 2.3, 4.5, 6.4-e/f/h |
