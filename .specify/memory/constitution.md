# Repo Constitution & Development Process (Devang Manjramkar Flow)

> [!IMPORTANT]
> This Constitution is the binding, inviolable law for all agents working in this repository.
> The architecture and development lifecycle strictly follow the Devang Manjramkar SDLC Flow.
> **Only one human is in the loop (Client / UAT Signoff)**. All other engineering, architectural, testing, and operational roles are performed autonomously by BMad agents adhering to this document.

---

## The Prime Directive: Verification-First / TDD Oracle Precedence
**No functional implementation code shall ever be written before or without its verification layer and failing test cases.**
1. **Verification Layer First:** As soon as requirements analysis is completed, the **Verification Layer MUST be built prior to writing implementation code**, or at a minimum constructed strictly in parallel before any logic is committed.
2. **Pre-seeded Failing Testcases:** All test cases and edge cases must be mapped and written as **failing oracles** beforehand. Code generation only proceeds to turn failing testcases into passing tests.
3. **Continuous Enforcement:** Writing implementation code blindly without an active contract, schema, or test oracle is a direct violation of this Constitution.

---

## The 8-Stage Lifecycle Architecture

```
[ Client Req ] (Human)
      │
      ▼
[ Multi-Round Requirement Analysis ] (BMad Spec Agent)
      │
      ▼
[ Verification Layer Creation ] (BMad Verification Agent) ◄───┐ Feedback Loop
      │                                                       │
      ▼                                                       │
[ AI Code Generation ] (BMad Dev Agent)                       │
      │                                                       │
      ▼                                                       │
[ Proof and Feedback ] (Automated Oracles & QA Agent) ────────┴─── (System Feedback)
      │
      ▼
[ Review ] (BMad Reviewer Agent)
      │
      ▼
[ UAT Signoff ] (Human)
      │
      ▼
[ Final Build and Deploy ] (BMad Release Orchestrator)
```

---

## Detailed Specifications Per Stage

### Stage 1: Client Requirement
- **Actor:** Human User (Single human in the loop).
- **Description:** Entry point for new features, ideas, or changes.

### Stage 2: Multi-Round Requirement Analysis
- **Actor:** BMad Spec Agent (`bmad-prd`, `bmad-spec`, `bmad-advanced-elicitation`).
- **Deliverables:**
  - Primary Spec Document: PRD (Product Requirements Document) & SRS (Software Requirements Specification).
  - Explicit business constraints, acceptance criteria, and edge-case boundaries.

### Stage 3: Verification Layer Creation (MANDATORY BEFORE CODE)
- **Actor:** BMad Verification Agent (Architect / QA).
- **Core Pillars (Sticky Note 1):**
  1. **Data Models:** Strict schema definitions (e.g., Zod, OpenAPI, Pydantic, protobuf) for all entity structures.
  2. **API Contracts & Core Interfaces:** Explicit boundary definitions, request/response models, and error interfaces.
  3. **Security Boundaries & Permissions:** Role-based checks, authentication contracts, and input sanitization boundaries.
  4. **Strict Structural Rules:** SOLID principles, Clean Architecture rules, strict function naming conventions, modularity boundaries, and code style.
  5. **Test Cases & Edge Cases Mapped:** Every requirement mapped to deterministic test suites and edge scenarios.
- **Oracle Mapping:** All artifacts are mapped to deterministic oracles:
  - Linters & Compilers (type-checkers).
  - Failing test cases (pre-seeded before implementation).
  - Semgrep AST static analysis rules.
  - Sentrux structural dependency & modularity rules.

### Stage 4: AI Code Generation
- **Actor:** BMad Dev Agent (`bmad-build`, Amelia).
- **Core Execution Rules (Sticky Note 2):**
  1. **Sub-Task Isolation & Story Snacking:** Epics and features must be decomposed into small, isolated, atomic stories.
  2. **Context Grounding:** Each feature gets its own story file with all needed context, contracts, and schema references linked directly within it.
  3. **Developer-Guided Refinement:** Work through the verification layer, spec, and code with failing test cases added beforehand.
  4. **Feature-Level Verification Contracts:** Every isolated feature operates under its own verification contract in addition to global repository verification gates.

### Stage 5: Proof and Feedback
- **Actor:** Automated Oracle Engines + BMad QA Agent (`bmad-qa-generate-e2e-tests`).
- **Core Pillars (Sticky Note 3):**
  1. **Automated Regression & Integration Testing:** Full test execution ensuring new code does not break existing modules.
  2. **Independent E2E Testing:** End-to-end testing of the entire system as a cohesive unit (not isolated feature-level checks only).
  3. **Adversarial Verification:** Deliberate stress testing against unexpected inputs, boundary edge cases, malformed payloads, and security stress limits.
- **Broad System Feedback Loop:** If any test, Semgrep rule, or Sentrux metric fails, broad system feedback is fed back into **AI Code Generation** (Stage 4) or **Verification Layer** (Stage 3) for self-correction.

### Stage 6: Review
- **Actor:** BMad Code Review Agent (`bmad-code-review`, Winston / Amelia Review lenses).
- **Core Pillars (Sticky Note 4):**
  1. **Code Review:** Verification of coding standards, auth flow integrity, and security postures.
  2. **Code Smell & Discipline:** Enforcement of clean code idioms, refactoring clutter, and ensuring no unneeded complexity was added.

### Stage 7: UAT Signoff (User Acceptance Testing)
- **Actor:** Human User (Single human in the loop).
- **Description:** The human verifies the working software against their original intent. No code proceeds to release without human acceptance.

### Stage 8: Final Build and Deploy
- **Actor:** BMad Release Orchestrator.
- **Core Pillars (Sticky Note 5):**
  1. **Rollback Accommodation:** Safe deployment mechanisms and rollback plans.
  2. **Configuration Management:** Environment variable separation and secure secret storage.
  3. **Communication:** Release notes, changelog generation, and user updates.
  4. **Versioning:** Strict semantic versioning (SemVer).
  5. **Change Requests:** Tracking modifications and operational notes.
  6. **Stakeholder Signoffs & Beta Deployments:** Structured promotion paths.

---

## Tooling & Verification Oracles in This Repository
- **Verification Runner:** `.bin/verify-pipeline` executes:
  - `.bin/semgrep-runner` (AST security & rule validation)
  - `.bin/sentrux-runner` (Modularity, circular dependency prevention, God-file avoidance)
  - Pre-seeded test runners (`pytest`, `vitest`, or runner of choice)
- **Memory & Invariants:** Kept in `.specify/memory/constitution.md` and referenced across all sessions.
