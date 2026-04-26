"""
AMB / CBAR — MFA for Privileged Accounts
=========================================

Bank IT sistemlərində imtiyazlı (admin, root, DBA və s.) hesabların çoxfaktorlu
autentifikasiya (MFA) ilə qorunduğunu yoxlayır.

Mənbə: Azərbaycan Mərkəzi Bankı, Bənd 5.1.4.

Status: AzCSPM demo build (stub).
"""

from __future__ import annotations

CHECK_ID = "cbar_mfa_privileged"
SEVERITY = "critical"
FRAMEWORKS = ["AMB-IT-Sec-2024", "AZ-Data-Sovereignty", "ISO27001-2022", "NIST-CSF-2.0"]
PRIVILEGED_ROLE_PATTERNS = (
    r"(?i)admin",
    r"(?i)root",
    r"(?i)owner",
    r"(?i)dba",
    r"(?i)power.*user",
)


class CbarMfaPrivilegedCheck:
    """AMB-2024 5.1.4 — imtiyazlı hesablar üçün MFA məcburidir."""

    id = CHECK_ID
    title_az = "İmtiyazlı hesablar üçün MFA aktiv olmalıdır"
    title_en = "MFA must be enforced for privileged accounts"

    def execute(self, context):
        return []


__all__ = [
    "CbarMfaPrivilegedCheck",
    "CHECK_ID",
    "FRAMEWORKS",
    "PRIVILEGED_ROLE_PATTERNS",
    "SEVERITY",
]
