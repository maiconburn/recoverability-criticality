"""Decisive probe for P21d.1: the m = -3, n = 2 counter-rotating mode for
B in [1.2, 3.0], where the continued fraction at kmax <= 3000 has NOT
converged (kmax-independence gate failed: Re(omega) at B = 1.45 is
0.021 / 0.014 / 0.008 for kmax 600 / 1500 / 3000). Uses kmax 10000 and
20000 at 30 digits; a value is accepted only if the two agree within
1e-4 and at least two inversions agree."""
import json, sys, time
import mpmath as mp
sys.path.insert(0, "src")
from recoverability_ep.dbt import find_qnm
mp.mp.dps = 30
M = -3
seed = mp.mpc(0.0461, -0.8964)   # kmax-3000 value at B = 1.14
out = {}
for B in (1.2, 1.3, 1.45, 1.6, 1.8, 2.0, 2.5, 3.0):
    row = {}
    for kmax in (10000, 20000):
        t0 = time.time()
        found = []
        for n in (2, 3, 1, 4):
            try:
                r = find_qnm(seed, M, B, n=n, kmax=kmax, tol=mp.mpf("1e-13"), maxsteps=60)
            except Exception:
                continue
            if abs(r - seed) < 0.15:
                found.append((n, r))
        agree = None
        for i in range(len(found)):
            for j in range(i + 1, len(found)):
                if abs(found[i][1] - found[j][1]) < 1e-6:
                    agree = found[i][1]
        row[str(kmax)] = {"roots": [[n, float(mp.re(r)), float(mp.im(r))] for n, r in found],
                          "agreed": [float(mp.re(agree)), float(mp.im(agree))] if agree else None,
                          "seconds": time.time() - t0}
        print(f"B={B} kmax={kmax}: found {[(n, mp.nstr(r, 7)) for n, r in found]} agreed={mp.nstr(agree, 8) if agree else None} ({time.time()-t0:.0f}s)", flush=True)
    a1, a2 = row["10000"]["agreed"], row["20000"]["agreed"]
    if a1 and a2 and abs(complex(*a1) - complex(*a2)) < 1e-4:
        row["converged"] = a2
        seed = mp.mpc(*a2)
        print(f"  => B={B}: CONVERGED omega = {a2[0]:.6f}{a2[1]:+.6f}i", flush=True)
    else:
        row["converged"] = None
        print(f"  => B={B}: NOT converged (10k {a1} vs 20k {a2})", flush=True)
        if a2:
            seed = mp.mpc(*a2)
    out[str(B)] = row
    json.dump(out, open("results/p21_m3_n2_deep.json", "w"), indent=1)
print("done", flush=True)
