# Constitution: Phase 00 — Runtime Guardrails, Resilience & Canvas Bridge

## 1. Core Principles & Governance Rules

### Rule 1: Strict Zero-Backend & Browser Sandbox Confinement
1. All network communications in Phase 00 MUST originate from the client-side browser context using standard `window.fetch`.
2. No Node.js polyfills, external web servers, or Python helper processes may be introduced.
3. Code MUST be pure ECMAScript 2020+ Vanilla JavaScript.

### Rule 2: Ambient Canvas Key Injection Integrity
1. All AI functions (`geminiGenerateText`, `geminiSearchText`, `geminiImageCreation`) MUST hardcode `const apiKey = "";` or rely on the ambient canvas injection pattern.
2. The URL query parameter `key=${apiKey}` MUST remain intact to allow the Canvas environment proxy to identify and intercept generative API calls.

### Rule 3: Zero Unhandled Syntax Errors
1. No AI generation call may fail with an uncaught `SyntaxError: Unexpected end of JSON input`.
2. The JSON auto-repair parser MUST inspect and repair all truncated payloads prior to parsing.
3. If repair fails completely, a structured recovery payload MUST be returned with status `'partial'` or `'unrecoverable'` rather than throwing an exception that freezes the UI.

### Rule 4: Decoupled Quota-Safe Storage
1. Visual assets (Base64 data URLs) MUST NEVER be committed to `localStorage`.
2. Storing an image asset MUST route directly to the IndexedDB `StudyForge_ImageDB` database.
3. `localStorage` payload size MUST NOT exceed 100 KB under any operational state.

### Rule 5: Exponential Backoff Retry Policy
1. Transient network errors (HTTP 429, HTTP 503, or fetch drops) MUST trigger up to 2 automated retries.
2. The retry backoff intervals are strictly defined as:
   - Attempt 1 failure: Wait 2000 ms before Attempt 2.
   - Attempt 2 failure: Wait 4000 ms with context simplification before Attempt 3.
   - Attempt 3 failure: Prompt user with diagnostic recovery modal.
