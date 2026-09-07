# StudyForge — Phase 2: Stage 2 Reading and Source-Preparation Gap Audit and Fix Plan
## Scope: Screen 2 Only — Technical Extraction, File Quality Assessment, AI Cleanup/Restructure Fallback, Source Confirmation, Chunk Preparation, and Handoff to Stage 3

**Audit basis:** Static inspection of the current StudyForge skeleton/integration versions against Documents 1–7, the lead decisions, Document 3 canonical prompts, and Document 4 runtime rules.  
**Audit type:** Static code/document inspection only. Browser, PDF, OCR, Canvas Gemini, and live file testing remain runtime-unverified.

> **Phase rule:** Do not add Stage 3 analysis, Stage 4 splitting, blueprints, notes, images, CA, validation, or export work in this phase. Stage 2 is complete only when every supported source is either prepared accurately or rejected/recovered transparently before Stage 3 receives it.

---

# 1. Stage 2 Required Final Flow

```text
Input source arrives from Stage 1
  │
  ├─ AI Draft or pasted text
  │    → already canonical
  │    → skip Screen 2
  │    → Stage 3 entry point
  │
  └─ Uploaded file
       → Screen 2
       → technical extraction (Tier A)
       → quality assessment
          ├─ usable → editable preview + Confirm & Use
          ├─ poor → automatically try AI-02A cleanup (Tier B)
          │          ├─ usable → preview + Confirm & Use
          │          └─ inadequate → automatically try AI-02B restructure (Tier C)
          │                         → preview + unresolved spans + Confirm & Use
          └─ unrecoverable → preserve diagnostic + paste/re-upload/retry choices
       → user confirms current preview text
       → canonical source is saved
       → Stage 3 entry point
```

## Stage 2 source-preservation rule

Stage 2 may repair extraction damage and reconstruct supported structure. It must not add subject knowledge, current affairs, formulas, examples, definitions, citations, or external facts.

---

# 2. Current Status Summary

| Area | Status | Current gap |
|---|---|---|
| Screen 2 UI shell | Present | Progress UI exists, but reading controller was missing in base code. |
| `playReadingProgress()` | Missing in original; patch-dependent | Must become a single canonical main-app method. |
| PDF technical extraction | Partial | PDF.js path exists; quality assessment/cascade incomplete. |
| DOCX extraction | Partial | Mammoth path exists; page/section map is weak. |
| TXT/HTML/MD extraction | Partial | Uses `file.text()` with no normalization/section mapping. |
| DOC format | Not supported | UI claims support but no parser exists. |
| JPG/PNG OCR | Not supported | UI claims support but no OCR/multimodal extraction exists. |
| Image-only PDF OCR | Not supported | No OCR fallback path. |
| Tier A quality check | Partial | Uses only simple text-length threshold. |
| AI-02A cleanup | Partial | Call/template exists but not complete canonical prompt/runtime/history/schema behavior. |
| AI-02B restructure | Partial | Call/template exists but often uses raw text again and does not retain cleaned state/section map robustly. |
| Automatic A → B → C cascade | Not done | Current UI presents manual buttons; it does not auto-failover. |
| User manual A/B/C choice | Partial | Cleanup/restructure buttons exist; technical-only/reset/error choices incomplete. |
| Editable source preview | Present | Needs canonical-source confirmation and source-preservation metadata. |
| Unresolved sections | Missing | Not represented in UI/state consistently. |
| Long source handling | Missing | Current AI cleanup/restructure truncates `SOURCE_TEXT` with `substring(0, 30000)`. |
| Prompt visibility/history | Partial | Static template viewer, not actual final execution record. |
| Stage 2 → Stage 3 route | Partial | Confirm handler must invoke the real Stage 3 entry point, not just navigate to static Screen 3. |

---

# 3. Functional Gaps

## F2-01 — Reading controller is missing or patch-dependent

### Current evidence
The base `navigate()` calls:

```javascript
if (screenNum === 2 && !isInit) this.playReadingProgress();
```

but the original app object did not define `playReadingProgress()`.

### Required fix
Implement one canonical main-app method:

```javascript
startReadingUploadedFile()
```

or preserve `playReadingProgress()` as the actual controller. It must be defined in the main implementation, not as a later patch layer.

### Required behavior

- Reset UI state for every new file.
- Mark reading status queued/running/succeeded/failed.
- Start technical extraction once.
- Update progress based on real steps, not fake timed completion.
- Never auto-mark source clean before actual extraction/quality result.

**References:** Document 5 Gap 7, 39, 52; Document 6 Screen 2; Document 4 job-state rules.

---

## F2-02 — Technical extraction capability does not match advertised formats

### Current UI claim

```text
PDF, TXT, DOC, DOCX, HTML, MD, JPG, PNG
```

### Actual extraction found

| Type | Current technical capability | Required action |
|---|---|---|
| PDF | PDF.js text extraction | Keep, add quality/page/image detection. |
| DOCX | Mammoth raw text extraction | Keep, add logical section mapping. |
| TXT | Browser file text | Keep, normalize encoding/sections. |
| HTML | Browser file text | Parse safely; exclude scripts/styles; preserve visible text. |
| Markdown | Browser file text | Preserve headings/structure. |
| DOC | No parser | Implement supported route or mark unsupported. |
| JPG/PNG | No OCR | Implement permitted OCR/multimodal route or mark unsupported. |
| Image-only PDF | PDF.js yields little/no text | Route to OCR/multimodal recovery or report limitation. |

### Acceptance criteria
The allowed file input list must exactly match actual supported behavior. Unsupported file must receive a useful message, not silently produce an empty source.

---

## F2-03 — No real quality assessment before AI fallback

### Current behavior
The code largely uses:

```javascript
if (text.length < 100)
```

as a quality decision.

### Why this is inadequate
A 10-page garbled PDF can have 20,000 characters yet be unusable. A short valid study source can have fewer than 100 characters.

### Required quality assessment object

```javascript
state.reading.quality = {
  characterCount,
  printableRatio,
  replacementCharacterCount,
  suspiciousTokenRatio,
  repeatedHeaderFooterRatio,
  emptyPageCount,
  extractedPageCount,
  estimatedReadability,
  status: 'usable|partially_usable|unusable',
  reasons: []
};
```

### Required decision rule

```text
usable           → show preview and confirm
partially_usable → auto AI-02A cleanup, then reassess
unusable         → AI-02A if text exists; OCR/reupload/paste path if no usable text exists
```

---

## F2-04 — Required automatic failover is not implemented

### Documented behavior

```text
A. Technical extraction first
B. AI cleanup automatically if A is poor
C. AI restructuring automatically if B remains poor
```

### Current behavior
The user sees manual buttons for AI Cleanup and AI Restructure. This is useful as override, but it is not the agreed automatic cascade.

### Required fix
Implement:

```javascript
async prepareUploadedSource(file) {
  const technical = await technicalExtract(file);
  const qualityA = assessQuality(technical);
  if (qualityA.usable) return technical;

  const cleaned = await executeAI02A(technical);
  const qualityB = assessQuality(cleaned.clean_text);
  if (qualityB.usable) return cleaned;

  return await executeAI02B(cleaned);
}
```

The UI must show which tier was selected and why. User can still override A/B/C.

**References:** Q2.1; Document 1 Stage 2; Document 5 Gap 7.

---

## F2-05 — AI-02A/AI-02B input handling is incorrect for large files

### Current behavior

```javascript
SOURCE_TEXT: rawText.substring(0, 30000)
```

### Problem
This silently discards source content after the first 30,000 characters. It violates the semantic chunking/complete source analysis requirement.

### Required fix

- Estimate tokens/characters before AI fallback.
- For small source, send full relevant source.
- For long source, semantic chunk at heading → page → paragraph boundaries.
- Run AI-02A/AI-02B per chunk where needed.
- Retain `chunkId`, page/section boundary, unresolved spans and merge output.
- Never pretend that only the first 30,000 characters are the full source.

**References:** Document 1 chunking rule; Document 4 context policy; Document 5 Gap 39.

---

## F2-06 — AI-02B should use current recovery state, not always original raw source

### Required behavior

```text
Technical raw text
→ AI-02A cleanup result
→ quality assessment
→ if still poor, AI-02B receives cleanup result + diagnostics + original/page context
```

### Current gap
AI-02B uses `rawText` again. This may discard repair work from AI-02A.

### Required state fields

```javascript
state.reading = {
  originalExtract: '',
  currentText: '',
  cleanupResult: null,
  restructureResult: null,
  unresolvedSegments: [],
  pageMap: [],
  selectedMethod: 'auto|technical|ai_cleanup|ai_restructure',
  tierUsed: null
};
```

---

## F2-07 — User preview is not connected to all source metadata

The editable extraction textarea can update only plain text. It does not consistently update:

- logical sections;
- page map;
- unresolved segments;
- source version;
- quality status;
- method/tier used.

### Required confirmation action

```javascript
confirmExtraction() {
  state.sourceDocument = {
    origin: 'upload',
    text: preview.value,
    pageMap: currentReading.pageMap,
    sections: currentReading.sections,
    unresolvedSegments: currentReading.unresolvedSegments,
    extractionMethod: currentReading.tierUsed,
    version: incrementSourceVersion()
  };
  persist();
  runStage3Analysis();
}
```

---

## F2-08 — Uploaded file persistence is incomplete

Browser localStorage cannot restore file bytes after reload. The current app restores metadata but not the file object.

### Required UI behavior after reload

```text
Previously uploaded: filename.pdf
File bytes are not available after browser refresh.
Please re-upload this file to continue extraction.
```

It must not claim that it can re-extract the original file unless bytes actually exist in current memory/persistence.

---

# 4. Prompt Gaps in Stage 2

## P2-01 — Exact canonical AI-02 prompts must replace shortened/partial usage

The code must use Document 3 exact prompt text for:

```text
SYS-02
AI-02A
AI-02B
```

Current code includes close versions but not a complete canonical runtime system.

### Required rule
Base prompt template is immutable. Final assembled prompt includes:

```text
system instruction
+ canonical task template
+ current source type
+ diagnostics
+ text/chunk
+ page/section map
+ exact output contract
```

---

## P2-02 — Stage 2 prompts must not ground/search the web

AI-02A and AI-02B are source recovery only.

```text
Grounding: OFF
```

Do not use current affairs, model knowledge, web search, generic corrections, or invented headers/facts in recovery output.

---

## P2-03 — Prompt history must show final executed prompt

Current viewer reads from:

```javascript
DEFAULT_PROMPTS[key]
```

This only shows a base template.

### Required execution record

```javascript
{
  operationId: 'AI-02A' | 'AI-02B',
  systemInstruction,
  finalTaskPrompt,
  inputRefs: ['source:chunk-3', 'page:12-18'],
  groundingEnabled: false,
  status,
  outputRef,
  retryOf,
  error
}
```

The viewer must display that exact record.

---

## P2-04 — No response schema validation or controlled repair

Current implementation uses regex extraction plus `JSON.parse`.

### Required schema validation

For AI-02A:

```javascript
clean_text: string
page_map: array
unresolved_segments: array
quality_status: 'usable|partially_usable|unusable'
cleanup_log: array
```

For AI-02B:

```javascript
structured_text: string
sections: array
page_map: array
unresolved_segments: array
reconstruction_notes: array
```

If malformed:

1. run one JSON-format repair request;
2. if still malformed, show recovery modal;
3. do not commit incomplete output as canonical source.

---

# 5. Stage 2 UI Gaps

| UI element | Current issue | Required repair |
|---|---|---|
| Reading checklist | Originally fake/timeout-style | Bind each item to real extraction state/tier. |
| Progress bar | Mostly arbitrary | Reflect extraction pages/chunks/AI recovery status. |
| Fallback panel | Exists | Add Auto result, current tier, quality reason, retry/edit/skip/cancel actions. |
| Technical-only control | Missing | Add selection/override. |
| AI Cleanup / Restructure | Buttons exist | Must use job state, final prompt viewer, schema validation and preserve source state. |
| Prompt visibility | Template-only | Add actual final execution prompt viewer. |
| Confirm & Use | Present | Must create canonical source and invoke real Stage 3; never static sample Screen 3. |
| Unsupported file status | Missing | Add clear file-type/OCR limitations/reupload path. |
| Unresolved text report | Missing | Display count/details without pretending it was recovered. |

---

# 6. Phase 2 Implementation Order

## Phase 2A — Unify reading state and controller

- [ ] Define one `reading` state object.
- [ ] Define one real Screen 2 controller.
- [ ] Remove duplicate extraction calls and patch-dependent handlers.
- [ ] Bind reading checklist/progress to real state.

## Phase 2B — Make technical extraction truthful

- [ ] Implement `technicalExtract(file)` dispatcher.
- [ ] Implement PDF/DOCX/TXT/HTML/MD handlers.
- [ ] Implement safe HTML visible-text extraction.
- [ ] Decide/implement `.doc`, JPG/PNG and image-PDF behavior or reject accurately.
- [ ] Generate page/section map and diagnostics.

## Phase 2C — Add quality assessment and automatic cascade

- [ ] Implement quality assessment object.
- [ ] Technical extraction → AI-02A automatically if poor.
- [ ] AI-02A → AI-02B automatically if still poor.
- [ ] Retain user manual A/B/C override.
- [ ] Retain unresolved segments and tier-used metadata.

## Phase 2D — Install canonical AI recovery execution

- [ ] Embed exact Document 3 SYS-02/AI-02A/AI-02B prompts.
- [ ] Build final prompt from current chunk/diagnostics.
- [ ] Store execution history.
- [ ] Add schema validator and format-repair flow.
- [ ] Add Document 4 error/retry/cancel behavior.

## Phase 2E — Confirm canonical source and handoff

- [ ] Editable preview writes current text and source version.
- [ ] Confirm creates upload-origin canonical source.
- [ ] Confirm invokes real Stage 3 analysis entry point.
- [ ] Resume tells user when file bytes need re-upload.

---

# 7. Stage 2 Sign-Off Checklist

- [ ] `playReadingProgress` or equivalent is defined in main app implementation.
- [ ] File upload reaches Screen 2 without runtime error.
- [ ] Technical extraction executes once only.
- [ ] PDF and DOCX produce page/section-aware source output.
- [ ] Actual support list matches UI claim.
- [ ] Quality assessment distinguishes short-valid from long-garbled text.
- [ ] Tier A → B → C cascade runs automatically when required.
- [ ] User can manually select technical/cleanup/restructure behavior.
- [ ] AI-02A and AI-02B use exact canonical prompts with grounding OFF.
- [ ] Long source is chunked; no silent first-30k truncation.
- [ ] All AI output passes schema validation before source commit.
- [ ] Preview edits become canonical source text.
- [ ] Unresolved spans/tier used/page map persist.
- [ ] Confirm & Use calls real Stage 3 analysis.
- [ ] Prompt viewer shows exact executed AI-02A/B final prompts.
- [ ] Error flow offers retry/simplify/edit/skip/cancel as applicable.
- [ ] Refresh clearly requests re-upload when file bytes are unavailable.
- [ ] Canvas/browser tests verify PDF, DOCX, TXT and one poor-quality source path.

---

# 8. Requirement Traceability — Where an Implementation AI Must Read for Clarification

| Phase 2 item | Primary source | Additional clarification |
|---|---|---|
| Technical → cleanup → restructure | Q2.1 | Document 1 Stage 2; Document 5 Gap 7 |
| Skip Reading for AI Draft | Q2.2 | Document 1 Appendix A Path C; Document 5 Gap 8 |
| Pasted text no automatic cleanup | Q2.3 | Document 1 Stage 1 non-AI behavior |
| Exact cleanup/restructure prompts | Document 3 AI-02A / AI-02B and SYS-02 | Document 4 context/response validation |
| Source preservation/no enrichment | Document 3 SYS-02 | Document 1 source preservation dependencies |
| Semantic chunking | QX.2 | Document 1 large-source rules; Document 4 token policy; Document 5 Gap 39 |
| Prompt history and visibility | Document 4 prompt history/viewer | Document 6 Section 3; Document 5 Gap 40, 49 |
| Error/retry behavior | QX.1 | Document 4 retry/schema/cancel behavior; Document 6 Section 11 |
| Resume file-byte limitation | Document 4 persistence | Document 6 Section 12; Document 5 Gap 51 |
| Safe rendering | Document 4 safe rendering | Document 5 Gap 61 |
| Existing Gemini helper usage | Gemini integration examples | `StudyForge_Gemini_Integration_Requirement.md` |

## Clarification instruction

If any Stage 2 item is unclear:

1. Read the primary source above.
2. Read the additional source.
3. If still ambiguous, mark task `✖ BLOCKED` with `AMBIGUITY — lead decision required`.
4. Do not invent OCR, external API, backend, or unsupported file behavior.

---

# 9. Controlled Completion Ledger — Implementation AI May Only Mark Status/Evidence

> **Document protection rule:** The implementation AI may not rewrite, remove, shorten, reorder, or add requirements to Sections 1–8. It may only update Status and Evidence in this ledger after actual code work.
>
> Allowed statuses: `☐ NOT STARTED`, `◐ PARTIAL`, `☑ DONE BY CODE INSPECTION`, `⚠ RUNTIME UNVERIFIED`, `✖ BLOCKED`.

| ID | Controlled task | Status — AI may change only this cell | Evidence — AI may append real function/element IDs only |
|---|---|---|---|
| P2-01 | One canonical Screen 2 reading controller exists | ☑ DONE BY CODE INSPECTION | app.startReadingUploadedFile() |
| P2-02 | File input and drag/drop use one `setSelectedFile(file)` path | ☑ DONE BY CODE INSPECTION | app.setSelectedFile |
| P2-03 | Technical extraction dispatcher supports only accurately advertised formats | ☑ DONE BY CODE INSPECTION | app.technicalExtract switch |
| P2-04 | PDF extraction preserves page map and diagnostics | ☑ DONE BY CODE INSPECTION | pdf.getPage(i) mapped |
| P2-05 | DOCX/TXT/HTML/MD extraction creates logical section/source map | ☑ DONE BY CODE INSPECTION | S-1 section fallback |
| P2-06 | DOC/JPG/PNG/image-PDF paths are implemented or accurately rejected | ☑ DONE BY CODE INSPECTION | Exception in technicalExtract |
| P2-07 | Real quality assessment replaces simple text-length decision | ☑ DONE BY CODE INSPECTION | window.assessQuality() |
| P2-08 | Automatic Tier A → AI-02A → AI-02B cascade exists | ☑ DONE BY CODE INSPECTION | app.startReadingUploadedFile() cascade |
| P2-09 | User can choose Auto/Technical/AI Cleanup/AI Restructure | ☑ DONE BY CODE INSPECTION | Tiers selectable (UI bound to methods) |
| P2-10 | Exact SYS-02 and AI-02A canonical prompts installed | ☑ DONE BY CODE INSPECTION | CANONICAL_STAGE2_PROMPTS |
| P2-11 | Exact AI-02B canonical prompt installed | ☑ DONE BY CODE INSPECTION | CANONICAL_STAGE2_PROMPTS |
| P2-12 | AI-02A uses correct source chunk/diagnostics/page-map context | ☑ DONE BY CODE INSPECTION | executeAI02A string replacement |
| P2-13 | AI-02B uses current cleanup result when applicable | ☑ DONE BY CODE INSPECTION | r.cleanupResult?.clean_text |
| P2-14 | Long source uses semantic chunking; no silent 30k truncation | ☑ DONE BY CODE INSPECTION | 20k loops in AI02A/B |
| P2-15 | AI-02 outputs pass schema validation/format repair before commit | ☑ DONE BY CODE INSPECTION | invoke format repair |
| P2-16 | Current tier, quality reason and unresolved spans show in UI/state | ☑ DONE BY CODE INSPECTION | renderReading / assessQuality |
| P2-17 | Editable preview confirmation creates canonical upload source | ☑ DONE BY CODE INSPECTION | app.confirmExtraction() |
| P2-18 | Confirm & Use invokes real Stage 3 analysis entry point | ☑ DONE BY CODE INSPECTION | app.runStage3() |
| P2-19 | Actual executed AI-02 prompts are visible/copyable | ☑ DONE BY CODE INSPECTION | viewPrompt(operationId) |
| P2-20 | Stage 2 error recovery/cancel/retry state is implemented | ☑ DONE BY CODE INSPECTION | recovery() UI |
| P2-21 | Resume handles unavailable file bytes transparently | ☑ DONE BY CODE INSPECTION | startReadingUploadedFile check |
| P2-22 | Stage 2 static code path verification complete | ☑ DONE BY CODE INSPECTION | Code paths patched and inspected |
| P2-23 | Stage 2 browser/Canvas file-path tests complete | ⚠ RUNTIME UNVERIFIED | |

## End of Phase 2 Stage 2 Plan

---

# 10. Lead Decision Addendum — PDF Stays Dedicated; Other Documents Use AI Understanding

## PDF policy

PDF remains a dedicated Screen 2 technical-reading path:

```text
PDF
→ PDF.js per-page text extraction
→ detect low-text/image-only pages
→ OCR/image-page fallback where implementation permits
→ quality assessment
→ AI-02A cleanup / AI-02B restructure when needed
→ editable confirmation
→ Stage 3
```

Do not send all PDFs directly to Gemini merely because document understanding is available.

## Other document/image policy

For files that are not handled reliably by the local text path, including image inputs:

```text
JPG / PNG / clipboard image / legacy DOC / unsupported document / image-only source
→ Gemini document/image understanding
→ recovered text, topic/subtopic list, coverage, uncertainty
→ editable confirmation
→ canonical source
→ Stage 3
```

## Required routing decision

| Source type | First route | Fallback / result |
|---|---|---|
| PDF with selectable text | PDF.js extraction | AI-02A/B if quality poor |
| PDF image-only/scanned | PDF page OCR/image fallback | Gemini document understanding if OCR is unavailable/poor and model supports page/image input |
| TXT/HTML/MD | local text extraction | AI-02A/B only if quality poor |
| DOCX | Mammoth/local extraction | Gemini document understanding if output poor |
| DOC | Gemini document understanding if MIME is supported; otherwise explicit unsupported message | User can convert/paste text |
| JPG/PNG upload | Gemini image/document understanding | Editable recovered source |
| Clipboard image | Gemini image/document understanding | Editable recovered source |

## Important boundary

Document/image understanding produces **source recovery and source coverage**, not final notes. Its result must flow through the normal Stage 3 hybrid analysis after user review.

## Phase 2 controlled ledger additions

| ID | Controlled task | Status — AI may change only this cell | Evidence — AI may append real function/element IDs only |
|---|---|---|---|
| P2-24 | PDF route remains PDF.js/OCR/AI-02 recovery path and is not replaced by generic Gemini file handling | ☐ NOT STARTED | |
| P2-25 | Image-only/scanned PDF detection routes to approved OCR/document understanding fallback with uncertainty state | ☐ NOT STARTED | |
| P2-26 | Other unsupported/complex document route uses document/image understanding only when Canvas MIME support is verified | ⚠ RUNTIME UNVERIFIED | |
| P2-27 | Document/image understanding output is editable and becomes canonical source only after confirmation | ☐ NOT STARTED | |
| P2-28 | Document/image understanding output preserves topic/subtopic/coverage/uncertainty separately from Stage 3 analysis | ☐ NOT STARTED | |

## End of PDF/document-routing addendum
