# StudyForge — IMPLEMENTATION_PLAN v2
## Codebase-Specific, Phase-by-Phase Implementation Plan
### Based on Documents 1–7 + Mandatory Architecture Analysis + Actual Code Inspection

> **Prepared:** 2026-07-19  
> **Source of truth precedence:** Doc 3 prompt wording → Docs 4, 1, 2, 5, 6, 7 → Mandatory Analysis → Existing code

---

# PART 1 — CODEBASE DISCOVERY REPORT

## 1.1 Actual AI Function Names and Signatures

Found in `studyforge_main.html` lines 39–88 (plain script, before Babel):

| Function | Signature | Grounding | Image | Model |
|---|---|---|---|---|
| `geminiGenerateText(promptText)` | `async (string) → string` | NO | NO | `gemini-3-flash-preview` |
| `geminiSearchText(searchQuery)` | `async (string) → string` | YES — `googleSearch: {}` | NO | `gemini-3-flash-preview` |
| `geminiImageCreation(imagePrompt)` | `async (string) → data:image/png;base64 string` | NO | YES | `imagen-4.0-generate-001` |

### Critical gaps vs. Document 4 requirements

| Gap | Description |
|---|---|
| **No temperature/token control** | All calls use API defaults. Doc 3 Amendment B mandates per-operation temperature (0.1–0.5) and token budgets. NOT DONE. |
| **No model settings matrix** | Cannot differentiate low-temp extraction (0.1) from creative image (0.5). |
| **No grounding flag per prompt** | Grounding is always ON for `geminiSearchText`, always OFF for `geminiGenerateText`. Canonical spec requires flag per-call. |
| **API key is empty string** | Lines 44, 57, 73. Works in browser AI mode; breaks in standalone. |
| **No retry logic** | Functions throw immediately on failure. Doc 4 requires 3-attempt retry with 2s/4s delays. NOT DONE. |
| **No prompt history save** | Executed final prompts not stored. Doc 3 §7.2 requires saving before each call. NOT DONE. |
| **No schema validation** | Raw `JSON.parse()` with no structural validation. Doc 3 requires schema check before state commit. NOT DONE. |

---

## 1.2 Current State Object Schema (lines 3207–3229)

```javascript
// CURRENT appState initial value
{
  fileInfo: null, fileContent: null, fileBase64: null,
  topic: '', subTopics: ['','',''], focus: '',
  pastedText: '', inputMethod: 'manual_paste',
  internetSearchUsed: false, lastSaved: null,
  prompts: DEFAULT_PROMPTS, analysisData: null,
  settings: { exam:'', objective:'', state:'',
    language:'English', difficulty:'Intermediate',
    length:'Medium (standard)', includeCA:false }
}
```

**Missing from canonical schema (Doc 7 §3.3):**

| Required field | Status |
|---|---|
| `schemaVersion` | MISSING |
| `sourceVersion` | MISSING |
| `sourceDocument.pageMap` | MISSING |
| `sourceDocument.chunks` | MISSING |
| `sourceDocument.diagnostics` | MISSING |
| `analysis.subjectSignals` (AI-03A output) | MISSING — merged into `analysisData` |
| `analysis.deepAnalysis` (AI-03B JSON) | MISSING |
| `analysis.bundleAnalysis` (AI-03C) | MISSING |
| `analysis.userBundleOverrides` | MISSING |
| `jobs` (cancellation tokens) | MISSING |
| `promptHistory` | MISSING |
| `retryHistory` | MISSING |
| `cache` | MISSING |
| `stale` | MISSING |

---

## 1.3 Persistence and Navigation

| Function | Line | Behavior | Gap |
|---|---|---|---|
| `updateState(updates)` | 3254 | Merges + auto-saves to IndexedDB `studyforge_session`. Strips `fileBase64`. | Does not update `currentScreen`/`maxReachedScreen`. |
| `navigateForward(targetScreen)` | 3266 | Sets screen, updates maxReachedScreen, saves. | Correct forward semantics. |
| `navigateBack(targetScreen)` | 3275 | Just sets currentScreen. | Correct backward semantics. |
| `handleResume()` | 3240 | Restores full `appState` from saved. | UI fields do repopulate correctly (partial — screens >1 need testing). |
| `DB.set/get` | 93–133 | IndexedDB `StudyForgeV1DB`, store `state`. | No schema versioning/migration. |

---

## 1.4 Existing Constants

| Constant | Lines | Status vs. Documents |
|---|---|---|
| `SCREEN_NAMES` | 139 | 8 screens present. Names slightly off from spec. Minor. |
| `VISUAL_STYLES` | 181 | 35 entries in 4 categories. DONE. |
| `FEATURE_CATEGORIES` | 225 | 11 categories matching architecture. DONE. |
| `DEFAULT_PROMPTS` | 359 | 12 old prompts with `[PLACEHOLDER]` style. NOT canonical Doc 3 prompts. All must be replaced. |
| `sanitizeInput()` | 375 | HTML entity escaping. DONE. |
| `sanitizeOutput()` | 386 | Strips `<script>` only. PARTIAL — needs allowlist renderer. |

---

## 1.5 Component Inventory

| Component | Lines (approx) | Status | Key gap |
|---|---|---|---|
| `Screen1Input` | 843–910 | DONE | 50k char indicator is soft warning only |
| `FileUploadSection` | 545–625 | DONE | No AI-02A/B failover |
| `TopicInputSection` | 627–778 | PARTIAL | Ad-hoc prompt, not canonical AI-01A/B JSON |
| `Screen2Reading` | 933–1032 | PARTIAL | One monolithic old analysis prompt, not 3-prompt hybrid |
| `Screen3Understanding` | 1034–1255 | PARTIAL | Feature toggles use old `detectedFeatures`, not canonical bundle analysis |
| `Screen4Parts` | 1368–1507 | PARTIAL | Old `partsGeneration` prompt; merge is alert stub |
| `Screen5Blueprints` | 1523–~1800 | PARTIAL | Old `blueprintGeneration`; per-blueprint approval works; AI-06A/B absent |
| `Screen6BlueprintDetail` | ~1800–~2100 | PARTIAL | Old `blueprintChat`; no surgical patch/undo; no AI-06B |
| `Screen7Workspace` | ~2100–~3050 | PARTIAL | Old prompts; CTX-LOC/PER/FORM absent; AI-07E/K absent; no safe structured blocks |
| `Screen8Export` | ~3050–3184 | PARTIAL | No AI call (correct). HTML compile works. No Markdown. |
| `PromptCenter` | 457–508 | DONE | Shows/edits old prompts. Must be updated for new canonical IDs. |
| `TopBar` | 510–543 | DONE | Navigation, dark mode, prompt button. |
| `ErrorModal` | 403–418 | PARTIAL | No editable prompt retry, no simplified retry, no rate-limit wait. |

---

## 1.6 All Required Operations — Current Status

| Canonical Op | Name | Status | Note |
|---|---|---|---|
| AI-01A | Sub-topic Expansion | PARTIAL | Ad-hoc prompt, not canonical JSON schema |
| AI-01B | Source-Material Draft | PARTIAL | Ad-hoc content prompt, not canonical JSON output |
| AI-02A | Extraction Cleanup Fallback | NOT DONE | No failover |
| AI-02B | Source Restructuring Fallback | NOT DONE | No failover |
| AI-03A | Subject & Signal Detection | NOT DONE | Merged into old `analysis` |
| AI-03B | Deep Core Extraction | NOT DONE | Merged into old `analysis` |
| AI-03C | Smart Routed Bundle Analysis | NOT DONE | No bundle routing |
| AI-03D | Force-Enabled Bundle | NOT DONE | No force-enable call |
| AI-04 | Coherent Part Splitting | PARTIAL | Old `partsGeneration` prompt |
| AI-05 | Per-Part Blueprint | PARTIAL | Old `blueprintGeneration` prompt |
| AI-06A | Blueprint Chat Modification | PARTIAL | Old `blueprintChat`, no surgical patch |
| AI-06B | Section-Only Blueprint Regen | NOT DONE | Not implemented |
| AI-07A | Per-Part Notes Generation | PARTIAL | Old `notesGeneration`, no safe structured blocks |
| AI-07B | Image Prompt Expansion | PARTIAL | Old `imagePromptGeneration` |
| AI-07C | Image Generation | DONE | `geminiImageCreation()` works |
| AI-07D | Grounded CA Research | PARTIAL | Old `currentAffairsSearch` via `geminiSearchText` |
| AI-07E | Post-Gen Image Gap Review | NOT DONE | |
| AI-07F | Highlight-to-Visualize | PARTIAL | Old `visualizeThis` prompt |
| AI-07G | Scope-Aware Refinement | PARTIAL | Old refinement chat |
| AI-07H | Per-Part Validation | PARTIAL | Old `validation` prompt |
| AI-07I | Final Consolidated Validation | PARTIAL | Exists but uses old prompt |
| AI-07J | New Part Quick Blueprint | PARTIAL | Limited implementation |
| AI-07K | Validation Image Adapter | NOT DONE | |
| CTX-LOC | Location Facts (deferred) | NOT DONE | Old `locationFacts` is rough approximation |
| CTX-PER | Personality Facts (deferred) | NOT DONE | |
| CTX-FORM | Formula Deep Dive (deferred) | NOT DONE | |

**Summary: 3 DONE, 11 PARTIAL, 11 NOT DONE**

---

## 1.7 Contradictions Between Code and Documents 1–7

| # | Code behavior | Required behavior (Doc reference) |
|---|---|---|
| C1 | Single monolithic analysis prompt | AI-03A → AI-03B → AI-03C in sequence; Doc 5-C1 |
| C2 | `dangerouslySetInnerHTML` on raw AI text in some containers | AI-07A returns structured safe blocks; renderer builds HTML; Doc 7 |
| C3 | `DEFAULT_PROMPTS` uses old `[PLACEHOLDER]` style | Canonical Doc 3 prompts with `{{VARIABLE}}` convention |
| C4 | One `analysisData` object | Three separate: `subjectSignals`, `deepAnalysis`, `bundleAnalysis`; Doc 3 AI-03A/B/C |
| C5 | PDF extracted into one flat string, no page numbering | `pageMap` required for per-part source slicing in AI-05 and AI-07A |
| C6 | Always default temperature/tokens | Per-operation settings from Doc 3 Amendment B |
| C7 | Single attempt, throws on failure | 3-attempt retry with 2s/4s backoff; Doc 7 Phase 8 |
| C8 | Prompt viewer shows stored template | Must show final assembled prompt actually sent; Doc 3 §7.2 |
| C9 | Images rendered at part level, no anchor system | `placement_anchor` must resolve to generated container anchor |
| C10 | 3-tag system: `source_backed`, `ai_enriched`, `ca_integrated` | 4-tag system including `WEB_SOURCED:url`; Doc 5 gap #15 |
| C11 | `handleMergeParts()` calls `alert()` | Must be functional merge |
| C12 | Screen 6 = "Generation" in `SCREEN_NAMES` | Should be "Blueprint Detail View" |

---

# PART 2 — PHASE-BASED IMPLEMENTATION PLAN

## Phase 0 — Foundation Infrastructure
**Goal:** Upgraded AI wrapper with model settings and retry. Full state schema. Canonical prompt registry. Safe renderer. Prompt history. Updated PromptCenter.  
**Working artifact:** App loads, navigates, all prompts visible with canonical IDs in Prompt Center.

### Functions / State Fields / DOM IDs to Modify

| Item | Action |
|---|---|
| `geminiGenerateText(promptText)` | Add `options = {temperature, maxOutputTokens, grounding}` parameter. Add 3-attempt retry with 2s/4s backoff. Save final prompt to `promptHistory` before call. |
| `geminiSearchText(searchQuery)` | Add retry; save to `promptHistory`. |
| `geminiImageCreation(imagePrompt)` | Add retry; save to `promptHistory`. |
| `appState` schema | Add all Doc 7 §3.3 fields: `schemaVersion`, `sourceVersion`, `sourceDocument`, `analysis`, `jobs`, `promptHistory`, `retryHistory`, `cache`, `stale`. |
| `DEFAULT_PROMPTS` | Replace all 12 old keys with new keys: `SYS_01` through `SYS_05`, `AI_01A` through `AI_07K`, `CTX_LOC`, `CTX_PER`, `CTX_FORM`, plus 12 `BND_*` fragments. Full canonical text from Doc 3. |
| New: `retryAI(fn, opts)` | `async (fn, {maxRetries:3, delays:[2000,4000], onError}) => result`. Classify error: rate-limit / token / network / schema. |
| New: `renderSafeBlock(block)` | Takes `html_blocks[]` item from AI-07A, returns safe JSX per `container_type`. Supports all 17+ container types. No `dangerouslySetInnerHTML` on raw AI text. |
| New: `buildPrompt(templateKey, variables)` | Reads canonical template, injects variables with `{{VAR}}` substitution, returns assembled string. Saves to `promptHistory`. |
| `sanitizeOutput()` | Upgrade to allowlist renderer: parse structured safe block objects, produce sanitized HTML per container type. |
| `PromptCenter` | Update to show new canonical prompt IDs. Add two tabs per prompt: "Canonical Template" vs "Last Executed (Final Assembled)". |
| `ErrorModal` | Add: editable prompt textarea (prefilled from `promptHistory`). Buttons: Retry As-Is, Retry Simplified, Retry Edited. |
| `DB` | Add `schemaVersion` check on `get`. If mismatch, clear stale state gracefully. |

### AI Operations This Phase
None (infrastructure only).

### State Mutations
- `appState.promptHistory[operationId]` → `{finalPrompt, timestamp, operationId}`
- `appState.retryHistory[operationId]` → `[{attempt, error, timestamp}]`

### Phase 0 Tests (12)
1. App loads without JS errors.
2. `geminiGenerateText` retries on 429 with correct backoff delays.
3. `retryAI` correctly classifies token-limit vs. rate-limit errors.
4. `renderSafeBlock` for `concept_box` produces valid HTML with no script tags.
5. `renderSafeBlock` for `formula_box` renders formula, variables correctly.
6. Old `[PLACEHOLDER]`-style keys no longer exist in `DEFAULT_PROMPTS`.
7. `PromptCenter` shows canonical prompt IDs (AI-03A, AI-07A etc.).
8. `PromptCenter` "Last Executed" tab shows the last prompt sent to model.
9. `ErrorModal` "Retry Edited Prompt" sends the user-modified prompt text.
10. `DB.get` with old schema version triggers graceful clear.
11. `appState.schemaVersion` present after first `updateState()`.
12. `promptHistory` entry created before each AI call.

### Sign-off Criteria
- [ ] All 12 tests pass.
- [ ] No raw AI text injected via `dangerouslySetInnerHTML` without `renderSafeBlock`.
- [ ] `PromptCenter` shows canonical prompt IDs.

---

## Phase 1 — Input (Screen 1) + Source Preparation (Screen 2)
**Goal:** All three input methods produce canonical source with page map. AI-01A/B use canonical prompts. AI-02A/B failover implemented.  
**Working artifact:** PDF upload → page-numbered text in state. Topic → scope JSON approval → draft JSON → editable Method 3 textarea.

### Functions / State Fields

| Item | Action |
|---|---|
| `FileUploadSection.handleFile()` | PDF extraction: retain per-page text + page number. Build `sourceDocument.pageMap`. |
| New: `extractFromPDF(file)` | Returns `{text, pageMap:[{page, text}], diagnostics}`. If text quality < threshold, set `diagnostics.needsCleanup = true`. |
| `Screen2Reading` | Split: Screen 2 handles source preparation and failover only — not analysis. Rename main function to `runSourcePreparation()`. |
| New: `runAI02A(sourceText, diagnostics, pageMap)` | Canonical AI-02A prompt (SYS-02 + AI-02A task). Returns `{clean_text, page_map, unresolved_segments, quality_status}`. |
| New: `runAI02B(sourceText, diagnostics, pageMap)` | Canonical AI-02B. Returns structured text with section map. |
| `TopicInputSection.handleAIExpand()` | Replace ad-hoc prompt with canonical AI-01A. Parse JSON `{guaranteed_topics, suggested_essential, suggested_optional, current_topics}`. Show tiered approval UI. |
| `TopicInputSection.handleAIGenerate()` | Replace ad-hoc prompt with canonical AI-01B. Parse JSON `{content, heading_map, web_sources}`. Inject `content` into `pastedText`. |
| `appState.sourceDocument` | Set `{origin, text, pageMap, chunks:[], diagnostics, unresolvedSegments:[]}` |
| `appState.inputProfile` | Set `{method, internetMode, depth, examContext}` |

### Canonical Prompts
- **AI-01A** — Sub-topic expansion (SYS-01 + optional SYS-04). Temp: 0.3, Tokens: 2,000.
- **AI-01B** — Source-material draft (SYS-01 + optional SYS-04). Temp: 0.4, Tokens: 15,000/30,000.
- **AI-02A** — Extraction cleanup (SYS-02). Temp: 0.1, Tokens: input-size matched.
- **AI-02B** — Source restructuring (SYS-02). Temp: 0.1, Tokens: input + 20%.

### Phase 1 Tests (12)
1. PDF upload produces `pageMap` with one entry per page.
2. Multi-page PDF preserves page references in extracted text.
3. Poor quality extraction triggers AI-02A automatically.
4. AI-02A result still `unusable` triggers AI-02B.
5. `handleAIExpand()` canonical JSON contains `guaranteed_topics` with all user entries unchanged.
6. Internet mode OFF → `current_topics` array is empty.
7. Internet mode ON → `current_topics` have `web_source_url` and `source_date`.
8. User unchecks items in approval UI → unchecked items absent from `APPROVED_SUBTOPICS_JSON` in AI-01B.
9. AI-01B `content` field appears in Method 3 `pastedText`.
10. `sourceDocument.pageMap` persisted to IndexedDB.
11. Resume from saved session repopulates `pastedText`, `topic`, `subTopics` in Screen 1 UI.
12. AI-02A network failure shows ErrorModal with Retry/Skip options.

### Sign-off Criteria
- [ ] All 12 tests pass.
- [ ] `sourceDocument.pageMap` non-empty after PDF upload.
- [ ] `guaranteed_topics` unchanged from user's original entries.

---

## Phase 2 — Analysis Engine (Screen 2 → Screen 3)
**Goal:** Replace old single-prompt analysis with canonical 3-prompt hybrid. Screen 3 feature display reflects canonical bundle states (auto_on / suggested / not_detected).  
**Working artifact:** Upload material → 3 sequential AI calls → Screen 3 shows structured counts from deep extraction, three-tier bundle display.

### Functions / State Fields

| Item | Action |
|---|---|
| `Screen2Reading.runAnalysis()` | Rename and refactor: `runSubjectDetection()` → `runDeepExtraction()` → `runBundleAnalysis()` in sequence. Each updates `appState.analysis` separately. |
| New: `runSubjectDetection(sourceText, pageMap, chunkContext)` | Canonical AI-03A (+Amendment C: `purpose` field). Stores in `appState.analysis.subjectSignals`. |
| New: `runDeepExtraction(sourceText, pageMap, subjectSignals, chunkContext)` | Canonical AI-03B (+Amendment D: `key_facts` with `KF-` IDs). Stores in `appState.analysis.deepAnalysis`. |
| New: `runBundleAnalysis(subjectSignals, deepAnalysis, sourceExcerpts)` | Canonical AI-03C. Build `ROUTED_BUNDLES_JSON` from `buildRoutedBundles(signals)`. Store in `appState.analysis.bundleAnalysis`. |
| New: `runForceEnableBundle(bundleDef, userMessage)` | Canonical AI-03D. Triggered when user force-enables hidden bundle. Updates `appState.analysis.userBundleOverrides`. |
| New: `buildRoutedBundles(signals)` | Deterministic router: reads signal strengths from AI-03A. Selects from BND_GEO, BND_PER, BND_FORM, BND_DATA, BND_LAW, BND_TIME, BND_STORY, BND_ADM, BND_PROC, BND_CS, BND_MED, BND_CA. |
| New: `chunkSource(text, pageMap)` | Splits at chapter > section > page > paragraph group. Returns `[{chunk_id, text, boundaries, prev_summary, next_preview}]`. |
| New: `mergeChunkAnalyses(chunkResults)` | Union topics, dedupe definitions/formulas by content, concatenate PYQs. |
| `Screen3Understanding` | Replace old `detectedFeatures` with canonical bundle states. Three-tier UI: green (auto_on), yellow (suggested), grey (force-enable). Evidence tooltip on hover. |
| `appState.analysis` | `{subjectSignals:{}, deepAnalysis:{}, bundleAnalysis:{}, userBundleOverrides:{}}` |

### Canonical Prompts
- **AI-03A** — Temp: 0.1, Tokens: 2,000, Grounding: OFF
- **AI-03B** — Temp: 0.1, Tokens: 8,000, Grounding: OFF
- **AI-03C** — Temp: 0.1, Tokens: 3,000–6,000, Grounding: OFF
- **AI-03D** — Temp: 0.2, Tokens: 3,000, Grounding: OFF

### Phase 2 Tests (12)
1. AI-03A returns valid JSON with `primary_subject`, `signals`, `routing_hints`.
2. Signals with `"not_detected"` strength do not route bundles to AI-03C.
3. AI-03B returns `topics[]` with `T-` IDs, `definitions[]` with `D-`, `formulas[]` with `F-`.
4. AI-03B Amendment D: `key_facts[]` with `KF-` IDs present.
5. AI-03C only contains bundles selected by router.
6. Screen 3 shows green for `auto_on`, yellow for `suggested`, grey for `not_detected`.
7. Force-enable button triggers AI-03D; result shown in toggle.
8. Large source activates chunker; chunk context included in AI-03A/B.
9. Merged analyses: topics deduped by title; formulas by expression.
10. `appState.analysis.subjectSignals`, `.deepAnalysis`, `.bundleAnalysis` all present.
11. `promptHistory` has 3 separate entries: `AI-03A`, `AI-03B`, `AI-03C`.
12. AI-03A `purpose` field present (Amendment C).

### Sign-off Criteria
- [ ] All 12 tests pass.
- [ ] Three separate AI calls in `promptHistory`.
- [ ] Three-tier bundle UI driven by `bundleAnalysis` output.

---

## Phase 3 — Parts (Screen 4)
**Goal:** Canonical AI-04 splitting with page-count guardrail. Per-part bundle inheritance. Edit modal with all fields. Merge parts functional.

### Functions / State Fields

| Item | Action |
|---|---|
| `Screen4Parts.generateParts()` | Replace `buildPartsPrompt` with `buildAI04Prompt(appState)`. Send: `DEEP_ANALYSIS_JSON`, `SOURCE_LENGTH_AND_PAGE_INFO_JSON`, `PART_COUNT_GUARDRAIL_JSON`, `BUNDLE_SELECTIONS_JSON`, `SPLITTING_SOURCE_CONTEXT`. |
| `PartCard` | Show page range, bundle chips from `applied_bundles` field. Remove old `hasFormulas`/`hasCode` booleans. |
| `EditPartModal` | Add: page range fields (start/end), formula count display, description field, applied bundles chip editor. |
| `handleMergeParts()` | Replace alert stub: select two parts → confirm → merge topics/page_ranges → update state. |
| New: `buildPartCountGuardrail(pageMap)` | Returns `{min_parts, max_parts}` from page count table. |
| `appState.parts[].applied_bundles` | Per-part bundle assignment from AI-04. |

### Canonical Prompt: AI-04
Temp: 0.2 | Max tokens: 5,000 | Grounding: OFF

### Phase 3 Tests (10)
1. AI-04 response has `parts[].part_id`, `page_range`, `applied_bundles`.
2. `out_of_range_warning` shown if parts count outside page guardrail.
3. Edit modal save updates title, page range, description in state.
4. Edit modal bundle chip removal removes bundle from `applied_bundles`.
5. Merge: two parts → one with combined topics and page_range.
6. Add part: gets `part_id` with timestamp suffix.
7. Delete: removed from state; Screen 5 skips blueprint for deleted part.
8. Parts in Screen 5 match `appState.parts` exactly.
9. Per-part bundle is subset of global bundle selections.
10. `promptHistory['AI-04']` saved before API call.

### Sign-off Criteria
- [ ] All 10 tests pass.
- [ ] Part card shows bundle chips from `applied_bundles`.
- [ ] Merge Parts is functional.

---

## Phase 4 — Blueprints (Screens 5–6)
**Goal:** Canonical AI-05 per-part blueprint. AI-06A surgical patch with undo. AI-06B section regen. Stale-state marking.

### Functions / State Fields

| Item | Action |
|---|---|
| `Screen5Blueprints.generateAllBlueprints()` | Replace with canonical AI-05. Stagger 1s between calls. Send: `PART_PLAN_JSON`, `SOURCE_SLICE`, `PART_ANALYSIS_JSON`, `ALL_DEFINITIONS_JSON`, `ALL_FORMULAS_JSON`, `BUNDLE_SELECTIONS_JSON`, `SUBJECT_STRATEGY`. |
| Blueprint cards (Screen 5) | Show: heading count, text plan count, image plan count, CA query count, validation plan count. |
| `Screen6BlueprintDetail` | AI chat uses canonical AI-06A. Per-section regen buttons use AI-06B. |
| New: `runAI06A(userMessage, partPlan, blueprint, bundles, partAnalysis)` | Returns JSON patch + undo payload. Apply patches to blueprint. |
| New: `runAI06B(targetSection, userDirection, blueprint, lockedSections, partAnalysis)` | Returns replacement section only. Does not modify other sections. |
| New: `applyBlueprintPatch(blueprint, patchOperations)` | Applies patch ops by path. Saves undo payload. |
| `appState.blueprintUndoHistory[partId]` | Stack of undo payloads. |
| `appState.stale.blueprints[partId]` | Set when source or parts change. |

### Canonical Prompts
- **AI-05** — Temp: 0.3, Tokens: 8,000, Grounding: OFF
- **AI-06A** — Temp: 0.2, Tokens: 5,000, Grounding: OFF
- **AI-06B** — Temp: 0.25, Tokens: 5,000, Grounding: OFF

### Phase 4 Tests (12)
1. AI-05 returns all 5 sections: `headings`, `text_plan`, `image_plan`, `ca_plan`, `validation_plan`.
2. Screen 5 cards show image count and CA query count from AI-05.
3. All blueprints approved enables "Start Generation" button.
4. AI-06A chat instruction "add more formulas" patches only `text_plan`.
5. AI-06A patch undo restores pre-change value.
6. AI-06B section regen does not modify other sections.
7. Editing parts on Screen 4 marks `stale.blueprints[partId] = true`.
8. Stale indicator shown on blueprint card.
9. Image plan shows style dropdown (35 styles) per planned image.
10. CA plan shows editable query strings.
11. All 5 section types accessible in Screen 6.
12. `promptHistory['AI-05-{partId}']` saved before each call.

### Sign-off Criteria
- [ ] All 12 tests pass.
- [ ] AI-06A surgical patch modifies only detected scope.
- [ ] Stale indicator appears when dependencies change.

---

## Phase 5 — Core Notes Generation and Safe Renderer (Screen 7 Part 1)
**Goal:** Canonical AI-07A generating structured safe blocks per part. Safe renderer for all 17+ container types. Anchor system. 4-tag traceability. CTX-LOC/PER/FORM.

### Functions / State Fields

| Item | Action |
|---|---|
| New: `runAI07A(part, appState)` | Assemble canonical AI-07A input. Call `geminiGenerateText`. Parse and schema-validate. Save to `promptHistory`. |
| New: `buildSourceSlice(pageMap, part)` | Returns source text for `part.page_range` only. |
| New: `buildPartAnalysis(deepAnalysis, part)` | Returns scoped analysis (topics, examples, etc.) for this part's `topic_ids`. Includes global definitions and formulas. |
| `renderSafeBlock(block)` | Full container renderer. All 17+ container types: `concept_box`, `formula_box`, `story_box`, `comparison_table`, `code_block`, `definition_box`, `pyq_box`, `quick_revision`, `geography_box`, `personality_card`, `data_insight`, `analogy_box`, `timeline_box`, `process_box`, `institution_box`, `ca_box`, `experiment_box`, `summary_box`, `key_fact_box`, `legal_box`. |
| `SourceTag` component | Add 4th tag: `WEB_SOURCED` (purple, shows URL link). |
| Anchor system | Each rendered block gets `data-anchor={block.anchor}`. `anchorRegistry` tracks all generated anchors. `validateAnchor(anchor)` checks registry. |
| `image_needed` handling | Creates placeholder block at `after_anchor`. Waits for Phase 6. |
| CTX-LOC / CTX-PER / CTX-FORM | Called before AI-07A when relevant bundle applied and part has relevant items. Inject enrichment results as additional context. Cache per `{itemId, partId}`. |
| `appState.generatedParts[partId]` | `{html_blocks:[], image_needed:[], citations:[], generation_summary:'', status:'pending|generating|done|approved'}` |
| `appState.stale.generatedParts[partId]` | Set when blueprint changes. |

### Canonical Prompts
- **AI-07A** — Temp: 0.4, Tokens: 15,000, Grounding: OFF
- **CTX-LOC** — Temp: 0.3, Tokens: 3,000, Grounding: OFF
- **CTX-PER** — Temp: 0.3, Tokens: 2,000, Grounding: OFF
- **CTX-FORM** — Temp: 0.3, Tokens: 3,000, Grounding: OFF

### Phase 5 Tests (14)
1. AI-07A returns valid JSON with `html_blocks[]` each having `anchor`, `container_type`, `safe_content`, `traceability`.
2. `renderSafeBlock` for `formula_box` shows formula expression + variables.
3. `renderSafeBlock` for `code_block` shows syntax-highlighted code.
4. `renderSafeBlock` for `comparison_table` shows headers and rows.
5. `renderSafeBlock` for `timeline_box` shows events in order.
6. `renderSafeBlock` for `personality_card` shows person name, role, facts.
7. `WEB_SOURCED` tag shows purple label with URL link.
8. `data-anchor` attribute present on every rendered container.
9. `image_needed` item creates placeholder block at correct anchor.
10. CTX-LOC called for part with geography bundle and central/supporting location.
11. CTX-LOC result cached; second call for same location+part uses cache.
12. `ALL_DEFINITIONS_JSON` and `ALL_FORMULAS_JSON` come from entire document.
13. `SOURCE_SLICE` contains only text from this part's page range.
14. `promptHistory['AI-07A-{partId}']` saved before call.

### Sign-off Criteria
- [ ] All 14 tests pass.
- [ ] No raw AI text via `dangerouslySetInnerHTML` without `renderSafeBlock`.
- [ ] All 17+ container types render without errors.

---

## Phase 6 — Visual and CA Systems (Screen 7 Part 2)
**Goal:** Canonical AI-07B/C/D/E/F/K image pipeline. CA fetch with URL/date validation. Highlight-to-Visualize. `WEB_SOURCED` CA rendering.

### Functions / State Fields

| Item | Action |
|---|---|
| New: `runAI07B(imageRequest, surroundingContext, partPlan, styleSelection, userDirection)` | Canonical AI-07B. Returns `{images_needed:[{image_id, expanded_prompt, style_recommended, placement_anchor, learning_goal}]}`. |
| New: `runAI07C(imageTitle, learningGoal, expandedPrompt)` | Calls `geminiImageCreation(expandedPrompt)`. Returns base64 data URI. |
| New: `insertImageAtAnchor(anchor, imageDataUri, imageMeta)` | Places image in rendered blocks at validated anchor. |
| New: `runAI07D(caQuery, partPlan, purpose)` | Canonical AI-07D (grounding ON). Parse `{results:[{fact, url, publisher, date}]}`. Validate URL non-empty. Render as `WEB_SOURCED` CA blocks. |
| New: `runAI07E(partPlan, blueprint, generatedPart, imageAssets, bundles)` | Canonical AI-07E. Returns `{missing_images:[]}`. User confirms each suggestion. |
| New: `runAI07F(selectedText, surroundingContext, partPlan, bundles, userDirection)` | Canonical AI-07F. Returns `{expanded_prompt, recommended_styles:[3], placement_anchor}`. |
| New: `runAI07K(validationSuggestion, partPlan, imageAssets)` | Canonical AI-07K. Converts validation-suggested image to `image_needed` format. |
| Highlight-to-Visualize | Text selection → camera button → AI-07F popup → style picker → confirm → AI-07B → AI-07C → insertImageAtAnchor. |
| CA zone | Fetch CA button → AI-07D per query → results with URL/date badges → "Merge" inserts `ca_box` at current part position. |
| `appState.imageAssets[partId]` | `{[image_id]: {title, prompt, dataUri, anchor, learning_goal, approved:false}}` |
| `appState.currentAffairs[partId]` | `{[queryId]: {results:[], fetchedAt:'', status}}` |

### Canonical Prompts
- **AI-07B** — Temp: 0.5, Tokens: 2,000, Grounding: OFF
- **AI-07C** — Provider settings, Grounding: OFF
- **AI-07D** — Temp: 0.1, Tokens: 5,000, **Grounding: ON**
- **AI-07E** — Temp: 0.2, Tokens: 2,000, Grounding: OFF
- **AI-07F** — Temp: 0.5, Tokens: 2,000, Grounding: OFF
- **AI-07K** — Temp: 0.2, Tokens: 1,500, Grounding: OFF

### Phase 6 Tests (12)
1. Blueprint image placeholder resolves after AI-07B → AI-07C chain.
2. AI-07B `placement_anchor` matches a known anchor in generated blocks.
3. Invalid anchor in AI-07B output is rejected; error shown.
4. AI-07D returns results with URL and date.
5. CA result without URL not rendered as WEB_SOURCED.
6. CA box appears as `ca_box` with purple WEB_SOURCED tag.
7. Highlight text → camera button → AI-07F popup shows 3 style recommendations.
8. AI-07E post-gen review runs conditionally; suggestions shown to user.
9. User confirms AI-07E suggestion → AI-07B → AI-07C → image inserted.
10. Regenerate image adds "Generate a different variation" suffix to prompt.
11. Style dropdown on each image allows changing from 35 options.
12. AI-07K converts validation-suggested image need to pipeline format.

### Sign-off Criteria
- [ ] All 12 tests pass.
- [ ] All three image trigger moments (blueprint / post-review / validation) use same `runAI07B → runAI07C → insertImageAtAnchor` chain.
- [ ] CA results without URL not displayed as WEB_SOURCED.

---

## Phase 7 — Refinement, Approval, Validation and Dynamic Parts (Screen 7 Part 3)
**Goal:** Canonical AI-07G/H/I/J. Per-part validation on approve. Sequential Approve All with progress. Final validation. Diff preview. Remove/Add part with AI.

### Functions / State Fields

| Item | Action |
|---|---|
| New: `runAI07G(userMessage, selectedText, generatedPart, blueprint, partPlan, bundles)` | Canonical AI-07G. Returns `{scope, proposed_edits:[{before, after}], image_actions, requires_full_regeneration}`. Show diff preview modal. |
| New: `runAI07H(partPlan, blueprint, generatedPart, imageAssets, caResults, sourceSlice, traceability)` | Canonical AI-07H. Returns `{overall_status, summary, issues, suggestions}`. Show ValidationPopup. |
| New: `runAI07I(allApprovedParts, deepAnalysis, allBlueprintPlans, allImageAssets, settings)` | Canonical AI-07I. Final consolidated validation. Returns `{cross_document_status, missing_coverage, new_part_suggestions}`. |
| New: `runAI07J(newTopic, subTopics, globalBundles, caToggle)` | Canonical AI-07J (new part quick blueprint). |
| `PartApprovalBar` | Per-part: Approve Text checkbox, Approve Images checkbox, Approve Part button (triggers AI-07H), Unlock to Edit button. |
| `ValidationPopup` | Shows AI-07H summary, issues, suggestions. Accept/Ignore per suggestion. |
| `FinalValidationPopup` | Shows AI-07I results. User can add suggested parts via AI-07J. |
| Diff preview modal | Shows `proposed_edits[].before` vs `.after` side-by-side. Apply All / Apply Selective / Discard. |
| Sequential Approve All | Iterates parts in order. Runs AI-07H per part. Shows progress "3 of 6". Cancel stops loop. |
| `appState.approvals[partId]` | `{text:false, images:false, part:false, lockedAt:null}` |
| `appState.jobs[operationId]` | `{status:'running|done|cancelled', abortController}` |

### Canonical Prompts
- **AI-07G** — Temp: 0.3, Tokens: 8,000, Grounding: OFF
- **AI-07H** — Temp: 0.1, Tokens: 5,000, Grounding: OFF
- **AI-07I** — Temp: 0.2, Tokens: 5,000, Grounding: OFF
- **AI-07J** — Temp: 0.3, Tokens: 5,000, Grounding: OFF

### Phase 7 Tests (12)
1. "Approve Part" triggers AI-07H and shows ValidationPopup.
2. "Accept" on AI-07H suggestion applies change; "Ignore" marks skipped.
3. "Approve All" runs AI-07H per part sequentially with progress counter.
4. AI-07H image suggestion triggers AI-07K → AI-07B → AI-07C.
5. AI-07I runs only after all parts approved.
6. AI-07I new part suggestion → user approves → AI-07J generates quick blueprint.
7. Refinement chat AI-07G shows before/after diff.
8. "Apply Selective" from diff preview applies only checked edits.
9. `requires_full_regeneration=true` shows warning before proceeding.
10. Remove part: remaining parts renumbered; final validation marked stale.
11. "Generate Immediately" on Add Part calls AI-07J without Screen 6 edit step.
12. Unlock to Edit: approval status reset; can re-approve.

### Sign-off Criteria
- [ ] All 12 tests pass.
- [ ] Sequential Approve All processes in order with progress indicator.
- [ ] Diff preview shows before/after for all proposed edits.

---

## Phase 8 — Export (Screen 8) + Resilience + Observability
**Goal:** Pure no-AI export of approved state. HTML / print / clipboard formats. Retry, chunking, cache, cancel, diagnostics hardened.

### Functions / State Fields

| Item | Action |
|---|---|
| `Screen8Export.handleDownload()` | Compile from `appState.approvals` approved parts only. Zero AI calls. |
| New: `compileApprovedHTML(appState, options)` | Builds final HTML from: approved html_blocks, image data URIs, CA boxes, traceability tags (conditional). Cover page and TOC if selected. |
| Format: HTML | Save as `.html` file via blob download. |
| Format: Print/PDF | `window.print()` with print-optimized CSS. |
| Format: Clipboard | `navigator.clipboard.writeText(compiledHTML)`. |
| Diagnostics panel | Toggle in TopBar: shows `promptHistory`, `retryHistory`, `cache` sizes, `stale` flags. |
| Cache invalidation | Source change → clear `cache.ctxLoc/Per/Form`. Blueprint change → set `stale.generatedParts[partId]`. |
| Cancellation | `AbortController` per long AI operation. Cancel button visible during generation. |

### Phase 8 Tests (12)
1. Export: only approved parts appear in downloaded HTML.
2. Export HTML contains cover page when option enabled.
3. Export HTML contains TOC when option enabled.
4. Print format triggers `window.print()`.
5. Copy to clipboard copies formatted HTML.
6. No AI call made on Screen 8.
7. Cancel button stops generation mid-way without corrupting partial state.
8. 100-page PDF: chunker splits into ≥3 chunks; merged analysis has union topics.
9. CTX-LOC for same location+part returns from cache on second call.
10. Diagnostics panel shows promptHistory and retryHistory counts.
11. Source change → `stale.generatedParts` set → stale indicator on Screen 7.
12. No `dangerouslySetInnerHTML` with raw AI output anywhere.

### Sign-off Criteria
- [ ] All 12 tests pass.
- [ ] Screen 8 makes zero AI calls.
- [ ] Grep for raw AI `dangerouslySetInnerHTML` returns zero results.

---

## Phase 9 — QA and Gap-Register Audit
**Goal:** Full end-to-end walkthrough. Document 5 gap audit. Browser compatibility. Honest declaration.

### Phase 9 Tests (12)
1. Full end-to-end: PDF upload → Screen 8 export with 3+ parts, images, CA.
2. Full end-to-end: Method 2 topic → Screen 8 export.
3. Full end-to-end: Paste text → Screen 8 export.
4. Resume: close browser mid-Screen 7 → reopen → resume shows correct screen.
5. Doc 5 gap matrix: every row marked DONE or documented as deferred with reason.
6. All 26 Doc 5 quick-comparison items verified.
7. Dark mode: all screens render correctly.
8. Large source (50k+ characters): no timeout; chunking activates.
9. Network failure during AI: retry flow shown.
10. Rate limit: auto-wait before popup.
11. Schema validation failure (malformed AI JSON): error flow, not crash.
12. All canonical prompt IDs (AI-01A through AI-07K + CTX-LPF) present in `DEFAULT_PROMPTS` verbatim.

---

# PART 3 — CANONICAL PROMPT LIBRARY APPENDIX

> All prompt text is stored verbatim in `DEFAULT_PROMPTS` using the keys below.  
> Full text: Document 3 (system prompts §2, operations §4, bundle fragments §4B, CTX prompts §4C).

## System Prompts (SYS-01 through SYS-05)
- **SYS-01** — Universal Educational Content System Instruction (used with: AI-01A/B, AI-03A–D, AI-04, AI-05, AI-06A/B, AI-07A/E–K, CTX-LOC/PER/FORM)
- **SYS-02** — Source Preservation System Instruction (AI-02A, AI-02B)
- **SYS-03** — Educational Image System Instruction (AI-07B, AI-07C)
- **SYS-04** — Grounded Current Affairs Research System Instruction (AI-07D; AI-01A/B when internet mode ON)
- **SYS-05** — Validation and Refinement System Instruction (AI-06A/B, AI-07G/H/I/K)

## Operation Prompts — Variable Contracts

| Prompt ID | Variables ({{VAR}} format) |
|---|---|
| AI-01A | `{{TOPIC}}`, `{{USER_SUBTOPICS_JSON}}`, `{{DEPTH}}`, `{{EXAM_CONTEXT}}`, `{{INTERNET_MODE}}` |
| AI-01B | `{{TOPIC}}`, `{{APPROVED_SUBTOPICS_JSON}}`, `{{DEPTH}}`, `{{EXAM_CONTEXT}}`, `{{INTERNET_MODE}}` |
| AI-02A | `{{SOURCE_TYPE}}`, `{{EXTRACTION_DIAGNOSTICS_JSON}}`, `{{SOURCE_TEXT}}`, `{{PAGE_MAP_JSON}}` |
| AI-02B | `{{SOURCE_TYPE}}`, `{{EXTRACTION_DIAGNOSTICS_JSON}}`, `{{SOURCE_TEXT}}`, `{{PAGE_MAP_JSON}}` |
| AI-03A | `{{SOURCE_ORIGIN}}`, `{{EXAM_CONTEXT}}`, `{{SOURCE_TEXT}}`, `{{PAGE_MAP_JSON}}`, `{{CHUNK_CONTEXT_JSON}}` |
| AI-03B | `{{SUBJECT_SIGNALS_JSON}}`, `{{SOURCE_TEXT}}`, `{{PAGE_MAP_JSON}}`, `{{CHUNK_CONTEXT_JSON}}` |
| AI-03C | `{{SUBJECT_SIGNALS_JSON}}`, `{{DEEP_ANALYSIS_JSON}}`, `{{ROUTED_BUNDLES_JSON}}`, `{{RELEVANT_SOURCE_EXCERPTS_JSON}}` |
| AI-03D | `{{REQUESTED_BUNDLE_JSON}}`, `{{USER_MESSAGE}}`, `{{SUBJECT_SIGNALS_JSON}}`, `{{DEEP_ANALYSIS_JSON}}`, `{{SOURCE_TEXT}}` |
| AI-04 | `{{TOPIC}}`, `{{EXAM_CONTEXT}}`, `{{SOURCE_LENGTH_AND_PAGE_INFO_JSON}}`, `{{PART_COUNT_GUARDRAIL_JSON}}`, `{{DEEP_ANALYSIS_JSON}}`, `{{BUNDLE_SELECTIONS_JSON}}`, `{{SPLITTING_SOURCE_CONTEXT}}` |
| AI-05 | `{{TOPIC}}`, `{{EXAM_CONTEXT}}`, `{{PART_PLAN_JSON}}`, `{{SOURCE_SLICE}}`, `{{PART_ANALYSIS_JSON}}`, `{{ALL_DEFINITIONS_JSON}}`, `{{ALL_FORMULAS_JSON}}`, `{{BUNDLE_SELECTIONS_JSON}}`, `{{SUBJECT_STRATEGY}}` |
| AI-06A | `{{USER_MESSAGE}}`, `{{PART_PLAN_JSON}}`, `{{BLUEPRINT_JSON}}`, `{{BUNDLE_SELECTIONS_JSON}}`, `{{PART_ANALYSIS_JSON}}` |
| AI-06B | `{{TARGET_SECTION}}`, `{{USER_DIRECTION}}`, `{{PART_PLAN_JSON}}`, `{{BLUEPRINT_JSON}}`, `{{LOCKED_SECTIONS_JSON}}`, `{{PART_ANALYSIS_JSON}}` |
| AI-07A | `{{TOPIC}}`, `{{EXAM_CONTEXT}}`, `{{PART_PLAN_JSON}}`, `{{SOURCE_SLICE}}`, `{{PART_ANALYSIS_JSON}}`, `{{ALL_DEFINITIONS_JSON}}`, `{{ALL_FORMULAS_JSON}}`, `{{BLUEPRINT_JSON}}`, `{{BUNDLE_SELECTIONS_JSON}}`, `{{CA_RESULTS_JSON}}` |
| AI-07B | `{{IMAGE_REQUEST_JSON}}`, `{{SURROUNDING_CONTEXT}}`, `{{PART_PLAN_JSON}}`, `{{IMAGE_STYLE_SELECTION_JSON}}`, `{{USER_DIRECTION}}` |
| AI-07C | `{{IMAGE_TITLE}}`, `{{IMAGE_LEARNING_GOAL}}`, `{{EXPANDED_IMAGE_PROMPT}}` |
| AI-07D | `{{CURRENT_DATE}}`, `{{CA_QUERY}}`, `{{TOPIC}}`, `{{EXAM_CONTEXT}}`, `{{PART_PLAN_JSON}}`, `{{CA_QUERY_PURPOSE}}` |
| AI-07E | `{{PART_PLAN_JSON}}`, `{{BLUEPRINT_JSON}}`, `{{CURRENT_GENERATED_PART_JSON}}`, `{{IMAGE_ASSETS_JSON}}`, `{{BUNDLE_SELECTIONS_JSON}}` |
| AI-07F | `{{SELECTED_TEXT}}`, `{{SURROUNDING_CONTEXT}}`, `{{PART_PLAN_JSON}}`, `{{BUNDLE_SELECTIONS_JSON}}`, `{{USER_DIRECTION}}` |
| AI-07G | `{{USER_MESSAGE}}`, `{{SELECTED_TEXT}}`, `{{CURRENT_GENERATED_PART_JSON}}`, `{{BLUEPRINT_JSON}}`, `{{PART_PLAN_JSON}}`, `{{BUNDLE_SELECTIONS_JSON}}` |
| AI-07H | `{{PART_PLAN_JSON}}`, `{{BLUEPRINT_JSON}}`, `{{CURRENT_GENERATED_PART_JSON}}`, `{{IMAGE_ASSETS_JSON}}`, `{{CA_RESULTS_JSON}}`, `{{SOURCE_SLICE}}`, `{{TRACEABILITY_JSON}}` |
| AI-07I | `{{ALL_APPROVED_PARTS_JSON}}`, `{{DEEP_ANALYSIS_JSON}}`, `{{ALL_BLUEPRINT_PLANS_JSON}}`, `{{ALL_IMAGE_ASSETS_JSON}}`, `{{SETTINGS_JSON}}` |
| AI-07J | `{{NEW_TOPIC}}`, `{{NEW_SUBTOPICS_JSON}}`, `{{GLOBAL_BUNDLE_SELECTIONS_JSON}}`, `{{CA_TOGGLE}}` |
| AI-07K | `{{VALIDATION_SUGGESTION_JSON}}`, `{{PART_PLAN_JSON}}`, `{{IMAGE_ASSETS_JSON}}` |
| CTX-LOC | `{{LOCATION_NAME}}`, `{{LOCATION_CONTEXT_JSON}}`, `{{PART_PLAN_JSON}}`, `{{SOURCE_SLICE}}` |
| CTX-PER | `{{PERSON_NAME}}`, `{{PERSON_CONTEXT_JSON}}`, `{{EXAM_CONTEXT}}`, `{{PART_PLAN_JSON}}` |
| CTX-FORM | `{{FORMULA_RECORD_JSON}}`, `{{SOURCE_SLICE}}`, `{{PART_PLAN_JSON}}`, `{{BUNDLE_SELECTIONS_JSON}}` |

## Bundle Fragments (BND-*)
All 12 fragments stored verbatim in `DEFAULT_PROMPTS`: BND_GEO, BND_PER, BND_FORM, BND_DATA, BND_LAW, BND_TIME, BND_STORY, BND_ADM, BND_PROC, BND_CS, BND_MED, BND_CA.  
Full verbatim text: Document 3, Section 4B.

---

# PART 4 — TESTING MATRIX

| Phase | Test Count | Key Binary Sign-off |
|---|---|---|
| 0 Foundation | 12 | No raw AI dangerouslySetInnerHTML |
| 1 Input/Source | 12 | pageMap non-empty; guaranteed_topics intact |
| 2 Analysis | 12 | 3 separate AI calls in promptHistory |
| 3 Parts | 10 | Bundle chips from applied_bundles; merge works |
| 4 Blueprint | 12 | AI-06A modifies only detected scope |
| 5 Notes/Renderer | 14 | All 17+ containers render; source slice correct |
| 6 Visual/CA | 12 | All image origins use one chain; CA URLs validated |
| 7 Approval/Validate | 12 | Sequential Approve All with progress |
| 8 Export/Resilience | 12 | Screen 8 = zero AI calls |
| 9 QA Audit | 12 | All 26 Doc 5 gaps verified |
| **Total** | **110** | |

---

# PART 5 — HONEST DECLARATION

## 5A: Binary Current Status (Pre-implementation)

| Item | Status |
|---|---|
| geminiGenerateText / Search / Image exist and work | DONE |
| All 8 screens rendered (some partial/stub) | DONE |
| Navigation forward/backward | DONE |
| IndexedDB persistence (basic) | DONE |
| Dark mode | DONE |
| Canonical Doc 3 prompts in DEFAULT_PROMPTS | NOT DONE |
| 3-prompt analysis hybrid (AI-03A/B/C) | NOT DONE |
| Page map from PDF extraction | NOT DONE |
| Safe structured block renderer (17+ types) | NOT DONE |
| AI-02A/B extraction failover | NOT DONE |
| Retry logic with backoff | NOT DONE |
| Prompt history before every call | NOT DONE |
| Schema validation on AI response | NOT DONE |
| Anchor system for image insertion | NOT DONE |
| 4-tag traceability (incl. WEB_SOURCED) | NOT DONE |
| CTX-LOC / CTX-PER / CTX-FORM | NOT DONE |

## 5B: Unknowns and Assumptions

1. **API key injection:** Empty string in all three functions. Assumes browser runtime injection. If build step needed, out-of-scope.
2. **Token limits for large PDFs:** 500-page PDF = 200,000+ tokens. Assumes Gemini 1.5+ with 1M context. Must validate with target model.
3. **AI-07I input size:** Sending all approved parts may be large. Doc 4 context policy says summaries only when needed. Exact truncation requires testing.
4. **Streaming:** Doc spec mentions real-time streaming. Current `geminiGenerateText` is non-streaming. Listed as enhancement for Phase 5.
5. **Subject strategy text:** Referenced in old code comments; full canonical text not confirmed in provided documents. If required, must be confirmed from Doc 3 §4 subject strategy section.

## 5C: Phase Risk Assessment

| Phase | Risk | Reason |
|---|---|---|
| 0 Foundation | Low | Infrastructure only |
| 1 Input/Source | Medium | PDF chunking correctness |
| 2 Analysis | High | 3-prompt pipeline with routing logic is most complex change |
| 3 Parts | Low | Well-defined canonical prompt |
| 4 Blueprint | Medium | Surgical patch logic |
| 5 Notes/Renderer | High | 17+ container types, anchor system |
| 6 Visual/CA | Medium | Anchor resolution, URL validation |
| 7 Approval/Validate | Medium | Sequential Approve All flow |
| 8 Export/Resilience | Low | Pure formatting; stress tests |
| 9 QA | Medium | Gap register audit completeness |

---

# PART 6 — CROSS-REFERENCE INDEX

## Document 5 Gap → Implementation Phase Mapping

| Doc 5 Gap # | Requirement Summary | Phase |
|---|---|---|
| 1 | Dynamic routed bundle detection | Phase 2 (AI-03C + BND-*) |
| 2 | Multiple sub-topics, AI expansion/approval | Phase 1 (AI-01A) |
| 3 | AI Draft Text multi-step flow | Phase 1 (AI-01A + AI-01B) |
| 4 | Resume repopulates UI fields | Phase 0 (state schema + handleResume) |
| 5 | navigate() vs navTo() semantics | Phase 0 (navigateForward vs navigateBack) |
| 6 | Screen 4 edit modal with all fields | Phase 3 (EditPartModal) |
| 7 | Prompt visibility, copy, editable | Phase 0 (PromptCenter + prompt history) |
| 8 | Content-driven cross-domain logic | Phase 2 (AI-03A secondary_domains + AI-03C) |
| 9 | Context-driven location facts | Phase 5 (CTX-LOC) |
| 10 | PSC-relevant personality facts | Phase 5 (CTX-PER) |
| 11 | Formula operations deep dive | Phase 5 (CTX-FORM) |
| 12 | Dynamic image insertion at 3 moments | Phase 6 (AI-07E, AI-07K, unified chain) |
| 13 | AI smart default image style + override | Phase 4 (AI-05 image_plan) + Phase 6 (AI-07B) |
| 14 | CA plan in blueprint; execute in Stage 7 | Phase 4 (AI-05 ca_plan) + Phase 6 (AI-07D) |
| 15 | 4-tag traceability (WEB_SOURCED) | Phase 5 (SourceTag) |
| 16 | Per-part bundle inheritance with evidence | Phase 3 (AI-04 applied_bundles) |
| 17 | Blueprint chat surgical patch + undo | Phase 4 (AI-06A) |
| 18 | Sliced source + scoped analysis + global defs/formulas | Phase 5 (buildSourceSlice + buildPartAnalysis) |
| 19 | Remove/Add parts on Screen 7 | Phase 7 (remove + AI-07J) |
| 20 | Per-part Approve Text/Images + Approve All | Phase 7 (PartApprovalBar + sequential) |
| 21 | Per-part AI-07H + final AI-07I | Phase 7 (ValidationPopup + FinalValidationPopup) |
| 22 | Safe output, anchor rules | Phase 0 (renderSafeBlock) + Phase 5 (anchor system) |
| 23 | Retry with error classification | Phase 0 (retryAI) |
| 24 | Semantic chunking + structured merge | Phase 1 (chunkSource + mergeChunkAnalyses) |
| 25 | Settings, grounding, cache, telemetry | Phase 0 (model settings) + Phase 8 (diagnostics) |
| 26 | Export is pure no-AI formatting | Phase 8 (Screen8Export) |

---

## End of IMPLEMENTATION_PLAN v2

**File:** `F:\Code by Akshat\testgemini\studyforge\implementation plan\IMPLEMENTATION_PLAN_v2.md`  
**Cross-references:** Documents 1–7, Mandatory Architecture Analysis, `studyforge_main.html` (3,318 lines).  
**All prompts:** Verbatim from Document 3 + Amendment 1. No wording changed.
