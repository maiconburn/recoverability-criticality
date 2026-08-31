# P9: entangled probe vs the cost law at the EP (one-day result; calibrated)

Question: does an entangled ancilla buy back part of the gap^-p cost near
an exceptional point?

Setup: post-selected PT channel K(t)=exp(-iH_eff t), H_eff=[[0,J],[J,-iγ/2]],
EP at J=γ/4. Three strategies with a fixed shot budget (noise per measured
quantity ∝ √N_quantities): A = probe |0⟩ (column 0 of K);
B = probe (|00⟩+|11⟩)/√2 with idle ancilla (all of K in one setting);
C = probes |0⟩ and |+⟩ (all of K, two settings, no entanglement).
Marginalized CRB for the splitting (free amplitudes) and the amplitude
(free frequencies). Script: scripts/entangled_probe_ep.py; data:
results/entangled_probe_ep.json.

Result:
- Exponents (gap window 0.07–0.87): A: −1.26 / −2.62; B: −1.08 / −2.46;
  C: identical to B by construction of the noise model.
- At the most critical point: prefactor gain ≈ 1.4× from A to B/C, in both
  tasks.

Reading: **entanglement does not change the scaling** gap^-p; it delivers
the same as classical setting diversity (B ≡ C), with only an operational
advantage (a single preparation). Consistent with the fundamental limits
of non-Hermitian sensing (arXiv:1805.11760), now in the program's task
language.

Caveats/open: (i) the additive per-quadrature noise model does not capture
collective/joint measurements: quantum advantage by MEASUREMENT remains
open; (ii) the finite gap window distorts exponents (~0.2); (iii) no
hardware run: not justified for a 1.4× prefactor explained classically.
