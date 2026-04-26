"""
AMB / CBAR — Encryption at Rest
================================

Bank və ödəniş infrastrukturunda saxlanılan **bütün məhrəm məlumatların**
istirahət vəziyyətində kriptoqrafik müdafiəsinin yoxlanılması.

Mənbə: Azərbaycan Mərkəzi Bankı (CBAR / AMB) — "Bank IT Sistemləri üçün
İnformasiya Təhlükəsizliyi Tələbləri", Bənd 4.2.1.

Status: AzCSPM demo build — production wiring ``azcspm-enterprise.checks``
paketində mövcuddur.
"""

from __future__ import annotations

CHECK_ID = "cbar_encryption_at_rest"
SEVERITY = "high"
FRAMEWORKS = ["AMB-IT-Sec-2024", "AZ-Data-Sovereignty", "ISO27001-2022"]


class CbarEncryptionAtRestCheck:
    """AMB-2024 4.2.1 — bank məlumatlarının istirahət vəziyyətində şifrələnməsi."""

    id = CHECK_ID
    title_az = "Bank məlumatları istirahət vəziyyətində şifrələnməlidir"
    title_en = "Banking data at rest must be encrypted"

    def execute(self, context):
        """Run the check against the supplied scan context.

        Returns
        -------
        list
            Findings list. Empty in this demo build.
        """
        return []


__all__ = ["CbarEncryptionAtRestCheck", "CHECK_ID", "FRAMEWORKS", "SEVERITY"]
