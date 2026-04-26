"""
AzInCloud — IAM Access Review
==============================

AzInCloud tenancy-də IAM hesabları və icazə siyasətlərinin auditi:
yetersiz minimum-imtiyaz prinsipi, istifadə olunmayan API açarları,
həddən artıq geniş icazələr.

Status: AzInCloud demo build (stub) — provider hələ implementasiya olunmayıb.
"""

from __future__ import annotations

CHECK_ID = "azincloud_iam_review"
SEVERITY = "high"
FRAMEWORKS = ["AZ-Data-Sovereignty", "CIS-Controls-v8", "ISO27001-2022"]

REVIEW_RULES = {
    "max_unused_days": 90,
    "require_mfa_for_admin": True,
    "deny_wildcard_actions": True,
    "max_inline_policy_actions": 50,
    "require_session_duration_max_hours": 12,
}


class AzInCloudIamReviewCheck:
    """AzInCloud IAM icazə yoxlaması — minimum imtiyaz prinsipinə uyğunluq."""

    id = CHECK_ID
    title_az = "AzInCloud IAM icazələri — minimum imtiyaz prinsipi"
    title_en = "AzInCloud IAM permissions — least-privilege review"

    def execute(self, context):
        return []


__all__ = [
    "AzInCloudIamReviewCheck",
    "CHECK_ID",
    "FRAMEWORKS",
    "REVIEW_RULES",
    "SEVERITY",
]
