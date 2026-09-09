"""P23 theory addendum: the barrier action of the pure vortex in closed
form and the analytic tower.

1. Symbolic expansion of J(h) = int sqrt(-q) d rho about the light ring
   (q = (gamma + 1/rho^2)^2 - 1/rho^2, gamma = 1/4 - h): coefficients of
   J/(pi h) in h are 2, 3, 15/2, 175/8, 2205/32 = 2 * 2F1(1/2, 3/2; 2; 4h)
   term by term, i.e. J(gamma) = 2 [K(k) - E(k)], k^2 = 1 - 4 gamma
   (complete elliptic integrals, parameter m = k^2).
2. Numerical check of the identity at real and complex gamma (quadrature
   against mpmath ellipk/ellipe).
3. Inversion of |m| J = i pi (n + 1/2): the tower series
   c = |m|/4 - i a/2 - (3/8) a^2/|m| + (3i/32) a^3/m^2 - (5/256) a^4/|m|^3
       + (9i/2048) a^5/m^4 + ...,  a = n + 1/2,
   and the elliptic condition solved directly for members of the tower.
4. The crossing constant kappa = (2/pi) Im[K - E] at the root of
   Re[K - E] = 0 on k^2 = 1 - 4 i y (y* = -0.35114692526,
   kappa = 0.80080533966), against the truncated series
   (0.816497 at a^2, 0.803118 at a^4).
Output: results/p23_action_series.json.
"""
import json
import pathlib

import mpmath as mp
import sympy as sp

OUT = {}
# ---- 1. symbolic expansion
x, h, y, th = sp.symbols("x h y theta", real=True)
ORD = 11
sig = 2 + x
gam = sp.Rational(1, 4) - h
f = sp.expand(sp.series(-((gam + 1 / sig ** 2) ** 2 - 1 / sig ** 2), x, 0, ORD).removeO())
g = sp.expand(sp.series(sp.expand(f.subs(x, sp.sqrt(h) * y) / h), h, 0, 5).removeO())


def root_series(y0):
    r = sp.Integer(y0)
    for _ in range(7):
        r = sp.expand(sp.series(r - g.subs(y, r) / sp.diff(g, y).subs(y, r), h, 0, 5).removeO())
    return sp.expand(sp.series(r, h, 0, 5).removeO())


ym, yp = root_series(-4), root_series(4)
Y = ym + (yp - ym) * (1 + sp.cos(th)) / 2
smooth = sp.expand(sp.series(sp.simplify(sp.cancel(sp.expand(g.subs(y, Y))) / (((yp - ym) / 2) ** 2 * sp.sin(th) ** 2)), h, 0, 5).removeO())
integrand = sp.expand(sp.series(sp.sqrt(smooth) * ((yp - ym) / 2) ** 2 * sp.sin(th) ** 2, h, 0, 5).removeO())
Jh = sp.expand(sp.simplify(sp.expand(sp.integrate(integrand, (th, 0, sp.pi)))))
coef = [sp.nsimplify(sp.simplify(Jh.coeff(h, k) / sp.pi)) for k in range(5)]
hyper = [sp.nsimplify(2 * sp.rf(sp.Rational(1, 2), k) * sp.rf(sp.Rational(3, 2), k) / sp.rf(2, k) * 4 ** k / sp.factorial(k)) for k in range(5)]
print("J/(pi h) coefficients:", coef, "; 2*2F1(1/2,3/2;2;4h):", hyper, flush=True)
OUT["J_over_pi_h_coefficients"] = [str(c) for c in coef]
OUT["hypergeometric_match"] = coef == hyper

# ---- 3. inversion
eps = sp.symbols("epsilon")
a = sp.symbols("a1:6")
hs = sum(a[k] * eps ** (k + 1) for k in range(5))
eq = sp.expand(sum(coef[k] * hs ** (k + 1) for k in range(5))) - eps
sol = {}
for k in range(1, 6):
    sol[a[k - 1]] = sp.solve(sp.expand(eq.coeff(eps, k)).subs(sol), a[k - 1])[0]
M, al = sp.symbols("M alpha", positive=True)
cser = sp.expand(M * (sp.Rational(1, 4) - sp.expand(hs.subs(sol)).subs(eps, sp.I * al / M)))
print("c(alpha, |m|) =", sp.collect(cser, M), flush=True)
OUT["tower_series"] = str(sp.collect(cser, M))
kap = sp.symbols("kappa", positive=True)
recl = sp.simplify(sp.expand(sp.re(sp.expand(cser.subs(al, kap * M)))) / M)
OUT["kappa_truncated_a4"] = [float(r) for r in sp.Poly(recl, kap).nroots() if abs(sp.im(r)) < 1e-12 and sp.re(r) > 0]
print("kappa from the series truncated at a^4:", OUT["kappa_truncated_a4"], flush=True)

# ---- 2 & 4. elliptic identity, tower members, kappa
mp.mp.dps = 30


def Jnum(gamma):
    gamma = mp.mpc(gamma)
    s = mp.sqrt(1 - 4 * gamma)
    rm, rp = (1 - s) / (2 * gamma), (1 + s) / (2 * gamma)
    D = rp - rm
    f = lambda t: mp.sqrt(t * (1 - t)) * mp.sqrt(gamma * (rm + t * D) ** 2 + (rm + t * D) + 1) / (rm + t * D) ** 2
    return mp.sqrt(gamma) * D ** 2 * mp.quad(f, [0, 0.5, 1])


def Jell(gamma):
    m = 1 - 4 * mp.mpc(gamma)
    return 2 * (mp.ellipk(m) - mp.ellipe(m))


checks = []
for gm in (mp.mpf("0.24"), mp.mpf("0.1"), mp.mpc("0.24", "-0.05"), mp.mpc("0.2", "-0.2"), mp.mpc("0.0099", "-0.3472")):
    d = abs(Jnum(gm) - Jell(gm))
    checks.append([complex(gm).real, complex(gm).imag, float(d)])
    print(f"  gamma={complex(gm)}: |J_quad - 2(K-E)| = {float(d):.1e}", flush=True)
OUT["identity_checks"] = checks


def solve_member(m, n, seed):
    am = abs(m)
    f = lambda cc: am * Jell(cc / am) - 1j * mp.pi * (n + mp.mpf(1) / 2)
    return complex(mp.findroot(f, mp.mpc(seed), solver="muller", tol=1e-15, maxsteps=60))


members = {}
for m, n, seed in ((-2, 1, 0.07 - 0.69j), (-4, 0, 0.98 - 0.25j), (-4, 2, 0.41 - 1.17j), (-7, 5, 0.07 - 2.43j), (-10, 7, 0.32 - 3.35j), (-15, 11, 0.33 - 5.1j)):
    c = solve_member(m, n, seed)
    members[f"{m},{n}"] = [c.real, c.imag]
    print(f"  elliptic condition m={m} n={n}: {c:.5f}", flush=True)
OUT["elliptic_members"] = members
g = lambda yv: mp.re(Jell(1j * yv))
ys = mp.findroot(g, (mp.mpf("-0.3"), mp.mpf("-0.4")), solver="bisect", tol=1e-25)
kappa = mp.im(Jell(1j * ys)) / mp.pi
print(f"  y* = {mp.nstr(ys, 15)}, kappa = {mp.nstr(kappa, 15)}", flush=True)
OUT["y_star"] = float(ys)
OUT["kappa"] = float(kappa)
OUT["kappa_str"] = mp.nstr(kappa, 20)
pathlib.Path("results/p23_action_series.json").write_text(json.dumps(OUT, indent=1))
print("done", flush=True)
