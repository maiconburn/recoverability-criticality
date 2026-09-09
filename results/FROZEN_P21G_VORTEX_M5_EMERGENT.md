# P21g, m = -5: escape count and modes born from the cut (freeze, 2026-09-09)

Frozen BEFORE any finite-B run at m = -5. State of the evidence:

- Finite-B escape counts 1, 2, 2, 3 for |m| = 1..4 (P21d/P21e).
- The scaled pure-vortex problem (P21f) reproduces every escaping mode
  to <= 2% and has resonances (Re c > 0, Im c > -2) numbering
  1, 2, 2, 3, 4, 4 for |m| = 1..6: it agrees with the finite-B counts
  through |m| = 4 and exceeds the frozen floor((|m|+2)/2) rule at
  |m| = 5 (four scaled resonances: 1.237-0.250i, 1.089-0.740i,
  0.779-1.203i, 0.296-1.586i).

Two readings, decided by the finite-B run at m = -5:

(R1) the floor rule is wrong and four B = 0 overtones escape at
     m = -5 (counts 1, 2, 2, 3, 4 = number of scaled resonances above
     some damping);
(R2) the floor rule holds (three escape from B = 0) and the fourth
     scaled resonance is a mode with NO B = 0 ancestor: it is born
     from the branch cut at some finite rotation B_b (the reverse of
     the absorption seen in P21.1) and joins the collapsing tower.

P21g.1 (finite-B count): robust tracking of the m = -5 overtones
n = 0..4 from B = 0 to B = 10 (kmax-gated classification as in P21e.2)
gives 3 escaping modes (R2) or 4 (R1).

P21g.2 (the born mode, if R2): at B = 10 and B = 20 there is a
principal-sheet root within 10% of c_3/B = (0.296 - 1.586i)/B that is
kmax-independent (600 -> 1500 -> 3000) and that, tracked DOWNWARD in B,
reaches the negative imaginary axis at a finite B_b (arrival from
below: Re(omega) -> 0 linearly as B decreases to B_b) rather than
connecting to any B = 0 overtone.
KILL of R2: no such root, or the root connects to a B = 0 overtone.

P21g.3 (universality of birth): if R2 holds at m = -5, the same
happens at m = -2 for the third scaled resonance (to be located with
Im c < -2 in the scaled problem) at B = 20: a principal-sheet root near
c_2/B with no B = 0 ancestor.
KILL: none found within the kmax gate.

Instrument: the robust tracker (`p21_vortex_m2_robust.py`) for the
finite-B counts; the scaled solver (`dbt_scaled.py`) for c_n; the
deep continued-fraction probe for kmax gates near the axis.
