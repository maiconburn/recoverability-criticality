# Top 5 testes PRÉ-LAB — ranking sintetizado das 6 lanes de busca

**Legenda de honestidade**: [ONTOLOGIA] = pode discriminar a ontologia especulativa (locking L2) contra a QM padrão. [RE-VERIFICAÇÃO] = valioso, mas apenas re-verifica/estende L1/L3 em sistemas novos — não decide a ontologia.

---

## 1. Teste de duas tarefas no mesmo registro — IBM Quantum (nuvem, tier gratuito) — [ONTOLOGIA]

**O que faríamos**: Reproduzir o qubit dissipativo com EP2 via dilatação com ancilla + pós-seleção (circuitos publicados: Dogra et al., Commun. Phys. 4, 26 (2021), código em github.com/Arty1498/Non-Hermitian; versões modernizadas com decomposição explícita de portas em arXiv:2507.08129, Fig. 2). Coletar o registro de shots com `memory=True`, truncar o MESMO registro em N crescente e extrair em paralelo: (a) taxa de reconstrução espectral/paramétrica de (Omega, gamma); (b) fidelidade de recuperação Petz/pretty-good usando os circuitos Petz já validados em hardware IBM (Biswas & Mandayam, arXiv:2510.08719) ou as compilações de baixa profundidade de Png & Scarani (PRA 112, 022613: 1–2 ancillas, 3–20 CNOTs). Varrer os knobs: distância ao EP, fração de pós-seleção, shots.

**O que testa**: L2 diretamente — é a ÚNICA rota identificada em todas as lanes que mede as duas taxas no mesmo registro quântico real. QM padrão prevê taxas independentes (razão 0,27–0,99, móvel; Petz NÃO cai pela metade no EP). Locking ou dupla-halving observados = assinatura de física nova, falsificável. Também entrega L1 (erro vs N no EP vs longe) e L3 (fração de sucesso da pós-seleção como eixo N natural, cf. Jebraeilli & Geller PRA 111, 032211) de graça. Nenhum experimento publicado fez as duas tarefas no mesmo registro — nicho aberto.

**Custo/esforço**: Zero custo monetário: IBM Open Plan dá 10 min QPU/28 dias (+ promoção única de 180 min); Dogra usou 8192 shots/ponto, Abbasi 4096 — a campanha cabe no tier gratuito. Esforço: ~1–2 semanas de engenharia de circuito + análise.

**Primeiro passo HOJE (laptop)**: `git clone https://github.com/Arty1498/Non-Hermitian`; montar o pipeline completo (dilatação EP + truncamento + fit espectral + Petz) no simulador Qiskit com modelo de ruído de um backend Heron — validar que as duas taxas são extraíveis com os shots disponíveis ANTES de gastar 1 segundo de QPU. O resultado do simulador já é, por si só, a predição QM-padrão de referência.

---

## 2. Truncamento dos dados públicos do grupo Murch — qubit dissipativo real com EP2 — [RE-VERIFICAÇÃO L1/L3, ONTOLOGIA parcial]

**O que faríamos**: Baixar os dois repositórios públicos do murchlab: (i) `Nonlinear-quantum-evolution-of-a-dissipative-superconducting-qubit` (arXiv:2510.25836 — CSVs brutos de tomografia Rabi, 10 configurações de drive/dissipação = os "knobs", múltiplos estados iniciais, notebooks que reconstroem densidades 2x2/3x3 por instante); (ii) `Exploring-the-topology-...-shortcuts-to-adiabaticity` (PRX Quantum 7, 010337 — séries temporais x/y/z de tomografia em circum-navegação do EP, 71 arquivos + notebook). Truncar registros em N pontos, ajustar o Hamiltoniano efetivo, medir a taxa de decaimento do erro perto vs longe do EP (L1); usar as configurações/tempos de loop como janelas de informação (L3). Das séries de matrizes densidade, computar offline a recuperação Petz vs truncamento e comparar com a taxa espectral do mesmo dataset.

**O que testa**: L1 com poder alto — é a linhagem exata da plataforma Naghiloo 2019 onde o halving foi previsto; dados quânticos reais, sem nenhum contato. L3 com poder médio (janelas discretas, não contínuas). L2 apenas parcialmente e com caveat honesto: o Petz aqui é computado offline sobre tomografia pós-selecionada — não é a recuperação física no mesmo registro; um "locking" visto assim seria sugestivo, não decisivo (a reconstrução tomográfica é ela mesma um estimador, contaminando a independência das duas taxas). Sirva como triagem: se nem aqui aparecer locking, a predição da ontologia já sofre pressão.

**Custo/esforço**: Gratuito, licença MIT, ~5 MB + repositório maior; dias, não semanas.

**Primeiro passo HOJE (laptop)**: clonar os dois repositórios, rodar os notebooks originais até reproduzir as figuras, e escrever o script de truncamento (fit de (Omega, gamma) com registro cortado em N) numa única configuração perto do EP.

---

## 3. Ringdown de buracos negros: rate-halving no avoided crossing de Kerr — [RE-VERIFICAÇÃO L1/L3, alto poder estatístico]

**O que faríamos**: Três camadas, todas públicas: (a) benchmarks Teukolsky com amplitudes exatamente conhecidas (Kubota-Motohashi, Zenodo 10.5281/zenodo.18511200, 10,3 GB, CC-BY, com notebook) — fits de N modos em registros truncados varrendo spins através do avoided crossing (2,2,n=5–6) em a/M≈0,9 (EP em a≈0,897+0,010i, Lo et al.) e das ressonâncias agudas (3,1) em 0,952–0,997; (b) tabelas de frequências + fatores de excitação (Zenodo 10.5281/zenodo.12696857 + CSVs de Lo-Sabani-Cardoso) para ringdowns sintéticos com dial calibrado de distância ao EP; (c) catálogo SXS: 17 simulações NR com spin remanescente 0,90±0,005 (SXS:BBH:4190, 3979, 1481, 3901, 4075, 0618, 0333, 4169...) vs centenas em chi_f≈0,69 — medir alpha(N) on-EP vs off-EP com qnmfits/jaxqualin.

**O que testa**: L1 com poder discriminante alto no lado espectral: sistema clássico, sem ruído, distância ao EP calibrada — se o halving de L1 for universal, TEM que aparecer aqui; se não aparecer nem em dados limpos, a formulação da lei precisa de revisão antes de qualquer laboratório. L3 idem: dependência da janela de fit é o observável padrão da área (a controvérsia GW150914 inteira, com posteriors públicos Zenodo 5965773/6949492, é literalmente "conteúdo extraível vs janela"). **Não toca L2**: nenhum grau de liberdade quântico — zero poder sobre a ontologia; contribui apenas falsificação do lado espectral. Caveats a modelar: perto do EP o próprio modelo de fit muda (termo secular linear em t — arXiv:2512.02110); instabilidade pseudo-espectral dos overtones (Jaramillo et al. PRX 11, 031003); avoided crossing não é genérico (Lo et al.).

**Custo/esforço**: Gratuito; `pip install qnm qnmfits sxs jaxqualin`; o dataset de 10 GB é opcional no início (as tabelas bastam para sintéticos). Semanas de análise, tudo em laptop/Colab.

**Primeiro passo HOJE (laptop)**: `pip install qnm sxs qnmfits`; baixar as tabelas de fatores de excitação de Motohashi (leves), gerar um ringdown sintético em a/M=0,90 e outro em 0,69, e rodar o primeiro fit erro-vs-N — resultado preliminar em uma tarde.

---

## 4. Escada de ordem do EP (EP2 → EP3 → cúspide): a taxa escala com a ordem? — [RE-VERIFICAÇÃO L1 com predição nova]

**O que faríamos**: Testar não só o halving verificado em EP2, mas a generalização "taxa/n em EP de ordem n" — uma predição mais afiada que nenhuma simulação do programa verificou ainda. Dados públicos e legíveis por máquina: íon aprisionado LEP2/LEP3 com jumps quânticos (figshare 10.6084/m9.figshare.30343429 — matrizes densidade, autovalores de Liouvillian vs gamma0/gamma_phi, 200 reps/ponto); linha excepcional de 3ª ordem em NV (Source Data XLSX, Nat. Nanotech. 19, 160); magnonics CPA-EP3 (Zenodo 10.5281/zenodo.18410900); MEMS cúspide vs EP vs ponto diabólico no mesmo dispositivo (figshare 10.6084/m9.figshare.19609350 + 29278061, resposta em lei 1/3 sobre múltiplas décadas). Ajustar erro de reconstrução vs orçamento de informação em cada ordem.

**O que testa**: L1 com poder alto de estender/quebrar a lei: um resultado "taxa/2 em EP2 mas NÃO taxa/3 em EP3" reformularia a lei antes do laboratório; confirmação em 2 plataformas quânticas (íon, NV) + 2 clássicas seria a validação mais forte disponível sem lab. Bônus L2-adjacente: os dados de íon distinguem EP Liouvilliano vs Hamiltoniano — exatamente onde a predição "Petz não sofre halving no EP Hamiltoniano" é mais nítida (mas sem registro contínuo, não fecha L2). Não discrimina a ontologia.

**Custo/esforço**: Gratuito (figshare/Zenodo, CC-BY); esforço médio — parsing de .fig MATLAB e XLSX heterogêneos é o custo real.

**Primeiro passo HOJE (laptop)**: baixar o figshare do íon (maintextdata.zip) e o XLSX do NV; extrair os autovalores de Liouvillian vs parâmetro de controle e verificar que a estrutura EP2/EP3 é re-ajustável a partir dos dados brutos.

---

## 5. Crossover de duas selas (L3) em espectroscopia bruta multi-EP — [RE-VERIFICAÇÃO L3, o teste mais limpo da lane clássica]

**O que faríamos**: Usar os dois maiores registros brutos públicos perto de EPs: (i) Harris/Yale (Nat. Commun. 15, 1369; Zenodo 10.5281/zenodo.10451386, CC-BY) — espectros I/Q brutos (.dat) perto de TRÊS EPs optomecânicos + folhas de autovalores complexos em .csv: truncar em N pontos/janelas de banda, re-ajustar autovalores, medir erro vs N e a dependência da taxa com a janela — a estrutura multi-EP fornece naturalmente os dois "endereços informacionais" de L3; (ii) voltímetro EP de Kottos (Zenodo 10.5281/zenodo.8250656, arquivo bruto de 1,9 GB) para truncamento de registro genuíno em série temporal com ruído real. Complemento EP2 de precisão: acelerômetro de Kononchuk (Zenodo 10.5281/zenodo.6397748, .mat) para a questão custo-de-ruído 1/sqrt(d) vs log.

**O que testa**: L3 com o melhor poder disponível pré-lab: o crossover de taxa vs orçamento N é diretamente mensurável em dados brutos, com múltiplos EPs competindo. L1 secundariamente. Plataformas clássicas de ondas — validam a MATEMÁTICA das duas selas, não a ontologia quântica; zero poder sobre L2.

**Custo/esforço**: Gratuito, CC-BY, download direto; análise de dias a 1–2 semanas.

**Primeiro passo HOJE (laptop)**: baixar Zenodo 10451386, ler um .dat I/Q, ajustar os autovalores de um modo com a janela completa e depois com metade da janela — se a taxa ajustada se mover, o observável de L3 existe nesses dados.

---

## Resumo brutalmente honesto

- **Só o Teste 1 decide a ontologia (L2)** — e é executável de graça, sem laboratório. Tudo o mais orbita.
- O Teste 2 é a melhor triagem L2 barata (Petz offline), mas com confusão metodológica embutida — nunca venderia um "locking" achado ali como descoberta.
- Testes 3–5 são re-verificações/extensões de L1/L3 em regimes novos (gravitação, EP3/cúspide, multi-EP clássico). Valor real: se L1/L3 falharem em dados limpos e públicos, o programa se reformula ANTES de gastar qualquer credibilidade experimental; se sobreviverem, o Teste 1 sobe de aposta.
- Lacunas que valem um e-mail (não parceria): dados brutos Naghiloo 2019/PRLs 2021–22 (Murch), registros de heterodino do grupo Huard (Six-Rouchon já demonstrou as duas tarefas no mesmo registro — o dataset L2 real mais próximo, a um pedido de distância), e verificação do depósito do experimento de Darwinismo quântico supercondutor (Sci. Adv., arXiv:2504.00781).
- Correções de citação herdadas das buscas: "Wang, Lau, Clerk, Nature 583, 60 (2020)" não existe (conflação de Nat. Commun. 11, 1610 com Nat. Commun. 9, 4320); o repositório do paper NV biestável (hanfengw/BPNV) retornava 404 em 2026-08-28.