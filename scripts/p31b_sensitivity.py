"""P31.5: minimum detectable shift, labelled against symmetric
(frozen in the addendum to results/FROZEN_P31_KW51.md).

Pre-retrofit hours only, split in half: first half sets the mean and
covariance and the 1% threshold, second half is the test set into which a
multiplicative shift delta is injected in ONE member of the pair. The
minimum detectable shift is the smallest delta flagging >= 50% of test
hours. Output: results/p31b_sensitivity.json
"""
import json
import pathlib
from datetime import datetime, timedelta

import numpy as np
from scipy.io import loadmat

MAT = "/Users/maiconesteves/fisica/prelab-data/kw51/trackedmodes/trackedmodes.mat"
RET0 = datetime(2019, 5, 15)
KNOT = 2.5
d = loadmat(MAT, squeeze_me=True, struct_as_record=False)["modes"]
sdn, f, env = np.asarray(d.sdn), np.asarray(d.f), np.asarray(d.env)
lab_env = [str(x) for x in np.asarray(d.labels_env)]
T = env[:, lab_env.index("tBD31A")]
t = np.array([datetime.fromordinal(int(s) - 366) + timedelta(days=s % 1) for s in sdn])
pre = t < RET0


def design(x):
    return np.stack([np.ones_like(x), x, np.maximum(x - KNOT, 0.0)], axis=1)


def resid_of(series, fit_mask):
    ok = np.isfinite(series) & np.isfinite(T)
    X = design(T[ok & fit_mask])
    beta, *_ = np.linalg.lstsq(X, series[ok & fit_mask], rcond=None)
    r = np.full_like(series, np.nan)
    r[ok] = series[ok] - design(T[ok]) @ beta
    return r


def min_detectable(a, b, which, deltas, mode):
    """which = index (a or b) to perturb; mode = 'labelled' or 'symmetric'."""
    fa, fb = f[:, a - 1].copy(), f[:, b - 1].copy()
    ok = np.isfinite(fa) & np.isfinite(fb) & np.isfinite(T) & pre
    idx = np.where(ok)[0]
    half = len(idx) // 2
    ref, test = idx[:half], idx[half:]
    if len(ref) < 200 or len(test) < 200:
        return None, len(ref), len(test)
    fit = np.zeros(len(fa), bool)
    fit[ref] = True
    out = None
    for delta in deltas:
        fa2, fb2 = fa.copy(), fb.copy()
        if which == a:
            fa2[test] *= 1 + delta
        else:
            fb2[test] *= 1 + delta
        if mode == "labelled":
            cols = [resid_of(fa2, fit), resid_of(fb2, fit)]
        else:
            cols = [resid_of(fa2 + fb2, fit), resid_of(fa2 * fb2, fit)]
        M = np.stack(cols, axis=1)
        mu, S = M[ref].mean(axis=0), np.cov(M[ref], rowvar=False)
        Si = np.linalg.pinv(np.atleast_2d(S))
        dv = M - mu
        t2 = np.einsum("ij,jk,ik->i", dv, Si, dv)
        thr = np.quantile(t2[ref], 0.99)
        rate = float(np.mean(t2[test] > thr))
        if rate >= 0.5 and out is None:
            out = delta
    return out, len(ref), len(test)


DELTAS = [1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2]
OUT = {"deltas": DELTAS}
print("| pair | perturbed | labelled min delta | symmetric min delta | gain factor | ref/test hours |")
print("|---|---|---|---|---|---|")
for a, b in ((8, 9), (4, 5), (12, 13)):
    for which in (a, b):
        dl, nr, nt = min_detectable(a, b, which, DELTAS, "labelled")
        ds, _, _ = min_detectable(a, b, which, DELTAS, "symmetric")
        gain = (dl / ds) if (dl and ds) else None
        OUT[f"{a}-{b}_perturb{which}"] = {"labelled": dl, "symmetric": ds, "gain": gain, "n_ref": nr, "n_test": nt}
        fmt = lambda x: f"{x:.0e}" if x else "not detected"
        print(f"| {a}-{b} | f_{which} | {fmt(dl)} | {fmt(ds)} | {f'{gain:.2f}' if gain else '-'} | {nr}/{nt} |")
pathlib.Path("results/p31b_sensitivity.json").write_text(json.dumps(OUT, indent=1))
print("done")
