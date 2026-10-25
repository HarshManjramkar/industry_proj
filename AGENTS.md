# Agent Guidelines & Repository Workflow Rules

> **MANDATORY INSTRUCTION FOR ALL AI ASSISTANTS & AGENTS IN THIS REPO:**
> You must strictly adhere to the workflow defined in [.specify/memory/constitution.md](file:///home/pop-os/Desktop/industry_proj/.specify/memory/constitution.md).

## Core Principles to Enforce at All Times

1. **Only One Human in the Loop:**
   - The user represents the **Client / UAT Signoff**.
   - All other roles (Analyst, Architect, Dev, QA, Reviewer, Release Manager) are operated autonomously using the installed BMad skills.

2. **Verification Layer & Testcases First (The Prime Directive):**
   - **NEVER** begin writing functional implementation code before the verification layer and test cases exist.
   - For every feature:
     1. Define Data Models (Zod/OpenAPI/Pydantic schemas) & API Contracts.
     2. Define security boundaries and structural rules.
     3. Write the test cases & edge cases as **failing testcases** (Oracles).
     4. Only then write functional code to turn failing testcases into passing ones.

3. **Story Snacking & Context Grounding:**
   - Break work down into atomic sub-tasks.
   - Ground each feature in its own story file with contracts linked.

4. **Automated Verification Gates:**
   - Always run `.bin/verify-pipeline` to validate Semgrep security rules, Sentrux architectural health, and test suites before presenting work for human review.
