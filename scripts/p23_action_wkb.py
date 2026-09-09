"""P23.1b companion: uniform first-order WKB for the pure-vortex tower
from the exact barrier action.

    -q(rho) = gamma (rho - rho_-)(rho_+ - rho)(gamma rho^2 + rho + 1) / rho^4,
    rho_+- = [1 -+ sqrt(1 - 4 gamma)] / (2 gamma),   gamma = c/|m|,

    J(gamma) = int_{rho_-}^{rho_+} sqrt(-q) d rho   (analytic in gamma),
    condition  |m| J(gamma_n) = i pi (n + 1/2).

Near the light ring J = 2 pi h + 3 pi h^2 + O(h^3), h = 1/4 - gamma
(the 3 pi is verified numerically to 1e-6), which gives
c_n = |m|/4 - i(2n+1)/4 - (3/8)(n+1/2)^2/|m| + ...: the empirical law's
k0 = 0.383 is 3/8. Here the condition is solved with the FULL action
for each (m, n) and compared with the exact tower; the crossing
constant kappa = alpha*/|m| (Re c = 0) is computed from the action.
"""
import json
import pathlib
import sys

import mpmath as mp

mp.mp.dps = 25


def J(gamma):
    gamma = mp.mpc(gamma)
    s = mp.sqrt(1 - 4 * gamma)
    rm, rp = (1 - s) / (2 * gamma), (1 + s) / (2 * gamma)
    D = rp - rm
    f = lambda t: mp.sqrt(t * (1 - t)) * mp.sqrt(gamma * (rm + t * D) ** 2 + (rm + t * D) + 1) / (rm + t * D) ** 2
    return mp.sqrt(gamma) * D ** 2 * mp.quad(f, [0, 0.5, 1])


def solve(m, n, seed):
    am = abs(m)
    f = lambda g: J(g) - 1j * mp.pi * (n + mp.mpf(1) / 2) / am
    g = mp.findroot(f, mp.mpc(seed) / am, solver="muller", tol=1e-12, maxsteps=60)
    return complex(g * am)


def law(m, n):
    am = abs(m)
    return complex(am / 4 - (0.375 * (n + 0.5) ** 2) / am, -(2 * n + 1) / 4)


# check the expansion
for h in (mp.mpf("1e-2"), mp.mpf("1e-3")):
    print(f"  J(1/4 - {h}) = {J(mp.mpf(1)/4 - h)}   2 pi h + 3 pi h^2 = {2*mp.pi*h + 3*mp.pi*h**2}", flush=True)

exact = {}
prev = json.loads(pathlib.Path("results/p21f_scaled_vortex.json").read_text())["P21f2"]
for k, v in prev.items():
    exact[k] = [complex(*x) for x in v]
exact["-6"] = exact["-6"] + [complex(0.1899, -2.0450)]
exact["-7"] = [complex(*x) for x in json.loads(pathlib.Path("results/p21h_m7_scaled_tower.json").read_text())["-7"]]
tw = pathlib.Path("results/p23_tower_law.json")
if tw.exists():
    for m, t in json.loads(tw.read_text()).get("towers", {}).items():
        exact[m] = [complex(*x["root"]) for x in t["members"] if x["root"]]

OUT = {}
for m in (-2, -3, -4, -5, -6, -7, -8, -9, -10):
    ex = exact.get(str(m), [])
    rows = []
    for n in range(max(len(ex) + 2, int(0.85 * abs(m)) + 2)):
        try:
            w = solve(m, n, law(m, n))
        except Exception as e:
            w = None
        e = ex[n] if n < len(ex) else None
        fmt = lambda z: f"{z.real:.4f}{z.imag:+.4f}i" if z else "----"
        dev = f"  dev {abs(w - e):.3f}" if (w and e) else ""
        print(f"  m={m} n={n}: exact {fmt(e)}  action-WKB {fmt(w)}{dev}", flush=True)
        rows.append({"n": n, "exact": [e.real, e.imag] if e else None, "action_wkb": [w.real, w.imag] if w else None})
    N_ex = sum(1 for z in ex if z.real > 0)
    N_w = sum(1 for r in rows if r["action_wkb"] and r["action_wkb"][0] > 0)
    OUT[str(m)] = {"rows": rows, "N_exact": N_ex, "N_action_wkb": N_w}
    print(f"  m={m}: N exact {N_ex}, N action-WKB {N_w}", flush=True)

# crossing constant: on the line gamma = i y (Re c = 0) the condition
# |m| J(i y) = i pi alpha needs Re J(i y) = 0; then kappa = alpha*/|m| = Im J(i y*) / pi
def kappa():
    g = lambda y: mp.re(J(1j * y))
    y1, y2 = mp.mpf("-0.3"), mp.mpf("-0.4")
    ys = mp.findroot(g, (y1, y2), solver="bisect", tol=1e-14)
    return ys, mp.im(J(1j * ys)) / mp.pi


try:
    ys, kap = kappa()
    print(f"  crossing: y* = {float(ys):.6f}, kappa = alpha*/|m| = {float(kap):.6f}  (quadratic truncation sqrt(2/3) = {float(mp.sqrt(mp.mpf(2)/3)):.6f}; empirical 0.808)", flush=True)
    OUT["kappa"] = {"y_star": float(ys), "kappa": float(kap)}
    print("  N(m) = floor(kappa |m| + 1/2):", {am: int(mp.floor(kap * am + mp.mpf(1) / 2)) for am in range(1, 13)}, flush=True)
except Exception as e:
    print("  kappa failed:", repr(e)[:200], flush=True)
pathlib.Path("results/p23_action_wkb.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
