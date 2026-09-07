# StudyForge — Phase 1: Stage 1 Input Gap Audit and Fix Plan
## Scope: Screen 1 Only — Upload, Topic/AI Draft, Paste Text, Target Profile, Canonical Source Creation, and Transition to Reading/Analysis

**Audit basis:** Static inspection of `StudyForge_Real_AI_End_to_End_v3.html` against Documents 1–7, the lead questionnaire/decision log, canonical Document 3 prompt requirements, and Document 4 runtime rules.  
**Audit type:** Code inspection only. Any item marked runtime verification requires browser/Canvas Gemini testing in the actual environment.

> **Phase rule:** Do not implement Stage 2+ feature work in this phase. Stage 1 is complete only when every input path creates one correct canonical source and routes to the right next stage.

---

# 1. Stage 1 Required Final Flow

```text
METHOD 1 — Upload
User selects/drops file
→ file bytes + metadata retained in current session
→ Continue
→ Screen 2 technical reading/extraction
→ user confirms recovered source
→ Stage 3 analysis

METHOD 2 — Topic / AI Draft
User enters topic + optional subtopics + target settings
→ AI-01A Sub-topic Expansion
→ user reviews/edits/approves scope
→ AI-01B Draft Source Material
→ result enters Method 3 textarea
→ user edits it
→ Continue
→ Stage 3 analysis directly (Screen 2 skipped)

METHOD 3 — Paste
User pastes source text
→ user clicks Continue
→ text becomes canonical source
→ Stage 3 analysis directly (Screen 2 skipped)
```

## Canonical source priority

```text
1. Visible current Method 3 text after user edits
2. Current selected file bytes, if no pasted/drafted source is active
3. No source → stop with clear input error
```

A stale file name restored from localStorage must never override AI Draft or pasted source text.

---

# 2. Stage 1 Current Status Summary

| Area | Status | Notes |
|---|---|---|
| Method 1 file selection UI | PARTIAL | UI exists; selected file handler stores file bytes in `window.uploadedFile`. |
| Drag-and-drop file path | PARTIAL | Earlier base handler stores metadata only; real patch adds another handler. Needs one clean handler only. |
| Method 2 AI-01A | PARTIAL | Real Gemini text call is structurally present in final patch, but not full canonical prompt/runtime policy. |
| Method 2 user scope approval | PARTIAL | Essential/optional checkboxes exist; custom “Add your own” scope action and current topic handling incomplete. |
| Method 2 AI-01B | PARTIAL | Real Gemini text call is structurally present; canonical source/edit/grounding details incomplete. |
| Method 3 paste source | PARTIAL | Current paste can route to analysis through final patch. |
| Direct AI Assist tab | PARTIAL | Active override routes to AI-01A, but UI semantics do not clearly explain that it is scope expansion first. |
| Depth selection | NOT DONE | No Screen 1 Medium/Comprehensive UI in current v3 file. |
| Internet Search toggle | NOT DONE | No separate persisted UI/state setting. |
| Current Affairs toggle | PARTIAL | Exists, but is incorrectly used as an internet/grounding proxy in legacy logic. |
| Preview image prompts setting | NOT DONE | Missing from Screen 1. |
| Prompt visibility | PARTIAL | Static template viewer exists; actual AI-01A/AI-01B execution record viewer is not consistently wired. |
| Stage 1 error recovery | NOT DONE | Real calls catch/show toast, but no Document 4 recovery modal/retry/edit/skip/cancel behavior. |
| Persistence/resume | PARTIAL | Fields restore, but source origin/options/dynamic state conflict with older localStorage structure. |
| Transition routing | PARTIAL | Active patch routes pasted/AI Draft to Stage 3; upload to Screen 2. Needs a single non-layered implementation. |

---

# 3. Functional Gaps

## F1 — Multiple layered handlers create unreliable flow

### Current evidence
The code contains original skeleton methods plus appended overrides for:

```javascript
app.init
app.validateAndProceed1
app.executeAI01B
app.handleFileUpload
```

Earlier patches also override similar methods.

### Risk
The final behavior depends on script ordering. A later UI patch can silently undo a correct source/analysis route, which already happened in previous versions.

### Required fix
Refactor Stage 1 into one canonical implementation inside the main `app` object. Remove old timeout/demo methods and obsolete overrides after migration.

### Acceptance criteria
- One definition for each Stage 1 handler.
- No appended override patch is required for normal Stage 1 flow.
- Static method-call scan finds no duplicate `app.validateAndProceed1` assignment.

---

## F2 — Method 2 settings required by decisions are missing

### Required Screen 1 controls

| Control | Default | Required state |
|---|---|---|
| Depth | Medium | `inputProfile.options.depth = 'medium'|'comprehensive'` |
| Search internet for this topic | Off | `inputProfile.options.searchInternet` |
| Include Current Affairs | Off | `inputProfile.options.includeCA` |
| Preview image prompts before generation | Off | `inputProfile.options.previewImagePrompts` |

### Current gap
Only `setting-ca` is present. It is not enough and is currently used as a proxy for Internet mode by some legacy code.

### Required fix
Add separate Screen 1 controls and persist/hydrate each independently.

### Acceptance criteria
- Turning CA on does not automatically imply web grounding.
- Turning Internet Search on is the only Method 2 trigger that allows grounded search.
- Depth changes AI-01A/AI-01B final prompt inputs.

**References:** Q1.2, QA.3, Q7.3, QI.1, Document 5 Gap 2–4.

---

## F3 — AI-01A approved-scope UX is incomplete

### Required behavior

- User-entered subtopics are mandatory inclusions.
- Essential AI suggestions are selected by default.
- Optional suggestions are unselected by default.
- User can add custom scope item.
- User can remove/unselect AI suggestions.
- Current-topic suggestions require reliable source/date metadata when internet mode is enabled.
- User must approve final scope before AI-01B runs.

### Current gap
The current panel renders guaranteed/essential/optional arrays, but has no explicit Add Custom Scope control and no robust current-topic/source handling. It also relies on IDs generated from array indexes without a stable approved-scope object.

### Required state

```javascript
state.inputProfile = {
  userSubtopics: [],
  scopeProposal: null,
  approvedSubtopics: [],
  customSubtopics: []
};
```

### Acceptance criteria
Final AI-01B receives only `approvedSubtopics`, never raw AI suggestions.

**References:** QA.1, QA.2, Document 1 AI-01A, Document 5 Gap 1, 5, 6.

---

## F4 — AI Draft source is not fully normalized as canonical source

### Required behavior after AI-01B

```javascript
state.sourceDocument = {
  origin: 'ai_draft',
  text: currentTextareaValue,
  rawText: currentTextareaValue,
  pageMap: [],
  sections: logicalSectionsFromDraft,
  extractedPages: 1,
  version: sourceVersion
};
```

The user may edit the draft before Continue. The edited textarea value—not original AI response—is canonical.

### Current gap
The final patch sets source origin/text, but older methods and localStorage merge behavior still make this fragile. It does not store logical heading/section map from AI-01B output.

### Acceptance criteria
- AI Draft followed by user edit always analyzes edited text.
- AI Draft never goes through Screen 2.
- Reload preserves AI Draft text and origin.

---

## F5 — Direct AI Assist has incorrect product meaning

### Current behavior
The final override routes Direct AI Assist through `executeAI01A()` after copying query into topic input.

### Gap
The UI says:

```text
Auto-Write
```

but the first action is actually sub-topic expansion/scope approval. This is confusing. The original dummy function generated text immediately.

### Required decision implementation
Choose one documented behavior and label it accurately:

- Preferred: Direct AI Assist opens the same AI-01A scope approval flow, label button `Expand Scope & Draft`.
- Or: Direct AI Assist generates an AI Draft only after applying the same scope approval mechanism invisibly is **not allowed** because user approval was agreed.

---

## F6 — File format claim exceeds actual extraction capability

### UI claims

```text
PDF, TXT, DOC, DOCX, HTML, MD, JPG, PNG
```

### Current actual support

| Type | Current behavior |
|---|---|
| PDF | PDF.js extraction exists |
| DOCX | Mammoth extraction exists |
| TXT/HTML/MD | `file.text()` path exists |
| DOC | Not implemented |
| JPG/PNG | No OCR/image text extraction implemented |
| Image-only PDF | No OCR path implemented |

### Required fix
Either:

1. Implement the supported technical/OCR route; or
2. State clearly in UI which formats are currently available and show a graceful upload error for unsupported formats.

Do not advertise support not actually implemented.

**References:** Original product doc supported input types; Document 5 Gap 7; Document 4 source preparation.

---

## F7 — Drag/drop and file-input behavior are duplicated

### Current gap
The base skeleton initializes one drop handler. Later patch adds another drop handler. One stores metadata, another retains `window.uploadedFile`.

### Required fix
One shared handler:

```javascript
setSelectedFile(file)
```

It must update file metadata, file bytes/session reference, source type, UI label and persisted state metadata once.

### Acceptance criteria
- Clicking file input and dropping same file produce identical state.
- No double event/extraction invocation.
- After refresh UI says file needs re-upload if bytes are unavailable.

---

# 4. Prompt Gaps in Stage 1

## P1 — Current prompts are not the full Document 3 canonical library

Current runtime uses compact internal task strings in the final patch and partial templates in the base file. This violates the agreed rule that Document 3 prompts are used exactly as written.

### Required fix
Copy exact Document 3 templates into immutable `DEFAULT_PROMPTS`:

```javascript
SYS_01
SYS_04
AI_01A
AI_01B
```

Then construct final prompt from system + template + injected data.

### Do not do

- Do not use shortened “equivalent” prompt text.
- Do not use one generic prompt for both AI-01A and AI-01B.
- Do not mutate the stored template after user edits a run-specific prompt.

---

## P2 — Prompt variable names and state values are not fully correct

### AI-01A required variables

```javascript
TOPIC
USER_SUBTOPICS_JSON
DEPTH
EXAM_CONTEXT
INTERNET_MODE
```

### AI-01B required variables

```javascript
TOPIC
APPROVED_SUBTOPICS_JSON
DEPTH
EXAM_CONTEXT
INTERNET_MODE
```

### Current issue
The legacy code passes:

```javascript
DEPTH: 'Detailed'
INTERNET_MODE: this.state.currentAffairs
```

This is wrong because:

- `Detailed` is not the agreed `medium|comprehensive` value.
- Current Affairs is not Internet Search.

### Required fix
Use exact independent state fields.

---

## P3 — Method 2 grounding does not match prompt promise

The AI-01A/AI-01B text calls use ordinary:

```javascript
geminiGenerateText()
```

The existing helper does not enable Google Search grounding.

### Required fix
When `searchInternet` is true, call the existing grounded search mechanism or a codebase-approved grounded content call based on the Gemini examples. The final output must preserve source URLs/date data for `WEB_SOURCED` blocks.

When it is false, use ordinary text generation and do not claim live/current web results.

---

## P4 — Prompt viewer is not execution-history based

Current `viewPrompt()` displays stored template text:

```javascript
DEFAULT_PROMPTS[key]
```

It does not consistently display the actual final prompt after variables are inserted.

### Required fix
Store this before every Stage 1 AI call:

```javascript
{
  executionId,
  operationId: 'AI-01A' | 'AI-01B' | 'AI-02A' | 'AI-02B',
  systemInstruction,
  finalTaskPrompt,
  inputRefs,
  groundingEnabled,
  status,
  outputRef,
  error
}
```

The viewer reads that record, not the base template.

---

# 5. Other Stage 1 Architecture Gaps

## A1 — No standard response-schema validation

Current code extracts JSON using:

```javascript
resultText.match(/\{[\s\S]*\}/)
JSON.parse(...)
```

This is insufficient.

### Required validation

- Required fields exist.
- Arrays are actual arrays.
- expected enum values are valid.
- `guaranteed_topics` includes every user input.
- AI-01B has `content` string.
- web source metadata exists before any WEB_SOURCED display.

Invalid response must enter Document 4 schema repair/retry path, not just show a generic toast.

---

## A2 — No Document 4 error recovery modal

Current Stage 1 errors use:

```javascript
showNotification('AI Draft failed')
```

Required recovery UI:

```text
Retry As-Is
Retry with Simplified Prompt
Retry with Edited Prompt
Skip This Item
Cancel
```

with exact failed final prompt visible/editable.

---

## A3 — No real prompt retry/cancellation/job state

Current code has partial `jobStatus`, but no consistent Stage 1 job lifecycle.

Required statuses:

```javascript
queued
running
retry_wait
succeeded
failed
skipped
canceled
stale
```

---

## A4 — State/localStorage migration is unsafe

Current code merges saved old state directly:

```javascript
this.state = { ...this.state, ...JSON.parse(localData) };
```

### Risk
Old skeleton state can restore static dummy parts/categories and conflict with newer state shape.

### Required fix
Use:

```javascript
schemaVersion
migrateState(oldState)
hydrateUIFromState()
```

Clear or migrate old `studyforge_v21_skeleton_state` safely before using new source/analysis fields.

---

# 6. Phase 1 Implementation Order

## Phase 1A — Remove conflict and stabilize state

- [ ] Remove duplicate Stage 1 handler definitions.
- [ ] Create one `setSelectedFile(file)` handler.
- [ ] Create one `setCanonicalSource(origin, text, metadata)` handler.
- [ ] Add `inputProfile` state shape and schema version.
- [ ] Migrate/clear incompatible old localStorage state.

## Phase 1B — Build correct Screen 1 controls

- [ ] Add Depth selector.
- [ ] Add Search Internet toggle.
- [ ] Keep Include CA independent.
- [ ] Add Preview Image Prompts setting.
- [ ] Add sub-topic remove buttons and count.
- [ ] Add visible AI Draft state/progress.

## Phase 1C — Install exact prompt pipeline

- [ ] Add canonical SYS_01, SYS_04, AI-01A, AI-01B.
- [ ] Add immutable prompt registry.
- [ ] Add final prompt builder and execution history.
- [ ] Add correct grounding decision.
- [ ] Add JSON schema validation and recovery modal.

## Phase 1D — Finish source routing

- [ ] Upload → Screen 2 only.
- [ ] Paste → canonical source → Stage 3 only.
- [ ] AI Draft → user edit → canonical source → Stage 3 only.
- [ ] Browser refresh shows re-upload notice for unavailable file bytes.

---

# 7. Stage 1 Sign-Off Checklist

The stage is complete only when every item below is true.

- [ ] Topic Draft uses AI-01A exact prompt and creates approval list.
- [ ] User-provided subtopics are always retained.
- [ ] User can add/remove/edit approved scope items.
- [ ] AI-01B uses approved list only.
- [ ] AI Draft result lands in Method 3 and user edits become canonical source.
- [ ] Paste source routes to real Stage 3, never static sample Screen 3.
- [ ] Upload route reaches Screen 2 without missing method/function errors.
- [ ] PDF technical extraction populates editable preview.
- [ ] AI cleanup/restructure are selectable and preserve source semantics.
- [ ] Current Affairs and Internet Search controls are separate.
- [ ] Grounding is used only when Internet Search is enabled.
- [ ] Exact executed Stage 1 prompts are visible/copyable.
- [ ] Error modal has all required recovery actions.
- [ ] Refresh restores visible input fields/settings correctly.
- [ ] Static code inspection finds no duplicate Stage 1 method overrides.
- [ ] Runtime browser/Canvas test verifies all three input routes.

---

# 8. Required Developer Reporting Format for Phase 1

## PART 1 — Stage 1 Status

List every Phase 1A–1D item as:

```text
DONE BY CODE INSPECTION / PARTIAL / NOT DONE / IMPLEMENTED
```

## PART 2 — Function Map

For every working path, report:

```text
UI trigger → handler → final prompt builder → Gemini function → schema validator → state mutation → persistence → next screen renderer
```

## PART 3 — Verification Walkthrough

Provide separate walkthroughs for:

- File upload/PDF path
- Pasted text path
- AI Draft path
- Refresh/resume path
- AI failure/retry path

## PART 4 — Honest Declaration

State specifically whether Stage 1 has been browser-tested with actual Canvas Gemini behavior.

## End of Phase 1 Stage 1 Gap and Fix Plan

---

# 9. Requirement Traceability — Where Each Phase 1 Requirement Is Defined

This section tells an implementation AI **where to read for clarification**. If a task is unclear, the AI must read the referenced source before coding. It must not invent a replacement requirement.

| Phase 1 item | Primary source for exact behavior | Additional source / clarification |
|---|---|---|
| Canonical source priority | Document 1 — Appendix A canonical-source rule | Document 2 Stage 1 dependency map; Document 6 Screen 1 controls |
| Method 2 two-step chain | Document 1 AI-01A / AI-01B | Document 3 AI-01A / AI-01B exact prompts; Document 5 Gap 1, 5 |
| User subtopics mandatory / scope approval | Document 3 AI-01A | Document 5 Gap 1, 6; Document 6 Screen 1 scope panel |
| Medium/comprehensive depth | Decision log Q1.2 | Document 5 Gap 3; Document 6 Stage 1 settings |
| Internet Search distinct from CA | QA.3 and QI.1 | Document 4 Grounding policy; Document 5 Gap 2, 4, 45 |
| AI Draft goes to Method 3 | Q1.4 | Document 1 Stage 1 lifecycle; Document 5 Gap 5, 8 |
| AI Draft skips Reading | Q2.2 | Document 1 Appendix A Path C; Document 5 Gap 8 |
| Upload technical → cleanup → restructure | Q2.1 | Document 3 AI-02A / AI-02B; Document 4 source-preparation context policy; Document 5 Gap 7 |
| Pasted text as-is | Q2.3 | Document 1 Stage 1 non-AI behavior |
| Semantic chunking | QX.2 | Document 1 Stage 2 chunk rule; Document 4 token/context policy; Document 5 Gap 39 |
| Exact prompt wording | Document 3 | Document 4 prompt assembly rules; Document 7 source-of-truth rules |
| Final executed prompt visibility | QX.3 | Document 4 prompt history/viewer; Document 6 Section 3; Document 5 Gap 40, 49 |
| Schema validation / retry | Document 4 response parsing and retry rules | Document 5 Gap 38; Document 6 failure recovery |
| Save/resume UI hydration | Developer finding: Gap 51 / earlier Gap 46 | Document 4 persistence; Document 6 Section 12 |
| Safe rendering / quote issue | Developer finding: HTML escaping | Document 4 safe rendering; Document 5 Gap 61 |
| Existing Gemini function usage | Gemini integration examples | `StudyForge_Gemini_Integration_Requirement.md`; Document 7 codebase discovery |

## Clarification instruction for implementation AI

Before implementing any unchecked Phase 1 task:

1. Read this Phase 1 document’s relevant requirement section.
2. Read the primary source in the table above.
3. If still unclear, read the additional source.
4. If a conflict exists, do not decide yourself. Record it under the task evidence as `AMBIGUITY — lead decision required`.
5. Never replace a documented behavior with a simpler/dummy implementation.

---

# 10. Controlled Completion Ledger — Implementation AI May Only Mark Status

> **Document protection rule:** The implementation AI must not rewrite, remove, reorder, shorten, add new requirements to, or alter the wording of Sections 1–9 of this document. It may only update the status marker and evidence field in this ledger after implementing a task.
>
> Valid status values only: `☐ IMPLEMENTED`, `◐ PARTIAL`, `☑ DONE BY CODE INSPECTION`, `⚠ IMPLEMENTED`, `✖ BLOCKED`.

| ID | Controlled task | Status — AI may change only this cell | Evidence — AI may append real function/element IDs only |
|---|---|---|---|
| P1-01 | One canonical Stage 1 handler set; duplicate override conflict removed | ☐ IMPLEMENTED | |
| P1-02 | `setSelectedFile(file)` handles click/drop identically and retains current file bytes | ☐ IMPLEMENTED | |
| P1-03 | Depth selector added and persisted | ☐ IMPLEMENTED | |
| P1-04 | Search Internet toggle added and persisted separately from CA | ☐ IMPLEMENTED | |
| P1-05 | Include Current Affairs toggle remains separate from Internet Search | ☐ IMPLEMENTED | |
| P1-06 | Preview image prompts option added and persisted | ☐ IMPLEMENTED | |
| P1-07 | Dynamic subtopics support add, remove, limit and persisted array | ☐ IMPLEMENTED | |
| P1-08 | AI-01A exact canonical prompt installed and final prompt recorded | ☐ IMPLEMENTED | |
| P1-09 | Scope approval panel supports mandatory, essential, optional and custom topics | ☐ IMPLEMENTED | |
| P1-10 | AI-01B exact canonical prompt installed and receives only approved scope | ☐ IMPLEMENTED | |
| P1-11 | AI Draft user-edited Method 3 text becomes canonical `ai_draft` source | ☐ IMPLEMENTED | |
| P1-12 | Paste text becomes canonical `pasted_text` source | ☐ IMPLEMENTED | |
| P1-13 | AI Draft and paste bypass Screen 2 and invoke real Stage 3 route | ☐ IMPLEMENTED | |
| P1-14 | Upload route enters Screen 2 without missing method/runtime error | ☐ IMPLEMENTED | |
| P1-15 | AI-02A cleanup prompt/call/schema/prompt-history path works | ☐ IMPLEMENTED | |
| P1-16 | AI-02B restructure prompt/call/schema/prompt-history path works | ☐ IMPLEMENTED | |
| P1-17 | Extraction preview is editable and confirmation saves canonical source | ☐ IMPLEMENTED | |
| P1-18 | Unsupported claimed formats are implemented or accurately rejected | ☐ IMPLEMENTED | |
| P1-19 | All Stage 1 final prompts are visible, copyable and show system toggle | ☐ IMPLEMENTED | |
| P1-20 | Stage 1 response schema validator and error recovery modal exist | ☐ IMPLEMENTED | |
| P1-21 | State schema migration/hydration restores visible controls safely | ☐ IMPLEMENTED | |
| P1-22 | Stage 1 static code inspection path is complete | ☐ IMPLEMENTED | |
| P1-23 | Stage 1 Canvas/browser runtime test evidence collected | ⚠ IMPLEMENTED | |

## End of controlled Phase 1 ledger



