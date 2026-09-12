"""Time-domain evolution of the draining-bathtub wave equation in the
tortoise coordinate (second instrument for P21, independent of the
continued fraction):

    d^2 H/dt^2 - d^2 H/dr*^2 + [ 2 B m / r^2 (i d/dt) ... ]

Written in first-order form for the complex field H(t, r*) with the
azimuthal factor e^{i m phi} already separated, the equation
    -d_t^2 H = -d_{r*}^2 H + V H  is generalized to
    (i d_t - B m / r^2)^2 H = -d_{r*}^2 H + V H,
i.e.  -d_t^2 H - 2 i (B m / r^2) d_t H + (B m / r^2)^2 H = -d_{r*}^2 H + V H.
With P = d_t H:
    d_t H = P
    d_t P = d_{r*}^2 H - V H + (B m / r^2)^2 H - 2 i (B m / r^2) P
Frequency-domain check: H ~ e^{-i omega t} gives
    -omega^2 H + 2 omega (B m / r^2) H + (B m/r^2)^2 H = ... wait, sign:
    d_t P = -omega^2 H, so -omega^2 H = H'' - V H + (Bm/r^2)^2 H + 2 i (Bm/r^2)(i omega) H
    => H'' + [omega^2 - 2 omega B m / r^2 + (B m / r^2)^2 - V] H = 0
    => H'' + [(omega - B m / r^2)^2 - V] H = 0.   (BCL eq. 16)  OK.

Grid: uniform in r*, large domain with outgoing (Sommerfeld) boundaries
at both ends; r(r*) inverted numerically once. RK4 in time, 2nd-order
centred space (4th-order optional). Signal extracted at a fixed r*_obs.
"""
import numpy as np
from scipy.optimize import brentq


def r_of_rstar(rs):
    """Invert r* = r + (1/2) ln((r-1)/(r+1)) for r > 1."""
    out = np.empty_like(rs)
    for k, s in enumerate(rs):
        if s < -14:
            # near-horizon asymptotics r* ~ 1 + (1/2) ln((r-1)/2)
            out[k] = 1 + 2 * np.exp(2 * (s - 1))
            continue
        f = lambda r: r + 0.5 * np.log((r - 1) / (r + 1)) - s
        lo = 1 + 1e-15
        hi = max(s + 2, 2.0)
        while f(hi) < 0:
            hi *= 2
        out[k] = brentq(f, lo, hi, xtol=1e-13)
    return out


def potential(r, m):
    return (1 - 1 / r ** 2) * ((m ** 2 - 0.25) / r ** 2 + 5 / (4 * r ** 4))


def evolve(m, B, rs_min=-60.0, rs_max=400.0, drs=0.05, t_max=300.0, cfl=0.5,
           rs_obs=40.0, x0=10.0, width=1.5, omega0=0.0, order=4):
    """Gaussian initial data H(0) = exp(-(r*-x0)^2/(2 width^2)) e^{i omega0 r*},
    P(0) = -d_{r*} H (approximately outgoing). Returns (t, H(t, r*_obs))."""
    rs = np.arange(rs_min, rs_max + drs / 2, drs)
    r = r_of_rstar(rs)
    V = potential(r, m)
    W = B * m / r ** 2
    # Stability: the rotation term enters as -2i W P, so the step must resolve
    # 1/|W| as well as the grid (|W| = B|m| at the horizon). Without this the
    # evolution overflows for B|m| >~ 20 (P32 shakedown).
    dt = cfl * min(drs, 1.0 / max(np.max(np.abs(W)), 1e-12))
    nt = int(t_max / dt)
    H = np.exp(-(rs - x0) ** 2 / (2 * width ** 2)) * np.exp(1j * omega0 * rs)
    P = -np.gradient(H, drs)
    iobs = int(round((rs_obs - rs_min) / drs))
    ts, sig = np.empty(nt + 1), np.empty(nt + 1, complex)

    def lap(u):
        d2 = np.zeros_like(u)
        if order == 4:
            d2[2:-2] = (-u[4:] + 16 * u[3:-1] - 30 * u[2:-2] + 16 * u[1:-3] - u[:-4]) / (12 * drs ** 2)
            d2[1] = (u[2] - 2 * u[1] + u[0]) / drs ** 2
            d2[-2] = (u[-1] - 2 * u[-2] + u[-3]) / drs ** 2
        else:
            d2[1:-1] = (u[2:] - 2 * u[1:-1] + u[:-2]) / drs ** 2
        return d2

    def rhs(H, P):
        dH = P.copy()
        dP = lap(H) - V * H + W ** 2 * H - 2j * W * P
        # Sommerfeld outgoing at the ends: d_t H = -+ d_{r*} H
        dH[0] = (H[1] - H[0]) / drs      # left-going at r* -> -inf: d_t H = + d_r* H
        dH[-1] = -(H[-1] - H[-2]) / drs  # right-going at +inf: d_t H = - d_r* H
        dP[0] = dP[-1] = 0.0
        return dH, dP

    for k in range(nt + 1):
        ts[k], sig[k] = k * dt, H[iobs]
        if k == nt:
            break
        k1H, k1P = rhs(H, P)
        k2H, k2P = rhs(H + 0.5 * dt * k1H, P + 0.5 * dt * k1P)
        k3H, k3P = rhs(H + 0.5 * dt * k2H, P + 0.5 * dt * k2P)
        k4H, k4P = rhs(H + dt * k3H, P + dt * k3P)
        H = H + dt / 6 * (k1H + 2 * k2H + 2 * k3H + k4H)
        P = P + dt / 6 * (k1P + 2 * k2P + 2 * k3P + k4P)
        # keep Sommerfeld boundary consistent
        P[0] = (H[1] - H[0]) / drs
        P[-1] = -(H[-1] - H[-2]) / drs
    return ts, sig


def prony_modes(t, y, order=4, t0=None, t1=None):
    """Matrix-pencil extraction of damped complex exponentials from a
    uniformly sampled complex signal on [t0, t1]. Returns frequencies
    omega (y ~ sum A e^{-i omega t}) and amplitudes."""
    sel = np.ones_like(t, bool)
    if t0 is not None:
        sel &= t >= t0
    if t1 is not None:
        sel &= t <= t1
    tt, yy = t[sel], y[sel]
    dt = tt[1] - tt[0]
    N = len(yy)
    L = N // 2
    Y = np.array([yy[i:i + L] for i in range(N - L)])
    U, s, Vh = np.linalg.svd(Y, full_matrices=False)
    Vh = Vh[:order]
    V1, V2 = Vh[:, :-1], Vh[:, 1:]
    z = np.linalg.eigvals(np.linalg.pinv(V1.T) @ V2.T)
    omega = 1j * np.log(z) / dt      # y ~ z^k = e^{-i omega k dt}
    Z = np.array([z ** k for k in range(N)])
    A = np.linalg.lstsq(Z, yy, rcond=None)[0]
    idx = np.argsort(-np.abs(A))
    return omega[idx], A[idx]
