# Azərbaycan Tənzimləyici Bilik Bazası

Bu qovluq AzCSPM RAG mühərriki üçün **lokal bilik bazasını** saxlayır. Bütün
sənədlər markdown formatındadır və `lib/ai/rag_remediation.py` modulu tərəfindən
indeksləşdirilir (FAISS vector store).

## Mənbələr

| Sənəd | Mənbə | Versiya | Sonuncu yenilənmə |
|-------|-------|---------|-------------------|
| `amb_it_security_guidelines.md` | Azərbaycan Mərkəzi Bankı (AMB) — IT Təhlükəsizliyi üzrə Təlimat | 2024.2 | 2024-11-12 |
| `fincert_advisories_2024_2026.md` | FinCERT.AZ illik məsləhətlər toplusu | — | 2026-04-15 |
| `iso_27001_2022_az_mapping.md` | ISO/IEC 27001:2022 — Azərbaycan dilinə uyğunlaşdırılmış nəzarət xəritəsi | 2022 | 2025-08-30 |
| `personal_data_law_998.md` | "Şəxsi məlumatlar haqqında" Qanun, № 998-IIIQ | 2010 (2023 düzəlişləri ilə) | 2023-12-20 |
| `cybersec_strategy_2023_2027.md` | Milli Kibertəhlükəsizlik Strategiyası | 2023 | 2023-09-01 |
| `azintelecom_data_center_ops.md` | Azintelecom MMC — Data Mərkəzi Əməliyyatları Reqlamenti | 1.4 | 2025-03-10 |

## Yenilənmə proseduru

Bilik bazasındakı sənədlər **rüblük** olaraq Azintelecom Compliance qrupu
tərəfindən yenilənir. Pull request-lər `azcspm-enterprise/compliance` repo-sunda
nəzərdən keçirilir, yalnız təsdiqdən sonra bu repo-ya sync olunur.

## RAG indeksinin yenidən qurulması

```bash
python -m lib.ai.rag_remediation --reindex --kb-dir data/knowledge_base/az_regulations
```

> **Qeyd**: Bu CLI bu demo build-də işləmir. Production wiring
> `azcspm-enterprise` paketində mövcuddur.
