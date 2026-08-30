# P8 — previsões congeladas (pré-registro, 2026-08-30; público desde a release v1.4)

Congeladas ANTES de qualquer verificação externa ou contato. Protocolo padrão
do repositório: cada previsão com critério de morte.

## Contexto
Rede de EP-2 provada na torre do patch estático de dS (ν ∈ ℤ; ponto físico
ν=1 ⇔ m² = 5/4·H²; ponto de fronteira ν=0 ⇔ m = 3/2·H = AHM logarithmic
operator). Camada de metrologia nossa; mecânica do log em ν=0 é prior art
(Arkani-Hamed–Maldacena 1503.08043, eq. 3.15 e nota 9).

## P8.1 — divergência universal do custo de estimação
Qualquer forecast de massa de espectador que inclua AMBAS as torres
(k_L/k_S)^{Δ±} com amplitudes livres exibirá σ(ν̂) = C/(S·|ν−ν_c|) perto de
ν_c ∈ {0, 1}, expoente −1.00 ± 0.05. Medido aqui: −1.002 (ν=0, C=2.0 exato
na janela r∈[0.05,0.6], 80 modos) e −1.022→−1.001 (ν=1, C=10.2).
MORTE: expoente fora de [−1.15, −0.85] em reanálise independente.

## P8.2 — resgate pelo canal logarítmico
Exatamente em ν_c, a informação de massa sobrevive apenas no coeficiente do
termo log (cadeia de Jordan; coeficientes exatos: soft factor ν=1 tem
−ln x·x³ com coef −1 e ¼ln²x·x⁵). Estimador com vínculo de cadeia:
σ_log = 2.7/S (nossa janela), FINITO.
MORTE: informação finita em ν_c sem usar o canal log (num modelo com ambas
amplitudes livres), ou canal log com informação nula.

## P8.3 — viés de pipelines sem log
Ajustar dados gerados em ν=1 (com o log físico presente) usando modelo de
dois power laws SEM log produz viés sistemático em ν̂ (empilhamento
observado em MC: viés +0.3 → estimativas colapsam para ν≈1 de longe;
quantificação fina pendente).
MORTE: MC bem calibrado sem viés.

## P8.4 — rede
Todo cruzamento de torre em ν ∈ ℤ é EP-2 (verificado ν=1,2,3 × 5 pontos,
posto-1 + Jordan ~1e-12). Previsão: nenhum cruzamento diabólico existe na
torre escalar do patch estático.
MORTE: um cruzamento com deficiência de posto 2.

## Status de novidade (auditado nesta sessão)
- Conhecido: log/Jordan em ν=0 (AHM 2015); EPs em QNMs Kerr-dS/SdS/RN-dS
  (2503.21276, 2512.06903, 2608.16521, 2601.00704); logs de Bessel inteiro.
- Não encontrado em abstracts nem nos full-texts checados (AHM 1503.08043;
  Chen–Wang 0911.3380; Moradinezhad Dizgah et al. 1801.07265): a REDE ν∈ℤ
  como EP-2 provado, a lei de custo σ = C/(S·d) nos pontos críticos, a
  janela de irresolubilidade, o resgate pelo canal log, o ln² como
  fingerprint de cadeia.
- Pendente: varredura full-text mais ampla (follow-ups de QSF/collider
  2016–2026) antes de claim público.

## Emenda A1 (2026-08-30, ANTES de qualquer teste externo)

P8.3 como escrita era mal-posta: exatamente em ν_c a verossimilhança em ν é
chata (é o conteúdo de P8.1), então "viés em ν̂" não é o observável certo.
Operacionalização corrigida (o texto original acima permanece para
auditoria):

**P8.3':** dados gerados em ν=1 com o termo log físico presente rejeitam o
modelo de dois power laws SEM log por qualidade de ajuste — medido:
χ²/dof = 12.3 (ruído 1e-3), 1.1×10³ (1e-4), 1.1×10⁵ (1e-5), janela
fiducial r∈[0.05,0.6], 80 modos — enquanto o modelo com canal log dá
χ²/dof = 1.00 e recupera o coeficiente da cadeia sem viés
(C = −0.3500 ± 0.0001 a ruído 1e-5, verdade −0.35).
MORTE: χ²/dof do modelo sem log compatível com 1 em dados com log físico,
ou C recuperado com viés > 3σ.

## P8-F2 (congelado 2026-08-30, ANTES de medir) — o log no objeto de duas escalas

Lição das fases anteriores: single-k é analítico em ν e não vê o log; o
log vive na estrutura de DUAS escalas. Objeto congelado: em quase-dS
(H = e^{−ε₁N}, m²/H² cruzando 5/4 em N*), o espectro a TEMPO FIXO
y(k) = k³|σ_k(N_ref)|², N_ref = N* + 6, para uma grade de k cujas saídas
de horizonte varrem o cruzamento. Em dS estático com ν=1, y(k) tem
(π²/4)y = k + [−ln k + c]k³ + ¼k⁵ln²k (nosso resultado exato).

P8-F2.1 (sobrevivência): o fit de y(k) na base {k, k³, k³ln k, k⁵, k⁵ln k}
melhora sobre a base sem logs com Δχ²/dof > 4, e o coeficiente do k³ln k
tem o sinal do estático (negativo), com amplitude atenuada
A ≡ |c_log/c_log^{estático}| ∈ (0.05, 1].
MORTE: sem melhora (log não sobrevive à varredura) ou A ≤ 0.05.

P8-F2.2 (localização): repetindo com m² tal que ν(N_exit da banda de k)
fique em 1±0.15 sem cruzar 1: |c_log| cai para < 0.3 do valor no
cruzamento.
MORTE: log igualmente presente longe do cruzamento (seria artefato de fit).

P8-F2.3 (atenuação pela varredura): A(ε₁) decresce monotonicamente em
ε₁ ∈ {0.002, 0.005, 0.01}.
MORTE: não-monotônico além do erro de fit.
