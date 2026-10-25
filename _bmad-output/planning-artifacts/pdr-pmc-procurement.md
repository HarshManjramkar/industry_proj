# Preliminary Design Review (PDR) & Technical Architecture Specification

## Project: PMC Procurement Reconciliation & Cross-Source Analysis
**Version:** 0.2 (Scope: Accounts & Water Supply Tenders)  
**Status:** Approved Reference Design  

---

## 1. System Architecture & Component Mapping

```
                               ┌────────────────────────────────┐
                               │       Client / Analyst UI      │
                               │   (Streamlit / Reports / CSV)  │
                               └───────────────▲────────────────┘
                                               │
                               ┌───────────────┴────────────────┐
                               │      Flag & Review Engine      │
                               │   (Review decisions & audit)   │
                               └───────────────▲────────────────┘
                                               │
                               ┌───────────────┴────────────────┐
                               │    Consistency Analysis R1-R7  │
                               │   (Deterministic & Statistical)│
                               └───────────────▲────────────────┘
                                               │
                               ┌───────────────┴────────────────┐
                               │     Entity Linking Engine      │
                               │  (Tier 1-3 Fuzzy Matcher)      │
                               └───────────────▲────────────────┘
                                               │
                               ┌───────────────┴────────────────┐
                               │   Cleaned & Versioned Relational│
                               │   Store (PostgreSQL / SQLite)  │
                               └───────────────▲────────────────┘
                                               │
                               ┌───────────────┴────────────────┐
                               │ Processing & Validation Layer  │
                               │  (Pydantic Models & Cleaners)  │
                               └───────────────▲────────────────┘
                                               │
                               ┌───────────────┴────────────────┐
                               │ Acquisition & Raw File Store   │
                               │  (Immutable SHA-256 storage)   │
                               └───────────────▲────────────────┘
                                               │
                     ┌─────────────────────────┴─────────────────────────┐
                     │                                                   │
        ┌────────────┴────────────┐                         ┌────────────┴────────────┐
        │  Track A: Accounts ETL  │                         │  Track B: Tenders Ingest│
        │  (Budget XLS / PDF rows)│                         │  (mahatenders & mirrors)│
        └─────────────────────────┘                         └─────────────────────────┘
```

---

## 2. Core Relational Schema & Entities

1. `source`: Registered site or document portal (`source_id`, `name`, `base_url`, `owner_dept`, `access_method`, `robots_ok`, `crawl_frequency`).
2. `dataset`: Dataset or page within source (`dataset_id`, `source_id`, `title`, `url`, `format`, `update_frequency`).
3. `crawl_run`: Execution record (`run_id`, `dataset_id`, `started_at`, `finished_at`, `status`, `http_status`, `items_found`).
4. `raw_document`: Raw immutable payload (`doc_id`, `run_id`, `storage_path`, `content_hash`, `size`, `fetched_at`).
5. `record`: Logical entity key (`record_id`, `dataset_id`, `natural_key`).
6. `record_version`: Historical state (`version_id`, `record_id`, `run_id`, `valid_from`, `attributes_json`, `row_hash`).
7. `change_event`: Field-level diff (`change_id`, `record_id`, `from_version`, `to_version`, `change_type`, `changed_fields`, `detected_at`).
8. `entity_link`: Relationship between entities (`link_id`, `left_ref`, `right_ref`, `method`, `confidence`, `status`).
9. `rule`: Comparison rule definition (`rule_id`, `name`, `description`, `parameters`, `version`).
10. `flag`: Raised anomaly (`flag_id`, `rule_id`, `severity`, `evidence_json`, `created_at`, `status`).
11. `review`: Reviewer decision (`review_id`, `flag_id`, `reviewer`, `outcome`, `comment`, `reviewed_at`).

---

## 3. Technology Stack Decisions
- **Language:** Python 3.11+ / 3.12
- **Acquisition & Parsing:** Requests, BeautifulSoup4, `lxml`, pandas (`openpyxl` for Excel)
- **Validation & Schemas:** Pydantic v2 (Strict Data Models & Oracles)
- **Matching & Linking:** `rapidfuzz` (token ratio & partial ratio) + composite key normalization
- **Database:** SQLite for self-contained prototype portability, compatible with PostgreSQL DDL
- **Testing & Oracles:** `pytest` with immutable mock fixtures (no live network requests in CI)
- **Verification Gates:** Semgrep (Security/Clean Architecture) + Sentrux (Structural Modularity & Acyclicity)
