# Programa de Pesquisa Priorizado — Geometria de Recoverability

## 1. Diagnóstico: o que a teoria tem e o que falta

**O que existe de sólido.** Dos 17 enunciados auditados no corpus, cerca de metade é física estabelecida reescrita em vocabulário de saturação/informação (Misner-Sharp, Smarr, QES/Engelhardt-Wall, gravidade superficial); a maior parte do restante é derivável com trabalho modesto de teoria de perturbação não-hermitiana (Kato/Puiseux), teoria de catástrofes e teoria de convergência Padé/Stahl. A validação de 2026-08-28 estabeleceu três coisas reais: (i) um resultado espectral novo e possivelmente publicável — o EP-2 genuíno do QNM escalar fundamental com seu parceiro-espelho em q²c = -16,1472 no brane EGB λ=0,08, incluindo o negativo útil de que o par ω₀/ω₁ nunca colide; (ii) uma proeza numérica real — o solver de shooting (Frobenius de 14ª ordem) contornando o condicionamento ~1e10 da colocação de Chebyshev; (iii) a confirmação quantitativa de P1-P4 congeladas no turno 112 (γ = 0,498±0,062; halving da taxa 1,03±0,22; colapso livre de parâmetros; lei logarítmica com R²=0,999). A disciplina metodológica — congelamento prévio, fits honestos, autofalsificação da versão "um α universal" — é genuína e rara.

**O que falta para ser revolucionária.** O veredicto da auditoria é inequívoco: a estrutura confirmada é um corolário de duas peças de livro-texto (sensibilidade √ de um EP-2 genérico + convergência exponencial de Padé), e qualquer esquema exponencialmente convergente aplicado a qualquer EP-2 — em fotônica, matrizes aleatórias, o que for — produziria as mesmas leis. Como ontologia e leitura deflacionária predizem números idênticos, a razão de verossimilhança é ~1 e a atualização bayesiana sobre a ontologia foi **zero**. As lacunas específicas:

1. **Nenhuma quantidade de informação quântica faz trabalho de carga** — fidelidade de Petz, entropia relativa, CMI: nada disso aparece na derivação nem no pipeline.
2. **α é ajustado, não previsto** — nenhuma predição a priori a partir da estrutura analítica.
3. **Suficiência, não necessidade** — a lei log é uma cota superior atingida por um esquema; "custo de emergência" afirma necessidade, e não existe cota inferior tipo Cramér-Rao.
4. **Nenhum problema inverso resolvido** — N conta coeficientes de Taylor de uma métrica *conhecida*, não recursos operacionais de fronteira ruidosa.
5. **Universalidade não testada** — um background, um EP, um canal.
6. A única afirmação genuinamente falseável contra a natureza (a₀(z) ∝ H(z), turno 044) não depende da ontologia de recoverability e tem prioridade fina (Milgrom, Verlinde, Hossenfelder-Mistele).

**O espaço em branco é real.** A varredura de literatura confirma que ninguém quantificou *custo* de reconstrução: o programa Lu-Ran-Wu (arXiv:2506.12890, PRL 2026; arXiv:2604.14638) prova existência ordem a ordem mas não taxa de convergência; o programa de pseudoespectro/EPs (Jaramillo et al., PRX 2021; Motohashi, PRL 134, 141401; arXiv:2605.17840) caracteriza instabilidade espectral mas nunca conecta proximidade de EP a custo de reconstrução; e a recoverability holográfica só tem a dicotomia grosseira do Python's Lunch (arXiv:1912.00228). A "lei de complexidade crítica" ocupa território desocupado — mas ocupá-lo com matemática padrão relabelada não é revolução. O programa abaixo é desenhado para forçar, em cada etapa, uma bifurcação onde a leitura informacional e a leitura deflacionária discordam.

---

## 2. O programa: seis projetos, do curto ao longo prazo

### Fase 1 — semanas, código existente, decisão barata

**P1. Varredura de acoplamento com taxas a priori: prever α(λ) do ponto de ramificação complexo antes de medir.**
*O quê:* repetir o pipeline congelado em λ_GB ∈ {0,02 … 0,225}. O ponto de ramificação de b(z) é fechado (1-4λ(1-z⁴)=0); para cada λ, computar **antes** a taxa Stahl/capacidade α_pred(λ) e a taxa de canal crítico corrigida por kernel, congelar as sete triplas em arquivo datado, e só então medir. Subprodutos: a trajetória do EP q²c(λ), ω_c(λ) (dado espectral novo em si) e o teste de persistência do splitting 0,85/0,57 em N grande.
*Por que decisivo:* α deixa de ser parâmetro ajustado e vira predição de zero parâmetros livres, testada sete vezes com divergência prevista quando λ → 1/4. Simultaneamente estressa o único refinamento com conteúdo próprio que sobreviveu: taxas por observável fixadas por kernels de sensibilidade.
*Diferença da física padrão:* Stahl fixa só a taxa sup-norm assintótica e prediz equalização dos canais em N grande; a versão-kernel prediz splitting persistente com dependência computável em λ. Se o splitting decai, o framework se reduz a teoria de Stahl relabelada — e o desenho estabeleceria isso de forma limpa.
*Critério de morte:* splitting α_ρ/α_sup → 1 com N (inclinação ≠ 0 a 3σ); ou levels/decade não rastreia ln10/(2α_pred(λ)) em ≥5 acoplamentos (R² < 0,9); ou divergência ausente quando λ → 1/4.
*Esforço:* semanas (~200 linhas novas + ~6 min de runtime por λ). Ressalva dos juízes: λ_GB > 0,09 viola causalidade de fronteira — pontos matematicamente válidos, duais patológicos.

**P2. Profundidade informacional operacional: inverter a torre de pole-skipping ruidosa (projetos 2 e 8 fundidos — ambos os juízes apontam que são um só).**
*O quê:* calcular a torre exata {q²_n} da recursão de Frobenius já em shooting.py, adicionar ruído gaussiano σ ∈ {1e-10 … 1e-2}, inverter via o sistema triangular de Lu-Ran-Wu, resumir por Padé restrito e medir erro espectral à distância d do EP. Congelar antes: a parede de truncamento ótimo N*(σ) = (1/2α_ρ)ln(1/σ); o expoente do piso de ruído (1/2 no canal ω, 1 no canal ρ); e o benchmark Cramér-Rao/Fisher — um estimador direto que ignora a torre bate a lei de níveis-por-década?
*Por que decisivo:* é a primeira vez que N conta recurso operacional medido, não coeficientes de uma métrica conhecida — responde diretamente à lacuna mais aguda da auditoria. E o braço Fisher é onde ontologia e deflação finalmente divergem: a leitura de recoverability exige que a lei seja cota sobre *todos* os estimadores; a matemática pura só a faz cota superior de um esquema.
*Diferença da física padrão:* a amplificação √σ no EP é física de Petermann padrão (Wang et al., Nature 2020) e Lau-Clerk (Nat. Commun. 9:4320) já mostrou ausência de vantagem de Fisher em *sensing* — mas nenhuma dessas literaturas contém lei de piso de ruído ou parede de truncamento para reconstrução de *métrica*, nem qualquer enunciado de necessidade.
*Critério de morte:* torre não converge antes da parede para σ > 1e-8 (a lei só existe em aritmética exata); expoente do piso no EP consistente com 1 e não 1/2 a 3σ; canal ρ também com expoente ~1/2 (decomposição de canais não compra nada); ou o estimador direto bate a lei por fator >10 — aí a linguagem de "custo" deve ser retirada.
*Esforço:* semanas.

**P3. Redes gêmeas adversariais: cota inferior construtiva de necessidade.**
*O quê:* análogo discreto do benchmark — rede tridiagonal não-hermitiana com EP-2 espelhado, torre espectral de fronteira = polos/resíduos da função de Green de borda (problema inverso de Jacobi). Construir numericamente pares de redes cujos primeiros N níveis coincidem exatamente maximizando a diferença δ*(N,d) num observável-alvo: cota minimax construtiva que nenhum estimador evade. Testar δ* ~ e^(-αN)/√d com o *mesmo* α do esquema Padé.
*Por que decisivo:* converte suficiência em necessidade por construção. E há risco matemático real para a teoria: expoentes de largura minimax (capacidade/Chebyshev) não precisam igualar a taxa Stahl de um esquema — α* ≠ α rebaixaria "profundidade informacional do observável" a "ordem de truncamento de um algoritmo".
*Diferença da física padrão:* nenhuma discrepância esperada se a lei for justa — mas ninguém jamais computou essa largura minimax perto de um EP, então qualquer resultado é informação nova: α* = α eleva a lei a cota de recurso genuína; α* ≠ α é discrepância que a teoria congelada não absorve.
*Critério de morte:* α* difere de α a >3σ, ou expoente de amplificação fora de 0,5±0,1 → publicar o negativo e abandonar a linguagem de "custo de emergência". (Ignorar a fase de bancada; a Fase 1 numérica basta.)
*Esforço:* semanas.

### Fase 2 — meses, onde a informação quântica precisa fazer trabalho de carga

**P4. Teorema da taxa CMI-de-fronteira: derivar α da estrutura analítica de J(u), não da métrica bulk.**
*O quê:* fazer a relação de Abel dos turnos 078-080 (B(u) como funcional de J(u)) carregar peso: (i) derivar o mapa geral entre singularidades complexas de J e de B sob o kernel √ (que genericamente *muda o tipo* de singularidade); (ii) computar J(u) para o brane EGB via entropia de emaranhamento de faixas com o funcional de Jacobson-Myers; (iii) localizar a singularidade mais próxima de J por Padé/Stahl e **congelar** α_CMI antes de comparar com α_ρ = 0,851±0,130 já medido.
*Por que decisivo:* é o primeiro lugar onde uma quantidade de informação quântica (CMI de fronteira) *prediria* um número até agora só ajustado — refutando ou confirmando a objeção central da auditoria ("recoverability faz zero trabalho de carga").
*Diferença da física padrão:* Stahl diz que a taxa é fixada pela singularidade de B (conhecida); HEE é irrelevante. O postulado diz que J é primário. As duas predições só coincidem se o funcional de Abel preservar singularidades um-a-um — o que o kernel √ genericamente viola. A taxa medida escolhe um lado.
*Critério de morte:* |α_CMI − α_medido| > 2σ nos dois canais; ou a derivação prova que as predições sempre coincidem (camada CMI matematicamente redundante — publicar o teorema deflacionário e parar); ou a identidade de Abel falha a 1e-6 em Gauss-Bonnet (a única ponte bulk-fronteira do framework quebra).
*Esforço:* meses — os juízes concordam que "semanas" era otimista: o extremizador de Jacobson-Myers é solver novo, e extrair coeficientes de Taylor de um J(u) numérico com precisão suficiente para localizar singularidades é delicado.

**P5. DPI vs NEC: monotonicidade de canal é uma condição de energia estritamente mais forte?**
*O quê:* se a profundidade u é direção emergente de um canal de coarse-graining, a desigualdade de processamento de dados (DPI) deve valer ao longo de u. Empurrar essas restrições pela relação de Abel até desigualdades de sinal sobre a₁…a_N e comparar, coeficiente a coeficiente, com a reformulação algébrica da NEC de Lu-Ran-Wu (arXiv:2506.12890). Três saídas: DPI ⟺ NEC (teorema limpo, postulado redundante); mais fraca (sem conteúdo); **estritamente mais forte** (física nova). Se mais forte: construir background que satisfaz NEC e viola DPI e testar a patologia espectral prevista.
*Por que decisivo:* é a única rota em que a ontologia *produz* gravitação em vez de descrevê-la — uma lei tipo condição-de-energia derivada de informação seria exatamente a predição proprietária e falseável que a auditoria diz faltar. Até o desfecho deflacionário ("DPI equivale à NEC nesta classe") é um teorema publicável em espaço em branco confirmado.
*Diferença da física padrão:* RG+QFT admite todo background NEC-satisfatório com torre de pole-skipping normal; o postulado prediz que um subconjunto estrito é codificável, e violadores de DPI devem ser espectralmente patológicos apesar de saudáveis em RG.
*Critério de morte:* (a) desigualdade DPI provadamente implicada por NEC + condições AdS (nenhum background separador — publicar equivalência e parar); (b) DPI não gera restrição definida porque o canal não é especificável além do exemplo trabalhado — o que confirma a acusação da auditoria de subdefinição operacional e fecha esta rota; (c) background NEC-ok/DPI-violador com torre completamente normal — falseamento direto da única consequência dinâmica do postulado.
*Esforço:* meses, alta variância. Financiar apenas ao lado dos projetos baratos da Fase 1, nunca sozinho.

### Fase 3 — longo prazo, o único experimento que separa as ontologias

**P6. Taxa de recuperação de Petz vs taxa de reconstrução espectral num qubit dissipativo com EP.**
*O quê:* na única plataforma onde "recoverability" é mensurável (qubit supercondutor pós-selecionado com EP-2 quântico, classe Naghiloo), medir duas taxas em função do número N de níveis retidos do registro de medida: α_Petz (decaimento da infidelidade da recuperação de Petz via tomografia) e α_spec (convergência da reconstrução de parâmetros do mesmo registro truncado), com o operador de salto engenheirado para que contração de canal e taxa de Puiseux difiram ≥2× por desenho. Testar α_Petz = α_spec e o halving de ambas no EP, com protocolo e números congelados antes dos dados.
*Por que decisivo:* é o único projeto de toda a lista em que um resultado positivo *surpreenderia a física padrão* — nenhum teorema trava o decaimento de Petz à taxa de estimação governada por Fisher; a expectativa genérica é α_Petz ≠ α_spec. Travamento observado seria lei nova e a primeira evidência de que recoverability, e não só teoria de aproximação, governa custo de reconstrução. O nulo aposenta a ontologia de forma limpa.
*Critério de morte (pré-registrado):* α_Petz/α_spec fora de 1±0,2 em ≥3 valores de d, ou taxa de Petz sem halving no EP (fora de 1±0,25) → aposentar a ontologia como afirmação física, manter a matemática validada, reenquadrar o programa como teoria de aproximação espectral não-hermitiana.
*Esforço:* o dry-run de simulação do protocolo completo custa dias no código existente e **deve ser feito já**; o experimento exige laboratório parceiro e ~1 ano. Ambos os juízes: campanha de hardware real, não "dispositivo em nuvem".

**Descartados ou adiados, com razão registrada:** a correção de Petermann à la Fawzi-Renner (proposta 5) tem falha estatística fatal — o "resíduo" 1,450 vs 1,35±0,21 está a ~0,5σ, não há nada a explicar até que P1 aperte α_ρ ~5×; a coerência de fase (proposta 3) tem poder estatístico marginal com ~13 valores de N e a asintótica de Padé *não* é muda sobre fases; o teste BTFR de alto-z (proposta 9) tem sinal do tamanho do orçamento de sistemáticos, blindagem já parcialmente comprometida (dados MUSE vistos antes do congelamento) e não testa a ontologia de profundidade; o ringdown de Kerr (proposta 7) e a bancada EP-3 (proposta 11) são valiosos mas dependem de transposições não afiadas ("N como décadas de SNR") ou de um laboratório que não existe — reavaliar após a Fase 1.

---

## 3. O próximo movimento mais afiado

**A varredura de acoplamento (P1), começando esta semana.** Três razões, em ordem de força:

1. **Melhor razão custo/decisão da mesa** (consenso dos dois juízes): ~200 linhas novas sobre um pipeline verificado, ~6 minutos por acoplamento, e *qualquer* desfecho é decisivo — ou α vira a primeira predição de zero parâmetros do programa, confirmada sete vezes com divergência prevista em λ → 1/4, ou o splitting de canais decai e o framework é convictamente reduzido a teoria de Stahl relabelada, o que encerraria honestamente a fase holográfica.

2. **É pré-requisito lógico do resto.** P2 precisa de α_ρ apertado para os expoentes congelados; a análise de resíduos que motivaria qualquer correção informacional (Petermann ou outra) só existe depois que o erro de α_ρ cair de ±0,130 para algo útil; e o teste de persistência do splitting decide se a versão-kernel — o único enunciado quantitativo proprietário sobrevivente — merece o investimento de P4.

3. **Produz ciência independente da teoria.** A trajetória q²c(λ), ω_c(λ) do EP espelhado em Einstein-Gauss-Bonnet não existe na literatura (o vizinho mais próximo, arXiv:2605.17840, é Kerr e puramente fenomenológico), e é publicável mesmo que todas as predições congeladas falhem.

A regra de decisão na saída: se P1 confirmar as taxas a priori e o splitting persistente, avançar imediatamente para P2+P3 em paralelo (semanas) e destravar P4; se P1 matar o kernel, executar mesmo assim P2 (o braço Fisher e a parede de ruído mantêm valor operacional próprio), rodar o dry-run de simulação de P6, e reescrever o programa como o que ele então provadamente será: teoria de aproximação espectral de sistemas não-hermitianos, sem a camada ontológica — que é, notavelmente, o mesmo desfecho que a disciplina de autofalsificação do próprio corpus vem praticando desde o turno 110.