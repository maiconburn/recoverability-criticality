**To:** Kater Murch (murch@physics.wustl.edu — verify current address on the group page)
**Subject:** Two-task analysis of your public dissipative-qubit data + a frozen EP protocol your lab could run

Dear Prof. Murch,

I'm an independent researcher in Brazil. Using the public data from your group's
repositories (the 101-amplitude PT-sweep in
`Nonlinear-quantum-evolution-of-a-dissipative-superconducting-qubit`), I measured
two costs from the same records as a function of distance to the exceptional
point: (a) the bootstrap uncertainty of estimating the effective-Hamiltonian
eigenvalue pair, and (b) the uncertainty of recovering the initial state. They
*anti-correlate* through the EP — the spectral cost rises ~3× while state
recovery gets easier — which cleanly instantiates, in your hardware, the
independence of "parameter information" and "state recoverability" near an EP.

I also ran a dilated two-task version (spectral estimation + a physical Petz
recovery circuit, same shot budget) on ibm_fez, with a frozen simulator
reference: 4× spectral enhancement in the EP band, Petz fidelity flat. As far
as I could find, no published experiment has measured both rates on the same
record; a protocol with preregistered kill criteria for a Naghiloo-class setup
is written up in the repository (p6/SPEC.md).

Everything (code, frozen predictions, reports) is here: [REPO_URL].
Two small asks, if any of this is of interest:
1) Is `temp_tools.py` (the tomography conventions for the CSV releases)
   available? It would unlock the full-tomography version of the reanalysis.
2) Any interest in the two-task protocol on your platform? The dry run says
   the discriminating power is ~5× above the noise.

Honestly stated: this is AI-assisted work by a non-academic, produced fast;
I'd value any correction.

Best regards,
Maicon Esteves
