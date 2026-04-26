"""
AzInCloud — Network Exposure
=============================

AzInCloud (Gcore-əsaslı) virtual maşın və load balancer resursları üçün
ictimai (public) IP eksponensiyasının auditi: SSH/RDP portlarının açıq
olması, məhdudlaşdırılmamış 0.0.0.0/0 trafiki və s.

Status: AzInCloud demo build (stub) — provider hələ implementasiya olunmayıb.
"""

from __future__ import annotations

CHECK_ID = "azincloud_network_exposure"
SEVERITY = "high"
FRAMEWORKS = ["AZ-Data-Sovereignty", "CIS-Controls-v8"]

DANGEROUS_PORTS = (
    22,     # SSH
    3389,   # RDP
    3306,   # MySQL
    5432,   # PostgreSQL
    27017,  # MongoDB
    6379,   # Redis
    9200,   # Elasticsearch
)


class AzInCloudNetworkExposureCheck:
    """AzInCloud şəbəkə ifşası — açıq portlar, məhdudlaşdırılmamış trafik."""

    id = CHECK_ID
    title_az = "AzInCloud şəbəkə ifşası — kritik portlar açıqdır"
    title_en = "AzInCloud network exposure — critical ports open to the internet"

    def execute(self, context):
        return []


__all__ = [
    "AzInCloudNetworkExposureCheck",
    "CHECK_ID",
    "DANGEROUS_PORTS",
    "FRAMEWORKS",
    "SEVERITY",
]
