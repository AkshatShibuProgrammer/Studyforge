# Constitution: Module 03 — IndexedDB Persistence Engine

## 1. Principles

### Rule 1: Zero Image Base64 Data in LocalStorage
Under NO circumstances may a Base64 data URL (`data:image/png;base64,...`) or large text blob (> 50 KB) be passed into `localStorage.setItem()`. All image records MUST be routed to IndexedDB.

### Rule 2: Automatic Hydration on Startup
When a user reloads or resumes a session, the UI MUST seamlessly hydrate visual cards from IndexedDB without prompting the user to regenerate images.

### Rule 3: Graceful In-Memory Fallback
If the user is operating in a restrictive browser mode (such as certain incognito configurations where IndexedDB is blocked), the module MUST fall back to an in-memory `Map` with a non-blocking UI alert, rather than throwing an uncaught exception.
