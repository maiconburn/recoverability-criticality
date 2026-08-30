"""P11': time-domain wormhole echoes and detectability (frozen before run)."""
import json
import pathlib

import numpy as np

U0 = 0.15

def V_double(x, L):
    return U0*(1/np.cosh(x - L/2)**2 + 1/np.cosh(x + L/2)**2)

def V_single(x, L):
    return U0*(1/np.cosh(x - L/2)**2)

def evolve(L, Vfun, T_end):
    dx = 0.05
    X = L/2 + 60.0
    x = np.arange(-X, X + dx, dx)
    dt = 0.4*dx
    nt = int(T_end/dt)
    V = Vfun(x, L)
    xs, sig = -(L/2 + 15.0), 2.0
    psi = np.exp(-(x - xs)**2/(2*sig**2))
    # rightward-moving pulse: psi_t = -psi_x (advection init)
    dpsi = np.gradient(psi, dx)
    psi_prev = psi - dt*(-dpsi)
    io = int(round((L/2 + 20.0 + X)/dx))
    rec = np.zeros(nt)
    tgrid = np.arange(nt)*dt
    c2 = (dt/dx)**2
    for n in range(nt):
        lap = np.zeros_like(psi)
        lap[1:-1] = psi[2:] - 2*psi[1:-1] + psi[:-2]
        psi_next = 2*psi - psi_prev + c2*lap - (dt**2)*V*psi
        # simple absorbing (Sommerfeld) ends
        psi_next[0] = psi[1] + (dt-dx)/(dt+dx)*(psi_next[1] - psi[0])
        psi_next[-1] = psi[-2] + (dt-dx)/(dt+dx)*(psi_next[-2] - psi[-1])
        psi_prev, psi = psi, psi_next
        rec[n] = psi[io]
    return tgrid, rec

def echo_delay(t, y, t_prompt):
    """Autocorrelation peak of the post-prompt signal."""
    m = t > t_prompt
    z = y[m] - y[m].mean()
    ac = np.correlate(z, z, "full")[len(z)-1:]
    dt = t[1] - t[0]
    # first prominent peak after lag > 5
    lag0 = int(5/dt)
    k = lag0 + np.argmax(ac[lag0:int(len(ac)*0.6)])
    return k*dt

out = {"echo": [], "detect": []}
NOISE = 1.0  # per-sample unit noise; SNR scales the signal
for L in (8.0, 12.0, 16.0, 20.0, 24.0):
    T_end = 40 + 12*L
    t, yW = evolve(L, V_double, T_end)
    _, yB = evolve(L, V_single, T_end)
    t_prompt = (15.0 + 20.0 + L) + 25.0   # travel + prompt ringdown clearance
    dly = echo_delay(t, yW, t_prompt)
    out["echo"].append([L, float(dly), float(2*L)])
    print(f"L={L}: echo delay={dly:.1f} (2L={2*L})", flush=True)
    # detectability: distinguishing statistic = |yW - yB| in post-prompt window
    m = t > t_prompt
    diff = yW[m] - yB[m]
    # Fisher for overall amplitude of the wormhole-extra signal (template):
    # SNR_min(5 sigma) = 5 / |diff| per unit signal amplitude, with the
    # signal normalized by the prompt peak (so SNR is prompt-referenced)
    prompt_peak = np.max(np.abs(yB))
    snr_template = 5.0*prompt_peak/np.linalg.norm(diff)
    # agnostic: excess-energy detection in the blind window; variance of the
    # chi2 with N dof -> threshold ~ sqrt(2N); SNR_min scales as
    # (2N)^{1/4} * sqrt(5) * prompt/||diff|| approx:
    N = int(np.sum(m))
    snr_agn = np.sqrt(5.0)*(2*N)**0.25*prompt_peak/np.linalg.norm(diff)
    out["detect"].append([L, float(snr_template), float(snr_agn)])
    print(f"      SNR_min template={snr_template:.1f} agnostic={snr_agn:.1f} "
          f"ratio={snr_agn/snr_template:.1f}", flush=True)

d = np.array(out["detect"])
mono = bool(np.all(np.diff(d[:, 1]) > 0))
print(f"P11'.2: monotonic={mono} ratio_L24/L8={d[-1,1]/d[0,1]:.2f}", flush=True)
print(f"P11'.3: agnostic/template at L=24: {d[-1,2]/d[-1,1]:.2f}", flush=True)
json.dump(out, open("results/p11_prime.json", "w"), indent=1)
print("done", flush=True)
