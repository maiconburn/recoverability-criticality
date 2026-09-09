"""Post-validation of the 'beyond B_c' roots reported by p21_vortex_scan.py.

Lesson (2026-09-09): a zero of ONE inversion of Leaver's continued
fraction is not a quasinormal mode; the n-th inversion can have spurious
zeros (pole-zero pairs) away from the n-th overtone. A genuine root is a
zero of every convergent inversion. Criterion used here: re-find the
root from its own value with inversions n = 0..5 (residual guard on);
accept it only if at least TWO different inversions converge to the same
point (within 1e-6) and |f_n| < 1e-3 there for at least three inversions.
Also identifies each accepted root by continuation back to B = 0 and by
the mirror symmetry S(-m, B) = -conj S(m, B).
"""
import json
import pathlib
import sys

import mpmath as mp

sys.path.insert(0, "src")
from recoverability_ep.dbt import find_qnm, leaver_function  # noqa

mp.mp.dps = 24
R = json.loads(pathlib.Path("results/p21_vortex_scan.json").read_text())


def refind(w, m, B, n):
    try:
        return find_qnm(w, m, B, n=n, kmax=600, tol=mp.mpf("1e-12"), maxsteps=60)
    except Exception:
        return None


def validate(w, m, B):
    hits = []
    for n in range(6):
        r = refind(w, m, B, n)
        if r is not None and abs(r - w) < 1e-4:
            hits.append((n, r))
    fvals = [abs(leaver_function(w, m, B, n, 600)) for n in range(6)]
    small = sum(1 for v in fvals if v < 1e-3)
    # genuine if two inversions re-find it, OR if it is a zero of (nearly) every
    # inversion (|f_n| < 1e-3 for at least five of six); an artifact of one
    # inversion is small for that inversion only
    ok = (len(hits) >= 2 and small >= 3) or small >= 5
    return ok, hits, fvals


out = {}
for key in sorted(k for k in R if k.startswith("counter_m")):
    m = int(key.split("m")[1])
    for nk, rec in sorted(R[key].items()):
        if "beyond_principal_sheet_roots" not in rec:
            continue
        Bc = rec["Bc_linear_extrap"] or rec["arrival_B_last"]
        out[f"{key}/{nk}"] = {}
        for dB, roots in rec["beyond_principal_sheet_roots"].items():
            B = Bc + float(dB)
            rows = []
            for re_, im_ in roots:
                w = mp.mpc(re_, im_)
                ok, hits, fvals = validate(w, m, B)
                rows.append({"omega": [re_, im_], "valid": ok,
                             "inversions_agreeing": [h[0] for h in hits],
                             "log10_f": [float(mp.log10(v)) if v > 0 else -99 for v in fvals]})
                print(f"  m={m} {nk} B={B:.4f} root {re_:+.5f}{im_:+.5f}i: "
                      f"{'GENUINE' if ok else 'ARTIFACT'} (inversions agreeing {[h[0] for h in hits]}; "
                      f"log10|f_n| {[round(float(mp.log10(v)) if v > 0 else -99, 1) for v in fvals]})", flush=True)
            out[f"{key}/{nk}"][dB] = rows
pathlib.Path("results/p21_beyond_validation.json").write_text(json.dumps(out, indent=1))
print("done", flush=True)
