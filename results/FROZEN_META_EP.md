# Previsão congelada — ponto de aniquilação de EPs (2026-08-29, antes das medições)

Hipótese estrutural: λ_ext é uma ANIQUILAÇÃO DE PAR de EP-2 (fold de ρ(q²)):
ρ(q²,λ) ≈ (ρ''/2)(q²−q²_m)² + μ·(λ−λ_ext) localmente.

Previsões (a medir em seguida):
- F1: para λ<λ_ext, DOIS cruzamentos reais de ρ próximos, colapsando em λ_ext;
  separação dos dois EPs ∝ (λ_ext−λ)^{1/2}.
- F2: ρ_min(λ) linear em λ através de λ_ext.
- F3: para λ>λ_ext, par de zeros complexos conjugados com Im q²_c ∝ (λ−λ_ext)^{1/2}.
- F4 (a consequência para a LEI DE CUSTO — o teste central): no ponto de
  aniquilação (λ_ext, q²_m), o gap fecha linearmente em |q²−q²_m|, logo o
  expoente de amplificação do canal crítico DOBRA: γ_meta = 1.0 (vs 0.5 no
  EP-2 ordinário), ENQUANTO o halving em N (resposta √ em δρ) PERMANECE:
  ε(N, d=0) ~ e^{−αN/2} ainda.
Critérios: F1–F3 com expoentes 0.5±0.1; F4 com γ_meta = 1.0±0.15 e razão de
halving 1.0±0.2. Qualquer outra coisa: estrutura diferente — reportar como está.

## VEREDITO FINAL (2026-08-30, fechamento documentado — auditoria)

O objeto destas previsões (o "meta-EP": aniquilação em um λ_ext único) foi
dissolvido pela ERRATA E3: a extinção é família-por-família e não há
limiar único. Consequência para cada previsão congelada:
- F1 (expoente de meia-largura 0.5): medições E1-era deram ~0.3 e foram
  VOIDADAS pela E2 (artefatos de colocação); com a E3, a própria grandeza
  "meia-largura do λ_ext" deixou de ser bem definida. **Void por conceito.**
- F2 (linearidade de ρ_min(λ)): mesma sorte — os dados shooting
  (rho_profile.json) mostram ρ_min com estrutura de agulha não capturada
  por fit linear; nunca recebeu fit formal porque a premissa caiu. **Void
  por conceito.**
- F3 (migração para q² complexo): segue genuinamente ABERTA
  (complex_migration.json foi inconclusivo perto da fronteira; README §1.3
  a lista como não determinada). **Aberta.**
- F4 (γ_meta = 1.0 na aniquilação): duas tentativas de medição falharam
  por identidade/piso (documentado em ERRATA E2 e RESULTS_DEEP_FAMILY);
  sem ponto de aniquilação único, a definição precisa ser refeita
  por família. **Void por conceito.**

Nada aqui altera os textos congelados acima (mantidos para auditoria);
este adendo só fecha o registro que a auditoria de 2026-08-30 apontou
como pendente.
