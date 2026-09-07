# STUDYFORGE — CORRECTED MASTER IMPLEMENTATION PLAN GENERATION PROMPT

## ROLE
You are a senior software architect. Produce a codebase-specific, phase-by-phase implementation plan for StudyForge, a single-HTML-file educational AI application.

## FIRST: READ THE CURRENT CODE AND ALL ARCHITECTURE DOCUMENTS

Read the actual current `studyforge.html` and the mandatory architecture-analysis note first. Then read the current canonical StudyForge documents in this precedence order:

1. **Document 3 — Canonical Stored Prompt Library**: exact immutable prompt text.
2. **Document 4 — Prompt Generation Rules and Runtime Implementation**: model settings, context assembly, schemas, retries, caching, safe rendering.
3. **Document 1 — Merged Master AI Usage**: current operation inventory and stage behavior.
4. **Document 2 — Merged Prompt Dependency Map**: data/control dependencies and stale-state rules.
5. **Document 5 — Missing Features and Agreed Amendments Register**: reconciled requirement/gap register and product-document changes.
6. **Document 6 — User Intervention, Approval and Prompt Transparency Specification**: user-control/UI requirements.
7. **Document 7 — Implementation Plan Reconciliation and External AI Review Prompt**: implementation-plan corrections and known conflicts.
8. Any original product/skeleton documents: background only, unless they do not conflict with the above.

## SOURCE-OF-TRUTH RULES

1. Document 3 prompt wording is canonical. Use it exactly as written. Do not rewrite, shorten, paraphrase, merge, split, or improve it.
2. The actual current codebase is authoritative only for existing function names, signatures, DOM IDs, state shape, and provider integration capabilities.
3. The architecture-analysis note must not override a later approved product requirement merely because old code does not yet implement it. Record such mismatch as a gap.
4. Documents 1–7 are the approved requirements source. Where older copies conflict, use the latest merged/reconciled document and record the conflict.
5. Do not use an obsolete “20 AI calls only” inventory. Use the full current operation inventory: AI-01A through AI-07K, conditional CTX-LOC/CTX-PER/CTX-FORM, and no-AI Stage 8 export.
6. Use existing AI functions exactly as found in code. Do not invent new provider wrappers. If the existing functions cannot support a required canonical operation, report it as an implementation gap requiring lead approval.
7. Single HTML file remains mandatory. Do not propose backend services, build tools, external JS files, or new dependencies without explicitly flagging them as out-of-scope/approval-required.
8. Do not invent features. Use only documented requirements.

## REQUIRED CODEBASE DISCOVERY REPORT BEFORE THE PLAN

Before phases, provide:

- actual AI function names, signatures, input/output formats, and grounding/image support;
- current state object, persistence, navigation, renderer, prompt registry, container renderers, DOM IDs and event handlers;
- current implementation status for every required operation: DONE / PARTIAL / NOT DONE;
- all contradictions between current code and Documents 1–7;
- all ambiguities requiring clarification.

Do not guess missing code details.

## PLAN OUTPUT

Create `IMPLEMENTATION_PLAN.md`.

The plan must include:

1. Executive summary and measurable success criteria.
2. Codebase discovery report and honest current-status table.
3. Single-file architecture and module order.
4. Complete state schema, mutation map, persistence/hydration, stale-state and cancellation behavior.
5. Canonical prompt library appendix: include each Document 3 canonical prompt **once**, verbatim, with ID/version. Do not duplicate the full same prompt inside every phase.
6. Full AI integration table for all current operations, including CTX calls, grounding, existing code function used, input assembly, schema validation, output state and failure path.
7. Phase-based implementation plan. Every phase must identify exact code functions/DOM IDs/state fields affected, canonical prompt IDs, requirement sources, tests and sign-off evidence.
8. Safe rendering/container plan for all documented containers.
9. Dynamic image insertion, grounded CA, refinement, add/remove part, approval and two-layer validation implementation plans.
10. Retry/schema/anchor/token/chunk/cache/diagnostic rules from Document 4.
11. Testing plan: unit-like manual checks, end-to-end flows, resume, failure, large-source, browser and gap-register audit.
12. Risk register with only evidence-based risks.
13. Developer delivery template: binary status, function map, manual walkthrough, honest declaration.
14. Cross-reference index mapping every requirement register item to phase, screen, AI operation and implementation point.
15. Ambiguities Requiring Clarification section. Never solve an ambiguity by inventing a requirement.

## PROMPT-INCLUSION RULE

- Include every canonical prompt verbatim exactly once in the canonical library appendix.
- In phase sections, reference prompt IDs and versions only, for example `AI-07A / partWriterPrompt / Document 3 v1`.
- Do not repeat full prompt bodies in every phase; that creates inconsistent duplicate copies and makes future maintenance unsafe.

## PHASE RULES

Every phase must deliver a working, testable artifact and include:

- goal;
- prerequisites;
- affected screens;
- exact current-code functions/DOM IDs/state fields;
- AI operations and canonical prompt IDs;
- requirement references;
- data/prompt/output path;
- error/retry/cancel path;
- persistence/stale-state impact;
- container work;
- at least 10 tests where scope supports it;
- binary sign-off criteria;
- developer 4-part delivery format.

## FINAL VALIDATION BEFORE DELIVERY

Verify:

- Every current AI operation from Document 1 is assigned to a phase.
- Every reconciled item in Document 5 is mapped; do not rely on an obsolete fixed count.
- All 8 screens and every documented user-control point in Document 6 are covered.
- Every canonical prompt is included once, unchanged.
- Existing AI function names are taken from actual code, not assumed.
- No raw model HTML is directly injected; structured safe rendering is planned.
- Grounding is limited to user-enabled Method 2 search and AI-07D CA, as specified.
- Stage 8 has no AI call.
- Contradictions/unknowns are disclosed.

Do not use marketing language or unsupported estimates. Deliver a complete, evidence-based plan.
