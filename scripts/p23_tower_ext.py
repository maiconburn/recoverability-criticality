"""P23 extension (after the freeze; recorded as such): action-WKB and
complex-ray towers at |m| = 12 and 15, where kappa |m| + 1/2 = 10.11 and
12.51 (the second is borderline: the law predicts N(15) = 12 with the
twelfth member close to the axis). Output: results/p23_tower_ext.json.
"""
import json
import pathlib
import sys
import time

import mpmath as mp

sys.path.insert(0, "src")
from recoverability_ep.dbt_scaled import find_c_cplx  # noqa

mp.mp.dps = 25
KAPPA = 0.800805


def J(gamma):
    gamma = mp.mpc(gamma)
    s = mp.sqrt(1 - 4 * gamma)
    rm, rp = (1 - s) / (2 * gamma), (1 + s) / (2 * gamma)
    D = rp - rm
    f = lambda t: mp.sqrt(t * (1 - t)) * mp.sqrt(gamma * (rm + t * D) ** 2 + (rm + t * D) + 1) / (rm + t * D) ** 2
    return mp.sqrt(gamma) * D ** 2 * mp.quad(f, [0, 0.5, 1])


def law(m, n):
    am = abs(m)
    return complex(am / 4 - 0.375 * (n + 0.5) ** 2 / am, -(2 * n + 1) / 4)


def action_wkb(m, n):
    am = abs(m)
    f = lambda g: J(g) - 1j * mp.pi * (n + mp.mpf(1) / 2) / am
    return complex(mp.findroot(f, mp.mpc(law(m, n)) / am, solver="muller", tol=1e-12, maxsteps=60) * am)


OUT = {}
for m in (-12, -15):
    am = abs(m)
    N_law = int(mp.floor(KAPPA * am + 0.5))
    t0 = time.time()
    rows = []
    for n in range(N_law + 2):
        try:
            w = action_wkb(m, n)
        except Exception:
            w = None
        c = None
        spread = None
        if w is not None and n >= N_law - 3:          # exact only near the crossing (cost)
            vals = []
            for kw in ({"theta": 0.5, "rho_m": 1.0}, {"theta": 0.8, "rho_m": 1.0}):
                try:
                    cc, res = find_c_cplx(w, m, rtol=1e-12, **kw)
                    if res < 1e-7:
                        vals.append(cc)
                except Exception:
                    pass
            if len(vals) == 2 and abs(vals[0] - vals[1]) < 1e-3:
                c, spread = vals[0], abs(vals[0] - vals[1])
        rows.append({"n": n, "action_wkb": [w.real, w.imag] if w else None, "exact": [c.real, c.imag] if c else None, "spread": spread})
        print(f"  m={m} n={n}: action-WKB {f'{w.real:.4f}{w.imag:+.4f}i' if w else '----'}  exact {f'{c.real:.4f}{c.imag:+.4f}i' if c else '----'}", flush=True)
    N_w = sum(1 for r in rows if r["action_wkb"] and r["action_wkb"][0] > 0)
    N_ex = sum(1 for r in rows if r["exact"] and r["exact"][0] > 0) + sum(1 for r in rows if r["exact"] is None and r["n"] < N_law - 3)
    OUT[str(m)] = {"rows": rows, "N_law": N_law, "N_action_wkb": N_w, "N_exact": N_ex, "kappa_m_plus_half": KAPPA * am + 0.5}
    print(f"  m={m}: kappa|m|+1/2 = {KAPPA * am + 0.5:.3f}; N law {N_law}, action-WKB {N_w}, exact {N_ex} ({time.time() - t0:.0f}s)", flush=True)
    pathlib.Path("results/p23_tower_ext.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
