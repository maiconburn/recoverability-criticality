# The graveyard — what we discarded, with pride

Every entry below is a hypothesis we took seriously, tested, and killed —
most of them our own, several within hours of proposing them. The trail is
public because the discipline that kills wrong ideas before readers see
them survive IS the method. Detailed post-mortems live in `ERRATA.md` and
the linked reports.

| Hypothesis | Fate | Record |
|---|---|---|
| **The founding conjecture: can strong-curvature backgrounds suppress environmental decoherence and restore quantum coherence in macroscopic degrees of freedom?** The inverse of the Penrose–Diósi gravitationally-induced-collapse program: instead of gravity classicalizing quantum states, whether horizon-scale physics could re-quantize classical ones. | The testable mechanism extracted from the conjecture failed its first controlled tests; the program pivoted to what the formalism actually supported — information cost near spectral critical points. Recorded as refuted from the outset. | `results/RESULTS.md` |
| "The EP extinguishes at λ_ext = X" | Died three times (0.1091 → 0.1248 → 0.1150). Every better microscope moved the number — the classic signature of measuring the instrument, not nature. The single-threshold CONCEPT was wrong: it is a forest of families, each with its own termination. | `ERRATA.md` E1–E3 |
| Unification with the eikonal threshold 1/8 (Konoplya–Zhidenko) | Retracted in full. Too beautiful; the data declined. | `ERRATA.md` E2 |
| EP-3/EP-4 on the cosmological horizon | Numerical artifact of a matrix chain test; killed by an exact Γ-function theorem the same day. | `results/RESULTS_P8_FASE1.md` |
| "The deep family does not halve" | Void — we measured the wrong channel, at the instrument floor. The test is indeterminate, not negative. | `results/RESULTS_DEEP_FAMILY.md` |
| EP-isolation hypothesis for the halving | Dead by its own discriminator: nearest-neighbor distances came out inverted vs its prediction. | `results/RESULTS_DEEP_FAMILY.md` |
| Closed form C = 1/(\|A₊−A₋\|·√F⊥) for the metrology constant | Refuted — measured C barely depends on the amplitude difference. | `results/RESULTS_P8_FASE1.md` |
| The "cosmological clock" (localized log feature from slow-roll EP crossing) | Demoted — two honest dynamical mode-evolution tests show no localized anomaly; single-k evolution is analytic in ν. The correct statement needs dynamical squeezed correlators. | `results/RESULTS_P8_FASE1.md` adendo 8 |
| "Information is a single currency" (spectral cost ⇔ recovery cost locking) | Refuted three times over: in simulation, in published superconducting-qubit data, and on a real quantum processor. | `prelab/REPORT_QPU.md`, `p6/RESULTS_P6.md` |

What survived every attack so far is in the README. Nothing enters that
list without first walking past this page.
| P10.1: a Hermitian periodic drive creates exceptional points at the Floquet replica resonance | Died by its own frozen criterion: the resonance opens a Rabi-type anticrossing (gap growing with drive amplitude, eigenvectors far from collinear). The death taught the mechanism: Hermitian coupling between frequency layers opens gaps; dissipative coupling makes them collide, which became the sharpened P10.4 and was confirmed at the 1e-10 level. | `results/RESULTS_P10_FLOQUET.md` |
| P11.1: a wormhole's twin-throat doublet splits exponentially in the throat separation | Died of a modeling error made at freezing time: the exponential symmetric-antisymmetric doublet belongs to a BOUND double well; an open two-barrier cavity (the wormhole) instead carries a tower of cavity modes (the echoes) whose spacing scales like pi over the cavity length, which is what the validated instrument measured. The correct detectability question (small cavity-mode amplitudes under the barrier ringdown) is posed but not yet frozen. | `results/RESULTS_P11_WORMHOLE.md` |
| P12.1: the minimal coupled-qubit wormhole (3+3, no decoder) shows a traversability window | Dead with a physics lesson, after two instrument iterations (a misplaced message caught by a sanity check, then a broken qubit-embedding caught by unit tests): with the clean protocol the coupling alone transfers at most 0.02 bits to the mirror qubit. The decoder-free window is a large-N semiclassical phenomenon; small systems need the Yoshida-Kitaev decoder, which is the documented next step. | `results/RESULTS_P12_P13.md` |
| P13.1 (amplitude task): the degenerating subring amplitude costs gap^-3 | The isolated-pair exponent does not survive the multi-tone tower: the measured exponent is a stable -2.40 over two decades, the cluster regime of Prony-type estimation. Scope refinement recorded; the frequency task confirmed its window. | `results/RESULTS_P12_P13.md` |
