# TEA (Test Engineering Architect) & CIS Quality Strategy

**Author:** Murat (Master Test Architect) & CIS Innovation Suite  
**Repository Standard:** Devang Manjramkar Flow & Article V of Constitution  
**Traceability Reference:** PRD v0.1 & PDR v0.2

---

## 1. Traceability Matrix: PRD Requirements to Deterministic Oracles

| Req ID | PRD Acceptance Criteria | Verification Oracle & Test Suite | Test Type | Risk Severity |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01** | Every source has terms status recorded | `test_source_registry_terms_oracle` | Unit/Contract | Low |
| **FR-02** | Row RI11A101 loads with actuals matching PDF/XLS | `test_story_2_1_budget_loader_oracle` | Unit/Ingest | High |
| **FR-03** | Weekly run stores new, changed, and removed tenders | `test_story_2_2_mahatenders_adapter_oracle` | Integration | Critical |
| **FR-04** | Every raw payload saved with SHA-256 hash | `test_database_immutable_raw_payload_and_change_event_oracle` | Unit/Storage | Critical |
| **FR-05** | Clean values (rupee units, dates, Marathi/English) | `test_story_2_3_rupee_string_normalizer_oracle` | Unit/Math | High |
| **FR-06** | Link tenders to budget lines with confidence $\ge 0.80$ | `test_entity_linking_token_ratio_oracle` | Integration | High |
| **FR-07** | Versioning detects field-level changes | `test_tender_version_diff_generation_oracle` | Integration | High |
| **FR-08** | Comparison rules R1-R7 raise flags with evidence | `test_comparison_rules_r1_to_r7_oracle` | Unit/Oracles | Critical |
| **FR-09** | Neutral language policy (no defamatory terms) | `test_flag_neutral_language_policy_oracle` | Security/Policy | Critical |
| **FR-10** | Review decisions recorded with audit trail | `test_review_decision_feedback_oracle` | Integration | Medium |
| **FR-11** | Exportable evidence sheets generated from stored data | `test_evidence_sheet_generation_oracle` | E2E | Medium |

---

## 2. CIS Adversarial Verification Matrix (Red-Teaming the Invariants)

| Adversarial Attack Vector | Failure Hypothesis | Autonomous Defense Implementation |
| :--- | :--- | :--- |
| **Transliteration Collision** | Two different villages in Pune (e.g. "Bavdhan Budruk" vs "Bavdhan Khurd") get collapsed into identical entity tokens. | Composite key gating: fuzzy token matcher requires district/zone context before linking. |
| **Denomination Confusion** | Tender values published in lakhs mixed with budget values in crores causing a 100x false discrepancy alarm. | Mandatory normalized base currency in integer/float INR with explicit `amount_type` checking. |
| **Mirror Timestamp Skew** | A mirror site updates 48 hours after Mahatenders, causing a false R1 mismatch flag. | Grace period window ($\tau = 48\text{ hrs}$) check before escalating R1 severity from Low to Medium. |
| **Budget Table Footnote Shift** | An amended budget changes historical actuals for closed years. | R4 (Cross-Document Actuals) specifically monitors cross-year revisions and records benign explanation "Revised estimates / differing audit cutoff". |
| **Language Smear Injection** | An LLM-generated title accidentally uses "fraud" or "corrupt official". | Pydantic runtime validator rejects the object instantiation with a hard exception before DB commit. |
