# P21e, the escape count at m = -4 (addendum freeze, 2026-09-09)

Frozen BEFORE any m = -4 run. State of the evidence:

- m = -1: one escaping mode (n = 0); n = 1, 2, 3 absorbed.
- m = -2: two escaping (n = 0, 1); n = 2, 3 absorbed.
- m = -3: two escaping (n = 0, 1); n = 2 absorbed at B_c ~ 1.6 (deep
  kmax 10k/20k probe: Re(omega) = 0.0228, 0.0093, 0.0059, 0.0016 at
  B = 1.30, 1.45, 1.50, 1.60, linear extrapolation to zero at ~1.64),
  n = 3 absorbed at 0.482. This KILLS P21d.1 (the |m| rule).

Two candidate rules survive the data 1, 2, 2:
(a) saturation: exactly two modes escape for every |m| >= 2;
(b) floor((|m| + 2)/2): 1, 2, 2, 3, 3, ...

P21e.1: for m = -4, tracked to B = 10 with the robust tracker
(n = 0..5), the number of escaping modes (Re and Im both decreasing
towards zero, no arrival up to B = 10) is 2 under (a) or 3 under (b);
n >= 3 (a) or n >= 4 (b) arrive at finite B_c < 3.
Reading: 2 escaping confirms (a) and kills (b); 3 confirms (b) and
kills (a); any other count kills both (new rule needed).

P21e.2 (classification robustness): the escape/arrival classification
of each mode is decided where the continued fraction still converges
(Re(omega) > 0.02, kmax 600 vs 1500 agreeing to 1e-3): an escaping mode
has Im(omega) -> 0 together with Re(omega) (collapse onto the branch
point), an arriving one has Im(omega) tending to a finite value while
Re(omega) -> 0 linearly. The last 1e-3 of Re near the cut is never
used for the classification.

Instrument lesson carried over from P21d: near the negative imaginary
axis the continued fraction converges only for kmax growing like
1/Re(omega)^2; roots that move with kmax (600 -> 1500 -> 3000) are
truncation artifacts, not modes (the m = -3 "cut-hugging" trajectory
for B in [1.9, 4.7] was such an artifact).
