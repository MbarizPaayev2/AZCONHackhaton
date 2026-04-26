"""
RAG-based Remediation Engine
============================

Retrieval-Augmented Generation pipeline that grounds remediation suggestions
on the local Azerbaijani regulatory knowledge base (AMB instructions,
FinCERT advisories, ISO 27001:2022 control mapping).

The vector store is intentionally local (FAISS index over markdown documents
under ``data/knowledge_base/az_regulations/``) so that no customer finding
metadata leaves the customer's tenancy.

This is a stub for the AzCSPM demo; the production RAG pipeline lives in
``azcspm-enterprise.ai.rag``.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

logger = logging.getLogger("azcspm.ai.rag")

KNOWLEDGE_BASE_DIR = Path("data/knowledge_base/az_regulations")


@dataclass(frozen=True)
class RetrievedDocument:
    source: str
    snippet: str
    score: float


@dataclass
class Remediation:
    finding_id: str
    summary_az: str
    summary_en: str
    steps: list[str]
    references: list[RetrievedDocument]


class RagRemediationEngine:
    def __init__(self, knowledge_base_dir: Path = KNOWLEDGE_BASE_DIR, top_k: int = 5) -> None:
        self.knowledge_base_dir = knowledge_base_dir
        self.top_k = top_k

    def remediate(self, finding_summary: str) -> Remediation:
        """Generate a remediation grounded on retrieved regulatory documents."""
        logger.debug("RAG remediation requested for: %s", finding_summary[:80])
        return Remediation(
            finding_id="<demo>",
            summary_az="Demo məqsədli boş cavab — production pipeline mövcud deyil.",
            summary_en="Demo placeholder — production pipeline not wired in this build.",
            steps=[],
            references=[],
        )

    def retrieve(self, query: str) -> Sequence[RetrievedDocument]:
        """Retrieve top-K snippets relevant to a query."""
        return ()


__all__ = ["RagRemediationEngine", "Remediation", "RetrievedDocument"]
