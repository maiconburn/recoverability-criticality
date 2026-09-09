"""P26: counter-rotating spectrum of the pure vortex with a REFLECTING
core (Dirichlet or Neumann wall at rho_c) against the absorbing tower
(frozen in results/FROZEN_P26_VORTEX_CORE.md).

Grid of seeds in Re c in (0.02, |m|/4 + 0.3), Im c in (-2, -0.005);
local secant from each seed (find_c_wall); roots kept if |W| < 1e-8
and reproduced at a second matching point (rho_m = rho_c + 1.0) to
1e-3. Output: results/p26_vortex_core.json.
Usage: p26_vortex_core.py [m ...]
"""
import json
import pathlib
import signal
import sys
import time

import numpy as np

sys.path.insert(0, "src")
from recoverability_ep.dbt_scaled import find_c_wall  # noqa

MS = [int(x) for x in sys.argv[1:]] or [-2, -4]


class SeedTimeout(Exception):
    pass


def _alarm(sig, frm):
    raise SeedTimeout()


signal.signal(signal.SIGALRM, _alarm)   # a few seeds drive the integrator into a NaN stall; 8 s per solve, then skip

CASES = [("dirichlet", 0.3), ("dirichlet", 0.5), ("dirichlet", 1.0), ("neumann", 0.5)]
OUT = {}
for m in MS:
    am = abs(m)
    for kind, rc in CASES:
        t0 = time.time()
        roots = []
        for re in np.linspace(0.06, am / 4 + 0.3, 10):
            for im in np.linspace(-0.01, -2.0, 12):
                signal.alarm(8)
                try:
                    c, res = find_c_wall(complex(re, im), m, rho_c=rc, kind=kind, rho_m=rc + 0.6, maxit=30)
                except (Exception, SeedTimeout):
                    signal.alarm(0)
                    continue
                signal.alarm(0)
                if not np.isfinite(c):
                    continue
                if res > 1e-8 or c.imag > 0 or c.real < -0.3 or c.imag < -2.6:
                    continue
                if any(abs(c - r) < 1e-4 for r in roots):
                    continue
                signal.alarm(8)
                try:
                    c2, res2 = find_c_wall(c, m, rho_c=rc, kind=kind, rho_m=rc + 1.0)
                except (Exception, SeedTimeout):
                    signal.alarm(0)
                    continue
                signal.alarm(0)
                if res2 < 1e-8 and abs(c2 - c) < 1e-3:
                    roots.append(c)
        roots.sort(key=lambda z: -z.imag)
        key = f"{m},{kind},{rc}"
        trapped = [z for z in roots if abs(z.imag) < 0.08 and 0 < z.real < am / 4]
        OUT[key] = {"roots": [[z.real, z.imag] for z in roots], "trapped": [[z.real, z.imag] for z in trapped], "seconds": time.time() - t0}
        print(f"  m={m} {kind} rho_c={rc}: {len(roots)} roots: {[f'{z.real:.4f}{z.imag:+.4f}i' for z in roots]}; trapped (|Im|<0.08, 0<Re<|m|/4): {len(trapped)}  ({time.time() - t0:.0f}s)", flush=True)
        pathlib.Path("results/p26_vortex_core.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
