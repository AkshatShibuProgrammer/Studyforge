# Master Architecture & Implementation Plan: StudyForge 0809

## 1. System Vision
StudyForge is a monolithic, zero-dependency browser-based learning platform hosted inside Gemini Canvas. It transforms documents, topics, or pasted syllabi into rich, exam-ready study notes equipped with domain-specific pedagogical containers, multi-exam PYQ intelligence, self-explanatory educational diagrams, and dual-pass verified Current Affairs.

---

## 2. End-to-End Operational Pipeline

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Screen 1    │ ──> │  Screen 2    │ ──> │  Screen 3    │ ──> │  Screen 4    │
│  Input &     │     │  Reading &   │     │  Analysis &  │     │  Parts &     │
│  Scope       │     │  Quality     │     │  Bundles     │     │  Coherence   │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
       │                                                              │
       ▼                                                              ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Screen 8    │ <── │  Screen 7    │ <── │  Screen 6    │ <── │  Screen 5    │
│  Export      │     │  Generation, │     │  Blueprint   │     │  Blueprint   │
│  (Zero-AI)   │     │  CA, Visuals │     │  Surgical    │     │  Strategy    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

---

## 3. Comprehensive 11-Phase Breakdown & Module Hierarchy

### Phase 00: Runtime Guardrails, Resilience & Canvas Bridge
*Foundational client-side execution harness ensuring zero-crash performance in Gemini Canvas.*
* **`Mod_01_Canvas_AI_Bridge`**: Ambient authorization handling, unified Gemini 3 Flash REST client, Google Search Grounding wrapper, and Imagen 4.0 predict interface.
* **`Mod_02_InBrowser_JSON_AutoRepair`**: Streaming quote/brace auto-repair engine, schema validation, and 2-attempt backoff retry logic.
* **`Mod_03_IndexedDB_Persistence_Engine`**: Decoupled `ImageDB` for Base64 visual assets and `localStorage` state schema v3.0 synchronization.

### Phase 01: Ingestion, Scope & Multi-Method Input
*Universal input layer accommodating files, syllabi, and guided AI scope expansion.*
* **`Mod_01_Multi_Format_Upload_and_OCR`**: PDF.js text extraction, Mammoth.js DOCX parsing, raw text/HTML sanitizer, and image clipboard OCR ingestion.
* **`Mod_02_Dynamic_Scope_Expansion_AI01A`**: Dynamic 10-item subtopic manager with guaranteed, essential, and optional scope proposals.
* **`Mod_03_Source_Drafting_AI01B`**: Full-content textbook-grade draft generator feeding directly into the editable textarea and skipping Screen 2.

### Phase 02: Reading, Extraction & Quality Assessment
*Document parsing integrity and automated structural recovery.*
* **`Mod_01_Extraction_and_Page_Mapping`**: Page-by-page text slicing, heading hierarchy inference, and segment ID assignment.
* **`Mod_02_Quality_Heuristics_Diagnostics`**: Non-printable ratio scoring, unicode replacement tracking, and empty-page boundary detection.
* **`Mod_03_AI_Cleanup_and_Restructure_AI02A_B`**: Automated failover to `AI-02A` (noise repair) and `AI-02B` (structural recovery) for damaged inputs.

### Phase 03: Content Understanding, Deep Extraction & Feature Bundles
*Structural content intelligence and dynamic domain capability routing.*
* **`Mod_01_Subject_and_Signal_Detection_AI03A`**: Domain classification (Economics, Polity, History, Science, etc.) and 12-signal evidence mapping.
* **`Mod_02_Deep_Core_Extraction_AI03B`**: Granular entity extraction with stable IDs (`T-`, `D-`, `F-`, `PYQ-`, `CMP-`, `TL-`, `TB-`).
* **`Mod_03_Smart_Bundle_Router_AI03C_D`**: 3-tier deterministic feature bundle routing (Auto-on, Suggested, Not detected) with force-enable overrides.
* **`Mod_04_Manual_Analysis_Correction_Editor`**: Interactive modal for manual signal/entity editing with automated downstream stale-state invalidation.

### Phase 04: Pedagogical Part Splitting & Structure
*Curricular decomposition adhering to strict learning guardrails.*
* **`Mod_01_AI_Part_Splitting_AI04`**: Document density calculation, page-count guardrails, out-of-range warnings, and orphan topic prevention.
* **`Mod_02_Part_Operations_Manager`**: Up/Down reordering, part merging with combined references, and add/remove part controls.

### Phase 05: Pedagogical Blueprint Strategy
*Per-part instructional design and planning.*
* **`Mod_01_Five_Section_Blueprint_AI05`**: Generation of Headings, Text Plan, Image Plan, Dual-Window CA Plan, and Validation Plan.
* **`Mod_02_Staggered_Job_Queue_Engine`**: Sequential queue with individual status badges, progress tracking, and master approval controls.

### Phase 06: Surgical Blueprint Refinement & Assistant Chat
*Precise, non-destructive editing of instructional plans.*
* **`Mod_01_Surgical_AI_Chat_AI06A`**: Intent recognition, atomic JSON patch operations (`add`, `replace`, `remove`), and full undo payload tracking.
* **`Mod_02_Targeted_Section_Regeneration_AI06B`**: Isolated regeneration of single blueprint sections while locking completed sections.

### Phase 07: Master Note Synthesis, Current Affairs & Visual Explanations
*The core content generation engine.*
* **`Mod_01_Dynamic_DualPass_CA_Engine`**: Pass 1 pre-generation parallel grounded research swarm covering 2020–2023 background and 2024–present developments.
* **`Mod_02_Master_Note_Writer_AI07A`**: Context-sliced synthesis injecting canonical subject strategies (`STRAT-ECO`, `STRAT-POL`, `STRAT-HIS`, `STRAT-SCI`, `STRAT-MP`).
* **`Mod_03_Self_Explanatory_Visuals_AI07B_C`**: Imagen 4.0 vector stenciling paired with mandatory component maps, lifecycle walkthroughs, and exam takeaways.
* **`Mod_04_Pedagogical_22_Container_Renderer`**: LaTeX formula derivation boxes, story/analogy cards, misconception clarifiers, and comparison matrices.
* **`Mod_05_Surgical_Refinement_Diff_AI07G`**: Targeted in-line note revision with visual `<del>` and `<ins>` diffs and selective application.

### Phase 08: Multi-Exam PYQ Intelligence Layer
*Targeted competitive exam analysis and model solutions.*
* **`Mod_01_Exam_Focus_Selector`**: Configurable exam targets (MPPSC/MP Exams, UPSC CSE, UPPSC, BPSC, State PSCs).
* **`Mod_02_PYQ_Trend_and_Official_Solution_Map`**: Historical 5-10 year question frequency, marking patterns, and model answer breakdowns.
* **`Mod_03_Examiner_Traps_and_Trap_Warnings`**: Common candidate mistakes, confusing alternatives, and key elimination rules.

### Phase 09: Two-Layer Validation & Verification Subagent
*Autonomous quality assurance and fact verification.*
* **`Mod_01_Per_Part_Actionable_Validator_AI07H`**: Actionable suggestion cards (apply text revision, add container, fetch CA, or ignore) with `AI-07K` visual adapter.
* **`Mod_02_Validator_Subagent_CA_Review_Pass2`**: Pass 2 verification scanning for dated figures, checking citation integrity, and injecting live updates.
* **`Mod_03_Consolidated_Document_Validator_AI07I`**: Cross-part coherence review and dynamic part addition suggestions.

### Phase 10: Deterministic Export & Monolithic Packaging
*Final compilation and delivery.*
* **`Mod_01_Approved_Content_Compiler_Zero_AI`**: Pure client-side compilation filtering out unapproved parts and blueprint metadata.
* **`Mod_02_Multi_Format_Exporter`**: Clean Markdown export, standalone HTML download, and browser Print/PDF formatting.
* **`Mod_03_Canvas_Single_File_Assembler`**: Unified single-file build script merging all modules into the production `sindhuskeleton.html`.

### Phase 11: In-Canvas Live Diagnostics, Automated E2E Testing & Benchmarks
*Production telemetry, verification, and competitive exam grading.*
* **`Mod_01_InCanvas_Live_Diagnostic_Console`**: Collapsible drawer for live telemetry, token budgets, and repair audits.
* **`Mod_02_Automated_E2E_Browser_Test_Harness`**: Automated in-browser test runner simulating full user workflows.
* **`Mod_03_Multi_Domain_Exam_Benchmark_Suite`**: Evaluation rubrics and synthetic test datasets ensuring >95% exam quality.

---

## 4. Phase Execution & Dependency Matrix

| Phase | Core Dependencies | Primary Artifacts Generated |
|---|---|---|
| **Phase 00** | Canvas Runtime, Browser APIs | `API`, `Guardrails`, `ImageDB` |
| **Phase 01** | Phase 00 | Ingestion state, Canonical Source |
| **Phase 02** | Phase 01 | Page map, Quality metrics, Clean text |
| **Phase 03** | Phase 02 | `subjectSignals`, `deepAnalysis`, Bundles |
| **Phase 04** | Phase 03 | `parts` array, Guardrail validation |
| **Phase 05** | Phase 04 | `blueprints` map, CA search queries |
| **Phase 06** | Phase 05 | Patch operations, Undo history |
| **Phase 07** | Phase 05, Phase 06 | `generatedParts`, Imagen visuals, Containers |
| **Phase 08** | Phase 07 | `pyqAnalysis`, Examiner traps |
| **Phase 09** | Phase 07, Phase 08 | Validations, Pass 2 CA patches |
| **Phase 10** | Phase 09 | Final Exported Document |
| **Phase 11** | Phase 00–10 | Telemetry Drawer, E2E Test Suite, Benchmarks |

