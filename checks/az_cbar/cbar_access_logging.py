"""
AMB / CBAR — Access Logging
============================

Bank IT sistemlərinə bütün giriş əməliyyatlarının audit jurnalında qeyd
olunmasını yoxlayır.

Mənbə: Azərbaycan Mərkəzi Bankı (CBAR / AMB), Bənd 4.5.3.

Status: AzCSPM demo build (stub).
"""

from __future__ import annotations

CHECK_ID = "cbar_access_logging"
SEVERITY = "high"
FRAMEWORKS = ["AMB-IT-Sec-2024", "AZ-Data-Sovereignty", "ISO27001-2022", "PCI-DSS-4.0"]


class CbarAccessLoggingCheck:
    """AMB-2024 4.5.3 — giriş jurnalı məcburi aktiv olmalıdır."""

    id = CHECK_ID
    title_az = "Bank sistemlərinə girişlərin jurnalı aktiv olmalıdır"
    title_en = "Access logging must be enabled for banking systems"

    REQUIRED_LOG_FIELDS = (
        "timestamp",
        "principal",
        "source_ip",
        "action",
        "resource",
        "result",
    )

    def execute(self, context):
        return []


__all__ = ["CbarAccessLoggingCheck", "CHECK_ID", "FRAMEWORKS", "SEVERITY"]
