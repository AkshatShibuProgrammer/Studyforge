# Specification: Phase 10 — Export & Monolithic Packaging

## 1. Requirements
- **FR-1001**: Clean filtering: compile only parts where `app.state.approvedParts[p.num] === true`.
- **FR-1002**: Optional export inclusions (Cover Page, Table of Contents, Diagrams, Current Affairs).
- **FR-1003**: Output formats:
  - Copy to Clipboard (Formatted Markdown).
  - Download `.md` file.
  - Download `.html` standalone styled file.
  - Browser Print / Save as PDF (print-optimized CSS rules).
- **FR-1004**: Single-file packager script unifying CSS, HTML markup, and all module namespaces.

## 2. Gap Traceability
- Eliminates GAP-29 (Export screen running AI calls or including unapproved parts).
- Eliminates GAP-30 (Missing clean Markdown file download).
- Eliminates GAP-04 (Monolithic single-file consolidation).
