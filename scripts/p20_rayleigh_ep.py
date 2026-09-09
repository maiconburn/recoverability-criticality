"""P20: Rayleigh's curse at the exceptional point.

Predictions frozen in results/FROZEN_P20_RAYLEIGH_EP.md before this run.

Sources: S1 coherent fixed source; S2 eigenmode-incoherent (fixed V,
non-analytic normalization); S3 port-incoherent (analytic, four port
configurations); S4 partially coherent eigenmode amplitudes (fixed V).
Measurements: M1 fixed-basis mode counting; M2 direct time-resolved
intensity; M3 quantum Fisher information (coherent state formula, or the
Gaussian-state formula gated against single-mode thermal and squeezed
vacuum results).

Slopes are d ln sigma / d ln epsilon; the gap slope in s is
2*slope_eps(sigma_eps) - 1 (since s = 2 sqrt(eps) and sigma(s) =
sigma(eps)/sqrt(eps)).
"""
import json
import pathlib
import sys

import mpmath as mp

mp.mp.dps = 40
NT = 600
TMAX = mp.mpf(6)
DT = TMAX / (NT - 1)
T = [DT * k for k in range(NT)]
MU = mp.mpc(mp.mpf('0.7'), -1)
I1 = mp.mpc(0, 1)
EPS_LIST = [mp.mpf(10) ** (-k) for k in range(1, 7)]
HREL = mp.mpf('1e-12')
NBG = mp.mpf('1e-12')
XS1 = mp.mpc(1, 0)
YS1 = mp.mpf('0.8') * mp.e ** (I1 * mp.mpf('0.4'))
NPH = mp.mpf(100)


# ---------- basic modes ----------
def v0(eps):
    r = mp.sqrt(eps)
    return [mp.e ** (-I1 * MU * t) * mp.cos(r * t) for t in T]


def v1(eps):
    r = mp.sqrt(eps)
    if eps == 0:
        return [mp.e ** (-I1 * MU * t) * t for t in T]
    return [mp.e ** (-I1 * MU * t) * mp.sin(r * t) / r for t in T]


def dv0(eps):
    r = mp.sqrt(eps)
    return [-mp.e ** (-I1 * MU * t) * t * mp.sin(r * t) / (2 * r) for t in T]


def dv1(eps):
    r = mp.sqrt(eps)
    return [mp.e ** (-I1 * MU * t) * (t * mp.cos(r * t) / (2 * eps)
                                      - mp.sin(r * t) / (2 * eps * r))
            for t in T]


def wpm(eps, sign):
    om = MU + sign * mp.sqrt(eps)
    return [mp.e ** (-I1 * om * t) for t in T]


def ip(a, b):
    return mp.fsum(mp.conj(x) * y for x, y in zip(a, b)) * DT


def gram_schmidt(vecs):
    basis = []
    for v in vecs:
        w = list(v)
        for u in basis:
            c = ip(u, w)
            w = [x - c * y for x, y in zip(w, u)]
        nrm = mp.sqrt(mp.re(ip(w, w)))
        basis.append([x / nrm for x in w])
    return basis


FIXED_BASIS = gram_schmidt([[mp.e ** (-I1 * MU * t) * t ** k for t in T]
                            for k in range(6)])


# ---------- source models ----------
# A source returns (kind, payload):
#   ("coh", amplitude vector a(t))                      coherent state
#   ("gauss", [(coef matrix C 2x2 or 1x1), [mode vectors]])  zero-mean Gaussian
def src_S1(eps, x=XS1, y=YS1):
    a0 = v0(eps)
    a1 = v1(eps)
    return ("coh", [mp.sqrt(NPH) * (x * p + y * q) for p, q in zip(a0, a1)])


def src_S2(eps, gamma=mp.mpf(0)):
    C = mp.matrix([[1, gamma], [gamma, 1]])
    return ("gauss", (C, [wpm(eps, 1), wpm(eps, -1)]))


def src_S3(eps, k, j):
    r = mp.sqrt(eps)
    if (k, j) in ((1, 1), (2, 2)):
        g = v0(eps)
    elif (k, j) == (1, 2):
        g = [-I1 * q for q in v1(eps)]
    else:  # (2, 1)
        g = [-I1 * eps * q for q in v1(eps)]
    return ("gauss", (mp.matrix([[1]]), [g]))


# ---------- populations and intensities ----------
def overlaps(basis, modes):
    return mp.matrix([[ip(u, w) for w in modes] for u in basis])


def G_matrix(src, basis):
    kind, payload = src
    if kind == "coh":
        a = payload
        c = mp.matrix([[ip(u, a)] for u in basis])
        return c * c.H
    C, modes = payload
    O = overlaps(basis, modes)
    return O * C * O.H


def total_population(src):
    kind, payload = src
    if kind == "coh":
        return mp.re(ip(payload, payload))
    C, modes = payload
    O = overlaps(modes, modes)  # Gram of the modes
    return mp.re(sum((C * O.T)[i, i] for i in range(C.rows)))


def intensity(src):
    kind, payload = src
    if kind == "coh":
        return [abs(a) ** 2 * DT for a in payload]
    C, modes = payload
    out = []
    for n in range(NT):
        w = mp.matrix([[m[n]] for m in modes])
        out.append(mp.re((w.H * C * w)[0, 0]) * DT)
    return out


# ---------- Fisher pieces ----------
def cdiff(fun, eps):
    h = HREL * eps
    fp, fm = fun(eps + h), fun(eps - h)
    if isinstance(fp, list):
        return [(a - b) / (2 * h) for a, b in zip(fp, fm)]
    return (fp - fm) / (2 * h)


def fisher_counts(n, dn, thermal):
    F = mp.mpf(0)
    for a, b in zip(n, dn):
        if a <= mp.mpf('1e-35'):
            continue
        F += b ** 2 / (a * (a + 1) if thermal else a)
    return F


def M1(srcfun, eps, thermal):
    def pops(e):
        src = srcfun(e)
        G = G_matrix(src, FIXED_BASIS)
        n = [mp.re(G[i, i]) for i in range(G.rows)]
        n.append(total_population(src) - sum(n))
        return n
    n = pops(eps)
    dn = cdiff(pops, eps)
    return fisher_counts(n, dn, thermal), n


def M2(srcfun, eps, thermal):
    n = intensity(srcfun(eps))
    dn = cdiff(lambda e: intensity(srcfun(e)), eps)
    return fisher_counts(n, dn, thermal)


# ---------- Gaussian QFI (Safranek convention: sigma_vac = I) ----------
def symplectic(m):
    O = mp.matrix(2 * m, 2 * m)
    for i in range(m):
        O[i, m + i] = 1
        O[m + i, i] = -1
    return O


def cov_from_G(G):
    m = G.rows
    S = mp.matrix(2 * m, 2 * m)
    for i in range(m):
        for j in range(m):
            re_, im_ = mp.re(G[i, j]), mp.im(G[i, j])
            S[i, j] = (1 if i == j else 0) + 2 * re_
            S[m + i, m + j] = (1 if i == j else 0) + 2 * re_
            S[i, m + j] = 2 * im_
            S[m + i, j] = -2 * im_
    return S


def kron(A, B):
    r = mp.matrix(A.rows * B.rows, A.cols * B.cols)
    for i in range(A.rows):
        for j in range(A.cols):
            for k in range(B.rows):
                for l in range(B.cols):
                    r[i * B.rows + k, j * B.cols + l] = A[i, j] * B[k, l]
    return r


def vec(M):
    return mp.matrix([[M[i, j]] for j in range(M.cols) for i in range(M.rows)])


def gaussian_qfi(sigma, dsigma, sign=-1):
    m2 = sigma.rows
    O = symplectic(m2 // 2)
    Mm = kron(sigma, sigma) + sign * kron(O, O)
    v = vec(dsigma)
    sol = mp.lu_solve(Mm, v)
    resid = mp.mnorm(Mm * sol - v) / max(mp.mnorm(v), mp.mpf('1e-40'))
    if resid > mp.mpf('1e-15'):
        raise RuntimeError(f"gaussian_qfi residual {mp.nstr(resid)}")
    return mp.re((v.T * sol)[0, 0]) / 2


def gate_gaussian_qfi():
    ok = True
    for n in (mp.mpf('0.1'), mp.mpf(3)):
        S = (2 * n + 1) * mp.eye(2)
        dS = 2 * mp.eye(2)
        F = gaussian_qfi(S, dS)
        exp_ = 1 / (n * (n + 1))
        err = abs(F / exp_ - 1)
        print(f"GATE thermal n={mp.nstr(n)}: F={mp.nstr(F, 10)} expected "
              f"{mp.nstr(exp_, 10)} rel err {mp.nstr(err, 3)}", flush=True)
        ok &= err < mp.mpf('1e-6')
    r = mp.mpf('0.3')
    S = mp.matrix([[mp.e ** (2 * r), 0], [0, mp.e ** (-2 * r)]])
    dS = mp.matrix([[2 * mp.e ** (2 * r), 0], [0, -2 * mp.e ** (-2 * r)]])
    F = gaussian_qfi(S, dS)
    err = abs(F / 2 - 1)
    print(f"GATE squeezed vacuum r=0.3: F={mp.nstr(F, 10)} expected 2 "
          f"rel err {mp.nstr(err, 3)}", flush=True)
    ok &= err < mp.mpf('1e-6')
    # two-mode thermal with a rotating mode basis: QFI must be basis
    # independent. Compare (n1,n2) thermal in fixed basis vs rotated by
    # theta with dtheta-dependence only through populations: skip.
    return bool(ok)


def M3(srcfun, eps, nbg=NBG):
    src = srcfun(eps)
    kind, payload = src
    if kind == "coh":
        da = cdiff(lambda e: srcfun(e)[1], eps)
        return 4 * mp.re(ip(da, da))
    basis = gram_schmidt([v0(eps), v1(eps), dv0(eps), dv1(eps)])
    def G_of(e):
        return G_matrix(srcfun(e), basis)
    G = G_of(eps) + nbg * mp.eye(len(basis))
    dG = cdiff(G_of, eps)
    return gaussian_qfi(cov_from_G(G), cov_from_G(dG) - mp.eye(2 * len(basis)) * 0)


def M3_marginalized_S1(eps):
    """Coherent state QFI matrix over (eps, Re x, Im x, Re y, Im y), Schur
    complement for eps."""
    def a_of(p):
        e, xr, xi, yr, yi = p
        return src_S1(e, mp.mpc(xr, xi), mp.mpc(yr, yi))[1]
    p0 = [eps, mp.re(XS1), mp.im(XS1), mp.re(YS1), mp.im(YS1)]
    cols = []
    for i in range(5):
        h = HREL * (abs(p0[i]) if p0[i] != 0 else mp.mpf(1))
        pp, pm = list(p0), list(p0)
        pp[i] += h
        pm[i] -= h
        ap, am = a_of(pp), a_of(pm)
        cols.append([(x - y) / (2 * h) for x, y in zip(ap, am)])
    F = mp.matrix(5, 5)
    for i in range(5):
        for j in range(5):
            F[i, j] = 4 * mp.re(ip(cols[i], cols[j]))
    C = F ** -1
    resid = mp.mnorm(F * C - mp.eye(5))
    if resid > mp.mpf('1e-18'):
        raise RuntimeError(f"marginalized inverse residual {mp.nstr(resid)}")
    return 1 / C[0, 0]


# ---------- driver ----------
def slopes(xs, ss):
    out = []
    for i in range(1, len(xs)):
        out.append(float((mp.log(ss[i]) - mp.log(ss[i - 1]))
                         / (mp.log(xs[i]) - mp.log(xs[i - 1]))))
    return out


def run_config(name, srcfun, thermal, do_M1=True, do_M2=True, do_M3=True,
               extra=None):
    rec = {}
    sig = {"M1": [], "M2": [], "M3": []}
    pops_last = None
    totals = []
    for eps in EPS_LIST:
        if do_M1:
            F, n = M1(srcfun, eps, thermal)
            sig["M1"].append(1 / mp.sqrt(F))
            pops_last = [float(x) for x in n]
        if do_M2:
            sig["M2"].append(1 / mp.sqrt(M2(srcfun, eps, thermal)))
        if do_M3:
            sig["M3"].append(1 / mp.sqrt(M3(srcfun, eps)))
        totals.append(total_population(srcfun(eps)))
    for m in ("M1", "M2", "M3"):
        if sig[m]:
            sl = slopes(EPS_LIST, sig[m])
            rec[m] = {"sigma_eps": [float(s) for s in sig[m]],
                      "slope_eps": sl,
                      "slope_gap_in_s": [2 * x - 1 for x in sl]}
            print(f"{name} {m}: slope_eps {['%.4f' % x for x in sl]} | "
                  f"gap slope in s {['%.4f' % (2 * x - 1) for x in sl]}",
                  flush=True)
    rec["total_population_slope"] = slopes(EPS_LIST, totals)
    rec["fixed_basis_populations_at_eps_min"] = pops_last
    if extra:
        rec.update(extra(EPS_LIST))
    return rec


def main():
    results = {"gate_gaussian_qfi": gate_gaussian_qfi()}
    if not results["gate_gaussian_qfi"]:
        print("GATE FAILED: Gaussian QFI implementation does not reproduce "
              "reference values. Stop.", flush=True)
        pathlib.Path("results/p20_rayleigh_ep.json").write_text(
            json.dumps(results, indent=1))
        sys.exit(1)

    # P20.1 coherent
    def extra_S1(eps_list):
        marg = [1 / mp.sqrt(M3_marginalized_S1(e)) for e in eps_list]
        sl = slopes(eps_list, marg)
        print(f"S1 M3 marginalized(x,y): slope_eps {['%.4f' % x for x in sl]}",
              flush=True)
        return {"M3_marginalized_slope_eps": sl}
    results["P20.1_S1"] = run_config("S1 coherent", src_S1, thermal=False,
                                     extra=extra_S1)

    # P20.2 eigenmode-incoherent
    results["P20.2_S2"] = run_config("S2 eigen-incoherent", src_S2,
                                     thermal=True)

    # P20.3 port-incoherent analytic
    for (k, j) in ((1, 1), (1, 2), (2, 1), (2, 2)):
        results[f"P20.3_S3_{k}{j}"] = run_config(
            f"S3 port ({k},{j})", lambda e, k=k, j=j: src_S3(e, k, j),
            thermal=True)

    # P20.4 partial coherence, fixed V
    for gamma in ("0.5", "0.9", "0.99", "1.0"):
        g = mp.mpf(gamma)
        results[f"P20.4_S4_gamma{gamma}"] = run_config(
            f"S4 gamma={gamma}", lambda e, g=g: src_S2(e, g), thermal=True,
            do_M2=False)

    # regularization insensitivity gate for M3 on S2 and S3(2,1)
    def m3_slopes(srcfun, nbg):
        s = [1 / mp.sqrt(M3(srcfun, e, nbg)) for e in EPS_LIST]
        return slopes(EPS_LIST, s)
    results["nbg_gate"] = {
        "S2_nbg_half": m3_slopes(src_S2, NBG / 2),
        "S3_21_nbg_half": m3_slopes(lambda e: src_S3(e, 2, 1), NBG / 2),
    }
    print(f"nbg gate S2: {['%.4f' % x for x in results['nbg_gate']['S2_nbg_half']]}",
          flush=True)
    print(f"nbg gate S3(2,1): "
          f"{['%.4f' % x for x in results['nbg_gate']['S3_21_nbg_half']]}",
          flush=True)

    pathlib.Path("results/p20_rayleigh_ep.json").write_text(
        json.dumps(results, indent=1))
    print("done", flush=True)


if __name__ == "__main__":
    main()
