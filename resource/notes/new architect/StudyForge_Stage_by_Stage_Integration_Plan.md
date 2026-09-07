# StudyForge — Stage-by-Stage AI Integration Plan
## Build Real AI Into the Existing Skeleton Without Losing UI, State, Traceability, or User Control

> This is the implementation order. It is intentionally stage-based. Do not jump to later generation features before upstream state, prompts and safe rendering work.

---

# Stage 0 — Discovery, Skeleton Audit and Integration Contract

## Goal
Understand what exists before changing it.

## Read and inspect

- Entire skeleton folder.
- Gemini text/image examples.
- All notes/new architect documents.
- Current entry HTML, scripts, CSS, localStorage behavior, navigation, modal helpers, rendering, event bindings, prompt placeholders.

## Required output before code

| Audit item | Required evidence |
|---|---|
| Skeleton entry file | Actual path/name |
| 8 screens | Actual section IDs and whether Screen 6 is overlay |
| Navigation | Actual forward/back/sidebar function names and current bugs |
| State | Current object shape and storage key(s) |
| Gemini | Exact text/image/grounding function names, signature, return types |
| Prompts | Existing constants/objects and how currently assembled |
| Rendering | Existing HTML/container renderers and unsafe `innerHTML` locations |
| UI preservation | Screens/styles/components that must remain unchanged |

## Sign-off
No implementation begins until the audit identifies real function names and a requirement-to-code gap table.

---

# Stage 1 — Foundation: Central State, Navigation, Persistence, Prompt History and Safe Rendering Base

## Goal
Make the skeleton reliably move through its screens, save/resume visible state, and support auditable AI operations before any real AI request is added.

## Implement

- Central state source of truth and state mutation functions.
- `navigate()` for valid forward progression and `navTo()` for completed/back navigation, using actual code names if different.
- Schema-versioned persistence.
- Resume/hydration for all visible Screen 1 fields, dynamic subtopics, settings, current screen and later state.
- Prompt execution record structure and generic View Prompt modal.
- Safe text/HTML/container/anchor validation foundation.
- Job status model: queued/running/retry_wait/succeeded/failed/skipped/canceled/stale.

## Required tests

- Fresh flow starts at Screen 1.
- Valid forward navigation reaches each skeleton screen.
- Sidebar/back navigation cannot bypass prerequisites.
- Refresh on every screen restores visible controls, not merely JSON.
- Prompt modal can render quote/HTML-like text safely.
- Reset clears state and UI.

## Do not implement yet
Real content AI calls, dummy replacement, images, CA, validation.

---

# Stage 2 — Stage 1 Input and Stage 2 Source Preparation

## Goal
Make all three input paths create one canonical source document.

## AI operations

- AI-01A: sub-topic expansion.
- AI-01B: AI draft source material.
- AI-02A: extraction cleanup fallback.
- AI-02B: extraction restructure fallback.

## Implement

### Method 1: upload
- Keep skeleton upload look/feel.
- Detect supported file type; technical extraction first.
- Preserve file metadata, page map, source diagnostics and unresolved segments.
- Add extraction method control: Auto / Technical / AI Cleanup / AI Restructure.

### Method 2: topic draft
- Dynamic sub-topic fields (up to documented limit).
- Depth default medium + comprehensive option.
- Separate Internet Search and Include CA controls.
- AI-01A scope panel: mandatory user topics, essential suggestions, optional suggestions, current topics when grounded.
- User approval/edit/custom sub-topic flow.
- AI-01B draft goes to Method 3 textarea.
- User edit before canonical source is saved.

### Method 3: paste
- Preserve as-is semantically; render safely.

### Reading behavior
- AI-drafted content skips Screen 2 after user source edit.
- Upload source falls through technical → cleanup → restructure only as needed.

## Tests

- Upload, paste and AI Draft each create canonical source.
- AI Draft source edit changes the exact content passed to Stage 3.
- Internet flag only enables grounding in AI-01A/AI-01B.
- Bad extraction triggers correct fallback without source enrichment.
- Prompt history/viewer works for all four operations.

---

# Stage 3 — Understanding, Deep Extraction, Smart Bundle Routing and Chunking

## Goal
Turn canonical source into reliable, structured analysis and user-controlled bundle selection.

## AI operations

- AI-03A: subject/signals/purpose detection.
- AI-03B: deep extraction including D-, F-, KF-, PYQ and other IDs.
- AI-03C: relevant routed BND-* bundle fragments.
- AI-03D: user force-enable bundle.

## Implement

- Semantic chunk decision at safe token threshold.
- Chunk boundaries: chapter → heading → page → paragraph group.
- Merge/dedupe structures while retaining source refs.
- Deterministic signal-to-bundle router.
- Screen 3 count row separate from bundle UI.
- Green/yellow/grey tiered bundle display with evidence hover.
- Show More, force-enable, manual subject/bundle correction and Reanalyse.
- Full extraction details view for definitions/formulas/PYQs/etc.

## Tests

- Analysis uses canonical source and page refs.
- Large source chunks and merged IDs remain stable.
- Irrelevant bundle prompts are not called.
- User force-enable invokes only chosen bundle.
- Screen 3 toggle state reaches persisted bundle state.
- No percentage confidence UI.

---

# Stage 4 — Coherent Parts and Per-Part Bundle Assignment

## Goal
Create editable, coherent part plan from analysis, without losing global/user bundle decisions.

## AI operation

- AI-04: part splitting.

## Implement

- Analysis primary input; full source only when safe, summaries otherwise.
- Page range guide as guardrail, coherence as priority.
- Formula/PYQ/example constraints.
- Per-part applied bundles from global selection only where evidence supports them.
- Screen 4 prompt viewer.
- Real Edit Settings modal: title, pages, counts, description, chips.
- Add/remove/merge/reorder parts.
- Outside-range warning.
- State invalidation rules for range/scope/bundle edits.

## Tests

- Edit modal saves/re-renders.
- Added parts preserve bundle data through Screens 5/6/7.
- Merge/remove/reorder state remains coherent.
- Forward Continue uses valid navigation function.

---

# Stage 5 — Parallel Blueprints and Screen 6 Targeted Editing

## Goal
Create one coherent editable blueprint per confirmed part.

## AI operations

- AI-05: per-part blueprint, staggered parallel.
- AI-06A: surgical blueprint chat patch.
- AI-06B: section-only regeneration.

## Implement

- One job per part with individual status/retry and approximately 1-second launch gap.
- AI-05 inputs: part slice, scoped analysis, all definitions/formulas, bundles, subject strategy.
- Render all 5 blueprint sections: headings, text, images, CA queries, validation.
- Blueprint card prompt viewer, status and bundle chips.
- Per-card and master blueprint approval controls.
- Screen 6 overlay, not a new navigation screen.
- Surgical patch/diff/undo; target section regeneration; editable CA query; per-part bundle chips.
- Stale handling after blueprint changes.

## Tests

- One failed blueprint does not reset other cards.
- Screen 6 only changes intended section.
- Undo restores exact patch.
- Image plan regeneration preserves text/CA/validation plans.
- Blueprint approval progress works.

---

# Stage 6 — Core Stage 7 Notes, Deferred Context, Safe Containers and Traceability

## Goal
Generate real source-aware notes per part and render them safely in skeleton UI.

## AI operations

- CTX-LOC, CTX-PER, CTX-FORM when relevant.
- AI-07A: structured part generation.

## Implement

- `buildPartGenerationContext()` according to Document 4.
- Source slice + scoped analysis + all definitions/formulas + blueprint + applied bundles.
- Conditional contextual enrichment, cached entity+context; CA requirement routes to AI-07D instead of hidden grounding.
- Parse/validate AI-07A JSON, stable anchors, container enum and traceability tags.
- Safe renderer for all documented containers.
- Text prompt viewer and structured source/reference metadata.
- Manual edit/unlock behavior and stale validation status.

## Tests

- Cross-part formula reference works through full formula registry.
- Source-backed blocks carry source references.
- Web facts are never incorrectly source-backed.
- Invalid container/anchor/model output cannot render unsafe HTML.
- Relevant location/person/formula context is specific rather than generic.

---

# Stage 7 — Images, Current Affairs, Refinement and Dynamic Parts

## Goal
Complete Stage 7 learning assets and user-controlled content changes.

## AI operations

- AI-07B: image prompt expansion.
- AI-07C: image generation.
- AI-07D: grounded CA.
- AI-07E: post-text image gap review.
- AI-07F: highlight-to-visualize.
- AI-07G: refinement/diff.
- AI-07J: quick new-part blueprint.
- AI-07K: validation-originated image request adapter.

## Implement

### Images
- One normalized image request object for blueprint/writer/review/validation/highlight sources.
- Validate known anchor, reserve slot, expand prompt, optional preview, generate, attach asset.
- Show Prompt, Regenerate, Edit Prompt & Regen, Different Style, Remove.
- Mixed-style composite when clear; split only when required.

### Current affairs
- Query visible/editable.
- Grounded search only through existing actual Gemini grounding function.
- Validate URL/date/publisher/fetch time.
- Merge into CA block, merge at selected safe anchor, omit, refresh.
- Use WEB_SOURCED tag only when valid source metadata exists.

### Refinement and parts
- Highlight flow uses context and returns three styles.
- Refinement returns scope and diff; apply all/selective/discard/expand scope.
- Add part modal: topic/subtopics/CA, Generate Immediately or Configure First.
- Remove part confirmation; reindex/progress/final-validation update.

## Tests

- Every image source uses same insertion chain.
- Image prompt preview setting works.
- CA cannot be silently grounded in normal writing.
- CA refresh/merge marks validation stale.
- Refinement preserves manual edits outside scope.
- New part receives correct bundle/approval state.

---

# Stage 8 — Approval, Per-Part Validation, Final Validation and Export

## Goal
Make approval deliberate, validated and exportable without additional AI.

## AI operations

- AI-07H: per-part combined validation.
- AI-07I: final consolidated validation.

## Implement

- Text/images review controls and part approval availability.
- AI-07H popup with summary, checks, per-suggestion Accept & Apply/Ignore and overall actions.
- Approve All sequential queue with user decision per part.
- All remaining approved triggers AI-07I automatically.
- AI-07I suggestions: add part, enrich part, add container, add visual; accepted additions loop through quick blueprint/generation/validation/final validation.
- Screen 8 approved-state-only preview and include options. Copy formatted content/images and PDF/print behavior. No AI call.

## Tests

- No part silently becomes approved.
- Cancel/ignore/apply routes work.
- Final validation re-runs after accepted new part.
- Removed parts do not block approval/export.
- Export excludes unapproved/draft content and uses no AI.

---

# Stage 9 — Resilience, Diagnostics and Full QA

## Goal
Make actual integrated app robust and verifiable.

## Implement

- Document 4 retry/error classification.
- Simplified context retry without changing canonical task instructions.
- Rate/network/safety/schema recovery.
- Cache with source/prompt version keys and TTLs.
- User cancellation of queued/running/retry jobs.
- Developer diagnostics panel: operation/model/grounding/cache/token/latency/retry/error/prompt link.
- Cross-browser/manual test protocol and Document 5 requirement-register audit.

## Sign-off

- Every requirement register item has evidence: screen, function, test action, result.
- Every current AI operation has prompt history, error behavior and user visibility.
- No console errors in full normal flow.
- Developer delivers the required 4-part honest report.
