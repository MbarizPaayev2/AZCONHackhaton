"""
G-Cloud Data Residency
=======================

Hökumət Buludu (G-Cloud) üzərində saxlanılan məlumatların **fiziki olaraq
Azərbaycan Respublikasının ərazisində** lokallaşdırıldığını yoxlayır.

Mənbə: "Şəxsi məlumatlar haqqında" Qanun, Maddə 8.2 + G-Cloud Operating
Standards, Bənd 9.

Status: AzCSPM demo build (stub).
"""

from __future__ import annotations

CHECK_ID = "gcloud_data_residency"
SEVERITY = "critical"
FRAMEWORKS = ["G-Cloud-Tier3", "AZ-Data-Sovereignty", "AZ-PDP-Law-998"]

# Azərbaycan G-Cloud-un təsdiqlənmiş regionları
ALLOWED_REGIONS = (
    "az-baku-1",
    "az-baku-2",
    "az-ganja-1",
)


class GCloudDataResidencyCheck:
    """G-Cloud — məlumatların yalnız Azərbaycan regionlarında saxlanılması."""

    id = CHECK_ID
    title_az = "Məlumatlar yalnız Azərbaycan ərazisində lokallaşdırılmalıdır"
    title_en = "Data must reside within Azerbaijani territory"

    def execute(self, context):
        return []


__all__ = [
    "ALLOWED_REGIONS",
    "CHECK_ID",
    "FRAMEWORKS",
    "GCloudDataResidencyCheck",
    "SEVERITY",
]
