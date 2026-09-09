"""Draining-bathtub (DBT) acoustic black hole quasinormal modes.

Wave equation (Berti-Cardoso-Lemos 2004, eq. 16-17; Cardoso-Lemos-Yoshida
2004, eq. 7-8), units A = c = 1, horizon at r = 1, rotation B:

    d^2 H / dr*^2 + [ (omega - B m / r^2)^2 - V ] H = 0,
    V = (1 - 1/r^2) [ (m^2 - 1/4) / r^2 + 5 / (4 r^4) ].

Leaver continued fraction with x = 1/r (CLY eqs. 13-21):

    Psi = e^{i omega / x} ((1 - x)/(1 + x))^{-i(omega - B m)/2} sum_k a_k (1 - x)^k

four-term recurrence alpha_k a_{k+1} + beta_k a_k + gamma_k a_{k-1}
+ delta_k a_{k-2} = 0, reduced to three terms by Gaussian elimination, and
the QNM condition is the vanishing of the continued fraction (with the
n-th inversion for the n-th overtone, Leaver 1985).

Symmetric-invariant helpers (mu, rho) for a pair of modes follow the
program's convention omega_pm = mu +- sqrt(rho).
"""
import mpmath as mp


def coeffs(k, omega, m, B):
    i = mp.mpc(0, 1)
    alpha = -8 * (1 + k) * (1 + k + i * B * m - i * omega)
    beta = 4 * (1 + 5 * k ** 2 + m ** 2 + k * (5 + 4 * i * B * m - 8 * i * omega)
                - 4 * i * omega - 4 * omega ** 2 + 2 * B * m * (i + 2 * omega))
    gamma = 2 * (3 - 8 * k ** 2 - 4 * i * k * (B * m - 2 * omega))
    delta = -3 - 4 * k + 4 * k ** 2
    return alpha, beta, gamma, delta


def three_term(omega, m, B, kmax):
    """Return lists alpha', beta', gamma' for k = 0..kmax after Gaussian
    elimination of the delta term (CLY eqs. 17-19)."""
    al, be, ga = [], [], []
    for k in range(kmax + 1):
        a, b, g, d = coeffs(k, omega, m, B)
        if k < 2:
            al.append(a)
            be.append(b)
            ga.append(g)
        else:
            bp = b - al[k - 1] * d / ga[k - 1]
            gp = g - be[k - 1] * d / ga[k - 1]
            al.append(a)
            be.append(bp)
            ga.append(gp)
    return al, be, ga


def nollert_seed(omega, m, B, K, al):
    """Nollert-type tail seed: X_{K+1} = -alpha'_K R_{K+1} with the
    asymptotic ratio R_k = a_k/a_{k-1} ~ 1 +- (-2 i omega)^{1/2} k^{-1/2}
    - (3 + 4 i omega)/(4k) (CLY eq. 21), minimal-solution branch
    Re[+-(-2 i omega)^{1/2}] < 0."""
    i = mp.mpc(0, 1)
    s = mp.sqrt(-2 * i * omega)
    if mp.re(s) > 0:
        s = -s
    k = mp.mpf(K + 1)
    R = 1 + s / mp.sqrt(k) - (3 + 4 * i * omega) / (4 * k)
    return -al[K] * R


def leaver_function(omega, m, B, n=0, kmax=400, nollert=True):
    """Leaver's continued-fraction function whose zeros are the QNMs.
    n-th inversion (Leaver 1985): the n-th overtone is the most stable
    root of the n-th inverted fraction. With nollert=True the tail is
    seeded with the asymptotic minimal-solution ratio."""
    omega = mp.mpc(omega)
    al, be, ga = three_term(omega, m, B, kmax)
    # tail: evaluate the infinite fraction from the bottom
    tail = nollert_seed(omega, m, B, kmax, al) if nollert else mp.mpc(0)
    for k in range(kmax, n, -1):
        tail = al[k - 1] * ga[k] / (be[k] - tail)
    # n-th inversion: the "upper" finite fraction
    head = mp.mpc(0)
    if n > 0:
        head = be[0]
        for k in range(1, n):
            head = be[k] - al[k - 1] * ga[k] / head
        # now include the term linking level n
        return be[n] - al[n - 1] * ga[n] / head - tail
    return be[0] - tail


def find_qnm(omega0, m, B, n=0, kmax=400, tol=mp.mpf("1e-14"), maxsteps=60,
             nollert=True, resid_max=mp.mpf("1e-18")):
    """Secant/Muller root of the Leaver function from a starting guess.
    Guard: the residual |f| at the root must be below resid_max, otherwise
    the iteration stalled (typically on the negative imaginary axis, where
    the continued fraction has its branch cut) and a RuntimeError is
    raised. Roots with |Re omega| < 1e-12 are rejected as cut artifacts
    unless the caller passes resid_max=None."""
    f = lambda w: leaver_function(w, m, B, n, kmax, nollert)
    w = mp.findroot(f, mp.mpc(omega0), solver='muller', tol=tol,
                    maxsteps=maxsteps)
    if resid_max is not None:
        r = abs(f(w))
        if r > resid_max:
            raise RuntimeError(f"stalled root {mp.nstr(w, 10)} residual {mp.nstr(r, 2)}")
        if abs(mp.re(w)) < mp.mpf("1e-12"):
            raise RuntimeError(f"on-axis root {mp.nstr(w, 10)} rejected (branch cut)")
    return w


def wkb_fundamental_large_m(m):
    """BCL eq. 23, large-m eikonal limit for B = 0."""
    return mp.mpc(m / mp.mpf(2), -1 / (2 * mp.sqrt(2)))


def sym_invariants(w1, w2):
    """mu, rho with omega_pm = mu +- sqrt(rho)."""
    mu = (w1 + w2) / 2
    rho = ((w1 - w2) / 2) ** 2
    return mu, rho


# ---------------------------------------------------------------------------
# Second instrument: spectral collocation in Leaver's variable x = 1/r with the
# asymptotic factor E(x) = e^{i omega / x} ((1-x)/(1+x))^{-i(omega - B m)/2}
# removed, so that the QNM condition becomes regularity of u = H/E on [0, 1].
# The ODE for u is derived symbolically once; it is quadratic in omega, and the
# collocation matrices give a quadratic eigenvalue problem linearized to a
# generalized eigenproblem (all modes at once, double precision, to be refined
# with the continued fraction).
# ---------------------------------------------------------------------------
_COLL_CACHE = {}


def _derive_u_ode():
    import sympy as sp
    x, w, B, m = sp.symbols('x omega B m')
    u = sp.Function('u')(x)
    I = sp.I
    E = sp.exp(I * w / x) * ((1 - x) / (1 + x)) ** (-I * (w - B * m) / 2)
    H = E * u
    D = lambda f: -x ** 2 * (1 - x ** 2) * sp.diff(f, x)
    Q = (w - B * m * x ** 2) ** 2 - (1 - x ** 2) * ((m ** 2 - sp.Rational(1, 4)) * x ** 2
                                                    + sp.Rational(5, 4) * x ** 4)
    eq = sp.simplify((D(D(H)) + Q * H) / E)
    eq = sp.expand(eq)
    c2 = sp.simplify(eq.coeff(sp.Derivative(u, (x, 2))))
    rest = sp.expand(eq - c2 * sp.Derivative(u, (x, 2)))
    c1 = sp.simplify(rest.coeff(sp.Derivative(u, x)))
    c0 = sp.simplify(sp.expand(rest - c1 * sp.Derivative(u, x)).subs(u, 1))
    # clear the common singular prefactor: multiply by (1+x)^2 / x^2 ... find
    # the minimal multiplier that makes all three polynomial in x
    # reduce so that P2 = x^2 (1+x)^2 (1-x): the rows at x = 0 and x = 1
    # then become the regularity conditions P1 u' + P0 u = 0 (regular
    # singular ends), instead of identically-zero rows
    mult = sp.cancel(x ** 2 * (1 + x) ** 2 * (1 - x) / c2)
    P2 = sp.expand(sp.cancel(c2 * mult))
    P1 = sp.expand(sp.cancel(c1 * mult))
    P0 = sp.expand(sp.cancel(c0 * mult))
    polys = []
    for P in (P2, P1, P0):
        Pw = sp.Poly(P, w)
        cs = [sp.lambdify((x, B, m), sp.expand(Pw.coeff_monomial(w ** k)), 'numpy')
              for k in range(3)]
        polys.append(cs)
    return polys, (P2, P1, P0)


def _cheb_lobatto(N):
    import numpy as np
    k = np.arange(N + 1)
    t = np.cos(np.pi * k / N)            # [-1, 1], descending
    xg = (1 - t) / 2                      # map to [0, 1], ascending
    # differentiation matrix on t (Trefethen), then chain rule d/dx = -2 d/dt
    c = np.ones(N + 1)
    c[0] = c[-1] = 2
    c *= (-1.0) ** k
    T = np.tile(t, (N + 1, 1)).T
    dT = T - T.T + np.eye(N + 1)
    Dt = (np.outer(c, 1 / c)) / dT
    Dt -= np.diag(Dt.sum(axis=1))
    Dx = -2 * Dt
    return xg, Dx


def collocation_spectrum(m, B, N=100, window=None):
    """All eigenvalues omega of the collocated QEP at rotation B, azimuthal m.
    Returns a numpy array; optional window (re_min, re_max, im_min, im_max)."""
    import numpy as np
    import scipy.linalg as sla
    if 'polys' not in _COLL_CACHE:
        _COLL_CACHE['polys'], _COLL_CACHE['sym'] = _derive_u_ode()
    polys = _COLL_CACHE['polys']
    xg, Dx = _cheb_lobatto(N)
    D2 = Dx @ Dx
    A = []
    for k in range(3):  # omega^k
        Ak = np.zeros((N + 1, N + 1), complex)
        for P, Dmat in zip(polys, (D2, Dx, np.eye(N + 1))):
            coef = np.asarray(P[k](xg, float(B), float(m)), dtype=complex)
            coef = np.broadcast_to(coef, (N + 1,))
            Ak += np.diag(coef) @ Dmat
        A.append(Ak)
    A0, A1, A2 = A
    n = N + 1
    Z, Id = np.zeros((n, n), complex), np.eye(n, dtype=complex)
    L = np.block([[Z, Id], [-A0, -A1]])
    R = np.block([[Id, Z], [Z, A2]])
    ev = sla.eig(L, R, right=False)
    ev = ev[np.isfinite(ev)]
    if window is not None:
        r0, r1, i0, i1 = window
        ev = ev[(ev.real >= r0) & (ev.real <= r1) & (ev.imag >= i0) & (ev.imag <= i1)]
    return np.sort_complex(ev)
