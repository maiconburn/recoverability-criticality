# Top 5 PRE-LAB tests: synthesized ranking from the 6 search lanes

**Honesty legend**: [ONTOLOGY] = can discriminate the speculative ontology (L2 locking) against standard QM. [RE-VERIFICATION] = valuable, but only re-verifies/extends L1/L3 in new systems; it does not decide the ontology.

---

## 1. Two-task test on the same record: IBM Quantum (cloud, free tier) [ONTOLOGY]

**What we would do**: Reproduce the dissipative qubit with an EP2 via ancilla dilation + post-selection (published circuits: Dogra et al., Commun. Phys. 4, 26 (2021), code at github.com/Arty1498/Non-Hermitian; modernized versions with explicit gate decomposition in arXiv:2507.08129, Fig. 2). Collect the shot record with `memory=True`, truncate the SAME record at increasing N and extract in parallel: (a) the spectral/parametric reconstruction rate of (Omega, gamma); (b) the Petz/pretty-good recovery fidelity using the Petz circuits already validated on IBM hardware (Biswas & Mandayam, arXiv:2510.08719) or the low-depth compilations of Png & Scarani (PRA 112, 022613: 1-2 ancillas, 3-20 CNOTs). Sweep the knobs: distance to the EP, post-selection fraction, shots.

**What it tests**: L2 directly: it is the ONLY route identified across all lanes that measures the two rates on the same real quantum record. Standard QM predicts independent rates (ratio 0.27-0.99, moving; Petz does NOT halve at the EP). Observed locking or double-halving = a signature of new physics, falsifiable. It also delivers L1 (error vs N at the EP vs far from it) and L3 (post-selection success fraction as a natural N axis, cf. Jebraeilli & Geller PRA 111, 032211) for free. No published experiment has done the two tasks on the same record: an open niche.

**Cost/effort**: Zero monetary cost: the IBM Open Plan gives 10 min QPU/28 days (+ a one-time promotion of 180 min); Dogra used 8192 shots/point, Abbasi 4096: the campaign fits in the free tier. Effort: ~1-2 weeks of circuit engineering + analysis.

**First step TODAY (laptop)**: `git clone https://github.com/Arty1498/Non-Hermitian`; build the full pipeline (EP dilation + truncation + spectral fit + Petz) in the Qiskit simulator with a noise model of a Heron backend: validate that the two rates are extractable with the available shots BEFORE spending 1 second of QPU. The simulator result is, by itself, the reference standard-QM prediction.

---

## 2. Truncation of the Murch group's public data: a real dissipative qubit with an EP2 [RE-VERIFICATION L1/L3, partial ONTOLOGY]

**What we would do**: Download the two public murchlab repositories: (i) `Nonlinear-quantum-evolution-of-a-dissipative-superconducting-qubit` (arXiv:2510.25836: raw Rabi tomography CSVs, 10 drive/dissipation configurations = the "knobs", multiple initial states, notebooks that reconstruct 2x2/3x3 densities per time point); (ii) `Exploring-the-topology-...-shortcuts-to-adiabaticity` (PRX Quantum 7, 010337: x/y/z tomography time series in circumnavigation of the EP, 71 files + notebook). Truncate records at N points, fit the effective Hamiltonian, measure the error decay rate near vs far from the EP (L1); use the configurations/loop times as information windows (L3). From the density-matrix series, compute offline the Petz recovery vs truncation and compare it with the spectral rate from the same dataset.

**What it tests**: L1 with high power: it is the exact lineage of the Naghiloo 2019 platform where the halving was predicted; real quantum data, without any contact. L3 with medium power (discrete windows, not continuous). L2 only partially and with an honest caveat: the Petz here is computed offline over post-selected tomography; it is not the physical recovery on the same record; a "locking" seen this way would be suggestive, not decisive (the tomographic reconstruction is itself an estimator, contaminating the independence of the two rates). Use it as triage: if locking does not appear even here, the ontology's prediction already comes under pressure.

**Cost/effort**: Free, MIT license, ~5 MB + a larger repository; days, not weeks.

**First step TODAY (laptop)**: clone the two repositories, run the original notebooks until the figures are reproduced, and write the truncation script (fit of (Omega, gamma) with the record cut at N) on a single configuration near the EP.

---

## 3. Black hole ringdown: rate-halving at the Kerr avoided crossing [RE-VERIFICATION L1/L3, high statistical power]

**What we would do**: Three layers, all public: (a) Teukolsky benchmarks with exactly known amplitudes (Kubota-Motohashi, Zenodo 10.5281/zenodo.18511200, 10.3 GB, CC-BY, with a notebook): fits of N modes on truncated records, sweeping spins across the (2,2,n=5-6) avoided crossing at a/M≈0.9 (EP at a≈0.897+0.010i, Lo et al.) and the sharp (3,1) resonances at 0.952-0.997; (b) frequency tables + excitation factors (Zenodo 10.5281/zenodo.12696857 + Lo-Sabani-Cardoso CSVs) for synthetic ringdowns with a calibrated distance-to-EP dial; (c) the SXS catalog: 17 NR simulations with remnant spin 0.90±0.005 (SXS:BBH:4190, 3979, 1481, 3901, 4075, 0618, 0333, 4169...) vs hundreds at chi_f≈0.69: measure alpha(N) on-EP vs off-EP with qnmfits/jaxqualin.

**What it tests**: L1 with high discriminating power on the spectral side: a classical system, no noise, calibrated distance to the EP: if the L1 halving is universal, it HAS to show up here; if it does not appear even in clean data, the law's formulation needs revision before any lab. L3 likewise: fit-window dependence is the field's standard observable (the entire GW150914 controversy, with public posteriors Zenodo 5965773/6949492, is literally "extractable content vs window"). **It does not touch L2**: no quantum degree of freedom, zero power over the ontology; it contributes only falsification on the spectral side. Caveats to model: near the EP the fit model itself changes (a secular term linear in t: arXiv:2512.02110); pseudospectral instability of the overtones (Jaramillo et al. PRX 11, 031003); the avoided crossing is not generic (Lo et al.).

**Cost/effort**: Free; `pip install qnm qnmfits sxs jaxqualin`; the 10 GB dataset is optional at the start (the tables suffice for synthetics). Weeks of analysis, all on laptop/Colab.

**First step TODAY (laptop)**: `pip install qnm sxs qnmfits`; download Motohashi's excitation factor tables (lightweight), generate one synthetic ringdown at a/M=0.90 and another at 0.69, and run the first error-vs-N fit: a preliminary result in one afternoon.

---

## 4. EP order ladder (EP2 → EP3 → cusp): does the rate scale with the order? [RE-VERIFICATION L1 with a new prediction]

**What we would do**: Test not only the halving verified at EP2, but the generalization "rate/n at an order-n EP", a sharper prediction that no simulation in the program has verified yet. Public, machine-readable data: trapped ion LEP2/LEP3 with quantum jumps (figshare 10.6084/m9.figshare.30343429: density matrices, Liouvillian eigenvalues vs gamma0/gamma_phi, 200 reps/point); a 3rd-order exceptional line in NV (Source Data XLSX, Nat. Nanotech. 19, 160); CPA-EP3 magnonics (Zenodo 10.5281/zenodo.18410900); MEMS cusp vs EP vs diabolic point on the same device (figshare 10.6084/m9.figshare.19609350 + 29278061, 1/3 power-law response over multiple decades). Fit reconstruction error vs information budget at each order.

**What it tests**: L1 with high power to extend/break the law: a result of "rate/2 at EP2 but NOT rate/3 at EP3" would reformulate the law before the lab; confirmation on 2 quantum platforms (ion, NV) + 2 classical ones would be the strongest validation available without a lab. An L2-adjacent bonus: the ion data distinguish a Liouvillian vs a Hamiltonian EP, exactly where the prediction "Petz does not suffer halving at the Hamiltonian EP" is sharpest (but without a continuous record, it does not close L2). It does not discriminate the ontology.

**Cost/effort**: Free (figshare/Zenodo, CC-BY); medium effort: parsing heterogeneous MATLAB .fig and XLSX files is the real cost.

**First step TODAY (laptop)**: download the ion figshare (maintextdata.zip) and the NV XLSX; extract the Liouvillian eigenvalues vs control parameter and verify that the EP2/EP3 structure is re-fittable from the raw data.

---

## 5. Two-saddle crossover (L3) in raw multi-EP spectroscopy [RE-VERIFICATION L3, the cleanest test in the classical lane]

**What we would do**: Use the two largest public raw records near EPs: (i) Harris/Yale (Nat. Commun. 15, 1369; Zenodo 10.5281/zenodo.10451386, CC-BY): raw I/Q spectra (.dat) near THREE optomechanical EPs + complex eigenvalue sheets in .csv: truncate at N points/band windows, re-fit the eigenvalues, measure error vs N and the rate's dependence on the window; the multi-EP structure naturally provides the two "information addresses" of L3; (ii) the Kottos EP voltmeter (Zenodo 10.5281/zenodo.8250656, a 1.9 GB raw file) for genuine record truncation on a time series with real noise. A precision EP2 complement: the Kononchuk accelerometer (Zenodo 10.5281/zenodo.6397748, .mat) for the 1/sqrt(d) vs log noise-cost question.

**What it tests**: L3 with the best power available pre-lab: the rate-vs-budget-N crossover is directly measurable on raw data, with multiple competing EPs. L1 secondarily. Classical wave platforms: they validate the MATHEMATICS of the two saddles, not the quantum ontology; zero power over L2.

**Cost/effort**: Free, CC-BY, direct download; analysis from days to 1-2 weeks.

**First step TODAY (laptop)**: download Zenodo 10451386, read one I/Q .dat, fit the eigenvalues of one mode with the full window and then with half the window; if the fitted rate moves, the L3 observable exists in these data.

---

## Brutally honest summary

- **Only Test 1 decides the ontology (L2)**, and it is executable for free, without a lab. Everything else orbits it.
- Test 2 is the best cheap L2 triage (offline Petz), but with a built-in methodological confound: never sell a "locking" found there as a discovery.
- Tests 3-5 are re-verifications/extensions of L1/L3 in new regimes (gravitation, EP3/cusp, classical multi-EP). Real value: if L1/L3 fail on clean, public data, the program reformulates itself BEFORE spending any experimental credibility; if they survive, the stakes on Test 1 go up.
- Gaps worth an e-mail (not a partnership): the Naghiloo 2019 / PRLs 2021-22 raw data (Murch), the heterodyne records of the Huard group (Six-Rouchon already demonstrated the two tasks on the same record: the closest real L2 dataset, one request away), and verification of the deposit of the superconducting quantum Darwinism experiment (Sci. Adv., arXiv:2504.00781).
- Citation corrections inherited from the searches: "Wang, Lau, Clerk, Nature 583, 60 (2020)" does not exist (a conflation of Nat. Commun. 11, 1610 with Nat. Commun. 9, 4320); the repository of the bistable NV paper (hanfengw/BPNV) returned 404 on 2026-08-28.
