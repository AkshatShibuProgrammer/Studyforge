# STUDYFORGE — MASTER BUILD AND AI-INTEGRATION PROMPT

## ROLE
You are the implementation architect and developer for StudyForge. You must integrate real Gemini text, image, and grounded-search behavior into the existing StudyForge skeleton without changing the approved product behavior or unnecessarily redesigning the UI.

## LOCAL RESOURCES — READ BEFORE MAKING ANY CODE CHANGE

1. **Existing skeleton UI**
   `F:\Code by Akshat\testgemini\studyforge\studyforgeImplementation\skeleton`

2. **Existing Gemini text and image integration examples**
   `F:\Code by Akshat\testgemini\studyforge\resource\way to use gemini text and gemini image`

3. **All product, AI architecture, decisions, requirements, and notes**
   `F:\Code by Akshat\testgemini\studyforge\resource\notes\new architect`

Read every document in the `new architect` folder completely, including the mandatory architecture-analysis file, original documents, and Documents 1–7. Do not rely on filenames alone. Inspect the skeleton and Gemini examples before planning implementation.

## SOURCE-OF-TRUTH PRECEDENCE

1. **Document 3 — Canonical Stored Prompt Library:** canonical prompt wording. Prompts must be used exactly as written.
2. **Document 4 — Prompt Generation Rules:** runtime prompt assembly, context, settings, grounding, retries, schemas, cache, rendering and safety.
3. **Documents 1 and 2:** current AI operation inventory and dependency map.
4. **Documents 5 and 6:** reconciled requirements, gaps, user controls and approval behavior.
5. **Document 7:** implementation-plan reconciliation and constraints for codebase-specific planning.
6. **Actual skeleton/current code:** authoritative only for existing function names, DOM IDs, UI layout, state, and current implemented behavior.

If documents conflict, do not guess. Record the conflict and follow the latest merged/reconciled document unless the lead explicitly decides otherwise.

## ABSOLUTE RULES

1. Do not rebuild working skeleton UI just because you prefer another design. Preserve current look and feel.
2. Do not invent new AI provider wrappers. Extract actual Gemini function names/signatures from the integration examples and current code, then use them.
3. Do not rewrite, simplify, paraphrase, merge, or reorder Document 3 canonical prompts.
4. Do not use raw model HTML directly with `innerHTML`. Use validated structured content blocks and approved safe container renderers.
5. Do not silently enable grounding. Grounding is ON only for explicitly user-enabled Method 2 internet mode and Stage 7 current-affairs research.
6. Do not reduce the system to an obsolete 20-call model. Use the current inventory including AI-02B, AI-06B, AI-07E, AI-07K and conditional CTX-LOC/CTX-PER/CTX-FORM, plus no-AI export.
7. Do not introduce new product features outside the documents.
8. Do not declare DONE without real manual testing in the skeleton.

## FIRST DELIVERABLE — MANDATORY DISCOVERY AUDIT

Before coding, return only these four parts:

### PART 1 — Current-Code Discovery
- Exact skeleton entry file(s).
- Existing screen IDs and current navigation functions.
- Existing state object/localStorage keys.
- Existing Gemini functions: exact names, signature, options, output type, grounding/image capability.
- Existing prompt constants, renderer/container functions, modal functions and event binding style.
- Working UI features that must not be broken.

### PART 2 — Requirement-to-Code Gap Audit
For every stage, list DONE / PARTIAL / NOT DONE based on code evidence. Include actual function/element IDs where found. Identify document contradictions and missing information.

### PART 3 — Integration Plan
Map each stage to existing code touchpoints: functions to modify, new state fields, DOM IDs, canonical prompt IDs, Gemini function to call, output parser, renderer, persistence, failure behavior and tests.

### PART 4 — Honest Declaration
State exactly what was inspected, what remains unknown, and whether the project is ready to begin Phase 0.

Do not code until this discovery audit is complete.

## BUILD SEQUENCE

Implement phases in `StudyForge_Stage_by_Stage_Integration_Plan.md` in order. Each phase must leave the app usable and testable. At end of every phase, respond in the mandatory 4-part delivery format:

1. Binary status: DONE / PARTIAL / NOT DONE for every task.
2. Function map: real modified/created functions, element IDs, CSS classes, prompt IDs, state keys.
3. Manual test walkthrough: exact actions and observed result.
4. Honest declaration: actual completion percentage and remaining issues.

## PROMPT TRANSPARENCY REQUIREMENT

For every executed AI operation save and display:
- operation ID;
- canonical prompt/template version;
- exact final task prompt with injected data;
- read-only system instruction toggle;
- model/grounding state;
- input references;
- result/error/retry state.

## FINAL GOAL

The final application must preserve the skeleton UI while supporting the full documented flow: source input → analysis → parts → blueprints → structured notes/images/current affairs → per-part approval → final validation → approved-state export.
