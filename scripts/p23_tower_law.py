"""P23.1 / P23.1b: the pure-vortex tower at |m| = 8, 9, 10 (count law
N(m) = floor(0.808 |m| + 1/2) against N = |m| - 1) and the Iyer-Will
WKB (second and third order) on the scaled potential, frozen in
results/FROZEN_P23_TOWER_LAW.md.

Tower: dbt_scaled.find_c (inner branch +1) from the law's seeds
c_n = |m|/4 - [0.383 (n+1/2)^2 - 0.033]/|m| - i(2n+1)/4; a root is
accepted if re-solving with a different matching point (rho_m 0.7)
and a different inner cutoff (rho_min 0.01) moves it by < 0.03.

WKB: Q(rho, c) = (c - m/rho^2)^2 - (m^2 - 1/4)/rho^2; the extremum
rho_0(c) (Q_rho = 0, complex Newton from rho = 2) and the derivatives
Q^(k)(rho_0) are exact (sympy); the eigencondition
i Q_0 / sqrt(2 Q_0'') - Lambda - Omega = n + 1/2 (Iyer-Will 1987,
Eqs. 1.5) is solved for complex c by Muller from the law's seed, at
second order (Lambda only) and third order (Lambda + Omega).
"""
import json
import pathlib
import sys
import time

import mpmath as mp
import numpy as np
import sympy as sp

sys.path.insert(0, "src")
from recoverability_ep.dbt_scaled import find_c  # noqa

K0, K1 = 0.383, -0.033
OUT = {"law": {"k0": K0, "k1": K1}}


def law(m, n):
    am = abs(m)
    return complex(am / 4 - (K0 * (n + 0.5) ** 2 + K1) / am, -(2 * n + 1) / 4)


def N_law(m):
    am = abs(m)
    return int(np.floor(0.808 * am * (1 + 0.07 / am ** 2) + 0.5))


# ------------------------------------------------------------------ towers
def robust_root(seed, m):
    try:
        c, res = find_c(seed, m, branch=+1, rho_m=1.0, rho_min=0.02)
    except Exception:
        return None
    if res > 1e-6:
        return None
    checks = []
    for kw in ({"rho_m": 0.7, "rho_min": 0.02}, {"rho_m": 1.0, "rho_min": 0.01}, {"rho_m": 1.4, "rho_min": 0.02}):
        try:
            c2, res2 = find_c(c, m, branch=+1, **kw)
            checks.append(abs(c2 - c) if res2 < 1e-6 else float("inf"))
        except Exception:
            checks.append(float("inf"))
    return c, max(checks)


MS = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 and sys.argv[1] != "--wkb" else [-8, -9, -10]
WKB_ONLY = len(sys.argv) > 1 and sys.argv[1] == "--wkb"
towers = {}
if WKB_ONLY:
    for f in pathlib.Path("results").glob("p23_tower_law_m*.json"):
        towers.update(json.loads(f.read_text()))
    MS = []
for m in MS:
    am = abs(m)
    nmax = N_law(m) + 2
    t0 = time.time()
    roots = []          # (c, sensitivity)
    for n in range(nmax + 1):
        seed = law(m, n)
        for ds in (0, 0.06 - 0.04j, -0.06 + 0.04j, 0.04j):
            r = robust_root(seed + ds, m)
            if r is None or r[1] > 0.03 or r[0].real < -0.6:
                continue
            if all(abs(r[0] - x[0]) > 1e-4 for x in roots):
                roots.append(r)
    # assign each root to the nearest law member
    members = []
    for n in range(nmax + 1):
        seed = law(m, n)
        cand = [(abs(c - seed), c, sens) for c, sens in roots if abs(c - seed) < 0.45]
        if not cand:
            print(f"  m={m} n={n}: seed {seed:.3f} -> no robust root", flush=True)
            members.append({"n": n, "seed": [seed.real, seed.imag], "root": None})
            continue
        _, c, sens = min(cand)
        print(f"  m={m} n={n}: seed {seed:.3f} -> c = {c.real:.4f}{c.imag:+.4f}i (sensitivity {sens:.1e}, law dev Re {c.real - seed.real:+.3f} Im {c.imag - seed.imag:+.3f})", flush=True)
        members.append({"n": n, "seed": [seed.real, seed.imag], "root": [c.real, c.imag], "sensitivity": sens})
    extra = [c for c, _ in roots if all(abs(c - law(m, n)) >= 0.45 for n in range(nmax + 1))]
    if extra:
        print(f"  m={m}: unassigned robust roots {[f'{c:.4f}' for c in extra]}", flush=True)
    N = sum(1 for x in members if x["root"] and x["root"][0] > 0)
    towers[str(m)] = {"members": members, "unassigned": [[c.real, c.imag] for c in extra], "N": N,
                      "N_law": N_law(m), "N_alt": am - 1, "seconds": time.time() - t0}
    print(f"  m={m}: N = {N} (law {N_law(m)}, |m|-1 = {am - 1}); {time.time() - t0:.0f}s", flush=True)
    pathlib.Path(f"results/p23_tower_law_m{m}.json").write_text(json.dumps({str(m): towers[str(m)]}, indent=1))
if not WKB_ONLY:
    sys.exit(0)
OUT["towers"] = towers
pathlib.Path("results/p23_tower_law.json").write_text(json.dumps(OUT, indent=1))

# ------------------------------------------------------------------ WKB
rho, c, mm = sp.symbols("rho c m")
Qs = (c - mm / rho ** 2) ** 2 - (mm ** 2 - sp.Rational(1, 4)) / rho ** 2
D = [sp.lambdify((rho, c, mm), sp.diff(Qs, rho, k), "mpmath") for k in range(7)]


def extremum(cval, m, r0=2.0):
    f = lambda r: D[1](r, cval, m)
    return mp.findroot(f, mp.mpc(r0), tol=1e-20, maxsteps=100)


def wkb_condition(cval, m, n, order):
    r0 = extremum(cval, m)
    q = [D[k](r0, cval, m) for k in range(7)]
    a = n + mp.mpf(1) / 2
    s2 = mp.sqrt(2 * q[2])
    lam = (1 / s2) * (sp.Rational(1, 8) * (q[4] / q[2]) * (mp.mpf(1) / 4 + a ** 2)
                      - sp.Rational(1, 288) * (q[3] / q[2]) ** 2 * (7 + 60 * a ** 2))
    val = 1j * q[0] / s2 - lam - a
    if order >= 3:
        om = (a / (2 * q[2])) * (
            mp.mpf(5) / 6912 * (q[3] / q[2]) ** 4 * (77 + 188 * a ** 2)
            - mp.mpf(1) / 384 * (q[3] ** 2 * q[4] / q[2] ** 3) * (51 + 100 * a ** 2)
            + mp.mpf(1) / 2304 * (q[4] / q[2]) ** 2 * (67 + 68 * a ** 2)
            + mp.mpf(1) / 288 * (q[3] * q[5] / q[2] ** 2) * (19 + 28 * a ** 2)
            - mp.mpf(1) / 288 * (q[6] / q[2]) * (5 + 4 * a ** 2))
        val -= om
    return val


def wkb_root(m, n, order, seed):
    f = lambda z: wkb_condition(z, m, n, order)
    try:
        r = mp.findroot(f, mp.mpc(seed), solver="muller", tol=1e-14, maxsteps=80)
        return complex(r)
    except Exception as e:
        return None


mp.mp.dps = 30
exact = {}
prev = json.loads(pathlib.Path("results/p21f_scaled_vortex.json").read_text())["P21f2"]
for k, v in prev.items():
    exact[k] = [complex(*x) for x in v]
exact["-6"] = exact["-6"] + [complex(0.1899, -2.0450)]        # P21h fifth member (bridge value 0.190-2.045i)
exact["-7"] = [complex(*x) for x in json.loads(pathlib.Path("results/p21h_m7_scaled_tower.json").read_text())["-7"]]
for f in pathlib.Path("results").glob("p23_tower_cplx_m*.json"):       # complex-ray towers (the instrument that works at |m| >= 8)
    d = json.loads(f.read_text())
    exact[str(d["m"])] = [complex(*x["root"]) for x in d["members"] if x["root"]]

wkb = {}
print("== WKB (Iyer-Will) against the exact tower", flush=True)
for m in (-4, -5, -6, -7, -8, -9, -10):
    ex = exact.get(str(m), [])
    rows = []
    for n in range(len(ex) + 1):
        seed = law(m, n)
        w2 = wkb_root(m, n, 2, seed)
        w3 = wkb_root(m, n, 3, seed)
        e = ex[n] if n < len(ex) else None
        rows.append({"n": n, "exact": [e.real, e.imag] if e else None,
                     "wkb2": [w2.real, w2.imag] if w2 else None, "wkb3": [w3.real, w3.imag] if w3 else None})
        fmt = lambda z: f"{z.real:.4f}{z.imag:+.4f}i" if z else "----"
        print(f"  m={m} n={n}: exact {fmt(e)}  wkb2 {fmt(w2)}  wkb3 {fmt(w3)}", flush=True)
    wkb[str(m)] = rows
OUT["wkb"] = wkb

# analytic expansion of the second-order condition at the light ring:
# c = |m| gamma, delta = gamma - 1/4; solve for the (n+1/2)^2 / |m| coefficient
print("== second-order series at the light ring", flush=True)
coef = {}
for m in (-6, -7, -8, -10, -20, -40):
    row = []
    for n in range(0, 4):
        w2 = wkb_root(m, n, 2, law(m, n))
        if w2:
            row.append((n, (w2.real - abs(m) / 4) * abs(m)))   # should be ~ -(k0 a^2 + k1) if the law is WKB
    coef[str(m)] = row
    print(f"  m={m}: |m| (Re c_n - |m|/4) = {[(n, round(v, 4)) for n, v in row]}", flush=True)
OUT["wkb_series"] = coef
pathlib.Path("results/p23_tower_law.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
