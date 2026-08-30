# Nosso trabalho e as "11 dimensões" — um mapa honesto

> **AVISO DE SUPERSESSÃO (2026-08-30):** este é um documento HISTÓRICO datado.
> Os valores de λ_ext aqui citados (0.1091 e derivados) foram RETRATADOS —
> ver `ERRATA.md` E1–E3: não existe limiar único; a extinção é
> família-por-família, com EPs genuínos até pelo menos λ = 0.120.

Pergunta curta: **o nosso trabalho toca a teoria de cordas? E as teorias que unificam o quântico com o macroscópico?** Resposta curta: toca a teoria de cordas num ponto técnico real e bem delimitado (e acabamos de obter um resultado *negativo* interessante exatamente nesse ponto); sobre "unificação quântico–macro", nossos resultados dizem coisas concretas sobre **modelos de colapso** e sobre **programas de gravidade emergente** — mas quase sempre na forma de restrições e independências, não de confirmações. Abaixo, o mapa sem exageros.

---

## 1. Onde tocamos (de verdade) a teoria de cordas

**Primeiro, o vocabulário.** A teoria M tem **11 dimensões de espaço-tempo** (10 de espaço + 1 de tempo) — não "11 universos". A construção vem da supergravidade em 11D (Cremmer–Julia–Scherk, 1978) e da percepção de Witten (1995) de que as cinco teorias de supercordas em 10D e a supergravidade 11D são limites de uma única teoria. "Multiverso" e "universos paralelos" são conceitos distintos (vácuos diferentes da mesma teoria; cenários de branas) — confundir contagem de dimensões com contagem de universos é o erro clássico de divulgação. E o "5D" do nosso brane de Einstein–Gauss–Bonnet **não é uma dimensão extra no laboratório**: é o bulk holográfico (4 dimensões da teoria de fronteira + 1 direção radial emergente).

**A conexão genuína: Gauss–Bonnet é a correção de cordas de primeira ordem.** Zwiebach (1985) mostrou que a combinação de Gauss–Bonnet é a única extensão em curvatura-quadrada livre de fantasmas, e ela aparece na ordem α′ da corda **heterótica** (nas cordas tipo II, a primeira correção só aparece em α′³R⁴). Ou seja: o modelo que estudamos é, estruturalmente, "gravidade de Einstein + a primeira correção que a teoria de cordas prevê". Honestidade obrigatória: em toda construção de cordas controlada, λ_GB ~ 1/N — ordens de magnitude abaixo dos 0,08–0,12 que exploramos. Nosso brane com λ_GB finito é um **laboratório fenomenológico bottom-up**, não o limite de uma compactificação de cordas controlada (Camanho–Edelstein–Maldacena–Zhiboedov, 2014, mostraram que λ_GB finito só é consistente com uma torre infinita de estados de spin alto — assinatura "stringy" por excelência).

**A janela de causalidade.** A consistência causal restringe −7/36 ≤ λ_GB ≤ 9/100 em 5D (Brigante–Liu–Myers–Shenker–Yaida 2008; Buchel et al. 2010). Acima de 9/100 = 0,09, a teoria de fronteira dual propaga sinais mais rápido que a luz — deixa de existir uma teoria consistente.

**O que descobrimos ali — e o que isso significa e não significa.** Nossa transição nova (o ponto excepcional espelhado do QNM escalar existe no eixo real de momento tipo-espaço para λ ≤ 0,08 e está extinto para λ ≥ 0,12) inicialmente colocava o limiar num intervalo que continha 0,09. **Se** o limiar convergisse para exatamente 9/100, teríamos a primeira afirmação de que uma transição de ponto excepcional do espectro *detecta* a fronteira de causalidade das cordas — previsão de zero parâmetros, testável num laptop. Isso **não** significaria "prova da teoria de cordas": seria um vínculo estrutural dentro de um modelo, entre duas propriedades de consistência. Pois bem: o refinamento numérico já decidiu. O log local (`extinction_hunt.log (log de sessão local, não distribuído)`) fecha o limiar em **λ_ext ∈ [0,10875, 0,11000]** — estritamente *acima* de 0,09, cerca de 20% além da última teoria de fronteira consistente. O ponto excepcional, e com ele a lei de complexidade com taxa pela metade, **sobrevive à morte da causalidade da fronteira**. Isso é um resultado negativo com conteúdo: a estrutura espectral-informacional do bulk é *indiferente* à consistência da teoria de fronteira (ver seção 3). Nota de rodapé especulativa, devidamente rotulada como numerologia até que alguém a derive: 7/64 = 0,109375 cai dentro do intervalo atual; o limiar de instabilidade eikonal de Konoplya–Zhidenko, 1/8 = 0,125, parece excluído.

---

## 2. Modelos de colapso: o que dizemos e o que não dizemos

Modelos de colapso objetivo (GRW/CSL, Diósi–Penrose) são a tentativa mais direta de "unificar quântico e macro": postulam que a superposição quântica morre de verdade acima de certa escala. Status experimental em 2026: o ponto GRW original ainda está vivo (os limites do Majorana Demonstrator, 2022, mataram os valores de Adler mas não o GRW); o modelo de Diósi–Penrose sem parâmetros livres está morto (Gran Sasso, 2021) e a versão com parâmetro está espremida numa janela de ~4 ordens de magnitude, cercada dos dois lados — situação estruturalmente idêntica à nossa janela de λ_GB.

**O que nossos resultados dizem.** No nível da matriz densidade, o CSL de ruído branco *é* exatamente uma equação de Lindblad — o mesmo objeto matemático cujos espectros e pontos excepcionais estudamos. Consequência dura: **nenhuma medida espectral só no sistema distingue colapso de decoerência ambiental**. Todos os experimentos propostos (ex.: o blueprint de Horchani, 2026) discriminam por escalas de energia e de massa — nunca por informação. Nosso segundo resultado (custo de reconstrução espectral e custo de recuperabilidade de Petz são invariantes **independentes**) fornece exatamente o eixo que falta: decoerência é recuperável-em-princípio a partir de fragmentos do ambiente (o mapa de Petz funciona; é o "platô de redundância" do darwinismo quântico, que Torvinen–Keski-Vakkuri–Pranzini publicaram em 2026); colapso verdadeiro não deixa fragmento nenhum com o registro. E nossa independência diz que esse eixo é **ortogonal** à criticalidade espectral — dois discriminadores genuinamente independentes.

**O que nossos resultados não dizem.** Não testamos colapso: nossos dados de transmon e QPU não restringem λ_CSL nem R₀. E os modelos de colapso sobreviventes são necessariamente *não-markovianos* (ruído colorido), regime onde nosso formalismo de pontos excepcionais markovianos precisaria de extensão — questão aberta, não resultado.

---

## 3. Gravidade emergente: onde cada veredicto morde

Temos três veredictos: **(a)** o "endereço" do ponto excepcional, q²_c(λ), não é fixado pela escala de emaranhamento da fronteira (a trajetória medida é não-monotônica em λ; toda escala de emaranhamento candidata é monotônica — uma função monótona não parametriza um alvo não-monótono); **(b)** sem "locking" entre custo espectral e custo de Petz (três derrotas consecutivas); **(c)** a extinção do EP em ~0,109, não em 0,09 — uma terceira independência, agora entre estrutura do bulk e consistência da fronteira.

- **Verlinde 2010 (gravidade entrópica, "informação é uma moeda única")**: é a ontologia que os veredictos (b) e (c) atingem em cheio — se toda a dinâmica fosse um único livro-caixa de entropia, os dois custos deveriam ser interconversíveis; medimos que não são. Nos nossos sistemas-modelo, essa ontologia está refutada. (No céu ela já ia mal: falha em curvas de rotação e efemérides do Sistema Solar por 7 ordens de magnitude, embora passe em lente fraca de galáxias isoladas.)
- **It-from-qubit / correção de erros quântica**: a versão *ingênua* ("as propriedades informacionais são propriedades do código consistente e devem morrer na borda de consistência, 0,09") é refutada pelo veredicto (c). Mas a versão refinada — dois endereços por observável: recuperabilidade (Petz) e complexidade de decodificação (Python's Lunch de Susskind et al.; "price vs distance" de Pastawski–Preskill) — é **fortemente apoiada** por (a) e (b): nosso par de invariantes independentes é uma instância de laboratório exatamente dessa estrutura.
- **Jacobson (gravidade termodinâmica, 1995/2016)**: derivada para *qualquer* acoplamento de Lovelock, não faz nenhuma afirmação sobre locking — é o único programa que **previa** indiferença à borda de 0,09, e foi o que medimos. Intocado, e fracamente apoiado.

Ressalva sem hype: tudo isso é em sistemas-modelo (brane holográfico, qubits, QPU). Não medimos gravidade real; medimos qual *estrutura lógica* as ontologias de gravidade emergente precisariam ter para sobreviver aos nossos dados.

---

## 4. O que ainda dá para computar neste laptop hoje à noite (ordenado)

1. **Bissectar λ_ext até largura < 0,0005** e testar 7/64 = 0,109375 contra o intervalo (rotular como numerologia até derivação). Decide se há um valor fechado a explicar.
2. **Potencial efetivo / velocidade de frente do canal escalar em q grande vs λ**: se a transição qualitativa do próprio canal escalar cair em ~0,109 (e não no 0,09 do canal tensorial), o EP se *re-trava* à causalidade canal-por-canal — derrubaria a leitura de "autonomia do bulk". É o teste mais decisivo da lista.
3. **Lei da metade em λ = 0,095 e 0,105** (banda acausal, EP vivo): transforma "a lei de complexidade sobrevive à inconsistência da fronteira" em número medido.
4. **Validações de pipeline**: poço de potencial tensorial exatamente em 0,09 (BLMSY) e colisão de cisalhamento em q²_c ≈ 1,18544, ω_c ≈ −1,63793i em λ ≈ −0,04956 (Grozdanov–Starinets–Tadić).
5. **Regressão de q²_c(λ) contra a(λ), c(λ), c/a e o coeficiente de entropia de emaranhamento** (fórmulas fechadas de Buchel et al.): quantifica o veredicto (a) com um R².
6. **corr(α_ρ, custo de Petz) com IC de bootstrap** sobre `results/sweep_fits.json`: o "sem locking" vira um único número citável.
7. **Demo-teorema numérica**: mesmo canal como dilatação unitária vs desdobramento estocástico com registro descartado — espectros idênticos, Petz maximamente diferente. É a ponte limpa entre nossos resultados e a discriminação colapso/decoerência da seção 2.

Arquivos relevantes: `extinction_hunt.log (log de sessão local, não distribuído)`, `/Users/maiconesteves/fisica/theory-validation/results/RESULTS_SWEEP.md`, `/Users/maiconesteves/fisica/theory-validation/results/sweep_fits.json`.