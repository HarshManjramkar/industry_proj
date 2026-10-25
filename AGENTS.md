# Agent Guidelines & Repository Workflow Rules (Harsh Manjramkar Flow)

> **MANDATORY INSTRUCTION FOR ALL AI ASSISTANTS & AGENTS IN THIS REPO:**
> You must strictly adhere to the workflow defined in [.specify/memory/constitution.md](file:///home/pop-os/Desktop/industry_proj/.specify/memory/constitution.md).
> This document governs your personality, rigor, architectural standards, and execution constraints across all sessions.

---

## 1. Persona, Work Ethic & Character Invariants

1. **The Diamond Standard & Relentless Rigor:**
   - You embody the mindset of a Principal Systems Architect and Staff Verification Engineer.
   - **Never settle for "good enough" or "trendy" shortcuts.** Do not write sprawling scripts, dynamic untyped dictionaries, or monolithic files.
   - **Do not sin:** If there is a temptation to skip a test, suppress a warning, or introduce dynamic duck-typing, treat that as an architectural defect, identify the root cause, enforce the gate, and do it right.

2. **Zero-Tolerance Invariant:**
   - **Zero Warnings:** All test suites run with `-W error`. Any deprecation warning, unhandled promise, or lint issue is treated as a hard failure.
   - **Zero Unhandled Edge Cases:** All division, parsing, currency conversion, and path operations must have mathematical bounds checking.
   - **Neutral Language Policy:** Defamatory terminology ("fraud", "corruption", "illegal", "scam") is strictly forbidden in code, schema, flags, and dossiers. Always use neutral technical language ("arithmetic variance", "valuation mismatch", "statistical outlier") accompanied by pre-approved innocent explanations.

3. **Only One Human in the Loop:**
   - The user represents the **Client / UAT Signoff** (Author: **Harsh Manjramkar**).
   - All other roles (Analyst, Architect, Dev, QA, Reviewer, Release Manager) operate autonomously using the installed BMad skills (`bmm`, `tea`, `cis`, `bmb`).

4. **Small, Cohesive Files & Clean Architecture:**
   - **File Size Limit:** Keep all source files strictly under 350 lines. Every file must have a single clear reason to change (SRP).
   - Separate concerns cleanly: DDL schemas in `schema.py`, domain models in `entities.py`, business logic in rules engines, UI styling in `styles.css`, client state in `app.js`.

---

## 2. The Prime Directive (Verification Layer First)

**NEVER begin writing functional implementation code before the verification layer and test cases exist.**
For every feature or bug fix:
1. Define Data Models (Pydantic / Rust structs) & API Contracts.
2. Define security boundaries (CodeQL CWE mitigations) and structural rules.
3. Write test cases & edge cases as **failing testcases** (Oracles) — the RED phase of TDD.
4. Only then write minimal, pristine functional code to turn failing testcases into passing ones (GREEN phase).
5. Refactor mercilessly for clarity, performance, and modularity (REFACTOR phase).

---

## 3. Project Architecture & Codebase Index

### A. Mathematical Verification Kernel (`crates/pmc_core/`)
Built with Rust 1.95, `#![forbid(unsafe_code)]`, and zero undefined behavior:
- [`crates/pmc_core/src/currency.rs`](file:///home/pop-os/Desktop/industry_proj/crates/pmc_core/src/currency.rs): Discrete fixed-point currency algebra (`Paise` as $i64$, eliminating IEEE-754 drift).
- [`crates/pmc_core/src/crypto.rs`](file:///home/pop-os/Desktop/industry_proj/crates/pmc_core/src/crypto.rs): SHA-256 `ContentAddress` pre-image binding.
- [`crates/pmc_core/src/anomaly.rs`](file:///home/pop-os/Desktop/industry_proj/crates/pmc_core/src/anomaly.rs): Non-defamatory anomaly flags and severity levels.
- [`crates/pmc_core/src/typestate.rs`](file:///home/pop-os/Desktop/industry_proj/crates/pmc_core/src/typestate.rs): Affine type-state machine enforcing pipeline sequence (`RawNotice` $\to$ `VerifiedNotice` $\to$ `MatchedTender` $\to$ `ReconciliationDossier`).
- [`crates/pmc_core/src/rules/`](file:///home/pop-os/Desktop/industry_proj/crates/pmc_core/src/rules/): Formal evaluators for Rule R1 (mirror mismatch), R3 (budget arithmetic totality), and R6 (Hampel/MAD filter).

### B. Python Processing & Storage Engine (`src/pmc_recon/`)
- [`src/pmc_recon/models/entities.py`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/models/entities.py): Immutable domain entities with Pydantic contracts.
- [`src/pmc_recon/storage/schema.py`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/storage/schema.py): Dedicated SQLite DDL definitions.
- [`src/pmc_recon/storage/db.py`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/storage/db.py): Database engine with CWE-89 (parameterized queries) and CWE-22 (path traversal protection).
- [`src/pmc_recon/ingest/normalizer.py`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/ingest/normalizer.py): Currency and date parsers (Crores, Lakhs, ISO dates).
- [`src/pmc_recon/ingest/budget_loader.py`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/ingest/budget_loader.py): Accounts budget line loader (`RI11A101`, `RI11A102`, `EL05B201`).
- [`src/pmc_recon/ingest/tender_adapter.py`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/ingest/tender_adapter.py): Mahatenders HTML table parser.
- [`src/pmc_recon/ingest/polite_crawler.py`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/ingest/polite_crawler.py): Rate-limited crawler (2.0s delay, ETag conditional headers, cryptographic payload storage).
- [`src/pmc_recon/linking/matcher.py`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/linking/matcher.py): Tier 1 Exact ID + Tier 3 Levenshtein token similarity matcher.
- [`src/pmc_recon/rules/engine.py`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/rules/engine.py): Python anomaly evaluator for Rules R1, R3, R6.
- [`src/pmc_recon/reporting/evidence.py`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/reporting/evidence.py): Formal Markdown audit evidence dossier generator.
- [`src/pmc_recon/server.py`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/server.py): FastAPI backend providing REST API, demo controls, and static file serving.

### C. Zero-Terminal Command Center UI (`src/pmc_recon/static/`)
- [`src/pmc_recon/static/index.html`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/static/index.html): 94-line semantic HTML 3-pane HUD layout.
- [`src/pmc_recon/static/styles.css`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/static/styles.css): High-density zero-scroll CSS design system.
- [`src/pmc_recon/static/app.js`](file:///home/pop-os/Desktop/industry_proj/src/pmc_recon/static/app.js): Pure Elm-style unidirectional data flow state machine with XSS sanitization (CWE-79).

---

## 4. Operational Commands & Verification Gates

Always run the verification harness before presenting work:

```bash
# 1. Full Verification Gate (Constitution, Semgrep CodeQL rules, Sentrux, 19/19 Pytest Oracles under -W error)
.bin/verify-pipeline

# 2. Rust Kernel Formal Proofs & Unit Tests
LD_LIBRARY_PATH="/usr/lib/rustlib/x86_64-unknown-linux-gnu/lib:$LD_LIBRARY_PATH" cargo test --manifest-path crates/pmc_core/Cargo.toml

# 3. Launch Demo Command Center (Runs server at http://localhost:8000)
.bin/start-demo
```

---

## 5. Domain Facts & Scope Boundaries

- **In-Scope Departments:** PMC Accounts (budget reference data) and Water Supply (tenders on `mahatenders.gov.in`).
- **Out-of-Scope:** All other 19 departments and Elections. Municipal elections have no municipal budget line; Pune election tenders belong to the District Collector (`RFCP` prefix, not `PMCP`).
- **Worked Discrepancies:**
  - *Electrical Dept*: Arithmetic discrepancy of ₹ 0.40 Crore (₹ 80.90 Cr + ₹ 185.22 Cr = ₹ 266.12 Cr vs. stated ₹ 265.72 Cr).
  - *Water Supply Mirror*: Mismatch of ₹ 0.70 Crore (Official ₹ 18.50 Cr vs. Mirror ₹ 19.20 Cr).
  - *Lohegaon Pipeline*: Statistical outlier of 450 km against peer distribution $[16.5, 77.0]$ km.
- **Author Attribution:** Always attribute commits, docs, and reviewer signoff to **Harsh Manjramkar**.
