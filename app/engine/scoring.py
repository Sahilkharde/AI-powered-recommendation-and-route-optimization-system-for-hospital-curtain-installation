"""
Weighted scoring engine for curtain-to-track recommendations.

Combines multiple signals into a single 0-100 confidence score:
  - Historical frequency  (how often this curtain went to this track)
  - Size match             (width compatibility)
  - Type match             (snap vs standard)
  - Style match            (rotational vs proprietary)
  - Recency                (more recent installs weigh more)
  - Capacity               (track still has room)
"""

from dataclasses import dataclass
from datetime import datetime

WEIGHTS = {
    "history":  0.35,
    "size":     0.25,
    "type":     0.15,
    "style":    0.10,
    "recency":  0.10,
    "capacity": 0.05,
}


@dataclass
class ScoringInput:
    history_count: int
    max_history: int
    size_delta: float
    size_tolerance: float
    type_match: bool
    style_match: bool
    days_since_last_install: int | None
    has_capacity: bool


def compute_score(inp: ScoringInput) -> float:
    history_score = (inp.history_count / max(inp.max_history, 1)) * 100

    if inp.size_delta <= 0:
        size_score = 100.0
    elif inp.size_delta <= inp.size_tolerance:
        size_score = max(0, 100 - (inp.size_delta / inp.size_tolerance) * 100)
    else:
        size_score = 0.0

    type_score = 100.0 if inp.type_match else 20.0
    style_score = 100.0 if inp.style_match else 30.0

    if inp.days_since_last_install is None:
        recency_score = 50.0
    elif inp.days_since_last_install <= 7:
        recency_score = 100.0
    elif inp.days_since_last_install <= 30:
        recency_score = 70.0
    elif inp.days_since_last_install <= 90:
        recency_score = 40.0
    else:
        recency_score = 10.0

    capacity_score = 100.0 if inp.has_capacity else 0.0

    total = (
        WEIGHTS["history"]  * history_score
        + WEIGHTS["size"]     * size_score
        + WEIGHTS["type"]     * type_score
        + WEIGHTS["style"]    * style_score
        + WEIGHTS["recency"]  * recency_score
        + WEIGHTS["capacity"] * capacity_score
    )

    return round(min(max(total, 0), 100), 1)


def build_reason(inp: ScoringInput, score: float) -> str:
    parts: list[str] = []

    if inp.history_count > 0:
        parts.append(f"installed here {inp.history_count} time(s) before")

    if inp.size_delta <= 0:
        parts.append("exact size match")
    elif inp.size_delta <= inp.size_tolerance:
        parts.append(f"size within {inp.size_delta:.1f}\" tolerance")

    if inp.type_match:
        parts.append("type matches")

    if inp.style_match:
        parts.append("style matches")

    if not inp.has_capacity:
        parts.append("WARNING: track at capacity")

    if not parts:
        parts.append("candidate based on availability")

    return f"Score {score}/100 — " + "; ".join(parts) + "."
