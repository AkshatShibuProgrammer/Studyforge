# Specification: Phase 01 — Ingestion, Scope & Multi-Method Input

## 1. Functional Requirements
- **FR-101**: File Drag-and-Drop & Picker supporting .pdf, .docx, .txt, .md, .html, .csv.
- **FR-102**: Clipboard paste event listener capturing pasted image data and converting to canvas OCR intake.
- **FR-103**: Dynamic Subtopic Fields allowing up to 10 subtopics with Add/Remove buttons and real-time state sync.
- **FR-104**: Method 2 Options Panel (Depth: basic/medium/comprehensive, Internet Search toggle, Current Affairs toggle, Target Exam selector).
- **FR-105**: AI-01A Execution returning guaranteed, suggested_essential, suggested_optional, and current_topics.
- **FR-106**: AI-01B Execution writing multi-page source notes into `#paste-area` with live character count update.
- **FR-107**: Direct Auto-Write bridge enabling instant generation from topic prompt input.

## 2. Gap Traceability
- Eliminates GAP-05 (Image clipboard OCR intake).
- Eliminates GAP-06 (Dynamic subtopic inputs cap and persistence).
- Eliminates GAP-07 (AI draft skipping Screen 2).
