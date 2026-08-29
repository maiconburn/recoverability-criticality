# P8 fase 1 — o ponto excepcional cosmológico (LOCAL, NÃO COMMITADO)

Data: 2026-08-29/30. Status: cadeia interna completa; NOVIDADE NÃO AUDITADA
— proibido claim externo antes da auditoria de literatura (cosmological
collider: Arkani-Hamed–Maldacena e sequência; degenerescências ν∈ℤ e termos
log podem ser conhecidos em parte).

## Cadeia (cada elo verificado por máquina nesta sessão)

### Elo 1 — EP-2 no horizonte de de Sitter: DEMONSTRADO
Escalar massivo, patch estático dS₄, ℓ=0, colocação QEP com ansatz
(1−x²)^{−iω/2} (equação: x(1−x²)u''+(2iωx²+2−4x²)u'+(ω²x+3iωx−m²x)u=0;
validada contra a torre analítica a ~10⁻³).
No ponto ν=1 (m²=5/4, unidades H=L=1), ω₀=−5i/2:
- menor valor singular de L(ω₀): 9.4e-13 (deficiência de posto 1 ⇒
  multiplicidade geométrica 1 — NÃO diabólico);
- condição de Jordan ⟨w₀|L'(ω₀)|u₀⟩ = 1.3e-12 (escala O(1)) ⇒ EP-2;
- abertura sob δV = εx²(1−x²): teoria de perturbação do feixe quadrático dá
  (δω)² = (9/4)ε EXATO (c₁ = 2.25000 numérico) ⇒ s = 3√ε; a série numérica
  de splittings converge: s²/ε = 8.0 (ε=0.02) → 9 (ε→0). ✓

### Elo 2 — assinatura observável: termo logarítmico no bispectro squeezed
A expansão squeezed carrega as torres (k_L/k_S)^{Δ±+2n}, Δ± = 3/2±ν.
Em ν=1: Δ−+2 = Δ+ = 5/2 — dois termos coincidem; o mecanismo padrão de
expoentes degenerados + bloco de Jordan força
    log(k_L/k_S)·(k_L/k_S)^{5/2}.
(Derivação analítica do coeficiente: pendente — próxima tarefa; o mecanismo
é standard, o conteúdo novo é a identificação com o EP-2 do patch estático.)

### Elo 3 — lei de custo no observável: σ(ν̂) ∝ |ν−1|^{−1}
Cramér–Rao exato (Fisher 3-par (ν, A₊, A₋) marginalizado), sinal
S(r) = A₊r^{3/2+ν} + A₋r^{7/2−ν}, r∈[0.05,0.6], 80 pontos:
expoente −1.022 global, slopes locais → −1.001 monotônico. Divergência de
custo limpa no ponto crítico. (MC ingênuo dá artefato de otimizador —
empilhamento em ν=1 com viés +0.3; usar CRB/likelihood profiling.)

## Enunciado candidato (calibrar após auditoria)
Campos espectadores com m² = 5/4·H² (ν=1) são um ponto crítico da
espectroscopia cosmológica: a estimação da massa a partir de correlatores
squeezed tem custo divergente ∝ 1/|ν−1|, e exatamente na criticalidade o
bispectro desenvolve running logarítmico — impressão digital observacional
de um ponto excepcional do horizonte cosmológico. Conexão direta com o
programa cosmological collider (CMB-S4, LSS, 21cm).

## Pendências
1. Auditoria de novidade (bloqueante para claim externo).
2. Coeficiente analítico do termo log (elo 2).
3. Rede ν=2,3,...: base numérica adaptada (colocação perde modos profundos).
4. Ligação quantitativa com slow-roll físico (ν efetivo do espectador em
   quase-dS; distância ao EP como função de parâmetros de inflação).
5. Mapear a tarefa do elo 3 na hierarquia 1/2/3 do programa (aqui: expoentes
   reais + amplitudes livres ⇒ −1; formalizar).

## Adendo (mesma sessão) — elo 2 EXATO

Fator soft do espectador ν=1 (função de modo dS, H_1):
    (π²/4)·x³·|H₁(x)|² = x + [−ln x + c₃]·x³ + [¼·ln²x + …]·x⁵ + …
verificado contra mpmath a 10⁻²⁴. O log entra na ordem relativa (k_L/k_S)²
com coeficiente EXATO −1; a ordem seguinte carrega ln² (colisão dupla de
torres) — fingerprint específico da cadeia de Jordan, que um log acidental
não produz. Nota de calibração: logs em ν inteiro são fato clássico de
Bessel; o conteúdo novo é (i) a identificação com o EP-2 do patch estático
(prova de posto + 9/4), (ii) o ln² como assinatura da cadeia, (iii) a lei de
custo σ ∝ |ν−1|⁻¹ na estimação — o composto não aparece em buscas de
abstract (WebFetch/arXiv API; auditoria full-text pendente).

## Adendo 2 — REDE COMPLETA + fórmula da janela crítica

Teste de posto direto em L(ω₀) nos pontos analíticos da rede (ordens 140 e
200, estáveis): ν=1 (Ω=2.5, 4.5), ν=2 (Ω=3.5, 5.5), ν=3 (Ω=4.5) — TODOS
com deficiência de posto 1 e ⟨w₀|L'|u₀⟩ ~ 10⁻¹²–10⁻¹⁴. **Toda
degenerescência de torre do patch estático em ν ∈ ℤ é EP-2** (linhas de EP:
infinitas colisões por ν). Único ponto não-taquiônico: ν=1 ⇔ m² = 5/4·H².
(A falha anterior em "ver" os pontos fundos era do solver de autovalores
global — o teste de posto no ω₀ analítico não sofre disso.)

Constante da lei de custo (da tabela CRB, r∈[0.05,0.6], 80 modos):
σ_CRB·|ν−1| = 10.2 (constante a <1% para |ν−1| ≤ 0.06). Logo, com
sinal-ruído total S no setor squeezed:
    σ(ν̂) = 10.2 / (S·|ν−1|)   ⇒   janela de irresolubilidade
    |ν−1|* = √(10.2/S)
— dentro dela o erro excede a distância ao ponto crítico: a massa do
espectador é IRRESOLVÍVEL. (S=100 → janela 0.32; S=1000 → 0.10. A constante
10.2 depende da janela de r e do número de modos — recalibrar por
experimento; a ESTRUTURA 1/(S·|ν−1|) é o conteúdo.)

## Adendo 3 — TEOREMA EXATO (álgebra de Γ) e correções internas

Redução hipergeométrica exata da equação validada (z=x²):
z(1−z)g'' + [3/2 − (5/2−iω)z]g' − [(m²−ω²−3iω)/4]g = 0, com
a,b = 3/4 ∓ ν/2 − Ω/2, c = 3/2 (ω = −iΩ). Condição de QNM (anulação do ramo
ingoing na fórmula de conexão): W(Ω) ∝ 1/[Γ(a)Γ(b)]. Torres
Ω = 3/2 ∓ ν + 2n (= López-Ortega ✓).

**Teorema (mapa completo de EPs):** a ordem de Jordan de cada QNM é a ordem
do zero de W. Logo: (i) ν genérico — todos simples; (ii) ν ∈ ℤ⁺ — cada
colisão de torres é zero duplo ⇒ EP-2, e NUNCA de ordem superior (há só dois
fatores Γ); (iii) ν=0 — a≡b ⇒ toda a torre é EP-2 nível a nível (o
logarithmic operator de AHM é o nível n=0). Unfolding exato em ν=1:
W ∝ [(ν−1)² − (Ω−5/2)²]/4 ⇒ Ω± = 5/2 ± (ν−1).

**Correções internas (artefatos meus, capturados pelo teorema antes de
qualquer registro externo):** a exploração numérica de "EP-3/EP-4/ordem-7"
em ν=0 era artefato do teste de cadeia matricial (contaminação de componente
nula no lstsq além de k=2) — RETIRADA; o "autovalor simples" em Ω=1.5 era a
truncação da colocação separando o par degenerado. O ln² observado em
x⁵ do fator soft é |função de modo com log|² — consistente com EP-2.

Status final da fase 1: estrutura de EP do escalar no patch estático de dS
resolvida EXATAMENTE; camada de metrologia (σ = C/(S·d), janela
√(C/S), resgate pelo canal log) verificada numericamente sobre essa base.

## Adendo 4 — deriva de slow-roll através do EP (pendência 4 fechada, analítico)

Em quase-dS, ν² = 9/4 − m²/H² com H decrescendo (ε₁ = −Ḣ/H²):
    dν/dN_e = −(m²/H²)·ε₁/ν = −(9/4 − ν²)·ε₁/ν  ⇒  em ν=1: dν/dN = −(5/4)ε₁.
Um espectador próximo do EP é VARRIDO através dele a (5/4)ε₁ por e-fold. O
tempo (em e-folds) dentro da janela de irresolubilidade |ν−1| < √(C/S):
    ΔN = (8/5)·√(C/S)/ε₁ ,
e como cada modo k congela em um ν(N) diferente, a assinatura log fica
LOCALIZADA numa banda Δln k = ΔN do espectro. Exemplo: S=10³, ε₁=0.005 →
janela |δν|<0.10, ΔN ≈ 32 e-folds — banda larga; S=10⁵, ε₁=0.02 → ΔN ≈ 0.8
e-fold — feição estreita e localizada. A posição da banda mede QUANDO
m²/H² cruzou 5/4; a largura mede ε₁/√S. Isso transforma o EP num RELÓGIO:
feição log localizada em k ↔ instante do cruzamento crítico. (Fase 2:
fazer o matching modo-a-modo honesto em quase-dS; aqui é o limite adiabático.)

## Adendo 5 — forma fechada de C: tentativa refutada

Hipótese natural C = 1/(|A₊−A₋|·√F⊥) (canal r^{3/2}ln r com peso (A₊−A₋)ν
no limite ν→0): REFUTADA — previa C ∝ 1/|A₊−A₋| (19.7/6.6/3.9 para
D=0.1/0.3/0.5) e o medido quase não move (1.79/2.0/2.28). A informação
dominante não vem do canal linear-em-ν; C fica como constante numérica
dependente de janela (recalibrar por experimento). NÃO publicar a derivação
ingênua.

## Adendo 6 — universalidade cruzada de famílias (EGB, parcial)

Ladder de reconstrução Padé ancorado no EP da FAMÍLIA FUNDA (λ=0.120,
ω_c=−9.730063i, q²_c=−32.285, âncora gap 3.1e-6):
**α_off = 0.805 constante através de 3 décadas de distância**
(d ∈ [3.2e-4, 1e-1]: 0.8051/0.8051/0.8050/0.8048/0.8041/0.8021) — a
estrutura exponencial da lei de custo transfere para o segundo estrato do
espectro. Halving no EP: ABERTO — a medição exige relocação do EP por nível
N; a versão simplificada mostrou patologia par/ímpar em d=0 (N par: ε~O(1),
perda de identidade) e relocações que vagam na floresta; driver completo
adaptado (run_validation_deep.py, guarda |Δq²|<0.5) em execução. d=1e-4
saturado (piso da âncora). Dados: results/deep_ladder_final.json.

## Adendo 7 — assinatura exata em ν=0 (tabela completa)

(π²/4)·x³·|H₀(x)|² = x³·[ln²x + 2(γ−ln2)·ln x + π²/4+(γ−ln2)²] + O(x⁵ln²)
— verificado numérico×analítico a 5 casas (resíduo 4e-13). Contraste dos
dois pontos críticos:
- ν=0 (m=3H/2): ln² em ORDEM DOMINANTE, coeficiente exato 1.
- ν=1 (m²=5H²/4): ln simples em ordem RELATIVA (k_L/k_S)², coeficiente −1;
  ln² uma ordem acima.
Assinaturas distinguíveis entre si e de qualquer log acidental — par de
fingerprints fechado para os dois alvos observacionais.
