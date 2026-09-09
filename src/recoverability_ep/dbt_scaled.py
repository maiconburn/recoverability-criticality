"""Scaled (pure-vortex) limit of the draining-bathtub counter-rotating
spectrum (P21f):

    H'' + [ (c - m/rho^2)^2 - (m^2 - 1/4)/rho^2 ] H = 0,   rho > 0,

outgoing at infinity, H ~ e^{i c rho} (1 + z_1/rho + ...), and one WKB
branch at rho -> 0, H ~ rho^{1/2} exp(-+ i |m| / rho) (1 + ...).
Eigenvalues c = lim_{B -> inf} B omega of the escaping modes.

Direct integration (scipy DOP853, complex), with the outer solution
integrated inward along a ray rotated into the complex rho plane so that
the outgoing solution is the growing one in the direction of
integration (Im(c e^{i phi}) > 0), and the inner solution integrated
outward from rho_min on the real axis. Wronskian matched at rho_m.
"""
import numpy as np
from scipy.integrate import solve_ivp


def Q(rho, c, m):
    return (c - m / rho ** 2) ** 2 - (m ** 2 - 0.25) / rho ** 2


def _outer_series(rho, c, m, nterms=8):
    """e^{i c rho} sum z_k rho^-k, z_0 = 1, from the recursion
    z_{k+1} = ([k(k+1) - b] z_k + a z_{k-2}) / (2 i c (k+1)),
    b = m^2 + 2 c m - 1/4, a = m^2. Returns (H, H')."""
    b = m ** 2 + 2 * c * m - 0.25
    a = m ** 2
    z = [1.0 + 0j]
    for k in range(nterms):
        zk = z[k]
        zkm2 = z[k - 2] if k >= 2 else 0.0
        z.append(((k * (k + 1) - b) * zk + a * zkm2) / (2j * c * (k + 1)))
    S = sum(zk * rho ** (-k) for k, zk in enumerate(z))
    dS = sum(-k * zk * rho ** (-k - 1) for k, zk in enumerate(z))
    e = np.exp(1j * c * rho)
    return e * S, e * (1j * c * S + dS)


def _inner_wkb(rho, c, m, branch=-1):
    """rho^{1/2} exp(branch * i (|m|/rho + beta rho)) with the next WKB
    phase term beta = (m^2 + 2 c m - 1/4)/(2|m|); returns (H, H')."""
    am = abs(m)
    beta = (m ** 2 + 2 * c * m - 0.25) / (2 * am)
    phase = branch * 1j * (am / rho + beta * rho)
    H = np.sqrt(rho) * np.exp(phase)
    dphase = branch * 1j * (-am / rho ** 2 + beta)
    dH = H * (0.5 / rho + dphase)
    return H, dH


def wronskian(c, m, branch=-1, rho_m=1.0, rho_min=0.02, rho_max=None, phi=None,
              rtol=1e-10, atol=1e-14):
    c = complex(c)
    if rho_max is None:
        rho_max = max(40.0 / abs(c), 30.0)
    if phi is None:
        # rotate so that e^{i c rho} decays outward along the ray (then it is
        # the growing solution when integrating inward): Im(c e^{i phi}) > 0
        # any phi in (-alpha, pi - alpha) works; keep the ray away from
        # rho = 0 (where Q ~ 1/rho^4) by capping it at ~120 degrees
        alpha = np.angle(c)
        phi = max(-alpha + 0.3, min(np.pi / 2 - alpha, 2.1))
        phi = min(phi, np.pi - 0.3)
    eiphi = np.exp(1j * phi)

    # outer: rho(s) = rho_m + s e^{i phi}, s from s_max to 0
    s_max = rho_max
    rho_start = rho_m + s_max * eiphi
    H0, dH0 = _outer_series(rho_start, c, m)
    # dH/ds = e^{i phi} dH/d rho
    y0 = [H0, dH0 * eiphi]

    def rhs_out(s, y):
        rho = rho_m + s * eiphi
        return [y[1], -eiphi ** 2 * Q(rho, c, m) * y[0]]

    sol = solve_ivp(rhs_out, (s_max, 0.0), y0, method="DOP853", rtol=rtol, atol=atol)
    Hout, dHout_ds = sol.y[0][-1], sol.y[1][-1]
    dHout = dHout_ds / eiphi

    # inner: from rho_min outward on the real axis
    Hi, dHi = _inner_wkb(rho_min, c, m, branch)

    def rhs_in(rho, y):
        return [y[1], -Q(rho, c, m) * y[0]]

    sol2 = solve_ivp(rhs_in, (rho_min, rho_m), [Hi, dHi], method="DOP853", rtol=rtol, atol=atol)
    Hin, dHin = sol2.y[0][-1], sol2.y[1][-1]
    # normalized Wronskian
    W = (Hin * dHout - dHin * Hout) / (abs(Hin * dHout) + abs(dHin * Hout))
    return W


def find_c(c0, m, branch=-1, tol=1e-10, maxit=60, **kw):
    """Secant/Muller iteration on the normalized Wronskian."""
    import mpmath as mp
    f = lambda z: complex(wronskian(complex(z), m, branch, **kw))
    r = mp.findroot(f, mp.mpc(c0), solver="muller", tol=tol, maxsteps=maxit)
    return complex(r), abs(f(r))


def wronskian_cplx(c, m, branch=+1, rho_m=1.0, rho_min=0.02, theta=0.5, rho_max=None, phi=None,
                   rtol=1e-11, atol=0.0):
    """Wronskian with the INNER solution integrated along the ray
    rho = r e^{-i theta} (r from rho_min to rho_m), then along the arc back
    to the real point rho_m. On that ray the physical branch
    rho^{1/2} exp(+i|m|/rho) has modulus exp(-|m| sin(theta)/r), i.e. it is
    the GROWING solution in the direction of integration, so the
    admixture of the other branch is suppressed instead of amplified
    (on the real axis both branches have equal modulus near rho = 0 and
    the wanted one is subdominant by exp(2 |Im c| rho_m) at the matching
    point, which made the deep members of the tower cutoff-sensitive for
    |m| >= 8). The outer solution is the same as in `wronskian`.
    """
    c = complex(c)
    if rho_max is None:
        rho_max = max(40.0 / abs(c), 30.0)
    if phi is None:
        alpha = np.angle(c)
        phi = max(-alpha + 0.3, min(np.pi / 2 - alpha, 2.1))
        phi = min(phi, np.pi - 0.3)
    eiphi = np.exp(1j * phi)
    rho_start = rho_m + rho_max * eiphi
    H0, dH0 = _outer_series(rho_start, c, m)

    def rhs_out(s, y):
        rho = rho_m + s * eiphi
        return [y[1], -eiphi ** 2 * Q(rho, c, m) * y[0]]

    sol = solve_ivp(rhs_out, (rho_max, 0.0), [H0, dH0 * eiphi], method="DOP853", rtol=rtol, atol=atol)
    Hout, dHout = sol.y[0][-1], sol.y[1][-1] / eiphi

    # inner, leg 1: along the ray rho = r e^{-i theta}, r in [rho_min, rho_m]
    e = np.exp(-1j * theta)
    Hi, dHi = _inner_wkb(rho_min * e, c, m, branch)          # dH/drho at the complex start

    def rhs_ray(r, y):                                        # d/dr = e d/drho
        rho = r * e
        return [y[1], -e ** 2 * Q(rho, c, m) * y[0]]

    sol1 = solve_ivp(rhs_ray, (rho_min, rho_m), [Hi, dHi * e], method="DOP853", rtol=rtol, atol=atol)
    H1, dH1 = sol1.y[0][-1], sol1.y[1][-1] / e                # back to dH/drho
    # inner, leg 2: along the arc rho = rho_m e^{-i t}, t from theta to 0
    def rhs_arc(t, y):                                        # d/dt = g d/drho, g = -i rho, dg/dt = -i g
        rho = rho_m * np.exp(-1j * t)                         # y1 = g H', so y1' = g^2 H'' + (dg/dt) H' = -g^2 Q H - i y1
        g = -1j * rho
        return [y[1], -g ** 2 * Q(rho, c, m) * y[0] - 1j * y[1]]

    g0 = -1j * rho_m * e
    sol2 = solve_ivp(rhs_arc, (theta, 0.0), [H1, dH1 * g0], method="DOP853", rtol=rtol, atol=atol)
    Hin, dHin = sol2.y[0][-1], sol2.y[1][-1] / (-1j * rho_m)
    return (Hin * dHout - dHin * Hout) / (abs(Hin * dHout) + abs(dHin * Hout))


def find_c_cplx(c0, m, tol=1e-10, maxit=40, step=0.004 + 0.002j, **kw):
    """Local secant iteration on wronskian_cplx (no Muller hops)."""
    import mpmath as mp
    f = lambda z: complex(wronskian_cplx(complex(z), m, **kw))
    r = mp.findroot(f, (mp.mpc(c0), mp.mpc(c0) + mp.mpc(step)), solver="secant", tol=tol, maxsteps=maxit)
    return complex(r), abs(f(r))


def wronskian_wall(c, m, rho_c=0.5, kind="dirichlet", rho_m=None, rho_max=None, phi=None, rtol=1e-11, atol=0.0):
    """Wronskian for a REFLECTING core: a wall at rho_c with H = 0 (Dirichlet)
    or H' = 0 (Neumann) instead of the absorbing branch at rho -> 0. The
    inner solution is integrated outward on the real axis from rho_c to
    rho_m (no branch selection is needed: the wall fixes the solution up to
    normalisation); the outer solution is the same outgoing ray as in
    `wronskian_cplx`. P26."""
    c = complex(c)
    if not np.isfinite(c) or abs(c) < 1e-3:
        return 1.0 + 0j
    if rho_m is None:
        rho_m = rho_c + 0.6
    if rho_max is None:
        rho_max = min(max(40.0 / abs(c), 30.0), 400.0)
    if phi is None:
        alpha = np.angle(c)
        phi = max(-alpha + 0.3, min(np.pi / 2 - alpha, 2.1))
        phi = min(phi, np.pi - 0.3)
    eiphi = np.exp(1j * phi)
    rho_start = rho_m + rho_max * eiphi
    H0, dH0 = _outer_series(rho_start, c, m)

    def rhs_out(s, y):
        rho = rho_m + s * eiphi
        return [y[1], -eiphi ** 2 * Q(rho, c, m) * y[0]]

    sol = solve_ivp(rhs_out, (rho_max, 0.0), [H0, dH0 * eiphi], method="DOP853", rtol=rtol, atol=atol, max_step=2.0)
    if not sol.success or not np.all(np.isfinite(sol.y[:, -1])):
        return 1.0 + 0j
    Hout, dHout = sol.y[0][-1], sol.y[1][-1] / eiphi
    y0 = [0.0 + 0j, 1.0 + 0j] if kind == "dirichlet" else [1.0 + 0j, 0.0 + 0j]

    def rhs_in(rho, y):
        return [y[1], -Q(rho, c, m) * y[0]]

    sol2 = solve_ivp(rhs_in, (rho_c, rho_m), y0, method="DOP853", rtol=rtol, atol=1e-30, max_step=0.05)
    if not sol2.success or not np.all(np.isfinite(sol2.y[:, -1])):
        return 1.0 + 0j
    Hin, dHin = sol2.y[0][-1], sol2.y[1][-1]
    W = (Hin * dHout - dHin * Hout) / (abs(Hin * dHout) + abs(dHin * Hout))
    return W if np.isfinite(W) else 1.0 + 0j


def find_c_wall(c0, m, tol=1e-10, maxit=40, step=0.004 + 0.002j, **kw):
    import mpmath as mp
    f = lambda z: complex(wronskian_wall(complex(z), m, **kw))
    r = mp.findroot(f, (mp.mpc(c0), mp.mpc(c0) + mp.mpc(step)), solver="secant", tol=tol, maxsteps=maxit)
    return complex(r), abs(f(r))
