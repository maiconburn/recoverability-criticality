"""Numerical validation tools for recoverability-criticality scaling."""

from .model import (
    ConstrainedPade,
    build_constrained_pade,
    chebyshev_matrix,
    exact_gb_metric,
    exact_horizon_coefficients,
    gb_normalization,
    qnm_spectrum,
)

__all__ = [
    "ConstrainedPade",
    "build_constrained_pade",
    "chebyshev_matrix",
    "exact_gb_metric",
    "exact_horizon_coefficients",
    "gb_normalization",
    "qnm_spectrum",
]

