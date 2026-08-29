"""Shooting-based mirror-EP hunt at one coupling (trusted instrument).

Purpose: decide whether the near-threshold EP band reported from collocation
scans (lambda in [~0.113, ~1/8]) survives the validated shooting solver, or is
a collocation artifact (deep-q^2 conditioning ~1e10).

Usage: shooting_ep_hunt.py LAMBDA [WALK_START] [FLOOR]
Prints the EP (q2_c, omega_c, gap) or the failure mode.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_validation  # noqa: E402
from run_validation import find_ep_global  # noqa: E402

from recoverability_ep.criticality import SpectralFamily, mirror_seed, track_pair
from recoverability_ep.model import exact_gb_metric, exact_horizon_coefficients

LAM = float(sys.argv[1])
START = float(sys.argv[2]) if len(sys.argv) > 2 else -12.0
FLOOR = float(sys.argv[3]) if len(sys.argv) > 3 else -55.0

b, bp, n_factor = exact_gb_metric(LAM)
geometry = (b, bp, exact_horizon_coefficients(LAM, 24))
family = SpectralFamily(b, bp, n_factor, collocation_order=56)
walk_seed = track_pair(family, [0.0, START], seed=mirror_seed(family))
print(f"lam={LAM}: seed at q2={START}: {walk_seed}", flush=True)

row = {"lam": LAM, "start": START, "floor": FLOOR}
try:
    q2_ep, omega_ep, gap, pair = find_ep_global(geometry, n_factor, walk_seed, floor=FLOOR)
    row.update(
        q2_ep=q2_ep,
        omega_ep=[omega_ep.real, omega_ep.imag],
        gap=gap,
        found=True,
    )
    print(f"lam={LAM}: EP q2_c={q2_ep:.9f} omega_c={omega_ep:.9f} gap={gap:.1e}", flush=True)
except RuntimeError as exc:
    row.update(found=False, error=str(exc))
    print(f"lam={LAM}: NO EP -- {exc}", flush=True)

out = pathlib.Path("results/shooting_ep_hunt.json")
data = json.loads(out.read_text()) if out.exists() else []
data.append(row)
out.write_text(json.dumps(data, indent=1))
