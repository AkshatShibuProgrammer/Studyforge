# Tasks: Phase 00 — Runtime Guardrails, Resilience & Canvas Bridge

## 1. Work Breakdown Structure

### Mod_01: Canvas AI Bridge
- [ ] Task 00.1.1: Implement `StudyForge.API.generateText` with native fetch and ambient `apiKey = ""` pattern.
- [ ] Task 00.1.2: Implement `StudyForge.API.searchText` with `tools: [{ googleSearch: {} }]` grounding payload.
- [ ] Task 00.1.3: Implement `StudyForge.API.generateImage` calling `imagen-4.0-generate-001:predict`.
- [ ] Task 00.1.4: Implement exponential backoff retry loop (2 retries, 2000ms / 4000ms intervals).
- [ ] Task 00.1.5: Wire generation options (`temperature`, `maxOutputTokens: 8192`, `responseMimeType: application/json`).

### Mod_02: In-Browser JSON Auto-Repair
- [ ] Task 00.2.1: Build `stripCodeFences()` utility function.
- [ ] Task 00.2.2: Implement `closeUnterminatedStrings()` parser tracking escaped quotes.
- [ ] Task 00.2.3: Implement `balanceBrackets()` utilizing a structural LIFO stack.
- [ ] Task 00.2.4: Implement `stripDanglingCommas()` before closing braces.
- [ ] Task 00.2.5: Implement `StudyForge.Guardrails.safeParseJSON()` returning `{ parsed, isRepaired }`.
- [ ] Task 00.2.6: Write unit tests verifying recovery from 5 synthetic truncated JSON scenarios.

### Mod_03: IndexedDB Persistence Engine
- [ ] Task 00.3.1: Implement `StudyForge.ImageDB.init()` creating `StudyForge_V3_DB`.
- [ ] Task 00.3.2: Implement `saveImage(record)` with Promise wrapper.
- [ ] Task 00.3.3: Implement `getImage(imageId)` and `getImagesByPart(partId)`.
- [ ] Task 00.3.4: Implement `deleteImage(imageId)` and `clearAll()`.
- [ ] Task 00.3.5: Refactor `app.save()` to sanitize image Base64 payloads before writing to `localStorage`.
- [ ] Task 00.3.6: Verify `localStorage` byte size stays under 100 KB even when 20 images are stored in IndexedDB.

---

## 2. Acceptance Verification Criteria
1. **Zero-API-Key Test**: `generateText()` resolves successfully without requiring an input key inside Gemini Canvas.
2. **Auto-Repair Acceptance**: Passing a truncated JSON string with 3 open brackets and an unclosed quote returns a valid JavaScript object without throwing.
3. **Storage Acceptance**: 10 high-resolution mock images (1.5 MB each) stored in `ImageDB` do not raise `QuotaExceededError` in `localStorage`.
4. **Retry Acceptance**: Simulating an HTTP 503 triggers a 2-second sleep followed by an automated retry.
