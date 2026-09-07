# StudyForge — Document 7: Implementation-Plan Reconciliation & External AI Review Prompt
## Review of the Supplied Implementation-Plan Draft and Rules for Producing a Codebase-Specific Plan

> **Purpose:** The supplied implementation-plan draft contains useful phase, state, testing and delivery ideas. This document preserves those useful ideas while correcting conflicts with the canonical StudyForge architecture in Documents 1–6.

---

# 1. Review Result

The supplied plan is useful as an **implementation-plan outline**, especially for:

- phased delivery;
- single-file JavaScript module organization;
- state persistence and UI hydration;
- 4-part honest developer delivery format;
- phase sign-off criteria;
- container-rendering registry;
- testing, error, performance and risk planning;
- grounding/function mapping verification.

However, it must **not be used unchanged** because it conflicts with several decisions already locked in Documents 1–6.

---

# 2. Mandatory Corrections Before Any Developer Uses the Plan

| Supplied-plan statement | Problem | Canonical correction |
|---|---|---|
| “20 AI calls” | The final architecture has more than the older 20-call view. It includes AI-02B, AI-06B, AI-07E, AI-07K and conditional `CTX-LOC`, `CTX-PER`, `CTX-FORM`. | Use the Document 1 inventory as the source of truth: main operations AI-01A through AI-07K plus conditional context subcalls and no-AI Stage 8. |
| “AI Call #3 text cleanup” but no dedicated restructuring call in phase mapping | AI-02B is a separate fallback with different preservation/restructure contract. | Implement and test AI-02A and AI-02B separately. |
| “Text generation returns raw formatted HTML” | Raw model HTML caused quote/escaping/sanitization risk and conflicts with Documents 3–4. | AI-07A returns structured safe blocks/containers. The renderer creates approved HTML. |
| “Final validation receives complete original source” | Can exceed context and repeats source unnecessarily. | Use approved document, blueprint/coverage map, traceability/assets; source references or summaries only when needed under Document 4 context policy. |
| “Latest data / India comparisons always included in writer” | Normal AI-07A grounding is OFF; forcing current facts breaks traceability and relevance. | Current/live facts come through AI-07D and render as `WEB_SOURCED`. State/country comparisons are context-driven. |
| “All 56 gaps” | The later reconciled register contains 63 tracked requirement categories; original summary count is inconsistent. | Use Document 5 master matrix and its priority reconciliation, not a fixed old count. |
| Exact function names are assumed | Existing code/function names have not been supplied in the current workspace. | Architect/reviewer must inspect code first and use exact existing names. Do not invent wrappers or rename established calls. |
| Fixed estimates such as 6–8 weeks, 8–12k LOC, 500 MB memory | These are planning assumptions, not accepted product decisions. | Mark as estimates to be measured/approved; never promise them as requirements without codebase validation. |
| Cover page, TOC, Markdown, B&W printing | Some may be supported by old skeleton ideas but are not all locked final scope. | Include only if current product document/skeleton confirms; otherwise list as deferred proposal, not required work. |
| Browser/security features such as DOMPurify | A sensible implementation option, but external dependencies may violate single-file/offline preview constraints. | Use an allowlist/safe renderer; adopt a library only if embedded/approved and compatible with single-file constraints. |

---

# 3. Requirements That Should Be Added to the Implementation Plan

## 3.1 Phase plan must include these operations explicitly

| Phase area | Missing/understated work that must be explicit |
|---|---|
| Reading | AI-02B restructuring, unresolved-span/page-map preservation, semantic chunker/merge foundation. |
| Analysis | `KF-*` key facts, all routed `BND-*` fragments, manual-analysis fallback that does not fabricate signals. |
| Blueprint | AI-06B one-section regeneration, blueprint card approvals/master approvals, stale-state behavior. |
| Generation | `CTX-LOC`, `CTX-PER`, `CTX-FORM`; safe block renderer; AI-07E post-text image gap review; AI-07K validation image adapter. |
| CA | URL/date/publisher/fetch-time validation, CA merge-at-specific-anchor and stale validation after refresh/merge. |
| Approval | Per-suggestion Accept & Apply/Ignore, sequential Approve All, approved-part unlock/edit behavior. |
| Export | Approved-state-only compilation and include/preview controls; no hidden AI call. |
| Runtime | Prompt history, schema validation, anchor validation, cancellation, cache/versioning, diagnostics. |

## 3.2 Required plan phase gates

No phase is signed off merely because UI exists. Each must include:

1. **State path:** UI action → handler → state mutation → persistence → render.
2. **Prompt path:** correct canonical prompt → final prompt saved → model call → schema validation → state commit.
3. **Failure path:** retry/edit/skip/cancel works without destroying sibling work.
4. **Resume path:** refresh restores visible UI state, not only internal JSON.
5. **Manual walkthrough:** developer identifies real function names and element IDs.

## 3.3 State planning additions

The implementation state must include, at minimum:

```javascript
{
  schemaVersion,
  sourceVersion,
  inputProfile,
  sourceDocument: { origin, text, pageMap, chunks, diagnostics, unresolvedSegments },
  analysis: { subjectSignals, deepAnalysis, bundleAnalysis, userBundleOverrides },
  parts: [],
  blueprints: {},
  generatedParts: {},
  imageAssets: {},
  currentAffairs: {},
  approvals: {},
  jobs: {},
  promptHistory: {},
  retryHistory: {},
  cache: {},
  stale: {}
}
```

Direct DOM changes without equivalent state updates are prohibited.

---

# 4. Corrected Phase Outline

This is a planning outline, not an estimated schedule. Actual duration must be determined after reviewing the real codebase.

| Phase | Deliverable | Required AI/runtime scope | Sign-off proof |
|---:|---|---|---|
| 0 | Codebase discovery | Identify actual Gemini functions, existing state, renderer, IDs, routing, existing prompts | Function map and architecture audit before changes |
| 1 | Safe foundation | navigation, central state, persistence/UI hydration, prompt registry/history/viewer shell, safe rendering base | Refresh/forward/backward/manual state trace works |
| 2 | Input and source preparation | Upload/paste/Method 2, AI-01A/B, AI-02A/B, canonical source, page maps | All three input paths produce canonical source correctly |
| 3 | Analysis engine | AI-03A/B/C/D, semantic chunk merge, counts, tier UI, BND fragments | Toggle → state → routing evidence verified |
| 4 | Parts and blueprints | AI-04, AI-05, AI-06A/B, modal, part/bundle state, approvals | Edited part/blueprint correctly affects only dependent state |
| 5 | Core notes and safe renderer | AI-07A, CTX subcalls, containers/tags, anchor system | Part slice/definitions/formulas and safe blocks render correctly |
| 6 | Visual and CA systems | AI-07B/C/D/E/F/K, image chain, CA merge/refresh, WEB sources | All image origins share one insertion path; CA URLs validated |
| 7 | Refinement, dynamic parts and approval | AI-07G/J/H/I, remove/add, approval/validation loops | Sequential Approve All and final suggestion loop verified |
| 8 | Export, resilience and observability | no-AI export, retries, chunk stress, cache/cancel/diagnostics, safe input/output handling | Approved-only export and failure/resume tests pass |
| 9 | QA and acceptance | Full gap-register audit, browser/manual performance tests | Evidence-based final report, not self-scoring |

---

# 5. External AI Review Prompt (Corrected)

Use the following prompt only with an AI that has real access to the **current codebase and all Documents 1–6**. Replace file paths/names with actual local paths.

```markdown
# STUDYFORGE — IMPLEMENTATION PLAN REVIEW AND GENERATION TASK

## ROLE
You are a senior software architect auditing an existing single-file StudyForge application and producing a codebase-specific implementation plan.

## REQUIRED READING BEFORE YOU PLAN
Read completely:
1. StudyForge Documents 1–6 (master AI usage, dependency map, canonical prompts, runtime rules, amendments register, user-control specification).
2. The current `studyforge.html` source file and any mandatory architecture-analysis note supplied with it.

Do not assume function names, file paths, model names, state shape, DOM IDs, or existing capabilities. Inspect the actual code first.

## NON-NEGOTIABLE RULES
1. Canonical prompt text in Document 3 must be used as written. Do not rewrite it.
2. Use existing AI functions and exact names found in code. Do not invent wrappers unless the codebase has no equivalent and you explicitly mark the requirement as an architecture decision requiring lead approval.
3. Keep the application in one HTML file unless the current product constraint has been formally changed.
4. Do not invent features. Use only requirements documented in Documents 1–6 and current code evidence.
5. Do not collapse the architecture to an obsolete 20-call list. Use Document 1’s full current inventory, including AI-02B, AI-06B, AI-07E, AI-07K and conditional CTX-LOC/CTX-PER/CTX-FORM.
6. Preserve safe structured rendering: do not plan direct raw-model HTML injection.
7. Use Document 5’s reconciled gap matrix as the requirement register; do not claim a fixed gap count if entries differ.
8. Every plan item must include source document/decision/gap reference and real current-code touchpoints.

## FIRST OUTPUT: CODEBASE DISCOVERY REPORT
Before implementation phases, report:
- actual AI function names/signatures and grounding/image support;
- current state object and persistence behavior;
- navigation functions and known routing issue status;
- actual prompt constants/registry;
- existing container/rendering functions and IDs;
- which requirements are already DONE, PARTIAL, NOT DONE;
- contradictions between code and Documents 1–6.

## SECOND OUTPUT: IMPLEMENTATION PLAN
Create a phase-based plan where every phase has:
- goal and working artifact;
- actual functions/DOM IDs/state fields affected;
- AI operations and canonical prompt IDs used;
- input assembly/output schema/grounding rules;
- container work;
- stale-state and persistence impact;
- error/retry/cancel behavior;
- manual test walkthrough;
- binary sign-off criteria;
- document/gap/decision references.

Include: architecture overview, complete state schema, local persistence plan, AI integration map, container rendering plan, test plan, risk register, and cross-reference index.

## DELIVERY FORMAT
PART 1 — Codebase discovery and honest current status
PART 2 — Phase plan with function map
PART 3 — Testing/sign-off matrix
PART 4 — Honest declaration of unknowns, missing files, and assumptions

Do not use marketing language or self-score without proof.
```

---

# 6. Review Validation

This reconciliation was checked against Documents 1–6. It preserves the useful implementation-plan content but prevents unsafe/raw HTML rendering, grounding misuse, obsolete call counting, hidden assumptions about existing functions, and speculative commitments.

## End of Document 7
