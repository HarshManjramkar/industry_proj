# Epics and Stories Breakdown: PMC Procurement Reconciliation Tool

This breakdown shards the requirements from the PRD and PDR into atomic, testable user stories adhering to the **Devang Manjramkar Flow** and **Story Snacking** principles.

---

## Epic 1: Verification Oracles & Core Schema Foundation (The Bedrock)
*Goal: Establish the mandatory verification layer, data schemas, database migrations, and pipeline gates before any feature logic.*

- **Story 1.1: Data Models & API Contracts (Schemas)**
  - Define strict Pydantic schemas for `Source`, `Dataset`, `RawDocument`, `TenderRecord`, `BudgetLine`, `EntityLink`, `Flag`, and `ReviewDecision`.
  - Verification Oracle: Type check & Schema serialization tests (must pass before adapters).
- **Story 1.2: Relational Store & Immutable Raw Storage Engine**
  - Implement SQLite/PostgreSQL schema with raw payload hashing (SHA-256) and versioned snapshot tracking.
  - Verification Oracle: DB migration tests, duplicate insertion rejection, rollback verification.
- **Story 1.3: Pre-seeded Failing Test Oracles & CI Verification Gate**
  - Commit test fixtures and failing test oracles for all upcoming stories.
  - Verification Oracle: `.bin/verify-pipeline` executes Semgrep, Sentrux, and test runner.

---

## Epic 2: Data Ingestion & Standardization (Tracks A & B)
*Goal: Ingest budget lines and water supply tenders into immutable versioned records.*

- **Story 2.1: Track A — Budget Line Parsing & Loader**
  - Ingest budget files (Excel/XLS tables) into normalized `budget_line` entries keyed by budget head codes (e.g. `RI11A101`).
  - Acceptance: Correct extraction of actuals, estimates, and Marathi descriptions.
- **Story 2.2: Track B — Water Supply Tender Adapter & Ingest**
  - Extract tenders from mock/recorded portal and mirror payloads (mahatenders and mirror format).
  - Acceptance: Preservation of tender ID, dates, INR values (in lakh/crore), and corrigenda.
- **Story 2.3: Cleaning, Field Normalization & Transliteration Cleaner**
  - Standardize rupee units, ISO-8601 dates, Marathi/English village name mappings.
  - Acceptance: Deterministic normalizer handling spelling variations and units.
- **Story 2.4: Versioning Engine & Field Change Event Detector (FR-07)**
  - Compare consecutive weekly snapshots of tenders; generate typed `change_event` rows for altered deadlines, values, or statuses.
  - Acceptance: Accurate diff generation without overwriting historical records.

---

## Epic 3: Cross-Dataset Entity Linking Engine
*Goal: Link tenders to budget lines and mirror records with confidence scoring.*

- **Story 3.1: Tier 1 & 2 Normalization and Exact Key Matcher**
  - Match tenders across official portal and mirror sites via normalized Tender IDs.
  - Acceptance: 100% precision on normalized identifier linking.
- **Story 3.2: Tier 3 Fuzzy Entity Linker (Tenders to Budget Heads & Villages)**
  - Match tender work descriptions and village areas to budget lines and DMAs using token similarity (`rapidfuzz`).
  - Acceptance: Confidence scoring (0.0 to 1.0) with gating threshold for review queue.

---

## Epic 4: Anomaly Detection Engine (Rules R1 to R7)
*Goal: Implement deterministic and statistical comparison rules to raise evidence-backed flags.*

- **Story 4.1: Rule R1 (Mirror Mismatch) & Rule R2 (Post-Publication Change)**
  - Detect discrepancies between official portal and mirror sites, or unexpected tender alterations.
  - Acceptance: Generates neutral flags with evidence payload and benign explanations list.
- **Story 4.2: Rule R3 (Budget Arithmetic) & Rule R4 (Cross-Document Actuals)**
  - Detect component subtotal mismatches and conflicting actuals across fiscal documents.
  - Acceptance: Flags arithmetic slips (e.g., worked example ₹0.40 cr difference).
- **Story 4.3: Rule R5 (Status vs Tender) & Rule R7 (Tender Against Budget Provision)**
  - Compare physical work status against awarded tenders, and compare total tenders against area budget provisions.
  - Acceptance: Proper severity assignment (Low/Medium/High) without defamatory terms.

---

## Epic 5: Review Workflow, Dashboard & Exportable Reports
*Goal: Provide the single human in the loop with an interactive review tool and evidence exports.*

- **Story 5.1: Review Decision Audit Engine (FR-10)**
  - Allow the reviewer to record decisions (`confirmed`, `explained`, `false_positive`) with notes.
  - Acceptance: Audit log recorded; decisions feed back into rule tuning.
- **Story 5.2: Exportable Evidence Sheets & Weekly Digest Generator (FR-11, FR-14)**
  - Generate standalone HTML/Markdown/CSV evidence sheets per flag and weekly summaries with neutral language.
  - Acceptance: Complete evidence provenance tracing back to raw document hashes.
- **Story 5.3: Streamlit Interactive Demonstration Dashboard (FR-13)**
  - Interactive UI for browsing sources, runs, diffs, linked records, and reviewing the flag queue.
  - Acceptance: Clean, runnable web interface for the human UAT signoff.
