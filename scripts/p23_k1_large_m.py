"""Pin the second-order WKB constant of the vortex tower (identified as
3/32 to 5e-5 from |m| <= 10): exact n = 0 and n = 1 members at
|m| = 15, 20, 30, 40 (complex-ray solver; rho_min scaled with |m| so the
inner branch does not underflow), against the elliptic first-order
value; |m| (c_exact - c_WKB1) - (-1/16) -> 3/32 = 0.09375 as |m| -> inf.
Output: results/p23_k1_large_m.json.
"""
import json
import pathlib
import sys

import mpmath as mp

sys.path.insert(0, "src")
from recoverability_ep.dbt_scaled import find_c_cplx  # noqa

mp.mp.dps = 25


def J_ell(c, am):
    return am * 2 * (mp.ellipk(1 - 4 * mp.mpc(c) / am) - mp.ellipe(1 - 4 * mp.mpc(c) / am))


def wkb1(am, n, seed):
    f = lambda cc: J_ell(cc, am) - 1j * mp.pi * (n + mp.mpf(1) / 2)
    return complex(mp.findroot(f, mp.mpc(seed), solver="muller", tol=1e-14, maxsteps=60))


OUT = {}
for am in (15, 20, 30, 40):
    m = -am
    rho_min = 0.02 * max(1.0, am / 8.0)
    for n in (0, 1):
        a = n + 0.5
        seed = complex(am / 4 - 0.375 * a * a / am + 1 / (32 * am), -a / 2 + 3 * a ** 3 / (32 * am * am))
        w1 = wkb1(am, n, seed)
        vals = []
        for kw in ({"theta": 0.5}, {"theta": 0.7}):
            try:
                c, res = find_c_cplx(seed, m, rtol=1e-12, rho_min=rho_min, rho_m=1.0, **kw)
                if res < 1e-7:
                    vals.append(c)
            except Exception as e:
                print(f"  |m|={am} n={n} theta={kw['theta']}: FAIL {str(e)[:50]}", flush=True)
        if not vals:
            continue
        c = vals[0]
        spread = abs(vals[0] - vals[-1])
        k1 = am * (c - w1)
        OUT[f"{am},{n}"] = {"exact": [c.real, c.imag], "wkb1": [w1.real, w1.imag], "k1_total": [k1.real, k1.imag], "second_order": k1.real + 1 / 16, "spread": spread}
        print(f"  |m|={am} n={n}: exact {c.real:.7f}{c.imag:+.7f}i  wkb1 {w1.real:.7f}{w1.imag:+.7f}i  |m|(exact-wkb1) = {k1.real:+.5f}{k1.imag:+.5f}i  second-order part = {k1.real + 1/16:.5f} (3/32 = 0.09375)  spread {spread:.0e}", flush=True)
        pathlib.Path("results/p23_k1_large_m.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
