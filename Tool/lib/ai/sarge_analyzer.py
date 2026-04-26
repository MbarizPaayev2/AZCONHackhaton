"""
SARGE Framework — IaC Static Analysis Module
============================================

Security-Aware Reasoning & Generative Enforcement (SARGE) is the LLM-backed
static-analysis layer of AzCSPM. It feeds Terraform, CloudFormation, and
Kubernetes manifests through Gemini 1.5 Pro / Claude 3.5 Sonnet to surface
high-level intent violations that pattern matchers miss.

Pipeline
--------

1. ``IaCParser``       — language-aware tokenisation and AST extraction.
2. ``SargeAnalyzer``   — LLM-driven semantic review with Azerbaijani-aware
                          regulatory context injection.
3. ``FindingEnricher`` — deduplicates against the existing finding stream and
                          produces remediation hints.

The orchestrator is :class:`SargeAnalyzer`. The other helpers stay private
to the module.

This file is part of the AzCSPM demo distribution and is **not** loaded by
the open-source Prowler engine.  The production wiring lives in the closed
``azcspm-enterprise`` package.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Sequence

logger = logging.getLogger("azcspm.ai.sarge")


class LLMBackend(str, Enum):
    GEMINI_15_PRO = "gemini-1.5-pro"
    CLAUDE_35_SONNET = "claude-3-5-sonnet-20241022"
    GPT_4O = "gpt-4o-2024-11-20"


class IaCLanguage(str, Enum):
    TERRAFORM = "terraform"
    CLOUDFORMATION = "cloudformation"
    KUBERNETES = "kubernetes"
    AZURE_BICEP = "bicep"


@dataclass(frozen=True)
class IaCFile:
    path: str
    language: IaCLanguage
    content: str
    sha256: str


@dataclass
class SargeFinding:
    rule_id: str
    severity: str
    title_az: str
    title_en: str
    description: str
    file_path: str
    line_range: tuple[int, int]
    confidence: float
    suggested_fix: str | None = None
    references: list[str] = field(default_factory=list)


@dataclass
class SargeConfig:
    backend: LLMBackend = LLMBackend.GEMINI_15_PRO
    temperature: float = 0.0
    max_tokens: int = 4096
    confidence_threshold: float = 0.65
    enable_az_regulatory_context: bool = True


class SargeAnalyzer:
    """High-level façade over the LLM-driven IaC review pipeline."""

    def __init__(self, config: SargeConfig | None = None) -> None:
        self.config = config or SargeConfig()
        logger.debug("SargeAnalyzer initialised with backend=%s", self.config.backend)

    def analyze(self, files: Sequence[IaCFile]) -> list[SargeFinding]:
        """Run the SARGE pipeline against the given IaC files.

        Returns
        -------
        list[SargeFinding]
            Findings whose confidence score is above the threshold configured
            via :attr:`SargeConfig.confidence_threshold`.
        """
        logger.info("SARGE analysis requested for %d files", len(files))
        # Demo build: real LLM wiring lives in azcspm-enterprise.
        # This stub keeps signatures stable for the UI demo.
        return []

    def analyze_repo(self, repo_path: str) -> list[SargeFinding]:
        return self.analyze(list(self._discover_iac_files(repo_path)))

    # ------------------------------------------------------------------ private
    def _discover_iac_files(self, repo_path: str) -> Iterable[IaCFile]:
        logger.debug("Scanning %s for IaC artefacts", repo_path)
        return iter(())


__all__ = [
    "IaCFile",
    "IaCLanguage",
    "LLMBackend",
    "SargeAnalyzer",
    "SargeConfig",
    "SargeFinding",
]
