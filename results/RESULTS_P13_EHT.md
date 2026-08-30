# P13-EHT — CRB do Lyapunov sobre cobertura interferométrica real

Extensão do P13 com dados reais (example enviado ao eht-imaging, PR #332).

- Cobertura EHT 2017 M87 (hops lo, 5877 visibilidades, σ mediana 24.3 mJy):
  σ(γ)/γ = 148% (γ=1.1) e 101% (γ=π) — **a campanha 2017 não constrange o
  expoente de Lyapunov** (quantificado pela primeira vez sobre a cobertura
  real com amplitudes de sub-anel livres).
- Curva de projeto (ruído 2017, cobertura densa): γ=1.1 atinge 10% em
  u_max ≈ 60 Gλ (28% em 40; 1.1% em 120). γ=π (Schwarzschild) é ordens de
  magnitude pior em toda a faixa (2067% em 60 Gλ): w=e^{−π} colapsa a torre
  na curva crítica — **a criticalidade de torre do programa aparece na
  régua interferométrica**: quanto mais Schwarzschild, mais caro medir γ
  com amplitudes livres.
- Auditoria (API arXiv): Fisher para SPIN no BHEX existe (2608.23672);
  pisos sistemáticos por ordem de anel (2512.16983); CRB explícito de γ de
  visibilidades + lei de degenerescência: não encontrados.
- Caveats: anéis finos, amplitudes livres, d_∞ fixo, cobertura sintética
  densa na curva de projeto, só ruído térmico. Best-case bounds.
