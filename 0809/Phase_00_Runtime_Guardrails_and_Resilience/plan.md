# Implementation Plan: Phase 00 — Runtime Guardrails, Resilience & Canvas Bridge

## 1. Architectural Strategy
Phase 00 encapsulates all foundational plumbing in client-side Vanilla JavaScript before any UI interaction or prompt execution takes place. It operates as an invisible, resilient proxy layer between the application logic and Google's Generative AI APIs.

---

## 2. Component Implementation Sequence

```
┌────────────────────────────────────────────────────────┐
│ 1. Mod_03_IndexedDB_Persistence_Engine                 │
│    Initialize StudyForge_V3_DB & connect ImageDB        │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ 2. Mod_02_InBrowser_JSON_AutoRepair                    │
│    Implement brace/quote balancing & schema validation │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ 3. Mod_01_Canvas_AI_Bridge                            │
│    Wire fetch client, retry backoff & Ambient Auth     │
└────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Step-by-Step Execution Plan

### Step 1: Initialize the IndexedDB Image Store (`ImageDB`)
* Define an asynchronous factory function `initImageDB()`.
* Handle `onupgradeneeded` to create the `image_assets` object store with index on `part_id`.
* Create wrapper methods `put`, `get`, `getByPart`, and `delete` returning standard Promises.
* Test against quota exceptions and ensure graceful degradation if private browsing restricts IndexedDB.

### Step 2: Implement the JSON Auto-Repair Algorithm
* Create `safeParseJSON(text)`:
  1. Extract content between first `{` or `[` and last `}` or `]`. If no closing delimiter exists, extract from opening delimiter to end of string.
  2. Scan the string character by character while tracking string quote state (escaping `\"` handling).
  3. If string ends inside an open quote, append `"`.
  4. Build a LIFO stack of structural braces `{` and brackets `[`.
  5. If the string terminates prematurely, remove dangling comma or incomplete key `: ` and close all remaining stack items in reverse order.
  6. Pass repaired string into native `JSON.parse()`.

### Step 3: Build the Unified REST Bridge with Backoff Retries
* Implement `executeWithRetry(fetchFn, retries = 2, delays = [2000, 4000])`:
  * Wrap in a `try...catch` loop.
  * If response status is 429 (Rate Limit) or 503 (Overloaded) or `fetch()` throws a TypeError (network drop):
    * Calculate wait time from `delays[attempt]`.
    * Wait via `new Promise(r => setTimeout(r, waitTime))`.
    * Log retry event into `app.state.promptHistory`.
    * Retry execution.
* For `generateText`, configure `generationConfig`:
  * `"responseMimeType": "application/json"`
  * `"maxOutputTokens": 8192`
  * `"temperature": options.temperature || 0.2`

### Step 4: Verification & Smoke Test Execution
* Run unit tests inside the browser console:
  * Truncated JSON test: Provide `{"topics": [{"id": "T1", "title": "Incom` and assert it repairs cleanly to `{"topics": [{"id": "T1", "title": "Incom"}]}`.
  * Image store test: Put a 1.5 MB test Data URL into `ImageDB` and assert `localStorage` size remains unaltered.
  * Retry test: Simulate a 429 status and assert auto-retry fires after 2000ms.
