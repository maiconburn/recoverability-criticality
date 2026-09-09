# P28, the Kerr analogue of the escape rule: verdicts (2026-09-10)

Preregistration: `FROZEN_P28_KERR_SURVIVORS.md` (commit c30a65b).
Instrument: `p28_kerr_survivors.py` (qnm NearbyRootFinder, m = 0,
s = -2; the angular seed keyword is `A_closest_to`, the first run had
passed `A0` and was silently on the l = 2 branch for every l; fixed
before any verdict) and `p28_l2_continuation.py`. Instrument change
recorded before the verdicts: the towers were computed at a = 0.99
instead of the frozen 0.9999, where the fraction does not converge
from rough seeds; the cached members move by ~1e-3 between the two.
Data: `p28_kerr_survivors_l{2,3,4}.json`, `p28_l2_continuation.json`.

## The towers at a = 0.99 (beyond the qnm cache, which stops at n = 7)

| l | n | omega M (Re, Im) |
|---|---|---|
| 2 | 0..9 | 0.4237-0.0727i, 0.4021-0.2207i, 0.3593-0.3776i, 0.2980-0.5520i, 0.2287-0.7519i, 0.1658-0.9756i, 0.1165-1.2132i, 0.0802-1.4573i (cached, not re-gated), 0.0544-1.7039i, 0.0369-1.9517i; n >= 10 not converged (seeds Re ~ 0.03) |
| 3 | 0..11 | 0.6633-0.0775i, 0.6481-0.2338i, 0.6180-0.3944i, 0.5733-0.5628i, 0.5160-0.7432i, 0.4504-0.9393i, 0.3830-1.1527i, 0.3199-1.3808i, 0.2644-1.6189i, 0.2168-1.8627i, 0.1764-2.1094i, 0.1421-2.3575i; n >= 12 not converged |
| 4 | 0..12, 15 | 0.8882-0.0793i, 0.8765-0.2387i, 0.8532-0.4006i, 0.8184-0.5669i, 0.7727-0.7399i, 0.7174-0.9221i, 0.6549-1.1157i, 0.5885-1.3222i, 0.5224-1.5415i, 0.4598-1.7716i, 0.4026-2.0097i, 0.3512-2.2533i, 0.3055-2.5002i, (n = 15) 0.1958-3.2493i; n = 13, 14, 16-18 not converged |

Two structures, the same for all three l:

- Re(omega) does not cross zero at an index; from n ~ 6 on it decays
  GEOMETRICALLY in n, ratio Re_{n+1}/Re_n -> 0.68 (l = 2), 0.81 (l = 3),
  0.87 (l = 4).
- The damping spacing -d Im/dn rises from 0.15-0.16 at low n to 0.248
  by n ~ 9-12, i.e. to 1/4: at high spin the m = 0 tower's damping
  becomes the quarter-integer ladder of the polynomial points -i n/4
  (Cook-Zalutskiy's endpoints), for every l.

## Verdict table

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P28.1 first member with Re < 0.02 at n*(l) +- 1, n* = 8, 18, 25 | KILL: off by >= 3 | l = 2: no member below 0.02 up to n = 9 (0.037), n >= 10 not converged; the members n = 8, 9 keep Re fixed to 1.6% from a = 0.99 to 0.994 (a zero-damping member would lose 22%), so at these spins they are damped modes with small real parts, not a crossing; l = 3, 4: the instrument stops at n = 11, 15, short of 18, 25 | KILLED for l = 2 as frozen (no crossing; geometric decay instead); UNTESTABLE for l = 3, 4 with this instrument |
| P28.2 Re fitted by w0 - k a^2 + k' a^4 with residual < 0.01 and k' > 0 | KILL: residual > 0.03 or k' < 0 twice | residuals 0.0018, 0.0102, 0.0200; k' = +1.1e-4, +2.8e-5, +1.2e-5; k = 0.0120, 0.0076, 0.0057 | passes its kill; the 0.01 clause holds at l = 2 only |
| P28.3 Im linear in n to 10% | KILL: nonlinear > 25% | spacing 0.148 -> 0.248 (l = 2), 0.156 -> 0.248 (l = 3), 0.159 -> 0.247 (l = 4): 60% | KILLED |

## What it means

The vortex escape rule rests on a scale-free strong-rotation limit
(the pure vortex, elliptic tower, a crossing index set by the
light-ring anharmonicity). Kerr's high-spin m = 0 tower is not of that
kind: its real parts fade geometrically with the overtone index and
its damping locks onto the polynomial ladder -i n/4, so the
damped/zero-damped split that Cook-Zalutskiy's onsets (8, 18, 25)
encode is a property of the a -> 1 limit, which Leaver's fraction at
fixed spin does not reach for n >= 10. The naive analogue of the
escape rule dies; what survives is descriptive: the anharmonic
decrease of Re with a positive quartic term (P28.2) and the two
structures above, which are new data beyond the public tables and
belong to the Cook-Zalutskiy bookkeeping rather than to a count law.
Tombstones 32 (P28.1) and 33 (P28.3). Instrument lesson 14: check a
library's keyword names against its source before relying on a seed
(the `A0` silently ignored would have produced l = 2 towers labelled
l = 3, 4; the identical digits gave it away).
