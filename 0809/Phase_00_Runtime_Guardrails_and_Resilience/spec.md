# Specification: Phase 00 — Runtime Guardrails, Resilience & Canvas Bridge

## 1. Problem Statement
In previous iterations of StudyForge:
1. Long generation tasks (deep extraction, part blueprints, comprehensive notes) exceeded the model's token output threshold, cutting off JSON strings mid-stream and causing instant crashes (`SyntaxError: Unexpected end of JSON input`).
2. Imagen 4.0 generates base64 images that are 1–2 MB each. After saving 2–3 images, the browser's 5 MB `localStorage` limit was exhausted, throwing an unhandled `QuotaExceededError` that corrupted all saved state.
3. Network hiccups and rate limits caused immediate red error notifications with zero automated retry attempts.

---

## 2. User Stories
* **US-001 (Resilient Generation)**: As a student generating study notes from a massive 50-page syllabus, I want Gemini's output to complete reliably without crashing if token limits truncate the response.
* **US-002 (Safe Asset Storage)**: As a user generating 15 educational diagrams across a multi-part study plan, I want all images saved safely in my browser without exceeding localStorage storage quotas.
* **US-003 (Self-Healing Network)**: As a user on a fluctuating connection, I want the app to automatically retry failed AI calls in the background without requiring me to restart my session.

---

## 3. Functional Requirements

### FR-001: Unified Canvas AI Bridge Client
* The client MUST provide three core async functions:
  * `StudyForge.API.generateText(promptText, options)`
  * `StudyForge.API.searchText(searchQuery, options)`
  * `StudyForge.API.generateImage(imagePrompt, options)`
* All requests MUST use `apiKey = ""` to leverage ambient Canvas authentication.
* Grounded search calls MUST enable Google Search by including `tools: [{ googleSearch: {} }]`.

### FR-002: In-Browser Deterministic JSON Auto-Repair
* The parser MUST intercept raw LLM response strings before calling `JSON.parse()`.
* Must strip leading/trailing Markdown code fences (` ```json ` and ` ``` `).
* If `JSON.parse()` fails:
  1. Detect unclosed double-quotes (`"`) within keys or string values and close them.
  2. Maintain a stack of opening braces `{` and brackets `[` and append their closing counterparts in reverse order.
  3. Strip trailing uncompleted keys or dangling commas (e.g., `, }` → `}`).
  4. Parse the repaired string and return the salvaged data object with a `_repaired: true` metadata flag.

### FR-003: Schema Validation & Defaulting
* Every parsed payload MUST pass through a module-specific schema validator.
* If mandatory arrays (e.g., `headings`, `html_blocks`, `pyqs`) are missing or null, the validator MUST inject safe default empty arrays `[]` rather than allowing `null` or `undefined`.

### FR-004: Automated Exponential Backoff Retry Harness
* On HTTP 429, HTTP 503, or network timeout, the runner MUST execute up to 2 retries.
* Attempt 1: 2000ms delay.
* Attempt 2: 4000ms delay with prompt context trimming (stripping extraneous reference text while preserving instructions).
* If all retries fail, emit a structured diagnostic record into `app.state.promptHistory`.

### FR-005: Decoupled IndexedDB Image Store (`ImageDB`)
* Initialize an IndexedDB database named `StudyForge_V3_DB` with an object store named `image_assets` (keyed by `image_id`).
* `saveImage(imageId, base64Url, metadata)` stores the binary asset directly in IndexedDB.
* `loadImage(imageId)` retrieves the asset on demand.
* The main state object in `localStorage` MUST store only the lightweight image reference (`{ image_id, title, style }`), keeping localStorage payload under 50 KB.

---

## 4. Gap Elimination Traceability
* **Eliminates GAP-01**: Truncated JSON syntax errors completely resolved via `FR-002`.
* **Eliminates GAP-02**: `localStorage` quota exceeded resolved via `FR-005`.
* **Eliminates GAP-03**: Lack of automated retry resolved via `FR-004`.
* **Eliminates GAP-04**: Consolidated into `StudyForge.API` and `StudyForge.Persistence` namespaces.
