"""P22.3 deep re-emergence check: track the {2,0,9_1} root found at
a = 0.44 (0.042694 - 2.375658i) DOWNWARD in spin with deep truncation
caps until it reaches the negative imaginary axis, giving the birth spin
a_1 and the law of emergence (mirror of the arrival law). The gated
search of the main run (cap 48000) is blind for Re(omega) < ~0.03 and
therefore could not see the 9_1 segment between a = 0.405 and 0.42.
Output: results/p22_kerr_nia_reemerge.json.
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
    prev = None
    spread = None
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


t0 = time.time()
w, A = find(0.44, 0.042694 - 2.375658j, 9, 0, 4.0, 100_000)
print(f"  start a=0.44: {w:.9f}", flush=True)
pts = [{"a": 0.44, "omega": [w.real, w.imag], "converged": True, "cap": 100_000, "spread": 0.0}]
a, step = 0.44, 0.005
while a > 0.395 and step > 2e-4:
    an = a - step
    if len(pts) >= 2:
        (a1, w1), (a2, w2) = (pts[-2]["a"], complex(*pts[-2]["omega"])), (pts[-1]["a"], complex(*pts[-1]["omega"]))
        guess = w2 + (w2 - w1) * (an - a2) / (a2 - a1)
    else:
        guess = w
    res = deep(an, guess, 9, 0, A)
    if res is None or not res[2]:
        step /= 2
        print(f"  a={an:.5f}: {'no root' if res is None else 'not converged %.3e' % abs(res[0] - guess)}; step -> {step}", flush=True)
        continue
    w, A, ok, cap, spread = res
    a = an
    pts.append({"a": a, "omega": [w.real, w.imag], "converged": ok, "cap": cap, "spread": spread})
    print(f"  a={a:.5f}: omega={w:.9f} cap={cap} spread={spread:.1e}", flush=True)
    if w.real < 5e-4:
        break
    step = min(step * 1.5, 0.005)

conv = [(p["a"], p["omega"][0], p["omega"][1]) for p in pts if p["converged"]]
conv.sort()
a1_lin = None
loc = []
if len(conv) >= 2:
    (aa, r1, _), (ab, r2, _) = conv[0], conv[1]
    a1_lin = aa - r1 * (ab - aa) / (r2 - r1)
    loc = [math.log(conv[i][1] / conv[i - 1][1]) / math.log((conv[i][0] - a1_lin) / (conv[i - 1][0] - a1_lin))
           for i in range(1, min(6, len(conv)))]
OUT = {"points": pts, "a1_linear_extrap": a1_lin, "Im_at_lowest": conv[0][2] if conv else None,
       "local_exponents_vs_a1_lin": loc}
pathlib.Path("results/p22_kerr_nia_reemerge.json").write_text(json.dumps(OUT, indent=1))
print(f"  re-emergence: a_1 (linear extrap) {a1_lin}; Im at lowest {OUT['Im_at_lowest']}; local exponents {[f'{x:.3f}' for x in loc]}", flush=True)
print(f"done ({time.time()-t0:.0f}s)", flush=True)
