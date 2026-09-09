"""P21f: the pure-vortex scaled limit (frozen in results/FROZEN_P21F_VORTEX_SCALED.md).

1. Extrapolate the finite-B escaping modes to B -> infinity (fit
   omega B = c + d/B on the tracked paths) to get the reference c_n(m).
2. Solve the scaled problem (dbt_scaled.find_c, inner branch +1, the one
   that passed the m = -2 anchor gate at 0.8%) from those seeds and
   compare (P21f.1).
3. Count the scaled resonances with Re c > 0, Im c > -2 for |m| = 1..6
   by a seed grid (P21f.2).
4. Schutz-Will WKB on the scaled potential, first order (P21f.3).
"""
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, "src")
from recoverability_ep.dbt_scaled import find_c, wronskian, Q  # noqa

OUT = {}

# ---------------------------------------------------------------- 1. references
def extrapolate(path, bmin):
    sel = [(b, r, i) for b, r, i in path if b >= bmin and r > 0]
    if len(sel) < 4:
        return None
    x = np.array([1 / b for b, _, _ in sel])
    y = np.array([complex(r, i) * b for b, r, i in sel])
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return complex(coef[0]), complex(coef[1]), len(sel)


refs = {}
files = {
    -1: ("results/p21_vortex_scan.json", "counter_m-1", ["n0"], 10.0),
    -2: (None, None, None, None),
    -3: ("results/p21_vortex_m-3_robust_n0-1-2-3-4.json", None, ["n0", "n1"], 3.0),
    -4: ("results/p21_vortex_m-4_robust_n0-1-2-3-4-5.json", None, ["n0", "n1", "n2"], 3.0),
}
d = json.loads(pathlib.Path("results/p21_vortex_scan.json").read_text())
refs[(-1, 0)] = extrapolate(d["counter_m-1"]["n0"]["path"], 10.0)
d2 = json.loads(pathlib.Path("results/p21_vortex_m-2_robust_n0.json").read_text())
refs[(-2, 0)] = extrapolate(d2["n0"]["path"], 10.0)
d2b = json.loads(pathlib.Path("results/p21_vortex_m-2_robust.json").read_text())
refs[(-2, 1)] = extrapolate(d2b["n1"]["path"], 3.0)
for m in (-3, -4):
    f, _, ns, bmin = files[m]
    dd = json.loads(pathlib.Path(f).read_text())
    for nk in ns:
        refs[(m, int(nk[1:]))] = extrapolate(dd[nk]["path"], bmin)
print("== reference c_n(m) extrapolated to B -> infinity (omega B = c + d/B):")
for k, v in sorted(refs.items()):
    if v:
        print(f"  m={k[0]} n={k[1]}: c = {v[0].real:.4f}{v[0].imag:+.4f}i  (1/B slope {abs(v[1]):.3f}, {v[2]} pts)")
OUT["references"] = {f"{k[0]},{k[1]}": [v[0].real, v[0].imag, abs(v[1]), v[2]] for k, v in refs.items() if v}

# ---------------------------------------------------------------- 2. P21f.1
print("== P21f.1: scaled eigenvalues vs references")
f1 = {}
for (m, n), v in sorted(refs.items()):
    if not v:
        continue
    try:
        c, res = find_c(v[0], m, branch=+1)
    except Exception as e:
        f1[f"{m},{n}"] = {"error": str(e)[:80]}
        print(f"  m={m} n={n}: FAIL {str(e)[:60]}")
        continue
    dev = abs(c - v[0]) / abs(v[0])
    f1[f"{m},{n}"] = {"scaled": [c.real, c.imag], "ref": [v[0].real, v[0].imag], "rel_dev": dev, "resid": res}
    print(f"  m={m} n={n}: scaled c = {c.real:.5f}{c.imag:+.5f}i  ref {v[0].real:.4f}{v[0].imag:+.4f}i  dev {100*dev:.2f}%")
OUT["P21f1"] = f1

# ---------------------------------------------------------------- 3. P21f.2 resonance count
print("== P21f.2: resonance count of the scaled problem (Re c > 0, Im c > -2)")
counts = {}
for m in (-1, -2, -3, -4, -5, -6):
    roots = []
    am = abs(m)
    for re0 in np.linspace(0.04, am / 2 + 0.5, 9):
        for im0 in (-0.15, -0.3, -0.5, -0.75, -1.0, -1.25, -1.5, -1.9):
            try:
                c, res = find_c(complex(re0, im0), m, branch=+1, maxit=40)
            except Exception:
                continue
            if res > 1e-8 or c.real <= 0 or c.imag <= -2.0 or c.imag >= 0:
                continue
            if all(abs(c - r) > 1e-5 for r in roots):
                roots.append(c)
    roots.sort(key=lambda z: -z.imag)
    counts[str(m)] = [[r.real, r.imag] for r in roots]
    print(f"  m={m}: {len(roots)} roots: " + ", ".join(f"{r.real:.4f}{r.imag:+.4f}i" for r in roots)
          + f"   (frozen rule floor((|m|+2)/2) = {(am + 2) // 2})")
OUT["P21f2"] = counts

# ---------------------------------------------------------------- 4. P21f.3 WKB (Schutz-Will, first order)
print("== P21f.3: Schutz-Will first-order WKB on the scaled potential")
import mpmath as mp


def wkb(m, n, c0):
    # Q(rho, c); condition: Q(rho0)/sqrt(2 Q''(rho0)) = i (n + 1/2), dQ/drho(rho0) = 0
    def system(c, rho):
        c = mp.mpc(c)
        rho = mp.mpc(rho)
        Qf = lambda r: (c - m / r ** 2) ** 2 - (m ** 2 - mp.mpf(1) / 4) / r ** 2
        dQ = mp.diff(Qf, rho)
        d2Q = mp.diff(Qf, rho, 2)
        # Schutz-Will: Q0 / sqrt(2 Q0'') = -i (n + 1/2) at the extremum of Q
        return [Qf(rho) / mp.sqrt(2 * d2Q) + 1j * (n + mp.mpf(1) / 2), dQ]
    # initial rho0: minimum of Q for real c ~ c0.real
    r0 = mp.mpf(abs(m) / max(c0.real, 0.05)) ** 0.5
    sol = mp.findroot(lambda c, r: system(c, r), (mp.mpc(c0), r0), tol=1e-12, maxsteps=60)
    return complex(sol[0]), complex(sol[1])


w = {}
for m in (-1, -2, -3, -4):
    for n in range(3):
        key = f"{m},{n}"
        if key not in f1 or "scaled" not in f1[key]:
            continue
        cex = complex(*f1[key]["scaled"])
        try:
            cw, rho0 = wkb(m, n, cex)
            w[key] = {"wkb": [cw.real, cw.imag], "rho0": [rho0.real, rho0.imag], "exact": [cex.real, cex.imag],
                      "re_dev": abs(cw.real - cex.real) / abs(cex.real), "im_dev": abs(cw.imag - cex.imag) / abs(cex.imag)}
            print(f"  m={m} n={n}: WKB {cw.real:.4f}{cw.imag:+.4f}i vs exact {cex.real:.4f}{cex.imag:+.4f}i  (Re dev {100*w[key]['re_dev']:.1f}%, Im dev {100*w[key]['im_dev']:.1f}%)")
        except Exception as e:
            print(f"  m={m} n={n}: WKB FAIL {str(e)[:60]}")
OUT["P21f3"] = w
pathlib.Path("results/p21f_scaled_vortex.json").write_text(json.dumps(OUT, indent=1))
print("done")
