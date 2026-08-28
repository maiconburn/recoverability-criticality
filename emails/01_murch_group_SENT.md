**Sent 2026-08-29 to katermurch@berkeley.edu (verified via arXiv:2510.25836 PDF) — Gmail id 1a04aa140fb6bcf0**

Subject: Two-task analysis of your public dissipative-qubit data (spectral cost vs Petz recovery through the EP)

Dear Prof. Murch,

I'm an independent researcher in Brazil. Using the public data from your group's repository "Nonlinear-quantum-evolution-of-a-dissipative-superconducting-qubit" (the 101-amplitude PT sweep, pf_pe_pg_july2nd.pkl), I measured two costs from the same records as a function of distance to the exceptional point: (a) the bootstrap uncertainty of estimating the effective-Hamiltonian eigenvalue pair, and (b) the uncertainty of recovering the initial state. They anti-correlate through the EP - the spectral cost rises ~3x while state recovery gets easier - a clean instantiation, in your hardware, of the independence of parameter information and state recoverability near an EP.

I also ran a dilated two-task version (spectral estimation plus a physically executed Petz recovery circuit, same shot budget) on ibm_fez, against a frozen simulator reference: ~4x spectral enhancement in the EP band, Petz fidelity flat. As far as I could find, no published experiment had measured both quantities on the same record.

Everything (code, frozen prediction files, reports) is public here:
https://github.com/maiconburn/recoverability-criticality
(your data analysis: prelab/REPORT_MURCH.md and prelab/analyze_sweepJ.py)

One small ask, if easy: is temp_tools.py (the tomography sign/scale conventions for the CSV releases) available anywhere? It would unlock the full-tomography version of the reanalysis - the population-only observable was all I could use convention-free.

Honestly stated: this is AI-assisted work by a non-academic, produced fast; every key number is cross-validated against literature anchors in the repository, and I would value any correction.

Best regards,
Maicon Esteves
maicon.burn@gmail.com
