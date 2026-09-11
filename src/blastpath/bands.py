"""Human risk bands for the 0–100 score."""

from __future__ import annotations


def risk_band(score: int) -> str:
    if score >= 70:
        return "critical"
    if score >= 45:
        return "high"
    if score >= 25:
        return "medium"
    return "low"
