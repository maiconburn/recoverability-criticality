"""P28 follow-up: (i) extend the a = 0.99 m = 0 towers of l = 3, 4 beyond
n = 11 / 15 with seeds from the observed geometric law of Re and the
1/4 spacing of Im, deep caps 4e6 (gate 1.6e7); (ii) carry the l = 2
members n = 8, 9 from 0.99 to 0.999 in steps of 0.001 with the same
caps. Output: results/p28b_kerr_extend.json.  Usage: p28b_kerr_extend.py l
"""
import json
import pathlib
import sys

from qnm.nearby import NearbyRootFinder

L = int(sys.argv[1])
A = 0.99


def find(a, guess, n_inv, A0, Nr_max):
    f = NearbyRootFinder(a=a, s=-2, m=0, A_closest_to=A0, l_max=L + 18, omega_guess=guess, tol=1e-12,
                         cf_tol=1e-12, n_inv=n_inv, Nr=300, Nr_min=300, Nr_max=Nr_max)
    r = f.do_solve()
    if r is None:
        raise RuntimeError("no root")
    return complex(r), complex(f.A)


def member(a, guess, n, A0, cap=4_000_000, gate_cap=16_000_000):
    vals = []
    for n_inv in (n - 1, n, n + 1):
        try:
            w, Aa = find(a, guess, n_inv, A0, cap)
        except Exception:
            continue
        if abs(w - guess) < 0.3 * abs(guess) + 0.03 and w.imag < 0 and w.real > 0:
            vals.append((w, Aa))
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            if abs(vals[i][0] - vals[j][0]) < 1e-6:
                w, Aa = vals[i]
                try:
                    w4, _ = find(a, w, n, Aa, gate_cap)
                    gate = abs(w4 - w) < 1e-5 * max(abs(w), 1e-2)
                except Exception:
                    gate = False
                return w, Aa, gate
    return None


d = json.loads(pathlib.Path(f"results/p28_kerr_survivors_l{L}.json").read_text())
mem = [(m["n"], complex(*m["omega"])) for m in d["members"] if m["omega"]]
OUT = {"l": L, "extension": [], "continuation": {}}
if L in (3, 4):
    (n1, w1), (n2, w2) = mem[-2], mem[-1]
    ratio = w2.real / w1.real
    n = n2 + 1
    A0 = float(L * (L + 1) - 2)
    fails = 0
    w = w2
    while n <= {3: 22, 4: 30}[L] and fails < 4:
        guess = complex(w.real * ratio, w.imag - 0.248)
        res = member(A, guess, n, A0)
        if res is None:
            fails += 1
            print(f"  l={L} n={n}: no converged member (seed {guess:.4f})", flush=True)
            w = guess
            n += 1
            continue
        fails = 0
        w, A0, gate = res
        OUT["extension"].append({"n": n, "omega": [w.real, w.imag], "gate": gate})
        print(f"  l={L} n={n}: {w:.6f} gate={gate}  Re ratio {w.real / (OUT['extension'][-2]['omega'][0] if len(OUT['extension']) > 1 else w2.real):.3f}", flush=True)
        n += 1
        pathlib.Path("results/p28b_kerr_extend.json").write_text(json.dumps(OUT, indent=1))
if L == 2:
    for n0, w0 in ((8, 0.054422 - 1.703930j), (9, 0.036926 - 1.951732j)):
        path = [(0.99, w0)]
        A0 = 4.0
        w = w0
        a = 0.99
        while a < 0.9989:
            a = round(a + 0.001, 4)
            if len(path) >= 2:
                (a1, wa), (a2, wb) = path[-2], path[-1]
                guess = wb + (wb - wa) * (a - a2) / (a2 - a1)
            else:
                guess = w
            res = member(a, guess, n0, A0)
            if res is None:
                print(f"  l=2 n={n0} a={a}: lost (seed {guess:.5f})", flush=True)
                break
            w, A0, gate = res
            path.append((a, w))
            print(f"  l=2 n={n0} a={a}: {w:.6f} gate={gate}  Re ratio to 0.99 {w.real / w0.real:.3f}  sqrt((1-a)/0.01) {((1 - a) / 0.01) ** 0.5:.3f}", flush=True)
        OUT["continuation"][str(n0)] = [[aa, ww.real, ww.imag] for aa, ww in path]
        pathlib.Path("results/p28b_kerr_extend.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
