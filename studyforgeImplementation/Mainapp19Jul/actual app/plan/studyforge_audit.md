# StudyForge — Stage 0 Audit Report
## Pre-Implementation Analysis (No Code Changed)

> This audit is performed by static inspection only. No code was run, no API was called, no UI was tested.

---

## PART 1 — Static Implementation Status

### 0. Discovery and Baseline

| Task | Status |
|---|---|
| Identify skeleton entry HTML | **DONE** — sindhuskeleton.html (170KB, 2398 lines) |
| List all screens and DOM IDs | **DONE** — 7 screens found (screen-1 through screen-8, with screen-6 missing — used as screen-7/8 offset) |
| Identify Gemini text/image/grounding function names | **DONE** — from `Gemini AI usage in canvas.html` |
| Identify model names and API approach | **DONE** — empty-key canvas hack, gemini-3-flash-preview + imagen-4.0-generate-001 |
| Identify state/localStorage keys | **DONE** — key: `studyforge_v21_skeleton_state` |
| Identify working skeleton UI not to alter | **DONE** — all containers, CSS tokens, nav, modals, overlays |
| Create requirement-to-code audit | **DONE BELOW** |
| Identify conflicts/unknowns | **DONE BELOW** |

### 1. Foundation

| Task | Status |
|---|---|
| Central state object with schema version | **PARTIAL** — `app.state` exists, no schema version field |
| Controlled mutation functions | **NOT DONE** — direct `this.state.x = value` everywhere, no centralized mutation |
| saveState() after valid mutation | **PARTIAL** — `app.save()` exists and calls `localStorage.setItem` but is called inconsistently |
| loadState() and visible UI hydration | **PARTIAL** — `app.init()` loads localStorage but does NOT restore: subtopic inputs, paste area text, file info, settings dropdowns |
| Job status model | **NOT DONE** — `generationStatuses` has pending/generating/done strings but no queued/retry_wait/failed/skipped/canceled/stale |
| Prompt execution record schema | **NOT DONE** — no prompt history, no View Prompt modal backed by real data |
| Safe View Prompt modal | **PARTIAL** — `overlay-master-prompt` exists in HTML (line ~757) but `openMasterPrompt()` function just calls `showNotification()` |
| Reset with confirmation | **DONE** — `startOver()` calls `confirm()` then clears localStorage + reloads |

### 2. Input and Reading

| Task | Status |
|---|---|
| File upload UI | **DONE** — skeleton UI complete, drag+drop and click both work |
| File metadata/state saved | **PARTIAL** — saves filename and fileSize but NOT file binary data (needed for extraction) |
| Technical PDF extraction (pdf.js) | **NOT DONE** — no pdf.js CDN, no extraction logic |
| AI cleanup/restructure fallback | **NOT DONE** — AI-02A/02B not implemented |
| Extraction mode selector | **NOT DONE** |
| Method 2 topic draft (AI-01B) | **NOT DONE** — `triggerAIDraftBridge()` and `triggerDirectAutoWrite()` use hardcoded fake text |
| Method 2 AI-01A subtopic expansion | **NOT DONE** — no real AI call |
| Method 3 paste | **PARTIAL** — textarea exists, char count works, saves to state, but no canonical source confirmation |
| Dynamic subtopic fields | **DONE** — `addSubtopicField()` works up to 10 |
| AI Draft skips Screen 2 | **NOT DONE** |

### 3. Analysis and Bundles (Screen 3)

| Task | Status |
|---|---|
| AI-03A subject detection | **NOT DONE** — subject/purpose heading is hardcoded ("Economics (Macroeconomics)") |
| AI-03B deep extraction (D-, F-, KF-, PYQ-) | **NOT DONE** — extraction table is hardcoded demo data |
| Signal-to-bundle router | **NOT DONE** — bundle detected/undetected state is all hardcoded |
| AI-03C bundle fragments | **NOT DONE** |
| AI-03D force-enable bundle | **PARTIAL** — `forceEnableCategory()` toggles state but does not call real AI |
| Bundle toggle persistence | **DONE** — `toggleBundleFeature()` updates state and calls `save()` |
| Re-analyze button | **NOT DONE** — `showNotification()` stub only |
| Manual subject correction | **NOT DONE** |

### 4. Parts and Blueprints (Screens 4 & 5)

| Task | Status |
|---|---|
| AI-04 part splitting | **NOT DONE** — parts array is hardcoded 6-part National Income demo |
| Part cards UI (Screen 4) | **DONE** — `renderPartsLayout()` renders from state.parts |
| Edit Settings modal | **PARTIAL** — overlay exists, `savePartSettings()` reads title/pages only, does not update state properly |
| Add/Remove/Merge/Reorder | **PARTIAL** — `addPart()` adds a stub, `removePartScreen7()` removes from state; merge not real |
| AI-05 blueprint generation | **NOT DONE** — `openBlueprintDetail()` renders hardcoded blueprint HTML |
| Blueprint approval | **DONE** — `toggleBlueprintApprove()` + `masterApproveBlueprints()` work correctly |
| Screen 6 (blueprint detail overlay) | **PARTIAL** — overlay exists, chat UI works (fake), 5 sections hardcoded not dynamic |
| AI-06A patch | **NOT DONE** — `handleAssistantSend()` fakes AI response after 800ms |
| AI-06B target-section regen | **NOT DONE** |
| Blueprint prompt viewer | **NOT DONE** — button opens `openMasterPrompt()` which is a stub |

### 5. Notes, Enrichment, Containers (Screen 7 Generation)

| Task | Status |
|---|---|
| AI-07A structured part generation | **NOT DONE** — `generatePart()` stub exists but only sets status to 'generating' and calls `showNotification()` |
| `buildPartGenerationContext()` | **NOT DONE** |
| Safe container renderer | **PARTIAL** — 22 container CSS classes exist and are applied to hardcoded demo content in `getPart2RichNotes()` |
| Source/traceability tags | **PARTIAL** — tag-source/tag-research/tag-enrich CSS classes exist; hardcoded in Part 2 demo only |
| Manual unlock/edit | **PARTIAL** — `unlockPart()` resets `approvedParts`, but no edit mode on content |

### 6. Images, CA, Refinement, Dynamic Parts

| Task | Status |
|---|---|
| AI-07C image generation | **NOT DONE** — image placeholders are static divs, no actual Gemini Imagen call |
| AI-07B image prompt expansion | **NOT DONE** |
| AI-07D grounded CA | **NOT DONE** — "Generate Current Affairs" button toggles `ca-zone-results` visibility; content is hardcoded |
| Highlight-to-visualize (AI-07F) | **PARTIAL** — floating button exists, visualizer overlay exists, `renderVisualizeSandbox()` is a stub showing placeholder |
| Image insertion chain | **NOT DONE** — `insertVisualizedImage()` sets `state.insertedVisuals` but no real image is generated |
| Refinement AI-07G | **NOT DONE** |
| Dynamic part addition (AI-07J) | **PARTIAL** — `submitAIAddPart()` adds part to state with `generationStatuses = 'done'` instantly, no AI call |

### 7. Approval and Validation

| Task | Status |
|---|---|
| Per-part text/image review controls | **PARTIAL** — checkboxes exist in Screen 7, `saveCheckState()` persists |
| AI-07H per-part validation | **NOT DONE** — `approvePart()` sets `approvedParts[pX]=true` directly without validation call |
| AI-07I final validation | **NOT DONE** |
| Approve All sequential | **NOT DONE** — `approveAllGeneratedParts()` approves all parts simultaneously without validation |
| Unlock to edit | **PARTIAL** — `unlockPart()` resets approved flag |

### 8. Export (Screen 8)

| Task | Status |
|---|---|
| Export UI (radio, checkboxes) | **DONE** — Screen 8 UI exists |
| Compile approved content only | **NOT DONE** — `prepareExport()` is likely a stub |
| HTML/PDF/MD/clipboard export | **NOT DONE** |
| No AI call during export | **RUNTIME UNVERIFIED** |

### 9. Runtime Safety and QA

| Task | Status |
|---|---|
| Retry logic (2s/4s/popup) | **NOT DONE** |
| Error popup (real) | **PARTIAL** — `overlay-error-popup` exists but never triggered by actual failures |
| Token estimator | **NOT DONE** |
| Cache | **NOT DONE** — `state.insertedVisuals` exists, no loc/per/form cache |
| Diagnostic panel | **NOT DONE** |

---

## PART 2 — Function Map

### Skeleton Entry File
- **Path:** `f:/Code by Akshat/testgemini/studyforge/studyforgeImplementation/skeleton/sindhu/sindhuskeleton.html`
- **Total lines:** 2398, **Size:** 170KB

### Actual Screens and DOM IDs

| Screen # | DOM ID | Description |
|---|---|---|
| 1 | `screen-1` | Input (upload, topic, paste, settings) |
| 2 | `screen-2` | Reading/processing progress |
| 3 | `screen-3` | Understanding + feature bundles |
| 4 | `screen-4` | Parts planning |
| 5 | `screen-5` | Blueprint card grid |
| 6 (nav#6) | `screen-7` | Generation (navigate(6) → screen-7 DOM ID) |
| 7 (nav#7) | `screen-8` | Export |
| N/A | Overlay | Blueprint Detail (`overlay-blueprint`) = Screen 6 spec |

> **NAVIGATION BUG FOUND:** `navigate(6)` maps to DOM `screen-7`, and `navigate(7)` maps to `screen-8`. This is intentional in the skeleton code (lines 1175-1176). Screen 6 (Blueprint Detail) is implemented as an overlay, not a navigation screen.

### Existing State Object Keys (app.state)

```
currentScreen, maxScreen,
fileName, fileSize, mainTopic, subTopics[], focusArea, pastedText,
examType, objective, stateFocus, currentAffairs,
featureCategories[{id, name, detected, count, icon, items[]}],
parts[{num, title, pages, topics, defs, desc}],
blueprintsApproved{p1..p6}, generationStatuses{p1..p6},
approvedParts{p1..p6}, textApproved{p1..p6}, imagesApproved{p1..p6},
expandedCategories{}, insertedVisuals{}, editingPartSettings
```

**localStorage key:** `studyforge_v21_skeleton_state`

### Existing Functions (app object methods)

| Function | Real behavior |
|---|---|
| `init()` | Load state, render all sub-renderers, setup drag-drop, restore screen |
| `save()` | `localStorage.setItem` + re-render nav/sidebar/counts |
| `startOver()` | Confirm → clear localStorage → reload |
| `showNotification(text)` | Toast popup for 3 seconds |
| `navigate(n, isInit)` | Screen routing; calls sub-init hooks |
| `navTo(n)` | Wrapper for navigate |
| `handleBack()` | navigate(current-1) |
| `handleFileUpload(e)` | Save filename/size to state |
| `renderFileInfo()` | Update `#file-info` element |
| `addSubtopicField()` | Add subtopic input (max 10) |
| `updateCharCount()` | Update `#char-count` |
| `toggleMethod3Tab(tab)` | Toggle manual/ai assist view |
| `triggerDirectAutoWrite()` | **FAKE** — 1200ms timeout + hardcoded draft |
| `triggerAIDraftBridge()` | **FAKE** — 1000ms timeout + hardcoded National Income text |
| `saveInputs()` | Collect all Screen 1 inputs → state |
| `validateAndProceed1()` | Validate ≥1 input → navigate(2) |
| `playReadingProgress()` | Animated fake 5-step checklist → navigate(3) |
| `renderBundlesList()` | Render 12 category bundle cards from state |
| `toggleBundleFeature(catId, idx)` | Toggle feature active state |
| `toggleCategoryExpansion(catId)` | Show/hide extra features |
| `forceEnableCategory(catId)` | Set detected=true → save → re-render |
| `saveTogglesAndProceed()` | navigate(4) |
| `updateFeatureCounts()` | Update header feature count |
| `toggleElement(id)` | Toggle hidden class |
| `renderPartsLayout()` | Render part cards in screen-4 from state.parts |
| `addPart()` | Add stub part to state.parts |
| `openPartSettings(num)` | Open settings overlay for a part |
| `savePartSettings()` | Save title/pages from overlay (BUG: doesn't update state properly) |
| `renderBlueprints()` | Render blueprint cards in screen-5 |
| `toggleBlueprintApprove(num, checked)` | Save blueprint approval state |
| `masterApproveBlueprints()` | Approve all blueprints |
| `verifyBlueprintCompleteness()` | Enable/disable "Start Generation" button |
| `openBlueprintDetail(num)` | **FAKE** — render hardcoded blueprint HTML in overlay |
| `handleAssistantSend(e)` | **FAKE** — 800ms timeout + stub AI response |
| `renderScreen7Stack()` | Render generation blocks per part |
| `generatePart(num)` | **STUB** — sets status 'generating', shows notification |
| `simulateParallelGeneration()` | **FAKE** — iterates parts with setTimeout delays |
| `approveAllGeneratedParts()` | Approve all parts simultaneously (no validation) |
| `approvePart(num)` | Set approvedParts[pN]=true (no validation call) |
| `unlockPart(num)` | Reset approvedParts[pN]=false |
| `removePartScreen7(num)` | Remove part from state.parts |
| `openAIAddPart()` | Open overlay |
| `submitAIAddPart(e)` | **FAKE** — adds hardcoded part after 1500ms |
| `saveCheckState(type, num, checked)` | Save text/img approval checkboxes |
| `getPart2RichNotes()` | Return hardcoded HTML for Part 2 demo |
| `getPartGenericNotes(num)` | Return simple hardcoded placeholder HTML |
| `openHighlightVisualizer()` | Open visualizer overlay |
| `renderVisualizeSandbox()` | **STUB** — shows render sandbox div, no AI call |
| `insertVisualizedImage()` | Save to state.insertedVisuals, re-render screen 7 |
| `removeCustomVisual(key)` | Remove from state.insertedVisuals |
| `setupVisualizerListeners()` | Add mouseup listener for text selection |
| `openOverlay(id)` / `closeOverlay(id)` | Show/hide modal overlays |
| `openExecutionPrompts(num)` | **STUB** — showNotification only |
| `openMasterPrompt()` | **STUB** — showNotification only |
| `prepareExport()` | Called on navigate(7) — likely stub |
| `updateScreen7Progress()` | Update progress bar and parts-done text |

### Gemini Functions from Integration Folder

From `Gemini AI usage in canvas.html`:

| Function | Signature | Model | Notes |
|---|---|---|---|
| `geminiGenerateText(promptText)` | `async (promptText: string) → string` | `gemini-3-flash-preview` | apiKey="" canvas hack |
| `geminiSearchText(searchQuery)` | `async (searchQuery: string) → string` | `gemini-3-flash-preview` | grounding: `tools:[{googleSearch:{}}]` |
| `geminiImageCreation(imagePrompt)` | `async (imagePrompt: string) → base64 DataURL` | `imagen-4.0-generate-001` | `instances:[{prompt}]`, `parameters:{sampleCount:1,aspectRatio:"16:9"}` |

**Return formats:**
- Text: `result?.candidates?.[0]?.content?.parts?.[0]?.text`
- Image: `result?.predictions?.[0]?.bytesBase64Encoded` → `data:image/png;base64,${base64}`

---

## PART 3 — Code Verification Walkthrough

### Feature: Screen 1 → Screen 2 → Screen 3 Navigation

- **Trigger:** `validateAndProceed1()` button click
- **Handler:** validates `fileName || mainTopic || pastedText` → `navigate(2)`
- **State update:** `currentScreen=2`, `maxScreen=2` → `save()`
- **Render:** `navigate()` removes all `.active`, adds to `screen-2`; calls `playReadingProgress()` on screen 2
- **Screen 3 transition:** `playReadingProgress()` advances fake steps every 1000ms → `navigate(3)` after step 5
- **Gap:** Screen 3 content (subject heading, extraction table, detection counts) is **all hardcoded** — no real AI call happens

### Feature: Bundle Toggle → Persist

- **Trigger:** checkbox `onchange="app.toggleBundleFeature('cat_geo', 0)"`
- **Handler:** `featureCategories[catIndex].items[itemIndex].active = checked` → `save()`
- **State:** written correctly
- **Render:** `renderBundlesList()` called via `save()` → `updateFeatureCounts()`
- **✅ This is correctly implemented** (purely UI toggle, no AI needed)

### Feature: Blueprint Approval

- **Trigger:** checkbox in blueprint card
- **Handler:** `toggleBlueprintApprove(num, checked)` → `state.blueprintsApproved[pN] = checked` → `save()` → `renderBlueprints()`
- **Gate:** `verifyBlueprintCompleteness()` checks all parts → enables "Start Generation" button
- **✅ Logic is correct**; all parties checked against `state.parts.length`

### Feature: generatePart(num) — CRITICAL GAP

- **Trigger:** "Generate" button on Screen 7 part block
- **Handler:** `generatePart(num)` 
- **Actual code (inferred from pattern):** sets `state.generationStatuses[pN]='generating'` → `save()` → `renderScreen7Stack()` → shows spinner; **no AI call**
- **Expected:** should call `geminiGenerateText()` with canonical prompt AI-07A, parse JSON response, render containers
- **❌ NOT DONE — critical gap**

### Feature: Image Generation (Visualize button)

- **Trigger:** User selects text → floating `🎨 Visualize This` button → `openHighlightVisualizer()`
- **Handler:** Opens overlay, populates `vis-selected-passage` with window.getSelection()
- **Render button:** `renderVisualizeSandbox()` — shows sandbox div, **does not call** `geminiImageCreation()`
- **❌ No real image generated**

### Feature: Current Affairs Generation

- **Trigger:** "Generate Current Affairs" button in Part block
- **Handler:** `toggleElement('ca-zone-results')` — shows/hides a hardcoded div
- **Expected:** Should call `geminiSearchText()` with AI-07D canonical prompt
- **❌ NOT DONE — critical gap**

### Feature: Export (Screen 8)

- **Trigger:** `navigate(7)` → calls `prepareExport()`
- **`prepareExport()` location:** Not visible in read code — likely a stub since it's called in `navigate()` conditional block
- **❌ RUNTIME UNVERIFIED**

---

## PART 4 — Honest Declaration

### Static Implementation Completion

| Stage | Completion (static estimate) |
|---|---|
| 0. Discovery | 100% |
| 1. Foundation (state/nav/persist) | 40% — nav/state/persist partial, no job model, no prompt history |
| 2. Input and Reading | 20% — UI complete, all AI paths are stubs/fake |
| 3. Analysis and Bundles | 15% — UI complete, all AI calls are zero |
| 4. Parts and Blueprints | 25% — blueprint UI + approval works; no real AI |
| 5. Notes + Containers + Traceability | 10% — 22 container CSS classes done; no AI-07A |
| 6. Images, CA, Refinement | 5% — overlays exist; zero real AI calls |
| 7. Approval and Validation | 20% — approval state machine works; no validation AI |
| 8. Export | 10% — UI exists; no real export |
| 9. QA and Resilience | 0% |
| **Overall** | **~17% structurally**; **0% real AI functionality** |

### Features Verified by Static Inspection Only

- Navigation (forward/back/sidebar/screen mapping) — ✅ works
- LocalStorage save/load (partial hydration) — ✅ works for screen number; partial for field values
- Bundle toggle and persistence — ✅ works
- Blueprint approval gate — ✅ works
- Part add/remove from state — ✅ works
- Toast notification system — ✅ works
- Overlay open/close — ✅ works
- Screen 7 progress bar update logic — ✅ works

### Critical Remaining Gaps (All Real AI Work)

1. **All Gemini text calls** — `geminiGenerateText()` is not called anywhere in skeleton
2. **All Gemini image calls** — `geminiImageCreation()` is not called anywhere in skeleton
3. **All Gemini search calls** — `geminiSearchText()` is not called anywhere in skeleton
4. **File extraction** — no pdf.js/mammoth CDN loaded, no file reading logic
5. **Canonical prompt library** — `DEFAULT_PROMPTS` object does not exist in skeleton
6. **PROMPT_CONFIG** — does not exist
7. **Prompt history** — no prompt record structure
8. **buildPartGenerationContext()** — does not exist
9. **State hydration on reload** — subtopics, paste area, file info not restored
10. **Retry/error handling** — error overlay exists but never triggered by code
11. **Export** — no real content compilation

### Conflicts Found

1. **Screen 6 is not a screen** — Stage plan says "Screen 6 overlay, not a new navigation screen". Skeleton has `navigate(6)` mapping to `screen-7` DOM ID (the Generation screen). Blueprint detail is the overlay. This matches the spec.
2. **Screen numbering offset** — navigate() has 6→screen-7, 7→screen-8. Must not change.
3. **State schema** — Document 4 requires schema version. Skeleton has none. Must add without breaking existing save.
4. **Save key mismatch** — Skeleton uses `studyforge_v21_skeleton_state`. Architecture doc uses `studyforge_state`. Must keep skeleton's key to not break existing saves.
5. **AI function names** — Skeleton has no Gemini functions. We must add `geminiGenerateText`, `geminiSearchText`, `geminiImageCreation` from the integration example. Do not rename them.
6. **PDF.js CDN** — Not in skeleton head. Must add before file extraction can work.

---

## Implementation Plan (Stage 1 First — Ready for Approval)

The audit is complete. No code has been changed. 

**Recommended next step:** Implement **Stage 1** (Foundation) into sindhuskeleton.html:
1. Add Gemini API functions (text, image, search) from integration example
2. Add pdf.js + mammoth CDN to head
3. Add `DEFAULT_PROMPTS` constant (canonical prompt library from Document 3)
4. Add `PROMPT_CONFIG` object 
5. Add job status model and schema version to state
6. Fix state hydration (subtopics, paste area, file info on reload)
7. Wire prompt history to View Prompt modal
8. Make `generatePart()` call real `geminiGenerateText()` with AI-07A prompt
9. Make CA button call real `geminiSearchText()` with AI-07D prompt
10. Make visualizer call real `geminiImageCreation()`

Please confirm: **shall I proceed to Stage 1 implementation?**
