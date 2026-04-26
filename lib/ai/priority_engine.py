"""
AI Priority Engine
==================

Re-ranks open findings using a small classifier that combines:

* CVSS / severity baseline,
* exploitability evidence (CISA KEV, EPSS),
* business-context tags (data sensitivity, customer-facing exposure),
* historical noise rate of the rule.

The output is a tier label — ``high`` / ``medium`` / ``low`` — that drives the
default sort order in the AzCSPM UI.

Stub implementation. Production model lives in ``azcspm-enterprise.ai``.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Sequence

logger = logging.getLogger("azcspm.ai.priority")


class PriorityTier(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class FindingFeatures:
    finding_id: str
    cvss: float
    epss: float
    exposed_to_internet: bool
    holds_pii: bool
    rule_noise_rate: float


@dataclass
class PriorityDecision:
    finding_id: str
    tier: PriorityTier
    score: float
    rationale: list[str]


class PriorityEngine:
    HIGH_THRESHOLD = 0.75
    LOW_THRESHOLD = 0.35

    def rank(self, features: Sequence[FindingFeatures]) -> list[PriorityDecision]:
        decisions = [self._score_one(f) for f in features]
        decisions.sort(key=lambda d: d.score, reverse=True)
        return decisions

    def _score_one(self, f: FindingFeatures) -> PriorityDecision:
        score = (
            0.40 * (f.cvss / 10.0)
            + 0.20 * f.epss
            + 0.15 * (1.0 if f.exposed_to_internet else 0.0)
            + 0.15 * (1.0 if f.holds_pii else 0.0)
            + 0.10 * (1.0 - f.rule_noise_rate)
        )
        score = max(0.0, min(1.0, score))
        if score >= self.HIGH_THRESHOLD:
            tier = PriorityTier.HIGH
        elif score <= self.LOW_THRESHOLD:
            tier = PriorityTier.LOW
        else:
            tier = PriorityTier.MEDIUM
        return PriorityDecision(
            finding_id=f.finding_id,
            tier=tier,
            score=round(score, 4),
            rationale=self._rationale(f),
        )

    def _rationale(self, f: FindingFeatures) -> list[str]:
        notes: list[str] = []
        if f.cvss >= 9.0:
            notes.append("Critical CVSS")
        if f.epss >= 0.5:
            notes.append("High exploitation likelihood (EPSS)")
        if f.exposed_to_internet:
            notes.append("Internet-facing asset")
        if f.holds_pii:
            notes.append("Resource holds PII")
        if f.rule_noise_rate >= 0.6:
            notes.append("Rule has historically high noise — verify manually")
        return notes


def rerank(features: Iterable[FindingFeatures]) -> list[PriorityDecision]:
    """Convenience wrapper kept for backward compatibility with v0.x callers."""
    return PriorityEngine().rank(list(features))


__all__ = [
    "FindingFeatures",
    "PriorityDecision",
    "PriorityEngine",
    "PriorityTier",
    "rerank",
]
