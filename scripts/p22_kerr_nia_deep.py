"""P22 deep-truncation push toward the NIA endpoints (companion to
p22_kerr_nia.py). Near the axis the radial continued fraction converges
only for Nr ~ 1/Re(omega)^2, so the 48000 cap of the main run stalls at
Re(omega) ~ 0.03. Here each point is computed at caps 1e5, 4e5, 1e6, 4e6
and accepted when two consecutive caps agree to 2e-6 relative; the
starting guess is the linear extrapolation from the previous accepted
points. Output: results/p22_kerr_nia_deep.json.
"""
import json
import math
import pathlib
import time

from qnm.nearby import NearbyRootFinder

CAPS = (100_000, 400_000, 1_000_000, 4_000_000)


def find(a, guess, n_inv, m, A0, Nr_max):
    f = NearbyRootFinder(a=a, s=-2, m=m, A0=A0, l_max=20, omega_guess=guess, tol=1e-13,
                         cf_tol=1e-13, n_inv=n_inv, Nr=300, Nr_min=300, Nr_max=Nr_max)
    return complex(f.do_solve()), complex(f.A)


def deep(a, guess, n, m, A0):
    """Returns (omega, A, converged, cap_used, inversion_spread)."""
    prev = None
    for cap in CAPS:
        vals = []
        for n_inv in (n - 1, n, n + 1):
            try:
                w, A = find(a, guess, n_inv, m, A0, cap)
            except Exception:
                continue
            if abs(w - guess) < 0.5 * abs(guess) + 0.02 and w.real > 0:
                vals.append((w, A))
        if not vals:
            continue
        w, A = min(vals, key=lambda t: abs(t[0] - guess))
        spread = max(abs(v[0] - w) for v in vals)
        if prev is not None and abs(w - prev[0]) < 2e-6 * abs(w):
            return w, A, True, cap, spread
        prev = (w, A)
    if prev is None:
        return None
    return prev[0], prev[1], False, CAPS[-1], spread


def run(m, n, a_list, w_start, A_start, a0_cz, label):
    pts = []
    w, A = w_start, A_start
    for a in a_list:
        if len(pts) >= 2:
            (a1, w1), (a2, w2) = (pts[-2]["a"], complex(*pts[-2]["omega"])), (pts[-1]["a"], complex(*pts[-1]["omega"]))
            guess = w2 + (w2 - w1) * (a - a2) / (a2 - a1)
        else:
            guess = w
        res = deep(a, guess, n, m, A)
        if res is None:
            print(f"  {label} a={a}: no root", flush=True)
            continue
        w, A, ok, cap, spread = res
        pts.append({"a": a, "omega": [w.real, w.imag], "converged": ok, "cap": cap, "spread": spread})
        print(f"  {label} a={a}: omega={w:.9f} converged={ok} cap={cap} spread={spread:.1e}", flush=True)
    conv = [(p["a"], p["omega"][0], p["omega"][1]) for p in pts if p["converged"]]
    loc = [math.log(conv[i][1] / conv[i - 1][1]) / math.log((a0_cz - conv[i][0]) / (a0_cz - conv[i - 1][0]))
           for i in range(1, len(conv))]
    dec = [(a, r) for a, r, _ in conv if 1e-3 <= a0_cz - a <= 1e-2]
    fit = None
    if len(dec) >= 3:
        xs = [math.log(a0_cz - a) for a, _ in dec]
        ys = [math.log(r) for _, r in dec]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        fit = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a0_lin = None
    if len(conv) >= 2:
        (a1, r1, _), (a2, r2, _) = conv[-2], conv[-1]
        a0_lin = a2 - r2 * (a2 - a1) / (r2 - r1)
    out = {"points": pts, "local_exponents_CZ_a0": loc, "last_decade_fit": fit,
           "a0_linear_extrap": a0_lin, "a0_CZ": a0_cz, "Im_last_converged": conv[-1][2] if conv else None}
    print(f"  {label}: local exponents {[f'{x:.3f}' for x in loc]}; last-decade fit {fit}; "
          f"a0 lin {a0_lin}; Im last {out['Im_last_converged']}", flush=True)
    return out


t0 = time.time()
OUT = {}
# seeds: last gated points of the main run (p22_kerr_nia.json), A from the solver at that point
w, A = find(0.27, 0.031989 - 2.266953j, 9, 0, 4.0, 100_000)
OUT["{2,0,9_0}"] = run(0, 9, [0.28, 0.29, 0.295, 0.30, 0.302, 0.303, 0.304, 0.3045, 0.305, 0.3053],
                       w, A, 0.305661, "{2,0,9_0}")
pathlib.Path("results/p22_kerr_nia_deep.json").write_text(json.dumps(OUT, indent=1))
w, A = find(0.62, 0.039442 - 3.365550j, 13, -2, 4.0, 100_000)
OUT["{2,-2,13_0}"] = run(-2, 13, [0.63, 0.64, 0.65, 0.652, 0.654, 0.655, 0.656, 0.6565, 0.657, 0.6572],
                         w, A, 0.657472, "{2,-2,13_0}")
pathlib.Path("results/p22_kerr_nia_deep.json").write_text(json.dumps(OUT, indent=1))
print(f"done ({time.time()-t0:.0f}s)", flush=True)
