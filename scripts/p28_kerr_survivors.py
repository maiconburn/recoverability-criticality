"""P28: extremal damped-mode towers of Kerr (l = 2, 3, 4; m = 0; s = -2) at
a = 0.9999, tracked in the overtone index with seeds from the anharmonic
law of the previous members (frozen in results/FROZEN_P28_KERR_SURVIVORS.md).
Each member: inversions n-1, n, n+1 at Nr_max 1e6 (two must agree to
1e-6), gate against Nr_max 4e6 at 1e-5. The scan stops two members
after the first with Re(omega) < 0.02 or when three consecutive members
fail. Output: results/p28_kerr_survivors.json.
Usage: p28_kerr_survivors.py l
"""
import json
import pathlib
import sys
import time

import numpy as np
from qnm.nearby import NearbyRootFinder

A = 0.9999
L = int(sys.argv[1]) if len(sys.argv) > 1 else 2
NSTAR = {2: 8, 3: 18, 4: 25}[L]


def find(guess, n_inv, A0, Nr_max):
    f = NearbyRootFinder(a=A, s=-2, m=0, A0=A0, l_max=L + 18, omega_guess=guess, tol=1e-12,
                         cf_tol=1e-12, n_inv=n_inv, Nr=300, Nr_min=300, Nr_max=Nr_max)
    return complex(f.do_solve()), complex(f.A)


def member(guess, n, A0):
    vals = []
    for n_inv in (max(n - 1, 0), n, n + 1):
        try:
            w, Aa = find(guess, n_inv, A0, 1_000_000)
        except Exception:
            continue
        if abs(w - guess) < 0.25 * abs(guess) + 0.05 and w.imag < 0:
            vals.append((w, Aa, n_inv))
    if len(vals) < 2:
        return None
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            if abs(vals[i][0] - vals[j][0]) < 1e-6:
                w, Aa, _ = vals[i]
                try:
                    w4, _ = find(w, n, Aa, 4_000_000)
                    gate = abs(w4 - w) < 1e-5 * max(abs(w), 1e-2)
                except Exception:
                    gate = False
                return w, Aa, gate
    return None


t0 = time.time()
members = []
A0 = float(L * (L + 1) - 2)          # s(s+1) = 2 for s = -2
w, A0 = find(complex(0.4 if L == 2 else 0.66 if L == 3 else 0.89, -0.075), 0, A0, 1_000_000)
members.append({"n": 0, "omega": [w.real, w.imag], "gate": True})
print(f"  l={L} n=0: {w:.6f}", flush=True)
fails = 0
first_cross = None
n = 1
while n <= NSTAR + 3:
    # seed: quadratic extrapolation in n of the last members (Re) and linear (Im)
    pts = [(mm["n"], complex(*mm["omega"])) for mm in members if mm["gate"]][-4:]
    if len(pts) >= 3:
        ns = np.array([p[0] for p in pts]); re = np.array([p[1].real for p in pts]); im = np.array([p[1].imag for p in pts])
        guess = complex(np.polyval(np.polyfit(ns, re, 2), n), np.polyval(np.polyfit(ns, im, 1), n))
    elif len(pts) == 2:
        (n1, w1), (n2, w2) = pts
        guess = w2 + (w2 - w1) * (n - n2) / (n2 - n1)
    else:
        guess = complex(w.real, w.imag - 0.16)
    res = member(guess, n, A0)
    if res is None:
        fails += 1
        print(f"  l={L} n={n}: no converged member (seed {guess:.4f})", flush=True)
        members.append({"n": n, "omega": None, "gate": False, "seed": [guess.real, guess.imag]})
        if fails >= 3:
            break
        n += 1
        continue
    fails = 0
    w, A0, gate = res
    members.append({"n": n, "omega": [w.real, w.imag], "gate": gate, "seed": [guess.real, guess.imag]})
    print(f"  l={L} n={n}: {w:.6f} gate={gate}", flush=True)
    if w.real < 0.02 and first_cross is None:
        first_cross = n
    if first_cross is not None and n >= first_cross + 2:
        break
    n += 1
out = {"l": L, "a": A, "n_star_CZ": NSTAR, "first_cross": first_cross, "members": members, "seconds": time.time() - t0}
pathlib.Path(f"results/p28_kerr_survivors_l{L}.json").write_text(json.dumps(out, indent=1))
print(f"  l={L}: first member with Re < 0.02 at n = {first_cross} (Cook-Zalutskiy onset {NSTAR}); {time.time() - t0:.0f}s", flush=True)
print("done", flush=True)
