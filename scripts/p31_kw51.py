"""P31: label confusion in bridge monitoring (frozen in
results/FROZEN_P31_KW51.md).

KW51 railway bridge, 11328 hourly modal identifications over 15 months
spanning a dated retrofit. Two close pairs of modes (4-5 at 2.44/2.57 Hz,
8-9 at 3.90/4.06 Hz) whose members respond differently to temperature, so
the gap breathes seasonally; two separated pairs (2-3, 12-13) as controls.
Tests whether the labelled frequencies carry excess anticorrelated error
(label confusion) that cancels in the pair invariants, and whether a
control chart on invariants detects the retrofit better than one on labels.
Blind PCA baseline included.
Output: results/p31_kw51.json
"""
import json
import pathlib
from datetime import datetime, timedelta

import numpy as np
from scipy.io import loadmat
from scipy.stats import chi2

MAT = "/Users/maiconesteves/fisica/prelab-data/kw51/trackedmodes/trackedmodes.mat"
RET0, RET1 = datetime(2019, 5, 15), datetime(2019, 9, 27)
KNOT = 2.5
CLOSE = [(4, 5), (8, 9)]
SEPARATED = [(2, 3), (12, 13)]

d = loadmat(MAT, squeeze_me=True, struct_as_record=False)["modes"]
sdn, f, env = np.asarray(d.sdn), np.asarray(d.f), np.asarray(d.env)
lab_env = [str(x) for x in np.asarray(d.labels_env)]
T = env[:, lab_env.index("tBD31A")]
t = np.array([datetime.fromordinal(int(s) - 366) + timedelta(days=s % 1) for s in sdn])
pre, post = t < RET0, t > RET1
OUT = {"n_records": int(len(sdn)), "knot_C": KNOT,
       "hours": {"pre": int(pre.sum()), "during": int(((t >= RET0) & (t <= RET1)).sum()), "post": int(post.sum())}}


def design(temp):
    """Piecewise linear in temperature with a knot at KNOT."""
    return np.stack([np.ones_like(temp), temp, np.maximum(temp - KNOT, 0.0)], axis=1)


def residual(series):
    """Temperature residual, regression fitted on pre-retrofit hours only."""
    ok = np.isfinite(series) & np.isfinite(T)
    fit = ok & pre
    X = design(T[fit])
    beta, *_ = np.linalg.lstsq(X, series[fit], rcond=None)
    r = np.full_like(series, np.nan)
    r[ok] = series[ok] - design(T[ok]) @ beta
    return r, beta


res, betas = {}, {}
for k in range(14):
    res[k + 1], betas[k + 1] = residual(f[:, k])
OUT["temperature_slopes"] = {str(k): [float(x) for x in betas[k]] for k in betas}

# ---- P31.1 and P31.2
print("| pair | kind | hours | corr(res_a, res_b) | sd_a | sd_b | sd(sum) | quadrature | ratio |")
print("|---|---|---|---|---|---|---|---|---|")
OUT["pairs"] = {}
for kind, pairs in (("close", CLOSE), ("separated", SEPARATED)):
    for a, b in pairs:
        ra, rb = res[a], res[b]
        ok = np.isfinite(ra) & np.isfinite(rb)
        ra, rb = ra[ok], rb[ok]
        c = float(np.corrcoef(ra, rb)[0, 1])
        sa, sb = float(ra.std(ddof=1)), float(rb.std(ddof=1))
        ssum = float((ra + rb).std(ddof=1))
        quad = float(np.hypot(sa, sb))
        OUT["pairs"][f"{a}-{b}"] = dict(kind=kind, hours=int(ok.sum()), corr=c, sd_a=sa, sd_b=sb,
                                        sd_sum=ssum, quadrature=quad, ratio=quad / ssum)
        print(f"| {a}-{b} | {kind} | {ok.sum()} | {c:+.3f} | {sa:.5f} | {sb:.5f} | {ssum:.5f} | {quad:.5f} | {quad/ssum:.3f} |")

# ---- P31.3 control charts
def chart(cols, name):
    """Hotelling T^2 on the given residual columns; threshold at 1% pre-retrofit
    false alarms; returns the flagged fractions."""
    M = np.stack(cols, axis=1)
    ok = np.all(np.isfinite(M), axis=1)
    Mp = M[ok & pre]
    if len(Mp) < 100:
        return None
    mu, S = Mp.mean(axis=0), np.cov(Mp, rowvar=False)
    Si = np.linalg.pinv(np.atleast_2d(S))
    dev = M[ok] - mu
    t2 = np.einsum("ij,jk,ik->i", dev, Si, dev)
    thr = float(np.quantile(t2[pre[ok]], 0.99))
    return dict(name=name, n=int(ok.sum()), threshold=thr, dim=M.shape[1],
                pre_rate=float(np.mean(t2[pre[ok]] > thr)),
                post_rate=float(np.mean(t2[post[ok]] > thr)),
                during_rate=float(np.mean(t2[((t >= RET0) & (t <= RET1))[ok]] > thr)))


labelled = chart([res[4], res[5], res[8], res[9]], "labelled f_4, f_5, f_8, f_9")
symmetric = chart([res[4] + res[5], res[4] * 0 + (f[:, 3] * f[:, 4] - np.nanmean(f[:, 3] * f[:, 4])),
                   res[8] + res[9], f[:, 7] * f[:, 8] - np.nanmean(f[:, 7] * f[:, 8])], "symmetric (placeholder)")
# proper symmetric residuals: regress the invariants themselves on temperature
s45, p45 = f[:, 3] + f[:, 4], f[:, 3] * f[:, 4]
s89, p89 = f[:, 7] + f[:, 8], f[:, 7] * f[:, 8]
inv_res = [residual(x)[0] for x in (s45, p45, s89, p89)]
symmetric = chart(inv_res, "symmetric s_45, p_45, s_89, p_89")
# blind PCA baseline on all 14 residuals
R = np.stack([res[k + 1] for k in range(14)], axis=1)
okR = np.all(np.isfinite(R), axis=1)
print(f"\nall-14 joint coverage: {okR.sum()} hours ({okR.mean():.1%})")
Rp = R[okR & pre]
Rc = Rp - Rp.mean(axis=0)
U, S, Vt = np.linalg.svd(Rc, full_matrices=False)
pcs = [R @ Vt[i] for i in range(3)]
pca = chart(pcs, "blind PCA (3 components of all 14)")
OUT["charts"] = {k: v for k, v in (("labelled", labelled), ("symmetric", symmetric), ("pca", pca)) if v}
print("\n| chart | dim | hours | threshold | pre-retrofit flagged | during | post |")
print("|---|---|---|---|---|---|---|")
for key, c in OUT["charts"].items():
    print(f"| {c['name']} | {c['dim']} | {c['n']} | {c['threshold']:.2f} | {c['pre_rate']:.2%} | {c['during_rate']:.2%} | {c['post_rate']:.2%} |")
if labelled and symmetric:
    OUT["P31_3_gain_points"] = 100 * (symmetric["post_rate"] - labelled["post_rate"])
    print(f"\nP31.3: symmetric minus labelled post-retrofit flagged = {OUT['P31_3_gain_points']:+.1f} percentage points")
pathlib.Path("results/p31_kw51.json").write_text(json.dumps(OUT, indent=1))
print("done")
