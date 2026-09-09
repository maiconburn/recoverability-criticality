# P26, absorbing versus reflecting vortex core: verdicts (2026-09-10)

Preregistration: `FROZEN_P26_VORTEX_CORE.md` (commit 1f6b6e7). Instrument:
`dbt_scaled.wronskian_wall` / `find_c_wall` (wall at rho_c, Dirichlet
or Neumann, integrated outward on the real axis; outgoing ray at
infinity as in the complex-ray solver; a per-seed alarm skips the few
seeds that stall the integrator). Script `p26_vortex_core.py`; data
`p26_vortex_core.json`. Reference (absorbing core, P23):
m = -2: 0.4675-0.2536i, 0.0707-0.6887i; m = -4: 0.9842-0.2510i,
0.7941-0.7351i, 0.4054-1.1652i.

## Spectra with a reflecting core (Re c > -0.3, Im c > -2.6)

| m | wall | rho_c | roots (Re c > 0 first) | least damped |
|---|---|---|---|---|
| -2 | Dirichlet | 0.3 | 0.6138-0.1768i, 0.1515-0.9744i | 0.177 |
| -2 | Dirichlet | 0.5 | 0.5251-0.0771i, 0.2690-0.8184i | 0.077 |
| -2 | Dirichlet | 1.0 | 0.4956-0.4124i, -0.1644-0.7917i | 0.412 |
| -2 | Neumann | 0.5 | 0.6004-0.3427i, -0.0887-0.9361i | 0.343 |
| -4 | Dirichlet | 0.3 | 0.6408-0.0006i, 1.1765-0.4573i, 0.8635-1.3299i, -0.0060-2.0364i | 0.0006 |
| -4 | Dirichlet | 0.5 | 1.1450-0.2013i, 0.9968-0.9909i, 0.3334-1.6689i | 0.201 |
| -4 | Dirichlet | 1.0 | 1.1274-0.3005i, 0.8244-0.9615i, 0.2196-1.3949i | 0.301 |
| -4 | Neumann | 0.5 | 0.7470-0.0031i, 1.1312-0.5470i, 0.7397-1.3314i, -0.0924-1.8886i | 0.003 |

## Verdict table

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P26.2 reflecting core: at least one trapped mode (Im < 0.08, 0 < Re < |m|/4) per rho_c, more for smaller rho_c; no 1:3:5 ladder within 15% | KILL: none for some rho_c, or ladder at rho_c = 0.5 | trapped modes exist only where the cavity between the wall and the barrier is long enough: m = -4 Dirichlet rho_c = 0.3 (0.6408-0.0006i) and Neumann 0.5 (0.7470-0.0031i); none at m = -2 (any rho_c) nor at m = -4 Dirichlet 0.5, 1.0. The ladder is absent in every reflecting case (damping ratios 5.5, 10.6, 1.9, 2.7 at m = -2; 762, 4.9, 3.2, 176 for the first two members at m = -4) | KILLED as written (the "per rho_c" clause), the ladder clause holds |
| P26.3 damping of the least-damped m = -2 mode differs by > 3 between the two cores at rho_c = 0.5 | KILL: as P26.2 | absorbing 0.254 against Dirichlet-0.5 0.077: ratio 3.3 | CONFIRMED (barely; at rho_c = 0.3 or 1.0 the ratio is 1.4 or 0.6) |
| P26.4 Neumann at rho_c = 0.5 same qualitative answer as Dirichlet | KILL: no trapped mode | m = -2: Dirichlet has the long-lived 0.077 mode, Neumann does not (0.343); m = -4: the reverse (Neumann trapped 0.003, Dirichlet none) | KILLED |

## What the calculation says

- An absorbing core gives a scale-free spectrum, the light-ring ladder
  with damping -(2n+1)/4 (P23). A reflecting core gives a spectrum
  that depends on the core radius and on the wall type, because the
  region between the wall and the light-ring barrier is a cavity:
  where its Bohr-Sommerfeld phase int_{rho_c}^{rho_-} sqrt(Q) d rho
  reaches a level, an ultra-narrow trapped mode appears (damping
  6e-4 to 3e-3, the tunnelling rate through the barrier), and the
  light-ring-like members are shifted and re-damped by the cavity
  (0.077 to 0.41 for the m = -2 fundamental across rho_c).
- The frozen "at least one trapped mode per rho_c" assumed every
  cavity holds a level; at m = -2 the phase is half that of m = -4 and
  no level fits for rho_c >= 0.3; at m = -4, rho_c = 0.5 the Dirichlet
  and Neumann cavities sit on opposite sides of a level. The count of
  trapped modes should follow floor(phase/pi + 1/2 - delta_wall), a
  rule not frozen here and left as the next freeze if the line is
  continued.
- The diagnostic that survives is the fingerprint, not the count: a
  ringdown whose counter-rotating damping rates form the ladder
  1 : 3 : 5 independent of the core size is an absorbing (horizon-like)
  core; damping rates that move with the core radius, or a mode with
  Q ~ 10^2-10^3 times that of the fundamental, are a reflecting core.
  For a tank this is a measurement of damping rates versus sink
  radius at fixed circulation, in the shallow regime of P23.

Tombstones 30 (P26.2 as written) and 31 (P26.4) in `GRAVEYARD.md`.
