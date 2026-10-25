# 🌐 Guide: Live Government Portal Crawling & Verification Proof

**Project:** Pune Municipal Corporation (PMC) Procurement Reconciliation  
**Target Domains:** `mahatenders.gov.in`, `pmc.gov.in`, `opencity.in`  
**Focus Areas:** Accounts Budget Datasets, Water Supply Procurement, and Election Department Analysis

---

## 1. Summary of Live Government Portals Accessed

In strict accordance with **PDR Section 5 (Initial Source Scan)** and **NFR-01 (Polite Crawling)**, our crawler and discovery layer evaluated the following live portals:

| Portal URL | Department / Agency | Status / Result | Findings & Access Method |
| :--- | :--- | :--- | :--- |
| **`https://mahatenders.gov.in/nicgep/app`** | National Informatics Centre (NIC) / Govt of Maharashtra | **LIVE (HTTP 200)** | Official state e-procurement portal. Successfully crawled using `PoliteCrawler`. Active listings are public; archive search requires captcha. |
| **`https://pmc.gov.in`** | Pune Municipal Corporation Official Portal | **LIVE (HTTP 200)** | Hosts annual municipal budget presentations and administrative departmental pages. |
| **`https://opendata.punecorporation.org`** | PMC Open Data Portal (Accounts / 19 datasets) | **CAPTCHA GATED / SSL MISMATCH** | 19 Accounts datasets (10 budget, 4 income/expenditure, 5 financial statements) sit behind a captcha/purpose-download form. |
| **`https://opencity.in`** | OpenCity Urban Data Portal | **LIVE (HTTP 200)** | Mirrors digitized PMC budgets from 2016-17 to 2025-26 in open structured formats (XLS/CSV). |

---

## 2. Why Election Was Evaluated & Rejected (PDR Decision D1 & Section 3)

When evaluating government procurement data, our source discovery analyzed the **Election department** and made an evidence-based decision:

1. **No Municipal Election Budget:** The PMC Annual Budget presentation (₹2,077.43 Cr total) contains **no Election department and no municipal election budget line item**.
2. **Collector Office Jurisdiction:** On `mahatenders.gov.in`, tenders with the keyword "election" in Pune are published under the **District Collector's Office** (notice IDs prefix `RFCP`), not the Municipal Corporation (`PMCP`).
3. **Portal Content:** The PMC portal's Election section only contains historical voting turnout (2007, 2012) and ward boundary maps, with no financial procurement or expenditure transactions.
4. **Resolution:** The prototype was focused on **Accounts** (authoritative reference numbers, `RI11A101`) and **Water Supply** (active tenders + project status across 141 zones and 368 DMAs).

---

## 3. How to Demonstrate Live Government Crawling to Judges / Stakeholders

To demonstrate live crawler interaction without risking rate limits or network issues:

### Step 1: Execute the Live Polite Crawler Script
Run the polite crawler against `mahatenders.gov.in` directly from the terminal:

```bash
PYTHONPATH=src .venv/bin/python -c "
from pmc_recon.storage.db import DatabaseEngine
from pmc_recon.ingest.polite_crawler import PoliteCrawler

db = DatabaseEngine()
crawler = PoliteCrawler(raw_store=db, request_interval_sec=2.0)
print('🚀 Initiating polite crawl on mahatenders.gov.in...')
res = crawler.fetch_url('https://mahatenders.gov.in/nicgep/app?page=FrontEndLatestActiveTenders&service=page', run_id='live_demo_run')
print('✅ Crawl successful!')
print(f'• HTTP Status: {res[\"status_code\"]}')
print(f'• Document ID: {res[\"raw_doc_id\"]}')
print(f'• SHA-256 Hash: {res[\"content_hash\"]}')
"
```

### Step 2: Show the Immutable Cryptographic Proof on Disk
Show the judges that the raw server response was captured verbatim and indexed into content-addressed storage:

```bash
# View stored raw document payload
ls -lh data/raw_store/live_demo_run*
```

Verify its cryptographic SHA-256 hash in the database:
```bash
sqlite3 pmc_recon.db "SELECT doc_id, run_id, content_hash, size_bytes, fetched_at FROM raw_documents WHERE run_id = 'live_demo_run';"
```

### Step 3: Show the Politeness & Compliance Safeguards
Highlight the engineering controls that make this crawler safe for government websites:
* **Rate Limiting:** Minimum 2.0-second delay per host.
* **Header Lineage:** Identifies itself via `PMCProcurementReconciliationBot/1.0 (+research@pmc-recon.org)`.
* **Conditional Requests:** Sends `If-None-Match` (ETag) headers to honor HTTP 304 Not Modified, eliminating unnecessary server load.
* **Captcha Safety:** Complies with Section 6.2 of the PDR: never attempts to break or bypass login/captcha systems.

---

## 4. Verification Check

To confirm all crawler oracles and security AST checks are green before demonstrating:

```bash
.bin/verify-pipeline
```
*(Executes Constitution invariants, Semgrep security rules, Sentrux architecture checks, and all 14 unit test oracles).*
