# P11: frozen before measuring (author's question: wormholes;
# "some way to experiment with our ideas?")

Date: 2026-08-30. Minimal model from the echo literature: symmetric
double barrier V(x) = (V0/2)[sech²(x−L/2) + sech²(x+L/2)] in the
tortoise coordinate (two "throats" separated by L); V0 = 0.3, unit
width. QNMs by shooting in complex ω with outgoing conditions at both
ends (Wronskian). The fundamental pair becomes a symmetric/antisymmetric
DOUBLET.

## P11.1: exponential splitting
δω(L) ≡ |ω₊ − ω₋| decays exponentially with the separation: ln δω linear
in L (R² > 0.98) over the range L ∈ [6, 16].
KILL: systematic curvature (power law or saturation).

## P11.2: hierarchy in the doublet (the cost of seeing a wormhole)
The CRB for estimating the splitting (free amplitudes) from a
finite-duration ringdown scales as δω^(−2±0.5), and amplitude with free
frequencies as δω^(−3±0.5): the same hierarchy of the program, now
saying: the SNR needed to DISTINGUISH a wormhole from a black hole by
agnostic spectroscopy grows exponentially with L (via δω(L)).
KILL: exponents outside the windows.

## P11.3: template beats agnostic exponentially
With frequencies fixed by a template (modeled search, LVK style), the
cost drops to δω^(−1±0.5); required SNR ratio
(agnostic/template) > 10 at the largest L of the sweep.
KILL: ratio < 10, or template exponent outside the window.

## P11' (frozen 2026-08-30, after the death of P11.1, BEFORE measuring)
Excitation specified: 1+1D wave equation, ∂²ψ/∂t² = ∂²ψ/∂x² − V(x)ψ,
same double-barrier V (U0=0.15, throats at ±L/2); initial condition a
Gaussian pulse ψ(x,0)=exp[−(x−x_s)²/2σ²], σ=2, x_s=−(L/2+15), ∂ψ/∂t(0)
such that the pulse travels toward +x; observer at x_o=+(L/2+20);
absorbing boundaries. "Black hole" reference: SINGLE barrier at x=+L/2,
same excitation and observer.

P11'.1 (echoes): the wormhole signal shows an echo train with delay
between echoes Δt = 2L ± 15% (round-trip time of the cavity).
KILL: no train, or delay outside the window.

P11'.2 (detectability): defining D(SNR) as the wormhole-vs-BH
distinction statistic via Fisher on the full signal (post-prompt
window), the minimum SNR for 5σ grows MONOTONICALLY with L over the
range L ∈ [8, 24] and the ratio SNR_min(L=24)/SNR_min(L=8) > 3.
KILL: non-monotonic or ratio ≤ 3.

P11'.3 (template wins): a search with the full wormhole template (known
shape, only the global amplitude free) requires SNR ≥ 10× lower than the
agnostic detection of "extra post-prompt energy" (blind window) at the
largest L.
KILL: ratio < 10.
