# StudyForge — Comprehensive Implementation Plan & TODO

This is the fully comprehensive implementation plan covering the entire system integration, adapted directly from the architect's detailed implementation TODO. It lays out exactly what my work is across all 9 stages of building the actual app inside the single HTML file (`sindhuskeleton.html`).

## Stage 0. Discovery and Baseline (COMPLETED)
- [x] Identify real skeleton entry HTML and make a backup/versioned copy.
- [x] List all existing screens, DOM IDs, CSS components, modals and event handlers.
- [x] Identify actual Gemini text, image and grounding function names/signatures from integration examples.
- [x] Identify current model names, API/key/config approach and response formats.
- [x] Identify current state/localStorage keys and any direct DOM-only state.
- [x] Identify working skeleton UI features not to alter.
- [x] Create requirement-to-code audit: DONE/PARTIAL/NOT DONE for Documents 1–7.
- [x] Identify and report conflicts/unknowns before coding.

## Stage 1. Foundation
- [ ] Add/normalize central state object with schema version.
- [ ] Add controlled mutation functions; eliminate untracked direct state mutations.
- [ ] Implement `saveState()` after valid mutation.
- [ ] Implement `loadState()` and visible UI hydration.
- [ ] Restore dynamic subtopic inputs, settings, source/paste text, active screen and later state.
- [ ] Implement reset with confirmation.
- [ ] Fix forward `navigate()` and backward/completed `navTo()` behavior using actual code names.
- [ ] Add job status model and stale-state flags.
- [ ] Add prompt execution record schema/history.
- [ ] Build reusable safe View Prompt modal with task/system toggle/copy/edit-run support.
- [ ] Test quotes, `< >`, ampersands and long prompt text in modal.

## Stage 2. Input and Reading
- [ ] Preserve existing upload UI and add file metadata/state.
- [ ] Implement technical extraction quality assessment (using PDF.js/Mammoth.js).
- [ ] Implement extraction mode selector Auto/Technical/AI Cleanup/AI Restructure.
- [ ] Add AI-02A with canonical prompt, source preservation, diagnostics and page map.
- [ ] Add AI-02B with canonical prompt, structured recovery and unresolved-span state.
- [ ] Render editable recovered-source preview before canonical source confirmation.
- [ ] Implement Method 3 paste as semantic as-is input with safe display.
- [ ] Implement dynamic Method 2 subtopics: add/remove/count/array state.
- [ ] Add Method 2 depth, internet, CA and preview-image settings.
- [ ] Add AI-01A scope expansion panel and user approval/custom entries.
- [ ] Add AI-01B source draft → Method 3 textarea.
- [ ] Ensure AI Draft skips Screen 2 after final editor review.
- [ ] Add prompt viewers/recovery paths for AI-01A/B/02A/02B.

## Stage 3. Analysis and Bundles
- [ ] Implement semantic token estimator and natural-boundary chunker.
- [ ] Store chunk continuity/page boundaries/source version.
- [ ] Implement AI-03A and validate subject/purpose/signals schema.
- [ ] Implement AI-03B and stable extraction IDs D-/F-/KF-/PYQ-/etc.
- [ ] Implement chunk-analysis merge/dedupe/source-ref preservation.
- [ ] Implement deterministic signal-to-bundle router.
- [ ] Store all BND fragment definitions from Document 3.
- [ ] Implement AI-03C only for routed bundle fragments.
- [ ] Implement AI-03D selected force-enable bundle call.
- [ ] Render separate basic counts row.
- [ ] Render green/yellow/grey bundle tiers with evidence tooltip.
- [ ] Implement manual subject/bundle correction, reanalyse and details tables.
- [ ] Verify final global selection reaches state and survives refresh.

## Stage 4. Parts and Blueprints
- [ ] Implement AI-04 context selection: deep analysis + safe source/summaries + global bundles.
- [ ] Validate all topic IDs are assigned and applied bundles are valid.
- [ ] Render part cards and outside-range warning.
- [ ] Build real Edit Settings modal.
- [ ] Implement add/remove/merge/reorder state and stale propagation.
- [ ] Verify added parts keep applied bundles through later screens.
- [ ] Implement staggered per-part AI-05 job queue/progress/retry.
- [ ] Validate five-section blueprint schema.
- [ ] Render card prompts, chips, per-card/master blueprint approvals.
- [ ] Implement Screen 6 overlay behavior.
- [ ] Implement AI-06A scoped patches and undo payload.
- [ ] Implement AI-06B target-section-only regeneration.
- [ ] Implement editable CA queries, bundle chips and blueprint stale warnings.

## Stage 5. Notes, Enrichment and Containers
- [ ] Build canonical `buildPartGenerationContext()`.
- [ ] Slice target source and scoped analysis correctly.
- [ ] Include all definitions/formulas but only relevant PYQs/examples/timelines/tables by default.
- [ ] Implement CTX-LOC with entity+context cache.
- [ ] Implement CTX-PER with exam/topic context cache.
- [ ] Implement CTX-FORM with formula/feature/source cache.
- [ ] Route current facts requested by CTX calls to AI-07D, not hidden grounding.
- [ ] Implement AI-07A response schema validation.
- [ ] Build/verify approved safe renderers for every documented container.
- [ ] Implement source/reference/traceability rendering.
- [ ] Reject invalid container type, tag, URL or anchor.
- [ ] Implement manual unlock/edit → stale validation behavior.

## Stage 6. Images, CA, Refinement and Dynamic Parts
- [ ] Normalize image request from blueprint, writer, AI-07E, AI-07H/K and highlight flows.
- [ ] Validate anchor and reserve slot before image generation.
- [ ] Implement AI-07B detailed image prompt.
- [ ] Implement preview-image-prompts setting.
- [ ] Implement AI-07C asset generation, metadata and safe insertion.
- [ ] Implement REG-01 normal variation and REG-02 edited-prompt context.
- [ ] Implement AI-07E suggested-image review UI; never silently create its suggestions.
- [ ] Implement AI-07F selection context and three style choices.
- [ ] Implement AI-07D grounded CA with URL/date/publisher/fetch validation.
- [ ] Implement CA merge default anchor, merge selected anchor, omit and refresh.
- [ ] Implement AI-07G scope/diff/apply selective behavior.
- [ ] Implement AI-07J Add New Part modal and quick blueprint/configure-first choices.
- [ ] Implement Remove Part confirmation/reindex/progress updates.

## Stage 7. Approval and Validation
- [ ] Add text/images review controls and full approval state display.
- [ ] Implement AI-07H combined per-part validation input/context.
- [ ] Render validation summary, per-check result, individual suggestion actions and overall actions.
- [ ] Implement approved-as-is, cancel, apply modification paths.
- [ ] Implement AI-07K for accepted validation image suggestion.
- [ ] Implement Approve All sequential queue/progress/cancellation.
- [ ] Implement AI-07I consolidated validation only after all remaining parts approved.
- [ ] Implement add/enrich/container/visual suggestion routes.
- [ ] Re-run final validation after accepted additions.

## Stage 8. Export
- [ ] Compile approved parts/assets/CA only.
- [ ] Add preview and include options.
- [ ] Ensure blueprint metadata is excluded by default.
- [ ] Implement formatted copy content/images.
- [ ] Implement PDF/browser print.
- [ ] Confirm no AI call happens during export.

## Stage 9. Runtime Safety and QA
- [ ] Implement Document 4 prompt assembly and unresolved-placeholder blocking.
- [ ] Implement model settings/grounding enforcement per operation.
- [ ] Implement JSON/schema repair once, then error modal.
- [ ] Implement context simplification preserving core source/blueprint/IDs.
- [ ] Implement rate/network/safety failure behavior.
- [ ] Implement cache key/TTL/invalidation rules.
- [ ] Implement cancellation for queued/running/retry jobs.
- [ ] Implement diagnostic logs/panel.
- [ ] Test prompt history shows actual executed prompt.
- [ ] Test all three input paths end-to-end.
- [ ] Test bad extraction, long source/chunk merge, force-enable, added/removed part, image failure, CA unavailable, validation loop and resume.
- [ ] Test Chrome, Firefox and Edge.
- [ ] Produce final Document 5 requirement-register audit with evidence.
## Stage 10. Check Architect Folder
- [ ] Check all the files again (there is a questionnaire file, check whether we implemented like this or not, there are two files)
- [ ] Perform gap analysis and create phase 2 plan (don't replace this plan)
