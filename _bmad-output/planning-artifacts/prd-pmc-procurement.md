# Product Requirements Document (PRD)

## Product: PMC Procurement Reconciliation Tool (Accounts and Water Supply)
**Version:** 0.1 (Extracted from Approved Specification)  
**Related Documents:** [Preliminary Design Review (PDR) v0.2](file:///home/pop-os/Desktop/industry_proj/_bmad-output/planning-artifacts/pdr-pmc-procurement.md), [.specify/memory/constitution.md](file:///home/pop-os/Desktop/industry_proj/.specify/memory/constitution.md)

---

## 1. Overview
Pune Municipal Corporation (PMC) publishes tender and budget information across the official e-tender portal, third-party mirror sites, and annual budget documents. Nobody cross-checks these sources systematically. This product collects the records, links them, tracks changes after publication, and flags inconsistencies so that a person can investigate.

The product flags differences for review. It never states or implies wrongdoing. Every flag carries evidence and a checklist of benign/innocent explanations.

---

## 2. Goals and Non-Goals

### Goals
1. Collect PMC Water Supply tenders weekly from public sources (`mahatenders.gov.in` and public mirrors).
2. Load Accounts budget and actual figures once a year, keyed by budget head code (e.g. `RI11A101`).
3. Link tenders to Water Supply budget lines and project areas with measured confidence scores.
4. Track every change to a tender after publication with immutable historical snapshots and diff events.
5. Flag inconsistencies with evidence, severity rating, and innocent explanations.
6. Provide a dashboard and exportable evidence reports for human review.
7. Let a reviewer record a decision (`confirmed`, `explained`, `false_positive`) on each flag.

### Non-Goals
1. Covering the other 19 PMC portal departments during initial prototype.
2. Bypassing captchas or unauthorized login portals.
3. Naming contractors, officials, or departments as suspects or implying fraud/corruption.
4. Real-time streaming monitoring (system is batch-oriented / weekly).
5. Fuel and vehicle analysis (deferred as a stretch target).
6. Black-box ML models requiring labeled fraud datasets.

---

## 3. Why These Two Departments
- **Accounts:** Gives reference numbers: budget, actuals, income, and expenditure with stable budget head codes (e.g., `RI11A101`).
- **Water Supply:** Full end-to-end story: 2026-27 budget shows ₹2,077.43 crore (₹802.78 cr capital + ₹1,274.65 cr revenue), 141 zones, 368 DMAs, and project status per village. Active tenders appear on mahatenders and public mirrors.
- *(Election department rejected: collector-managed RFCP IDs, no PMC budget line).*

---

## 4. Users & Needs
- **Analyst or Researcher:** Spot discrepancies between tenders and budget provisions with explainable lineage.
- **Journalist or Civic Watcher:** Obtain evidence-backed, neutrally worded inconsistency flags.
- **Project Team & Guide:** Demonstrate an explainable, verifiable prototype.

---

## 5. Functional Requirements (FRs)

| ID | Requirement | Acceptance Check | Priority |
| :--- | :--- | :--- | :--- |
| **FR-01** | Maintain a source registry (URL, access method, terms status, crawl frequency) | Every source has a terms status recorded before crawling | Must |
| **FR-02** | Load budget files (XLS first, PDF fallback) into budget lines keyed by budget head code | Row `RI11A101` loads with yearly actuals matching source | Must |
| **FR-03** | Collect Water Supply tenders weekly from allowed sources | Weekly run stores new, changed, and removed tenders | Must |
| **FR-04** | Save every raw payload with timestamp and content SHA-256 hash | Past runs can be completely replayed from stored raw files | Must |
| **FR-05** | Clean and standardise values (ISO dates, rupee units like lakh/crore, Marathi/English names) | Unit conversions and transliterated name normalization pass test cases | Must |
| **FR-06** | Link tenders to budget lines and project areas with confidence scores | Match quality verified against labeled test fixtures | Must |
| **FR-07** | Keep full history of each tender version and detect field changes | Changed value or deadline appears as a typed `change_event` | Must |
| **FR-08** | Run comparison rules (R1 to R7) and raise flags | Deterministic discrepancy rules produce flags with evidence | Must |
| **FR-09** | Display flags with neutral wording, evidence, severity, and benign explanations | Zero use of words "fraud" or "corruption" | Must |
| **FR-10** | Record reviewer decisions (`confirmed`, `explained`, `false_positive`) | Review decisions are stored with audit trail and fed back into thresholds | Should |
| **FR-11** | Provide dashboard and exportable reports (HTML/CSV/evidence sheet) | Weekly digest and per-flag evidence sheets generated from stored data | Should |

---

## 6. Comparison Rules (R1 to R7)

1. **R1: Mirror Mismatch:** Same tender on official portal vs mirror differs in value, dates, or status. (*Innocent: mirror lag, derived EMD value, rounding*).
2. **R2: Post-Publication Change:** Tender versions over weeks change value, scope, or deadline. (*Innocent: official corrigendum, typo fix*).
3. **R3: Budget Arithmetic:** Components against totals inside budget files do not add up. (*Innocent: typing slip, extraction error, rounding*).
4. **R4: Cross-Document Actuals:** Same budget head and year across two documents differ in amount. (*Innocent: revised figures, different cutoff date*).
5. **R5: Status Against Tender:** Project status "work started" has no matching tender, or "proposed" already has awarded tender. (*Innocent: work awarded earlier year, naming differences*).
6. **R6: Outlier Value:** Tender value or dimension far outside peer group range. (*Innocent: large geographic area, unit slip*).
7. **R7: Tender Against Budget:** Tendered total for an area/year exceeds budget provision. (*Innocent: multi-year work, separate funding head*).

---

## 7. Non-Functional Invariants
- **Politeness:** Obey robots.txt, 1 req / 2s rate limit, never bypass captchas.
- **Traceability & Lineage:** Every flag traces back to raw documents, run IDs, and rule versions.
- **Strict Neutrality:** Only neutral language ("inconsistency", "requires review").
- **Verification Layer First:** In accordance with repository constitution, all data models, API contracts, Semgrep rules, and failing test oracles are committed before implementation.
