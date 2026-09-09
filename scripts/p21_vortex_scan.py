"""P21: draining-bathtub vortex QNM scan (predictions frozen in
results/FROZEN_P21_VORTEX.md before this run).

Tracks counter-rotating (m < 0, Re omega > 0 branch) and co-rotating
overtones in the rotation B with the Leaver continued fraction, measures
the approach to the negative imaginary axis (branch cut), searches for
principal-sheet roots beyond the arrival point, scans adjacent-pair gaps
for avoided crossings, and fits the large-B behaviour of the fundamental.
Writes results/p21_vortex_scan.json incrementally.
"""
import json
import pathlib
import sys
import time

import mpmath as mp

sys.path.insert(0, "src")
from recoverability_ep.dbt import find_qnm, leaver_function, sym_invariants  # noqa

mp.mp.dps = 24
OUT = pathlib.Path("results/p21_vortex_scan.json")
RES = {"meta": {"dps": 24, "started": time.strftime("%Y-%m-%d %H:%M:%S")}}


def save():
    OUT.write_text(json.dumps(RES, indent=1, default=str))


def cplx(w):
    return [float(mp.re(w)), float(mp.im(w))]


def safe_find(w0, m, B, n, kmax):
    try:
        return find_qnm(w0, m, B, n=n, kmax=kmax, tol=mp.mpf("1e-12"), maxsteps=80)
    except Exception:
        return None


def track(m, n, w0, B_start, B_end, dB, kmax=500, max_jump=0.08, min_dB=1e-5,
          stop_re=None, label=""):
    """Continue the root w0 from B_start toward B_end. Returns list of
    (B, omega). Stops when the step underflows (arrival at the cut) or when
    Re(omega) crosses stop_re."""
    path = [(mp.mpf(B_start), mp.mpc(w0))]
    B, w = mp.mpf(B_start), mp.mpc(w0)
    step = mp.mpf(dB)
    direction = 1 if B_end > B_start else -1
    while (B_end - B) * direction > 0:
        Bn = B + direction * step
        if (B_end - Bn) * direction < 0:
            Bn = mp.mpf(B_end)
        # linear extrapolation seed
        if len(path) >= 2:
            (B1, w1), (B2, w2) = path[-2], path[-1]
            seed = w2 + (w2 - w1) * (Bn - B2) / (B2 - B1) if B2 != B1 else w2
        else:
            seed = w
        wn = safe_find(seed, m, Bn, n, kmax)
        if wn is None or abs(wn - w) > max_jump or mp.re(wn) * mp.re(w) < 0:
            step /= 2
            if step < min_dB:
                break
            continue
        B, w = Bn, wn
        path.append((B, w))
        if stop_re is not None and mp.re(w) < stop_re:
            break
        # gentle step growth
        step = min(step * mp.mpf("1.5"), mp.mpf(dB))
    print(f"  track {label} m={m} n={n}: {len(path)} points, last B={mp.nstr(B, 8)} "
          f"omega={mp.nstr(w, 10)}", flush=True)
    return path


def approach_exponent(path, npts=12):
    """Fit Re(omega) ~ a (B_c - B)^p on the last npts points, with B_c
    fitted; returns (p, B_c, Bc_linear_extrap). Uses a 3-parameter
    Levenberg-free approach: grid over B_c beyond the last B, best
    log-log linearity."""
    pts = path[-npts:]
    Bs = [float(b) for b, _ in pts]
    Rs = [float(mp.re(w)) for _, w in pts]
    # linear extrapolation of Re to zero from the last two points
    (b1, r1), (b2, r2) = (Bs[-2], Rs[-2]), (Bs[-1], Rs[-1])
    Bc_lin = b2 - r2 * (b2 - b1) / (r2 - r1) if r2 != r1 else None
    best = None
    import math
    Bmax = Bs[-1]
    span = max(abs(Bs[-1] - Bs[0]), 1e-6)
    for k in range(1, 400):
        Bc = Bmax + span * k / 400.0
        xs = [math.log(Bc - b) for b in Bs]
        ys = [math.log(abs(r)) for r in Rs]
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        sxx = sum((x - mx) ** 2 for x in xs)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        p = sxy / sxx
        resid = sum((y - my - p * (x - mx)) ** 2 for x, y in zip(xs, ys))
        if best is None or resid < best[0]:
            best = (resid, p, Bc)
    return best[1], best[2], Bc_lin


def beyond_search(m, B, w_last, radius=0.3, kmax=600):
    """Exhaustive local search for principal-sheet roots near w_last at
    rotation B, inversions 0..5, 5x5 grid of starts."""
    found = []
    for n in range(6):
        for i in range(5):
            for j in range(5):
                w0 = w_last + mp.mpc(-radius + 2 * radius * i / 4, -radius + 2 * radius * j / 4)
                w = safe_find(w0, m, B, n, kmax)
                if w is not None and abs(w - w_last) < radius:
                    if all(abs(w - f) > 1e-6 for f in found):
                        found.append(w)
    return found


# ---------------------------------------------------------------- seeds
B0_SEEDS = {1: [mp.mpc("0.406832619667", "-0.341236118126"),
                mp.mpc("0.197485919888", "-1.23279178598"),
                mp.mpc("0.0917790615406", "-2.24612961199"),
                mp.mpc("0.03497384613", "-3.259712193")]}


def seeds_for(m):
    """m = +-2 fundamentals at B = 0 from a direct search (m enters via m^2
    at B = 0, so +-2 share the spectrum; the sign of Re selects the
    branch)."""
    if abs(m) == 1:
        base = B0_SEEDS[1]
    else:
        base = []
        for w0, n in [(mp.mpc("0.9527", "-0.3507"), 0), (mp.mpc("0.75", "-1.15"), 1),
                      (mp.mpc("0.55", "-2.05"), 2), (mp.mpc("0.4", "-3.0"), 3)]:
            w = safe_find(w0, abs(m), 0.0, n, 600)
            if w is None:
                # try a wider grid
                for dr in (-0.15, 0.15, -0.3, 0.3):
                    for di in (-0.15, 0.15):
                        w = safe_find(w0 + mp.mpc(dr, di), abs(m), 0.0, n, 600)
                        if w is not None:
                            break
                    if w is not None:
                        break
            base.append(w)
        print(f"  m={m} B=0 seeds: {[mp.nstr(w, 8) if w else None for w in base]}", flush=True)
    return base


def main():
    # ---- P21.1 / P21.5: counter-rotating overtones n >= 1 first (cheap, decisive)
    for m in (-1, -2):
        base = seeds_for(m)
        RES[f"counter_m{m}"] = RES.get(f"counter_m{m}", {})
        RES[f"seeds_m{m}"] = [cplx(w) if w is not None else None for w in base]
        for n, w0 in enumerate(base):
            if w0 is None or n == 0:
                continue
            w0 = mp.mpc(abs(mp.re(w0)), mp.im(w0))  # Re > 0 member for m < 0
            path = track(m, n, w0, 0.0, 5.0, 0.01, kmax=600, label="counter")
            B_last, w_last = path[-1]
            p, Bc_fit, Bc_lin = approach_exponent(path)
            path2 = track(m, n, w_last, float(B_last), float(B_last) + 0.05, 0.002,
                          kmax=1200, min_dB=1e-6, label="counter-refine")
            B_last2, w_last2 = path2[-1]
            p2, Bc_fit2, Bc_lin2 = approach_exponent(path + path2[1:])
            beyond = {}
            for dB in (0.02, 0.1):
                Bq = (Bc_lin2 or float(B_last2)) + dB
                roots = beyond_search(m, mp.mpf(Bq), w_last2)
                beyond[str(dB)] = [cplx(r) for r in roots]
                print(f"  beyond search m={m} n={n} B={Bq:.4f}: {[mp.nstr(r, 8) for r in roots]}", flush=True)
            RES[f"counter_m{m}"][f"n{n}"] = {
                "path": [[float(b)] + cplx(w) for b, w in path + path2[1:]],
                "arrival_B_last": float(B_last2), "omega_last": cplx(w_last2),
                "approach_exponent_coarse": p, "Bc_fit_coarse": Bc_fit,
                "approach_exponent": p2, "Bc_fit": Bc_fit2, "Bc_linear_extrap": Bc_lin2,
                "beyond_principal_sheet_roots": beyond,
            }
            print(f"  m={m} n={n}: arrival B~{Bc_lin2} exponent {p2:.3f} (Bc_fit {Bc_fit2:.4f})", flush=True)
            save()

    # ---- P21.2: co-rotating branch (m > 0, Re > 0), gaps between adjacent overtones
    for m in (1, 2):
        base = seeds_for(m)
        paths = []
        for n, w0 in enumerate(base):
            if w0 is None:
                paths.append([])
                continue
            w0 = mp.mpc(abs(mp.re(w0)), mp.im(w0))
            paths.append(track(m, n, w0, 0.0, 10.0, 0.02, kmax=500, label="co"))
            save()
        gaps = {}
        for n in range(len(paths) - 1):
            pa, pb = paths[n], paths[n + 1]
            if not pa or not pb:
                continue
            rows = []
            for B, wa in pa:
                j = min(range(len(pb)), key=lambda k: abs(pb[k][0] - B))
                if abs(pb[j][0] - B) < 0.011:
                    wb = pb[j][1]
                    mu, rho = sym_invariants(wa, wb)
                    rows.append([float(B), float(abs(wa - wb)), cplx(mu), cplx(rho)])
            gmin = min(rows, key=lambda r: r[1]) if rows else None
            gaps[f"n{n}_n{n+1}"] = {"rows": rows, "min_gap": gmin}
            print(f"  co m={m} pair {n},{n+1}: min gap {gmin[1] if gmin else None} at B={gmin[0] if gmin else None}", flush=True)
        RES[f"co_m{m}"] = {"paths": [[[float(b)] + cplx(w) for b, w in p] for p in paths], "gaps": gaps}
        save()

    # ---- P21.4: counter-rotating fundamental to large B on a geometric grid (last: slowest)
    import math
    for m in (-1, -2):
        base = seeds_for(m)
        w0 = base[0]
        if w0 is None:
            continue
        w = mp.mpc(abs(mp.re(w0)), mp.im(w0))
        path = [(mp.mpf(0), w)]
        B = mp.mpf("0.05")
        while B <= 100:
            wn = safe_find(w, m, B, 0, 500)
            if wn is None or abs(wn - w) > 0.5 * abs(w) + 0.05:
                # fall back to a short fine continuation from the last point
                sub = track(m, 0, w, float(path[-1][0]), float(B), float(B - path[-1][0]) / 8, kmax=500, label="n0-fine")
                if len(sub) < 2:
                    break
                wn = sub[-1][1]
                if abs(sub[-1][0] - B) > 1e-9:
                    break
            w = wn
            path.append((B, w))
            B = B * mp.mpf("1.15")
        Bs = [float(b) for b, _ in path]
        Rs = [float(mp.re(w)) for _, w in path]
        sel = [(b, r) for b, r in zip(Bs, Rs) if b >= 10 and r > 0]
        expo = None
        if len(sel) > 3:
            xs = [math.log(b) for b, _ in sel]
            ys = [math.log(r) for _, r in sel]
            mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
            expo = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
        RES[f"counter_m{m}"]["n0"] = {"path": [[float(b)] + cplx(w) for b, w in path],
                                      "largeB_exponent_Re": expo, "last_B": Bs[-1]}
        print(f"  m={m} n=0: last B={Bs[-1]:.2f} large-B exponent of Re: {expo}", flush=True)
        save()
    RES["meta"]["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save()
    print("done", flush=True)


if __name__ == "__main__":
    main()
