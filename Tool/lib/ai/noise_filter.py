"""
Noise Filter
============

Lightweight false-positive reducer that runs **after** the SARGE analyzer and
the rule engine have produced findings. It looks at:

* tag-based mute-lists (project, environment, owner team),
* statistical regression — rules that historically resolve to "won't fix",
* near-duplicate suppression across rotating ephemeral resources.

Stub — production implementation under ``azcspm-enterprise.ai.noise``.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Sequence

logger = logging.getLogger("azcspm.ai.noise")


@dataclass
class FindingRecord:
    finding_id: str
    rule_id: str
    resource_uid: str
    tags: dict[str, str] = field(default_factory=dict)


@dataclass
class FilterDecision:
    finding_id: str
    keep: bool
    reason: str


class NoiseFilter:
    DEFAULT_MUTED_TAGS = {"environment": {"sandbox", "scratch", "ephemeral"}}

    def __init__(self, muted_tags: dict[str, set[str]] | None = None) -> None:
        self.muted_tags = muted_tags or self.DEFAULT_MUTED_TAGS

    def apply(self, findings: Sequence[FindingRecord]) -> list[FilterDecision]:
        return [self._decide(f) for f in findings]

    def _decide(self, f: FindingRecord) -> FilterDecision:
        for tag_key, muted_values in self.muted_tags.items():
            if f.tags.get(tag_key, "").lower() in muted_values:
                return FilterDecision(
                    finding_id=f.finding_id,
                    keep=False,
                    reason=f"muted via tag {tag_key}={f.tags[tag_key]}",
                )
        return FilterDecision(finding_id=f.finding_id, keep=True, reason="kept")


__all__ = ["FilterDecision", "FindingRecord", "NoiseFilter"]
