**To:** authors of the pole-skipping metric-reconstruction program (Lu, Ran, Wu — verify addresses on arXiv:2506.12890)
**Subject:** The convergence *cost* of your reconstruction program, quantified — with a zero-parameter rate law

Dear authors,

Your result that pole-skipping data reconstructs the near-horizon metric
order-by-order left open, as far as I can tell, the quantitative question of
*how fast* — i.e., the information cost of the reconstruction. I measured it
in the 5D Einstein-Gauss-Bonnet black brane, using N horizon Taylor
coefficients as the information proxy and constrained Pade resummation:

- The spectral error at distance d from the fundamental mirror-mode
  exceptional point obeys eps ~ e^(-alpha N)/sqrt(d), with the rate halving
  exactly at the EP (2 alpha_EP / alpha = 1.00, nine couplings, including two
  beyond the causality window), and all (N, d) data collapsing onto
  sqrt(u+1) - sqrt(u).
- The rate alpha(lambda) is itself predictable with zero fitted parameters
  (linear response at the EP x Pade error of b(z) alone): R^2 = 0.9988, and
  4-decimal agreement on two virgin couplings frozen before measurement.
- The cost functional has two "informational addresses" (near-horizon and
  near-boundary saddles) whose dominance switches with N — the measured rate
  is a window-dependent blend (1.46 -> 0.68 in the benchmark).

By-products possibly of independent interest: the full mirror-EP trajectory
q^2_c(lambda), and its extinction at lambda_ext = 0.1091(2) > 9/100.

Code, frozen-prediction files and reports: https://github.com/maiconburn/recoverability-criticality (laptop-reproducible,
AI-assisted independent work — corrections welcome). If a cost/convergence
layer would strengthen your program, I'd be glad if any of this is useful.

Best regards,
Maicon Esteves
