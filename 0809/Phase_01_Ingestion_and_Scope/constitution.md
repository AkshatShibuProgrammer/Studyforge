# Constitution: Phase 01 — Ingestion, Scope & Multi-Method Input

## 1. Principles
### Rule 1: Client-Side Parsing Exclusivity
File parsing for PDF, DOCX, TXT, HTML, and Images MUST execute 100% inside the browser using client-side libraries (PDF.js CDN, Mammoth.js CDN, native Canvas OCR/FileReader). No binary file data may be uploaded to external servers.

### Rule 2: User-in-the-Loop Scope Confirmation
AI-01A scope expansion MUST NOT automatically generate content. It MUST display the approved proposal panel allowing the user to uncheck suggested topics or add custom topics.

### Rule 3: Screen 2 Bypass for Pure AI Drafts
When Method 2 (AI Draft) generates source text, the user reviews and edits it in the Method 3 textarea. Upon clicking Continue, the app MUST navigate directly to Screen 3 (Understanding), bypassing Screen 2 (Reading/Extraction) entirely.
