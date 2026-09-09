"""P28, l = 2 boundary members: continue n = 6, 7, 8, 9 (m = 0, s = -2)
from a = 0.99 to 0.999 in fine steps (Nr_max 1e6, gate 4e6 at 1e-5,
inversions n-1..n+1 agreeing to 1e-6). A damped mode keeps Re(omega)
finite (ratio Re(0.999)/Re(0.99) ~ 1); a zero-damping-like member
loses it as sqrt(1-a) (ratio ~ 0.32). Output: results/p28_l2_continuation.json.
"""
import json
import pathlib

from qnm.nearby import NearbyRootFinder

START = {6: (0.116521 - 1.213191j), 7: (0.080165 - 1.457344j), 8: (0.054422 - 1.703930j), 9: (0.036926 - 1.951732j)}
SPINS = (0.99, 0.992, 0.994, 0.996, 0.997, 0.998, 0.9985, 0.999)


def find(a, guess, n_inv, A0, Nr_max):
    f = NearbyRootFinder(a=a, s=-2, m=0, A_closest_to=A0, l_max=20, omega_guess=guess, tol=1e-12,
                         cf_tol=1e-12, n_inv=n_inv, Nr=300, Nr_min=300, Nr_max=Nr_max)
    r = f.do_solve()
    if r is None:
        raise RuntimeError("no root")
    return complex(r), complex(f.A)


def member(a, guess, n, A0):
    vals = []
    for n_inv in (n - 1, n, n + 1):
        try:
            w, Aa = find(a, guess, n_inv, A0, 1_000_000)
        except Exception:
            continue
        if abs(w - guess) < 0.3 * abs(guess) + 0.02 and w.imag < 0:
            vals.append((w, Aa))
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            if abs(vals[i][0] - vals[j][0]) < 1e-6:
                w, Aa = vals[i]
                try:
                    w4, _ = find(a, w, n, Aa, 4_000_000)
                    gate = abs(w4 - w) < 1e-5 * max(abs(w), 1e-2)
                except Exception:
                    gate = False
                return w, Aa, gate
    return None


OUT = {}
for n, w0 in START.items():
    path = []
    A0 = 4.0
    w = w0
    for a in SPINS:
        if path:
            # linear extrapolation in sqrt(1-a) of Re and linear in a of Im
            (a1, w1), (a2, w2) = (path[-2] if len(path) >= 2 else path[-1]), path[-1]
            s1, s2, s = (1 - a1) ** 0.5, (1 - a2) ** 0.5, (1 - a) ** 0.5
            guess = complex(w2.real + (w2.real - w1.real) * (s - s2) / (s2 - s1) if s2 != s1 else w2.real,
                            w2.imag + (w2.imag - w1.imag) * (a - a2) / (a2 - a1) if a2 != a1 else w2.imag)
        else:
            guess = w
        res = member(a, guess, n, A0)
        if res is None:
            print(f"  n={n} a={a}: lost (seed {guess:.5f})", flush=True)
            break
        w, A0, gate = res
        path.append((a, w))
        print(f"  n={n} a={a}: {w:.6f} gate={gate}  Re ratio to a=0.99: {w.real / path[0][1].real:.3f}  sqrt((1-a)/0.01) = {((1 - a) / 0.01) ** 0.5:.3f}", flush=True)
    OUT[str(n)] = [[a, w.real, w.imag] for a, w in path]
pathlib.Path("results/p28_l2_continuation.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
