# Speckit Master Workflow & Execution Manifest

## Project Metadata
- **Project**: StudyForge Canvas Modernization
- **Runtime**: Single-File Monolithic HTML/CSS/Vanilla JS (`sindhuskeleton.html`)
- **Target Platform**: Google Gemini Canvas
- **Git Branch**: `0809Studyforge`
- **Specification Methodology**: Speckit (Specify-Clarify-Plan-Tasks-Implement)

---

## Speckit Command Pipeline
Every phase and submodule executes through the standard 6-stage Speckit lifecycle:

1. `/speckit-constitution`
   - Defines inviolable rules: Zero backend, ambient auth, storage quota isolation, deterministic JSON repair.
   - Master Reference: [constitution.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/0809/constitution.md)
   - Status: **ENFORCED & ACTIVE**

2. `/speckit-specify`
   - Formal specification of functional behavior, user interactions, acceptance criteria, and edge cases.
   - Files: `specify.md` and `spec.md` across all 12 Phases and 36 Modules.
   - Status: **COMPLETE**

3. `/speckit-clarify`
   - Clarification of architectural constraints, ambiguous user needs, and gap resolutions.
   - Cross-Reference: [GAP_REGISTER.md](file:///f:/Code%20by%20Akshat/testgemini/studyforge/0809/GAP_REGISTER.md)
   - Status: **RESOLVED**

4. `/speckit-plan`
   - Detailed technical architecture, DOM structure, state transformations, and error handling.
   - Files: `plan.md` in every phase and module.
   - Status: **COMPLETE**

5. `/speckit-tasks`
   - Atomic, dependency-ordered implementation checklists.
   - Files: `tasks.md` in every phase and module.
   - Status: **ACTIVE EXECUTION**

6. `/speckit-implement`
   - Clean, verified integration into `sindhuskeleton.html`.
   - Current Target: Phase 00 (Integrated), Phase 01 (In Progress).

---

## Phase Execution Matrix
| Phase ID | Name | Modules | Speckit Status | Implementation Status |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 00** | Runtime Guardrails & Resilience | 3 | Complete | **INTEGRATED** |
| **Phase 01** | Ingestion & Scope Expansion | 3 | Complete | **IN PROGRESS** |
| **Phase 02** | Reading & Quality Assessment | 3 | Complete | Ready |
| **Phase 03** | Deep Understanding & Bundles | 4 | Complete | Ready |
| **Phase 04** | Parts Planning & Coherence | 2 | Complete | Ready |
| **Phase 05** | Blueprint Architecture & Strategy | 2 | Complete | Ready |
| **Phase 06** | Surgical Blueprint Detail | 2 | Complete | Ready |
| **Phase 07** | Notes, Dynamic CA & Visuals | 5 | Complete | Ready |
| **Phase 08** | Multi-Exam PYQ Intelligence | 3 | Complete | Ready |
| **Phase 09** | Two-Layer Validation Subagent | 3 | Complete | Ready |
| **Phase 10** | Deterministic Export & Assembly | 3 | Complete | Ready |
| **Phase 11** | Diagnostics & E2E Benchmarks | 3 | Complete | Ready |
