# P13-EHT: CRB of the Lyapunov exponent over real interferometric coverage

Extension of P13 with real data (example sent to eht-imaging, PR #332).

- EHT 2017 M87 coverage (hops lo, 5877 visibilities, median σ 24.3 mJy):
  σ(γ)/γ = 148% (γ=1.1) and 101% (γ=π): **the 2017 campaign does not
  constrain the Lyapunov exponent** (quantified for the first time over
  the real coverage with free sub-ring amplitudes).
- Design curve (2017 noise, dense coverage): γ=1.1 reaches 10% at
  u_max ≈ 60 Gλ (28% at 40; 1.1% at 120). γ=π (Schwarzschild) is orders
  of magnitude worse over the whole range (2067% at 60 Gλ): w=e^{−π}
  collapses the tower onto the critical curve: **the program's tower
  criticality shows up in the interferometric ruler**: the more
  Schwarzschild, the more expensive it is to measure γ with free
  amplitudes.
- Audit (arXiv API): Fisher for SPIN in BHEX exists (2608.23672);
  systematic floors per ring order (2512.16983); an explicit CRB of γ
  from visibilities + a degeneracy law: not found.
- Caveats: thin rings, free amplitudes, fixed d_∞, dense synthetic
  coverage in the design curve, thermal noise only. Best-case bounds.
