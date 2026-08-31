# P12 + P13: verdicts (big-theory radar; frozen before measuring)

## P12: traversability ↔ Petz (operational ER=EPR)

Instrumentation trail (all recorded): v1 had the message in the wrong
place (it measured preservation, not teleportation: caught by the U=1
sanity check); v2 fixed the insertion but used embed() with a BUGGY
permutation (caught by a unit test: the gate landed on the wrong qubit;
all previous results void); v3 = tensor application with unit tests
PASS.

**P12.1 KILLED in the minimal model**: with the clean protocol (3+3
qubits, kicked Ising 8 steps, coupling exp(igΣZZ) on the 2 carrier
pairs, decoding U* or U^T), F(g) ≈ 0.25 with contrast ≤ 0.007 and
MI(REF:R0) ≤ 0.022 bits over g ∈ [−2, 2]. Physical reading: the GJW
"no-decoder" traversability window is a large-N semiclassical
phenomenon; at small N teleportation-by-size REQUIRES the decoder
(Grover/YK), consistent with the design of the 7-qubit experiment of
Landsman et al. P12.2/P12.3: void by premise.

Open (next step defined): implement the probabilistic YK decoder (Bell
projection) or the deterministic one (Grover) and re-test the Petz
bridge: the conceptual connection (traversing = recovery channel)
remains intact and testable.

## P13: photon ring tower (spatial echoes)

**P13.2 CONFIRMED (the number)**: with 4 sub-rings, band 2–40 Gλ, 200
points, SNR=100/point: σ(γ)/γ = **0.29%**: the photon ring Lyapunov
exponent is measurable with sub-percent precision in this model. This
is the EHT-facing claim of the line.

**P13.1 partial**: in the deep regime (γ = 1.2→3.0, gap 0.147→0.0009,
2.3 decades):
- amplitude with γ fixed: exponent −0.86 (final local −0.98 → 1) ✓
- γ with free amplitudes: −1.67 (within 2 ± 0.5) ✓ CONFIRMED
- amplitude of the degenerating mode (a₄) with γ free: **−2.40 stable**
  (locals −2.37..−2.44): outside 3 ± 0.5: KILLED as frozen. The
  prediction of 3 assumed an isolated pair; the multi-tone tower gives
  2.4 (cluster regime, cf. Batenkov): a scope refinement, not a
  collapse.

Qualitative hierarchy (1 → 1.7 → 2.4) present and clean across decades
of gap. Data: p13_photon_ring.json, p13_deep.json, p13_a4.json;
p12_v3_{conj,T}.json.

## P12'': the bridge closed (YK decoder ↔ Petz)

Full Hayden–Preskill/Yoshida–Kitaev protocol (8 qubits, post-selected
Bell projection), gates with unit tests.

- **P12''.2 in the original formulation: KILLED BY THEOREM**: it
  compared with the Petz of the channel WITHOUT post-selection, which
  no-signaling forbids from containing information; the data obeyed
  with F_Petz = 0.2500 exact and independent of scrambling (an
  accidental verification of the theorem).
  Amendment A1 (before the re-test): Petz of the CONDITIONED channel.
- **P12''.1 CONFIRMED** (amended): F_max = 0.9467 at 12 scrambling
  steps (p_succ = 0.26); the dip at 8 steps is a revival of the kicked
  Ising in a small system, characterized in the sweep.
- **P12''.2 CONFIRMED** (amended): corr(F_YK, F_Petz_cond) = 0.979 over
  7 depths, with F_YK ≥ F_Petz_cond always (minimum ratio 1.05,
  consistent with the near-optimality of Petz).

Synthesis of the line: "traversing the wormhole = running the Petz
recovery of the conditioned channel", now measured. This welds the Petz
axis of the program (no-locking on a real QPU; collapse-vs-decoherence
discriminator) to the holographic side (HP/YK) into a single
operational object.
Data: p12_yk.json, p12_yk2.json.
