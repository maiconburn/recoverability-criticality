# P27, the trapped-mode count of a reflecting vortex core: verdicts (2026-09-10)

Preregistration: `FROZEN_P27_CAVITY_COUNT.md` (commit 60622e8). Instrument:
`dbt_scaled.wronskian_wall` scan (`p26_vortex_core.py` with explicit
cases). Data: `p27_cavity_count.json`.

## Blind cases

| case | |m| | wall | rho_c | predicted count / c | exact trapped mode | count | position |
|---|---|---|---|---|---|---|---|
| A | 2 | Dirichlet | 0.15 | 0 (borderline) | none (roots 0.5742-0.1090i, 0.2617-0.9619i) | ok | |
| B | 4 | Dirichlet | 0.2 | 1 / 0.487 | 0.5146-0.0001i | ok | 5.7% |
| C | 4 | Neumann | 0.2 | 0 | none (roots 1.0436-0.0693i, 1.1541-0.8132i, 0.6178-1.6881i) | ok | |
| D | 6 | Dirichlet | 0.5 | 1 / 1.013 | 1.0330-0.0001i | ok | 2.0% |
| E | 6 | Dirichlet | 0.3 | 1 / 0.208 | 0.2328-0.0000i | ok | 12% |
| F | 6 | Neumann | 0.5 | 0 | none (roots 1.5391-0.0659i, 1.7120-0.7465i, 1.4377-1.5498i, 0.8283-2.2482i) | ok | |

## Verdict table

| prediction | frozen | measured | verdict |
|---|---|---|---|
| P27.1 counts right in >= 5 of 6; every position within 8% | KILL: two counts wrong or a position off > 15% | 6/6 counts; positions 5.7%, 2.0%, 12% | CONFIRMED on the counts; the 8% position clause missed once (case E, 12%; the trapped mode sits lowest in the well, where the first-order phase is least accurate) |
| P27.2 trapped dampings < 0.02; the deeper (smaller Re c) the narrower | KILL: a trapped mode with Im < -0.05 | dampings 1e-4 (B), 1e-4 (D), < 5e-5 (E); E narrower than D | CONFIRMED |

## Reading

With the eight P26 cases, the cavity rule is now 14/14 on counts.
The trapped modes are the Bohr-Sommerfeld levels of the region
between the wall and the light-ring barrier, phase pi(n + 3/4) for a
node at the wall and pi(n + 1/4) for a Neumann wall, with tunnelling
dampings 1e-4 and below; the count changes with the core radius, the
wall type and the azimuthal number, which is the fingerprint of a
reflecting core (P26). A second fingerprint appears in every
reflecting case: a barrier-top resonance just ABOVE the light-ring
frequency |m|/4 with damping 0.07-0.09 (m = -4, rho_c = 0.2 Neumann:
1.044-0.069i; m = -6: 1.539-0.066i, 1.582-0.090i; m = -2, rho_c = 0.5:
0.525-0.077i), three times longer-lived than the absorbing fundamental
(0.25), which the absorbing core never shows.
