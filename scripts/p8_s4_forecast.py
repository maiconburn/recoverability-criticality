"""Design-curve forecast: what CMB sensitivity is needed to detect the
Jordan log channel at nu = 1.

Anchor (measured, Planck T-only, CMB-BEST Legendre basis, this repo's
examples/qsf_nu_constraints.py): sigma(A_log) = 29.5 single-shape,
37.2 marginalized jointly with S(nu=1).

Scaling assumption, stated: for a cosmic-variance-limited bispectrum
survey the number of usable triangles grows as l_max^3 and the
sensitivity improves as sigma ~ 1/l_max (standard bispectrum scaling;
see Baumann/Komatsu reviews). Planck T-only anchor l_max = 2000.
Polarization adds a further factor reported separately below.
"""
import numpy as np

SIG_SINGLE, SIG_JOINT = 29.5, 37.2
LMAX_PLANCK = 2000.0
POL_GAIN = 2.0   # T+E vs T-only, conservative literature range 2-3

print("Detection requirement for the Jordan log channel (2 sigma):\n")
print(f"{'A_log signal':>13} | {'sigma needed':>12} | {'gain over Planck':>16} | "
      f"{'l_max (T only)':>14} | {'l_max (T+E)':>11}")
print("-" * 80)
for A in (1.0, 5.0, 10.0, 20.0, 50.0):
    need = A / 2.0
    gain_single = SIG_SINGLE / need
    gain_joint = SIG_JOINT / need
    lmax_T = LMAX_PLANCK * gain_joint
    lmax_TE = LMAX_PLANCK * gain_joint / POL_GAIN
    print(f"{A:13.0f} | {need:12.1f} | {gain_joint:15.1f}x | "
          f"{lmax_T:14.0f} | {lmax_TE:11.0f}")

print("\nReference points:")
print("  Planck T-only (measured here): sigma(A_log) = "
      f"{SIG_SINGLE:.1f} single, {SIG_JOINT:.1f} joint")
print("  CMB-S4 style survey, l_max ~ 5000 with polarization:")
g = (5000.0 / LMAX_PLANCK) * POL_GAIN
print(f"    expected gain ~ {g:.1f}x  ->  sigma(A_log) ~ {SIG_JOINT / g:.1f}")
print(f"    detectable at 2 sigma if |A_log| > {2 * SIG_JOINT / g:.1f}")
print("  Cosmic-variance-limited T+E to l_max = 10000 (optimistic ceiling):")
g2 = (10000.0 / LMAX_PLANCK) * POL_GAIN
print(f"    gain ~ {g2:.1f}x  ->  sigma(A_log) ~ {SIG_JOINT / g2:.1f}, "
      f"detects |A_log| > {2 * SIG_JOINT / g2:.1f}")
print("\nHonest reading: this is a scaling forecast anchored on a measured")
print("Planck constraint, not a full survey Fisher forecast. It says the")
print("log channel is reachable only for a strongly non-Gaussian universe")
print("(|A_log| of order 10 or larger). For |A_log| ~ 1 no planned CMB")
print("survey gets there; the observable would have to be a different one.")
